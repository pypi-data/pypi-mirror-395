import logging
import subprocess
from typing import List, Union, Any, Optional

import psutil

from .models import PluginConfig
from zhkj_plugins.plugin_manager.plugin_utils import get_proc_by_plugin, get_plugin_info

logger = logging.getLogger("ProcessManager")


class ProcessManager:
    """进程管理器，负责跟踪和清理所有启动的插件进程"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.processes = {}
            cls._instance._initialized = False
            cls._instance.plugin_install_dir = None
        return cls._instance

    def initialize(self, plugin_install_dir):
        """初始化信号处理和退出清理"""
        if self._initialized:
            return
        self._initialized = True
        self.plugin_install_dir = plugin_install_dir
        logger.info("进程管理器已初始化")

    def register_process(self, plugin_name: str, process: subprocess.Popen) -> None:
        """注册插件进程"""
        self.processes[plugin_name] = process
        logger.debug(f"注册进程: {plugin_name} (PID: {process.pid})")

    def unregister_process(self, plugin_name: str) -> None:
        """取消注册插件进程"""
        if plugin_name in self.processes:
            del self.processes[plugin_name]
            logger.debug(f"取消注册进程: {plugin_name}")

    def cleanup_all(self, plugins: List[PluginConfig]) -> None:
        """清理所有注册的进程"""
        logger.info("开始清理所有插件进程...")

        for plugin_name, process in list(self.processes.items()):
            try:
                plugin = get_plugin_info(plugin_name, plugins)
                self.terminate_process(plugin, process)
            except Exception as e:
                logger.error(f"清理进程 {plugin_name} 失败: {str(e)}")

        self.processes.clear()
        logger.info("所有插件进程清理完成")

    def stop_process_tree(self, pid: Union[int, Any]):
        # 终止整个进程树
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)

        # 先终止子进程
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass

        # 然后终止父进程
        try:
            parent.terminate()
        except:
            pass

        try:
            # 等待进程终止
            gone, alive = psutil.wait_procs([parent] + children, timeout=5)

            if alive:
                # 强制杀死仍在运行的进程
                for p in alive:
                    try:
                        p.kill()
                    except psutil.NoSuchProcess:
                        pass
        except:
            pass

    def terminate_process(self, plugin: PluginConfig, process: Optional[subprocess.Popen] = None) -> None:
        """终止单个进程"""
        plugin_name = plugin.name
        try:
            # 检查进程是否还在运行
            if process is None:
                process = self.processes.get(plugin_name)
            if process and process.poll() is None:
                logger.info(f"终止进程: {plugin_name} (PID: {process.pid})")

                self.stop_process_tree(process.pid)
                try:
                    process.wait(timeout=5)
                    logger.info(f"进程 {plugin_name} 已优雅终止")
                except subprocess.TimeoutExpired:
                    # 强制杀死
                    logger.warning(f"进程 {plugin_name} 未响应，强制杀死")
                    process.kill()
                    process.wait()
                    logger.info(f"进程 {plugin_name} 已被强制杀死")
            else:
                proc = get_proc_by_plugin(self.plugin_install_dir, plugin)
                if proc is not None:
                    self.stop_process_tree(proc.info['pid'])
                logger.debug(f"进程 {plugin_name} 已退出")

        except Exception as e:
            logger.error(f"终止进程 {plugin_name} 时出错: {str(e)}")

    def get_running_plugins(self) -> List[str]:
        """获取正在运行的插件列表"""
        running = []
        for plugin_name, process in self.processes.items():
            if process.poll() is None:
                running.append(plugin_name)
        return running
