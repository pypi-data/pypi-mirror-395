import atexit
import signal
import sys
import threading
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Callable
import logging

from zhkj_plugins.wrap import singleton
from .dependency_manager import DependencyManager

from .models import PluginConfig, VersionInfo
from .config_manager import ConfigManager
from .plugin_loader import PluginLoader
from .version_manager import VersionManager
from .download_manager import DownloadManager
from .archive_handler import ArchiveHandler
from .plugin_install_manager import PluginInstallManager
from .plugin_runtime_manager import PluginRuntimeManager
from .plugin_update_manager import PluginUpdateManager
from .plugin_package_manager import PluginPackageManager
from ..task_progress_manager import NestedProgressCallback

logger = logging.getLogger("PluginManager")


@singleton
class PluginManager:
    def __init__(self, config: Dict[str, Any] = None, config_path: str = "config.yaml"):
        """通过 YAML 配置文件初始化插件管理器"""
        # 初始化各个管理器
        self.config_manager = ConfigManager(config_path)
        if config:
            self.config_manager.update(config)


        self.plugin_install_dir = Path(self.config_manager.get('plugin_install_dir', 'plugins'))

        # 初始化各个功能模块
        self.plugin_loader = PluginLoader(self.plugin_install_dir)
        self.version_manager = VersionManager(self.config_manager)
        self.download_manager = DownloadManager()
        self.archive_handler = ArchiveHandler()

        # 初始化依赖管理器
        self.dependency_manager = DependencyManager(
            self.version_manager,
            self.plugin_install_dir
        )

        # 初始化功能管理器
        self.install_manager = PluginInstallManager(
            self.plugin_loader,
            self.config_manager,
            self.download_manager,
            self.archive_handler,
            self.plugin_install_dir,
            self.dependency_manager
        )
        self.runtime_manager = PluginRuntimeManager(
            self.plugin_install_dir,
            self.config_manager
        )
        self.update_manager = PluginUpdateManager(
            self.plugin_loader,
            self.config_manager,
            self.version_manager,
            self.download_manager,
            self.archive_handler,
            self.plugin_install_dir,
            self.runtime_manager,
            self.dependency_manager,
            self.install_manager
        )
        self.package_manager = PluginPackageManager(
            self.plugin_loader,
            self.download_manager,
            self.archive_handler,
            self.config_manager
        )

        # 加载插件配置
        self.plugins = self.plugin_loader.load_all_plugins()

        # 注册所有已加载插件的依赖关系
        for plugin in self.plugins:
            self.dependency_manager.register_plugin_dependencies(plugin)

        self._lock = threading.RLock()

        # 启动自动更新检查
        if self.config_manager.get('auto_check_updates', True):
            self._start_auto_update_check()

        # 注册退出清理
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info("插件管理器初始化完成")

    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        logger.info(f"接收到信号 {signum}，开始清理进程...")
        self.cleanup()
        sys.exit(0)

    def _start_auto_update_check(self) -> None:
        """启动自动更新检查后台线程"""
        self.update_manager._start_auto_update_check(self.plugins)

    def is_plugin_installed(self, plugin_name: str) -> bool:
        """检查插件是否已安装"""
        return self.install_manager.is_plugin_installed(plugin_name, self.plugins)

    def check_plugin_update(self, plugin_name: str) -> Tuple[bool, Optional[VersionInfo]]:
        """检查插件是否有更新"""
        return self.update_manager.check_plugin_update(plugin_name, self.plugins)

    def check_all_updates(self, background: bool = False) -> Dict[str, VersionInfo]:
        """检查所有插件的更新"""
        return self.update_manager.check_all_updates(self.plugins, background)

    def install_plugin(self, plugin_name: str,
                       progress_callback: Optional[NestedProgressCallback] = None,
                       auto_install_dependencies: bool = True, version: Optional[str] = None) -> bool:
        """安装指定插件"""
        plugin = None
        version_info = self.dependency_manager.version_manager.get_version_info(plugin_name, version)
        if not self.is_plugin_installed(plugin_name):
            if not version_info or version_info.download_url is None:
                logger.error(f"无法获取插件 {plugin_name} 的下载地址")
                raise Exception(f"Missing download URL for dependency plugin: {plugin_name}")

            with self.archive_handler.temp_directory() as temp_dir:
                config_file_name = f"{plugin_name}-{version_info.version}.yaml"
                temp_config = temp_dir / config_file_name
                plugin_config_path = DownloadManager().download(
                    self.config_manager.config_url + "/" + config_file_name, temp_config)
                if plugin_config_path:
                    remote_config = self.plugin_loader.load_plugin_config_from_file(Path(plugin_config_path))
                    plugin = remote_config
        else:
            plugin = self.plugin_info(plugin_name)
            if version_info is not None:
                version_comparison = self.version_manager._compare_versions(version_info.version,
                                                                            plugin.current_version)
                if version_comparison != 0:
                    # 版本不一样, 重新下载
                    self.uninstall_plugin(plugin_name)

        if plugin is None:
            logger.error(f"找不到插件 {plugin_name} 的配置")
            return False

        if progress_callback is None:
            progress_callback = NestedProgressCallback(
                parent_callback=None,
                start_percent=0,
                end_percent=100,
                parent_step=f"安装插件：{plugin_name}",
            )
        if auto_install_dependencies:
            # 获取已安装插件的版本信息
            installed_plugins = {p.name: p.current_version for p in self.plugins if self.is_plugin_installed(p.name)}
            # 检查依赖
            dependencies = plugin.dependencies or {}
            for idx, (dep_name, dep_version) in enumerate(dependencies.items()):
                start_pct = int(idx * 100 / len(dependencies.items()))
                end_pct = int((idx + 1) * 100 / len(dependencies.items()))
                plugin_cb = progress_callback.create_sub_callback(start_pct, end_pct, f"安装依赖 {dep_name}")
                # 如果依赖未安装，则递归安装
                if dep_name not in installed_plugins:
                    logger.info(f"安装依赖插件: {dep_name}")
                    if not self.install_plugin(dep_name, plugin_cb, auto_install_dependencies=True):
                        logger.error(f"依赖插件 {dep_name} 安装失败，无法安装 {plugin_name}")
                        return False

            for dep_name, dep_version in dependencies.items():
                if dep_name not in installed_plugins:
                    # 检查版本是否满足
                    if not self.dependency_manager.validate_plugin_dependencies(dep_name, installed_plugins):
                        logger.error(
                            f"依赖插件 {dep_name} 依赖不满足，无法安装 {plugin_name}")
                        return False
        return self.install_manager.install_plugin(plugin_name, progress_callback, self.plugins,
                                                   self._lock, auto_install_dependencies
                                                   )

    def uninstall_plugin(self, plugin_name: str) -> bool:
        """卸载插件（增强版，支持依赖安全检查）"""
        # 检查是否可以安全卸载
        can_uninstall, dependents = self.dependency_manager.can_safely_uninstall(plugin_name)
        if not can_uninstall:
            logger.error(f"无法卸载插件 {plugin_name}，它被以下插件依赖: {', '.join(dependents)}")
            return False

        # 获取安全卸载计划
        uninstall_plan = self.dependency_manager.get_safe_uninstall_plan(plugin_name)
        logger.info(f"安全卸载计划: {', '.join(uninstall_plan)}")

        # 执行卸载
        success = self.install_manager.uninstall_plugin(plugin_name, self.plugins, self._lock)
        if success:
            # 从依赖管理器中取消注册
            self.dependency_manager.unregister_plugin_dependencies(plugin_name)

        return success

    def update_plugin(self,
                      plugin_name: str,
                      version_info: VersionInfo,
                      progress_callback: Optional[NestedProgressCallback] = None):
        plugin = self._get_plugin_info(plugin_name)
        self.update_manager.update_plugin(plugin, version_info, progress_callback)

    def rollback_plugin(self,
                        plugin_name: str,
                        version_info: VersionInfo,
                        progress_callback: Optional[NestedProgressCallback] = None):
        plugin = self._get_plugin_info(plugin_name)
        return self.update_manager.rollback_plugin_version(plugin, version_info, progress_callback)

    def register_plugin(self, plugin_config: PluginConfig):
        """注册插件到依赖管理器"""
        self.dependency_manager.register_plugin_dependencies(plugin_config)

    def get_dependency_tree(self, plugin_name: str) -> str:
        """获取插件的依赖树"""
        installed_plugins = {p.name: p.current_version for p in self.plugins if self.is_plugin_installed(p.name)}
        return self.dependency_manager.get_dependency_tree(plugin_name, installed_plugins)

    def analyze_dependencies(self) -> Dict[str, Any]:
        """分析所有插件的依赖关系"""
        return self.dependency_manager.get_dependency_report(self.plugins)

    def auto_update_plugins(self) -> Dict[str, bool]:
        """自动更新所有有更新的插件"""
        return self.update_manager.auto_update_plugins(self.plugins)

    def start_plugin(self, plugin_name: str, wait_for_ready: bool = True, timeout: int = 30,
                     success_indicator=None, ignore_validate_exe=False) -> bool:
        """启动插件"""
        plugin = self._get_plugin_info(plugin_name)
        return self.runtime_manager.start_plugin(
            plugin, wait_for_ready, timeout, success_indicator, ignore_validate_exe=ignore_validate_exe
        )

    def is_plugin_running(self, plugin_name: str) -> bool:
        """检查插件是否在运行"""
        plugin = self._get_plugin_info(plugin_name)
        return self.runtime_manager.is_plugin_running(plugin)

    def get_service_port(self, plugin_name: str) -> Optional[int]:
        """获取服务插件端口"""
        plugin = self._get_plugin_info(plugin_name)
        return self.runtime_manager.get_service_port(plugin)

    def stop_plugin(self, plugin_name: str) -> bool:
        """停止插件"""
        plugin = self._get_plugin_info(plugin_name)
        return self.runtime_manager.stop_plugin(plugin)

    def cleanup(self) -> None:
        """清理所有资源"""
        self.runtime_manager.cleanup(self.plugins)

    def __del__(self):
        """析构函数，确保资源清理"""
        try:
            self.cleanup()
        except Exception as e:
            logger.error(f"析构函数清理失败: {str(e)}")

    def plugin_info(self, plugin_name: str) -> Optional[PluginConfig]:
        """获取插件信息"""
        with threading.RLock():
            return next((p for p in self.plugins if p.name == plugin_name), None)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """列出所有插件状态"""
        plugins_info = []

        for plugin in self.plugins:
            plugin_dir = self.plugin_install_dir / plugin.extract_folder
            install_status = self.is_plugin_installed(plugin.name)
            run_status = self.is_plugin_running(plugin.name)
            port = self.get_service_port(plugin.name) or "-"
            plugin_type = "服务" if plugin.plugin_type == "service" else "应用"

            # 从远程获取自动更新设置
            version_check_info = self.version_manager.get_version_check_info(plugin.name)
            auto_update = self.config_manager.get('auto_update', False)
            latest_version = version_check_info.get('latest_version', False)

            plugin_info = {
                'name': plugin.name,
                'version': plugin.current_version,
                'type': plugin_type,
                'install_status': "已安装" if install_status else "未安装",
                'run_status': "运行中" if run_status else "未运行",
                'auto_update': "是" if auto_update else "否",
                'latest_version': latest_version,
                'port': str(port),
                'path': str(plugin_dir)
            }
            plugins_info.append(plugin_info)

        return plugins_info

    def print_plugin_list(self) -> None:
        """打印插件列表"""
        plugins_info = self.list_plugins()

        print("\n插件列表:")
        print("-" * 120)
        print(
            f"{'名称':<15} {'版本':<10} {'类型':<8} {'安装状态':<10} {'运行状态':<10} {'自动更新':<8} {'端口':<6} {'安装路径':<40}")
        print("-" * 120)
        for info in plugins_info:
            print(
                f"{info['name']:<15} {info['version']:<10} {info['type']:<8} {info['install_status']:<10} "
                f"{info['run_status']:<10} {info['auto_update']:<8} {info['port']:<6} {info['path']:<40}"
            )
        print("-" * 120 + "\n")

    def install_all_plugins(self,
                            progress_callback: Optional[NestedProgressCallback] = None) -> Dict[str, bool]:
        """安装所有插件 - 从远程版本检查配置中获取下载地址"""
        return self.install_manager.install_all_plugins(
            self.plugins, self.version_manager, progress_callback
        )

    def package_plugin(self, plugin_name: str, plugin_dir: str, plugin_config: PluginConfig = None,
                       version_note: Optional[str] = None,
                       progress_callback: Optional[Callable[[float, str], None]] = None) -> \
            Optional[Dict[str, Any]]:
        """打包插件为zip文件"""
        return self.package_manager.package_plugin(plugin_name, plugin_dir, plugin_config=plugin_config,
                                                   version_note=version_note,
                                                   progress_callback=progress_callback)

    def _get_plugin_info(self, plugin_name: str) -> Optional[PluginConfig]:
        """获取插件信息"""
        if self.plugins is None:
            return None
        return next((p for p in self.plugins if p.name == plugin_name), None)

    def plugin_version_histories(self, plugin_name):
        return self.version_manager.get_histories(plugin_name)

    def plugin_version_info(self, plugin_name, version: Optional[str] = None) -> Optional[VersionInfo]:
        return self.version_manager.get_version_info(plugin_name=plugin_name, version=version)
