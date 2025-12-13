import os
import subprocess
import sys
import threading
import time
import socket
from pathlib import Path
from typing import Optional, List
import logging

from .models import PluginConfig
from .plugin_utils import get_service_port_by_process
from ..plugin_util import PluginUtil
from ..utils import get_free_port, get_running_processes
from zhkj_plugins.plugin_manager.process_manager import ProcessManager
from zhkj_plugins.plugin_manager.port_manager import PortManager
from zhkj_plugins.exceptions import SecurityError

logger = logging.getLogger("PluginManager.Runtime")


class PluginRuntimeManager:
    def __init__(self, plugin_install_dir: Path, config_manager):
        self.plugin_install_dir = plugin_install_dir
        self.config_manager = config_manager

        # 初始化进程和端口管理器
        self.process_manager = ProcessManager()
        self.process_manager.initialize(plugin_install_dir)
        self.port_manager = PortManager()

    def validate_plugin_command(self, plugin: PluginConfig, cmd: list) -> bool:
        """验证插件命令安全性"""
        if not cmd:
            raise SecurityError("命令为空")

        # 验证可执行文件
        exe_path = cmd[0]
        if not self._is_safe_executable(exe_path, plugin.name):
            raise SecurityError(f"不允许的可执行文件: {exe_path}")

        # 验证参数安全性
        for arg in cmd[1:]:
            if self._contains_dangerous_chars(arg):
                raise SecurityError(f"参数包含危险字符: {arg}")

        return True

    def _is_safe_executable(self, file_path: str, plugin_name: str) -> bool:
        """安全检查可执行文件"""
        try:
            path = Path(file_path).resolve()

            # 1. 路径必须在插件安装目录内
            if not str(path).startswith(str(self.plugin_install_dir.resolve())):
                return False

            # 2. 文件存在且是普通文件
            if not path.exists() or not path.is_file():
                return False

            # 3. 文件扩展名检查
            allowed_extensions = {'.exe', '.bat', '.cmd', '.py', ''}
            if path.suffix.lower() not in allowed_extensions:
                return False

            return True
        except Exception:
            return False

    def _contains_dangerous_chars(self, text: str) -> bool:
        """检查危险字符"""
        dangerous = {'&', '|', ';', '`', '$', '(', ')', '<', '>', '\n', '\r'}
        return any(char in text for char in dangerous)

    def start_plugin(self, plugin: PluginConfig, wait_for_ready: bool = True,
                     timeout: int = 30, success_indicator=None, output_encoding="utf-8",
                     ignore_validate_exe: bool = False) -> bool:
        """启动插件"""
        if self.is_plugin_running(plugin):
            logger.info(f"插件已在运行: {plugin.name}")
            return True

        plugin_dir = self.plugin_install_dir / plugin.extract_folder
        app_path = plugin_dir / plugin.app_relative_path

        if not plugin_dir.exists():
            logger.error(f"插件未安装: {plugin.name}，无法启动")
            return False

        if not app_path.exists():
            logger.error(f"插件程序不存在: {app_path}")
            return False

        try:
            cmd = [str(app_path.resolve())]
            port = None
            if plugin.plugin_type == "service":
                port = get_free_port()
                cmd.extend([f"--port={port}"])  # 传递端口参数
                logger.info(f"为服务插件 [{plugin.name}] 分配端口: {port}")

            logger.info(f"启动插件: {plugin.name} ({app_path})")

            process = self.start_plugin_with_safe_logging(plugin, cmd, output_encoding,
                                                          ignore_validate=ignore_validate_exe)

            # 注册到进程管理器
            self.process_manager.register_process(plugin.name, process)

            if plugin.plugin_type == "service" and port:
                self.port_manager.set_port(plugin.name, port)

            # 如果需要等待就绪
            if wait_for_ready:
                if plugin.plugin_type == "service":
                    # 服务插件：等待端口就绪
                    success = self._wait_for_port_ready(plugin, port, process, timeout)
                else:
                    # 非服务插件：区分一次性任务和常驻进程
                    success = self._wait_for_non_service_ready(plugin, process, timeout,
                                                               success_indicator)

                if success:
                    logger.info(f"插件 {plugin.name} 启动成功")
                    return True
                else:
                    logger.error(f"插件 {plugin.name} 启动超时或失败")
                    # 启动失败，清理资源
                    self.stop_plugin(plugin)
                    return False
            else:
                # 不等待就绪，直接返回
                logger.info(f"插件 {plugin.name} 已启动（未等待就绪）")
                return True

        except Exception as e:
            logger.error(f"启动插件失败: {str(e)}")
            if plugin.plugin_type == "service":
                self.port_manager.clear_port(plugin.name)
            return False

    def make_stream_non_blocking(self, stream):
        """
        跨平台设置流为非阻塞模式
        - 类 Unix 系统：使用 fcntl
        - Windows 系统：使用 msvcrt
        """
        if not stream:
            return stream

        try:
            fd = stream.fileno()
            if sys.platform == 'win32':
                # Windows 平台：使用 msvcrt 设置非阻塞
                import msvcrt
                msvcrt.setmode(fd, os.O_BINARY | os.O_NONBLOCK)  # 二进制模式 + 非阻塞
            else:
                # 类 Unix 平台：使用 fcntl
                import fcntl
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        except Exception as e:
            logger.warning(f"设置非阻塞模式失败: {e}")
        return stream

    def start_plugin_with_safe_logging(self, plugin, cmd: list, output_encoding: str = "utf-8",
                                       ignore_validate: bool = False) -> Optional[
        subprocess.Popen]:
        """
        启动插件并安全处理输出日志

        :param plugin: 插件配置对象
        :param cmd: 启动命令列表
        :param output_encoding: 输出编码
        :return: 子进程对象，失败时返回None
        """
        stop_event = threading.Event()  # 用于通知线程停止
        log_dir = Path("logs")
        if not log_dir.exists():
            log_dir.mkdir(exist_ok=True)
        stdout_log = log_dir / f"{plugin.name}_stdout.log"
        stderr_log = log_dir / f"{plugin.name}_stderr.log"
        try:
            if not ignore_validate:
                # 安全检查：验证命令安全性
                self.validate_plugin_command(plugin, cmd)

            plugin_dir = self.plugin_install_dir / plugin.extract_folder
            env = os.environ.copy()
            work_dir = env.get("WORK_DIR", str(Path(os.path.curdir).resolve()))
            env["PATH"] = work_dir + ";" + env["PATH"]  # 修改已有变量
            env["WORK_DIR"] = work_dir
            # 使用PIPE捕获输出，但通过安全的日志线程处理
            with open(stdout_log, "ab") as out_f, open(stderr_log, "ab") as err_f:
                process = subprocess.Popen(
                    cmd,
                    stdout=out_f,
                    stderr=err_f,
                    env=env,
                    shell=True if sys.platform == 'win32' else False,
                    cwd=str(plugin_dir.resolve()),
                    bufsize=1024,  # 适度缓冲区大小,
                    close_fds=True,  # 关闭不必要的文件描述符
                )

            logger.info(f"插件[{plugin.name}] 启动成功，PID: {process.pid}")
            return process

        except SecurityError as e:
            logger.error(f"插件[{plugin.name}] 安全验证失败: {e}")
            return None
        except Exception as e:
            logger.error(f"插件[{plugin.name}] 启动失败: {e}")
            return None

    # 假设你已经有了 logger, PluginConfig, is_plugin_running 等定义

    def _wait_for_non_service_ready(self, plugin: 'PluginConfig', process: subprocess.Popen,
                                    timeout: int,
                                    success_indicator: Optional[str] = None) -> bool:
        """等待非服务插件就绪（简化版，只看新日志）"""
        logger.info(f"等待插件 {plugin.name} 就绪...")

        start_time = time.time()
        stdout_log_path = Path("logs") / f"{plugin.name}_stdout.log"
        stderr_log_path = Path("logs") / f"{plugin.name}_stderr.log"

        # --- 关键步骤：记录日志文件当前大小，确保只看新内容 ---
        # 在循环开始前，获取一次文件大小作为初始偏移量
        stdout_offset = stdout_log_path.stat().st_size if stdout_log_path.exists() else 0
        stderr_offset = stderr_log_path.stat().st_size if stderr_log_path.exists() else 0

        while timeout == -1 or time.time() - start_time < timeout:
            # 1. 首要检查：进程是否已经退出
            return_code = process.poll()
            if return_code is not None:
                if return_code == 0:
                    logger.info(f"插件 {plugin.name} 已执行完成（退出码: {return_code}）")
                    return True
                else:
                    logger.error(f"插件 {plugin.name} 执行失败（退出码: {return_code}）")
                    return False

            # 2. 如果不需要监控日志，使用旧的进程检查逻辑
            if success_indicator is None:
                if self.is_plugin_running(plugin):
                    logger.info(f"插件 {plugin.name} 启动成功（通过进程检查）")
                    time.sleep(1)
                    return True
            # 3. 如果需要监控日志
            else:
                found = False
                if stdout_log_path.exists():
                    # --- 检查STDOUT日志 ---
                    try:
                        with open(stdout_log_path, 'r', encoding='utf-8', errors='ignore') as f:
                            f.seek(stdout_offset)  # 跳到上次读取的位置
                            new_lines = f.read()
                            stdout_offset = f.tell()  # 更新偏移量
                            if success_indicator in new_lines:
                                logger.info(f"插件 {plugin.name} 启动成功（在stdout日志中找到成功标识）")
                                found = True
                    except FileNotFoundError:
                        # 日志文件可能还没被创建，忽略
                        pass

                if not found:
                    # --- 检查STDERR日志 ---
                    if stderr_log_path.exists():
                        try:
                            with open(stderr_log_path, 'r', encoding='utf-8', errors='ignore') as f:
                                f.seek(stderr_offset)
                                new_lines = f.read()
                                stderr_offset = f.tell()
                                if success_indicator in new_lines:
                                    logger.warning(f"插件 {plugin.name} 启动成功（在stderr日志中找到成功标识）")
                                    found = True
                        except FileNotFoundError:
                            # 日志文件可能还没被创建，忽略
                            pass

                if found:
                    return True

            # 等待一下再循环
            time.sleep(0.5)

        # 4. 超时处理
        logger.warning(f"等待插件 {plugin.name} 就绪超时")
        return False

    def _wait_for_port_ready(self, plugin: PluginConfig, port: int, process: subprocess.Popen, timeout: int) -> bool:
        """等待服务插件的端口就绪"""
        logger.info(f"等待服务插件 {plugin.name} 端口 {port} 就绪...")

        start_time = time.time()

        while timeout == -1 or time.time() - start_time < timeout:
            try:
                # 尝试连接端口
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex(('localhost', port))
                    if result == 0:
                        logger.info(f"服务插件 {plugin.name} 端口 {port} 已就绪")
                        return True
            except Exception:
                pass

            # 检查进程是否还在运行
            return_code = process.poll()
            if return_code is not None:
                # 进程已退出
                logger.error(f"服务插件进程已退出: {plugin.name} (退出码: {return_code})")
                return return_code == 0  # 如果正常退出，视为成功

            time.sleep(0.5)  # 每隔0.5秒检查一次

        # 超时处理
        return_code = process.poll()
        if return_code is not None:
            # 进程在超时前已退出
            logger.info(f"服务插件 {plugin.name} 在超时前退出 (退出码: {return_code})")
            return return_code == 0
        else:
            logger.error(f"等待端口就绪超时: {plugin.name} (端口: {port})")
            return False

    def is_plugin_running(self, plugin: PluginConfig) -> bool:
        """检查插件是否在运行"""
        plugin_dir = self.plugin_install_dir / plugin.extract_folder
        app_path = plugin_dir / plugin.app_relative_path
        if not app_path.exists():
            return False

        app_abs_path = str(app_path.resolve())
        exists = app_abs_path in get_running_processes()
        if plugin.plugin_type == "service":
            port = self.get_service_port(plugin)
            if port:
                self.port_manager.set_port(plugin.name, port=port)
        return exists

    def get_service_port(self, plugin: PluginConfig) -> Optional[int]:
        """获取服务插件端口"""
        if not plugin.plugin_type == "service":
            logger.warning(f"不是服务类型插件: {plugin.name}")
            return None
        port = self.port_manager.get_port(plugin.name)
        if port is None:
            return get_service_port_by_process(self.plugin_install_dir, plugin)
        return port

    def stop_plugin(self, plugin: PluginConfig) -> bool:
        """停止插件"""
        # 先从进程管理器中获取进程
        process = None
        for name, proc in self.process_manager.processes.items():
            if name == plugin.name:
                process = proc
                break

        if process:
            try:
                # 使用进程管理器的方法终止进程
                self.process_manager.terminate_process(plugin, process)
                self.process_manager.unregister_process(plugin.name)

                if self.port_manager.get_port(plugin.name):
                    self.port_manager.clear_port(plugin.name)

                logger.info(f"成功停止插件: {plugin.name}")
                return True
            except Exception as e:
                logger.error(f"停止插件失败: {str(e)}")
                return False
            finally:
                self.clear_plugin_std_log(plugin)
        else:
            # 回退到原来的进程查找方式
            return self._stop_plugin_fallback(plugin)

    def clear_plugin_std_log(self, plugin):
        try:
            log_dir = Path("logs")
            stdout_log = log_dir / f"{plugin.name}_stdout.log"
            stderr_log = log_dir / f"{plugin.name}_stderr.log"
            # 清理 stdout 日志
            if stdout_log.exists():
                if stdout_log.is_file():  # 确保是文件（而非目录）
                    os.remove(stdout_log)  # 删除文件用 os.remove()
                    logger.info(f"已清理插件[{plugin.name}]的stdout日志: {stdout_log}")
                else:
                    logger.warning(f"{stdout_log} 不是文件，跳过清理")

            # 清理 stderr 日志
            if stderr_log.exists():
                if stderr_log.is_file():
                    os.remove(stderr_log)
                    logger.info(f"已清理插件[{plugin.name}]的stderr日志: {stderr_log}")
                else:
                    logger.warning(f"{stderr_log} 不是文件，跳过清理")

            return True

        except Exception as e:
            logger.error(f"清理插件[{plugin.name}]日志失败: {str(e)}")
            return False

    def _stop_plugin_fallback(self, plugin: PluginConfig) -> bool:
        """回退的进程停止方法"""
        import psutil
        app_abs_path = str((self.plugin_install_dir / plugin.extract_folder / plugin.app_relative_path).resolve())

        try:
            terminated = False
            for proc in psutil.process_iter(['pid', 'exe', 'cmdline']):
                try:
                    # 多种方式匹配进程
                    if (proc.info['exe'] and str(Path(proc.info['exe']).resolve()) == app_abs_path) or \
                            (proc.info['cmdline'] and app_abs_path in ' '.join(proc.info['cmdline'])):
                        pid = proc.pid
                        self.process_manager.stop_process_tree(pid)
                        logger.info(f"已终止插件进程: {plugin.name} (PID: {pid})")
                        terminated = True

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if plugin.plugin_type == "service":
                self.port_manager.clear_port(plugin.name)

            if terminated:
                logger.info(f"成功停止插件: {plugin.name}")
            else:
                logger.warning(f"未找到插件进程: {plugin.name}")

            return True
        except Exception as e:
            logger.error(f"停止插件失败: {str(e)}")
            return False

    def cleanup(self, plugins: List[PluginConfig]) -> None:
        """清理所有资源"""
        logger.info("开始清理插件管理器资源...")

        # 停止所有运行中的插件
        for plugin in plugins:
            logger.info(f"停止插件: {plugin.name}")
            try:
                self.process_manager.terminate_process(plugin)
            finally:
                self.clear_plugin_std_log(plugin)

        # 清理进程管理器
        self.process_manager.cleanup_all(plugins)

        # 清理端口管理器
        self.port_manager.clear_all()

        logger.info("插件管理器资源清理完成")
