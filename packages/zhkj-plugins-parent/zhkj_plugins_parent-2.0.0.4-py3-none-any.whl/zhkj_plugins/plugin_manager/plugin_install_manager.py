import shutil
import threading
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any
import logging

from .dependency_manager import DependencyManager
from .progresses import InstallDownloadBridge
from .models import PluginConfig
from .plugin_loader import PluginLoader
from .config_manager import ConfigManager
from .download_manager import DownloadManager
from .archive_handler import ArchiveHandler
from ..task_progress_manager import NestedProgressCallback
from ..utils import thread_lock

logger = logging.getLogger("PluginManager.Install")


class PluginInstallManager:
    def __init__(self, plugin_loader: PluginLoader, config_manager: ConfigManager, download_manager: DownloadManager,
                 archive_handler: ArchiveHandler, plugin_install_dir: Path,
                 dependency_manager: DependencyManager):
        self.plugin_loader = plugin_loader
        self.config_manager = config_manager
        self.download_manager = download_manager
        self.archive_handler = archive_handler
        self.plugin_install_dir = plugin_install_dir
        self.dependency_manager = dependency_manager

    def is_plugin_installed(self, plugin_name: str, plugins: List[PluginConfig]) -> bool:
        """检查插件是否已安装"""
        plugin = self._get_plugin_info(plugin_name, plugins)
        if not plugin:
            return False

        plugin_dir = self.plugin_install_dir / plugin.extract_folder
        return plugin_dir.exists() and (plugin_dir / "plugin.yaml").exists()

    def install_plugin(
            self,
            plugin_name: str,
            progress_callback: Optional[NestedProgressCallback] = None,
            plugins: List[PluginConfig] = None,
            lock: threading.RLock = None,
            auto_install_dependencies: bool = True,
    ) -> bool:
        """安装指定插件（进度回调升级为嵌套式，零逻辑删减）"""

        # -------- 以下所有逻辑与原文件完全一致，仅把“打印”部分抽离 --------
        if progress_callback is None:  # 兼容旧接口
            progress_callback = NestedProgressCallback(
                parent_callback=None,
                start_percent=0,
                end_percent=100,
                parent_step=f"安装插件：{plugin_name}",
            )

        plugin_config = self.get_plugin_info(plugin_name, plugins)
        if plugin_config is None:
            logger.error(f"找不到插件 {plugin_name} 的配置")
            return False

        if auto_install_dependencies:
            install_order = self._resolve_install_dependencies(plugin_name, plugins)
            logger.info(f"插件安装顺序: {install_order}")
        else:
            install_order = [plugin_name]

        for idx, plugin_to_install in enumerate(install_order):
            # 计算该插件在总进度里的占比（平均切分）
            start_pct = int(idx * 100 / len(install_order))
            end_pct = int((idx + 1) * 100 / len(install_order))
            if len(install_order) == 1:
                plugin_cb = progress_callback
            else:
                plugin_cb = progress_callback.create_sub_callback(start_pct, end_pct, f"插件 {plugin_to_install}")

            # 原逻辑：检查已安装
            if self.is_plugin_installed(plugin_to_install, plugins):
                logger.info(f"插件已安装: {plugin_to_install}")
                plugin_cb(100, "已安装，跳过")
                continue

            # 原逻辑：获取版本/下载地址
            version_info = self.dependency_manager.version_manager.get_version_check_info(plugin_to_install)
            if not version_info or 'download_url' not in version_info:
                logger.error(f"无法获取插件 {plugin_to_install} 的下载地址")
                raise Exception(f"Missing download URL for dependency plugin: {plugin_to_install}")

            plugin_url = version_info['download_url']
            version = version_info['latest_version']
            download_url = plugin_url if (plugin_url.startswith(
                "https://soft.555168.com/disk/download") or plugin_url.endswith(
                ".zip")) else f"{plugin_url}/{plugin_to_install}-{version}.zip"
            logger.info(f"开始安装插件: {plugin_to_install}")

            temp_plugin_dir = self.plugin_install_dir / f"_temp"

            # 原逻辑：临时目录
            with self.archive_handler.temp_directory(temp_plugin_dir) as temp_dir:
                temp_archive = temp_dir / f"{plugin_to_install}.zip"
                temp_yaml = temp_dir / f"{plugin_to_install}.yaml"

                download_cb = InstallDownloadBridge(
                    plugin_cb.create_sub_callback(0, 70, "下载")
                )
                if not self.download_manager.download_with_progress(
                        download_url,
                        str(temp_archive),
                        progress_callback=download_cb,  # 仅改这里
                ):
                    logger.error(f"下载插件失败: {plugin_to_install}")
                    return False

                # 原逻辑：解压
                extract_cb = plugin_cb.create_sub_callback(70, 90, "解压")
                extract_cb(50, "正在解压...")
                extract_temp_dir = temp_dir / "extracted"
                if not self.archive_handler.extract_archive(temp_archive, extract_temp_dir):
                    logger.error(f"解压插件失败: {plugin_to_install}")
                    return False
                extract_cb(100, "解压完成")

                # 原逻辑：下载 yaml、校验、移动、写配置、加锁、清理目录...
                # 以下全部保持原样，只把需要进度的地方继续用 plugin_cb / final_cb
                final_cb = plugin_cb.create_sub_callback(90, 100, "收尾")

                plugin_config_path = self.download_manager.download(
                    f"{self.config_manager.config_url}/{plugin_to_install}-{version}.yaml", str(temp_yaml)
                )
                if not plugin_config_path:
                    logger.error(f"下载插件配置文件失败: {plugin_to_install}")
                    return False

                plugin_config = self.plugin_loader.load_plugin_config_from_file(Path(plugin_config_path))
                if not plugin_config:  # 原判空
                    logger.error(f"无法加载插件配置文件: {plugin_to_install}")
                    return False

                if plugin_config.name != plugin_to_install:  # 名校验
                    logger.error(f"插件名称不匹配: 配置中为 {plugin_config.name}, 期望为 {plugin_to_install}")
                    return False

                plugin_dir = self.plugin_install_dir / plugin_config.extract_folder
                if plugin_dir.exists():  # 原目录清理
                    logger.info(f"目标目录已存在，先删除: {plugin_dir}")
                    try:
                        shutil.rmtree(plugin_dir, ignore_errors=True)
                    except Exception as e:
                        logger.error(f"删除现有目录失败: {str(e)}")
                        return False

                try:  # 原移动
                    shutil.move(str(extract_temp_dir), str(plugin_dir))
                    logger.info(f"插件文件已移动到: {plugin_dir}")
                except Exception as e:
                    logger.error(f"移动插件文件失败: {str(e)}")
                    return False

                if plugins is not None and lock is not None:  # 原加锁写配置
                    with thread_lock(lock):
                        if not any(p.name == plugin_config.name for p in plugins):
                            plugins.append(plugin_config)
                            logger.info(f"添加插件配置到管理器: {plugin_config.name}")

                if not self.plugin_loader.save_plugin_config(plugin_config):
                    logger.warning(f"保存插件配置失败，但插件文件已安装: {plugin_to_install}")

                final_cb(100, "安装完成")
                logger.info(f"插件安装完成: {plugin_to_install}")

        return True  # 原返回值

    def get_plugin_info(self, plugin_name: str, plugins: Optional[list[PluginConfig]]) -> Any:
        # 获取插件配置（本地或远程）
        plugin_config = None
        if not self.is_plugin_installed(plugin_name, plugins):
            # 通过版本管理器获取依赖插件的下载地址
            version_info = self.dependency_manager.version_manager.get_version_check_info(plugin_name)
            if not version_info or 'download_url' not in version_info:
                logger.error(f"无法获取插件 {plugin_name} 的下载地址")
                raise Exception(f"Missing download URL for dependency plugin: {plugin_name}")

            with self.archive_handler.temp_directory() as temp_dir:
                config_file_name = f"{plugin_name}-{version_info.get('latest_version')}.yaml"
                temp_config = temp_dir / config_file_name
                plugin_config_path = DownloadManager().download(
                    self.config_manager.config_url + "/" + config_file_name, temp_config)
                if plugin_config_path:
                    remote_config = self.plugin_loader.load_plugin_config_from_file(Path(plugin_config_path))
                    plugin_config = remote_config
        else:
            plugin_config = self._get_plugin_info(plugin_name, plugins)
        return plugin_config

    def _find_plugin_config(self, directory: Path) -> Optional[Path]:
        """在目录中递归查找 plugin.yaml 文件"""
        try:
            for file_path in directory.rglob("plugin.yaml"):
                if file_path.is_file():
                    return file_path
            return None
        except Exception as e:
            logger.error(f"查找插件配置文件失败 {directory}: {str(e)}")
            return None

    def uninstall_plugin(self, plugin_name: str, plugins: List[PluginConfig] = None,
                         lock: threading.RLock = None) -> bool:
        """卸载插件"""
        plugin = self._get_plugin_info(plugin_name, plugins)
        if not plugin:
            logger.error(f"插件不存在: {plugin_name}")
            return False

        plugin_dir = self.plugin_install_dir / plugin.extract_folder
        if not plugin_dir.exists():
            logger.info(f"插件未安装: {plugin_name}")
            return True

        try:
            shutil.rmtree(plugin_dir)
            logger.info(f"插件卸载完成: {plugin_name}")

            # 从插件列表中移除
            if plugins is not None and lock is not None:
                with thread_lock(lock):
                    plugins = [p for p in plugins if p.name != plugin_name]

            return True
        except Exception as e:
            logger.error(f"卸载插件失败: {str(e)}")
            return False

    def install_all_plugins(self, plugins: List[PluginConfig], version_manager,
                            progress_callback: Optional[NestedProgressCallback] = None) -> Dict[str, bool]:
        """安装所有插件 - 从远程版本检查配置中获取下载地址"""
        logger.info("开始安装所有插件...")
        results = {}

        for plugin in plugins:
            try:
                # 从远程版本检查配置中获取下载地址
                version_check_info = version_manager.get_version_check_info(plugin.name)
                url = version_check_info.get('download_url')
                if url:
                    success = self.install_plugin(plugin.name, progress_callback=progress_callback)
                    results[plugin.name] = success
                else:
                    logger.warning(f"插件 {plugin.name} 未配置下载地址，跳过安装")
                    results[plugin.name] = False
            except Exception as e:
                logger.error(f"安装插件 {plugin.name} 失败: {str(e)}")
                results[plugin.name] = False

        logger.info("所有插件安装操作完成")
        return results

    def _get_plugin_info(self, plugin_name: str, plugins: List[PluginConfig]) -> Optional[PluginConfig]:
        """获取插件信息"""
        if plugins is None:
            return None
        return next((p for p in plugins if p.name == plugin_name), None)

    def _resolve_install_dependencies(self, plugin_name: str, plugins: List[PluginConfig]) -> List[str]:
        """解析安装插件所需的依赖安装顺序"""
        # 获取已安装插件的名称和版本
        installed_plugins = {p.name: p.current_version for p in plugins if self.is_plugin_installed(p.name, plugins)}

        # 使用依赖管理器获取安装顺序
        install_order = self.dependency_manager.get_dependency_install_order(plugin_name, installed_plugins)
        return install_order
