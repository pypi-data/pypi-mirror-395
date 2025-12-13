import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, Callable
import logging

from .plugin_loader import PluginLoader
from .config_manager import ConfigManager
from .download_manager import DownloadManager
from .archive_handler import ArchiveHandler
from .models import PluginConfig

logger = logging.getLogger("PluginManager.Package")


class PluginPackageManager:
    def __init__(self, plugin_loader: PluginLoader, download_manager: DownloadManager,
                 archive_handler: ArchiveHandler, config_manager: ConfigManager):
        self.plugin_loader = plugin_loader
        self.download_manager = download_manager
        self.archive_handler = archive_handler
        self.config_manager = config_manager

    def package_plugin(self, plugin_name: str, plugin_dir: str, plugin_config: PluginConfig,
                       version_note: Optional[str] = None,
                       progress_callback: Optional[Callable[[float, str], None]] = None) -> \
            Optional[Dict[str, Any]]:
        """打包插件为zip文件"""
        plugin_path = Path(plugin_dir)

        # 检测插件实际路径是否存在
        if not plugin_path.exists():
            logger.error(f"插件目录不存在: {plugin_dir}")
            return None

        package_output_dir = Path(
            self.config_manager.get('package_output_dir', 'packages/' + plugin_name if plugin_name else "packages"))
        if not self.plugin_loader.ensure_dir(package_output_dir):
            return None

        if not plugin_name:
            plugin_name = plugin_config.name
            if not plugin_name:
                logger.error("plugin.yaml 中未找到插件名称")
                return None

        # 如果没有version就读取pyproject.toml的版本
        if plugin_config.current_version is None:
            try:
                from importlib.metadata import version as _version, PackageNotFoundError
                plugin_config.current_version = _version(plugin_name)
            except PackageNotFoundError:
                logger.warning(f"无法从pyproject.toml读取版本号，使用默认版本")
                plugin_config.current_version = "1.0.0"

        # 打包插件
        zip_path = self.archive_handler.package_plugin(plugin_name, plugin_path, package_output_dir, plugin_config,
                                                       progress_callback)
        if not zip_path:
            return None

        # 保存到输出路径
        if not self.plugin_loader.save_plugin_config(plugin_config,
                                                     package_output_dir,
                                                     f"{plugin_config.name}-{plugin_config.current_version}.yaml"):
            logger.warning(f"更新plugin.yaml失败，但继续打包")

        # 计算文件哈希值
        md5_hash = self.download_manager.calculate_file_md5(zip_path)
        file_size = zip_path.stat().st_size

        # 构建version_check内容
        config_url = self.config_manager.get(
            "download_url") if self.config_manager.get(
            "download_url") is not None else self.config_manager.config_url
        if not config_url:
            logger.warning("config_url未配置")

        download_url = f"{config_url}"

        version = plugin_config.current_version
        version_check_info = {
            "version": version,
            "download_url": download_url,
            "release_notes": f"Release {version}" if version_note is None else version_note,
            "release_date": datetime.now().strftime("%Y-%m-%d"),
            "file_size": file_size,
            "md5_hash": md5_hash
        }

        # 保存版本检查配置到 <插件名>-<版本号>.json 文件
        version_check_filename = f"{plugin_name}-{version}.json"
        version_check_path = package_output_dir / version_check_filename

        try:
            with open(version_check_path, 'w', encoding='utf-8') as f:
                json.dump(version_check_info, f, indent=2, ensure_ascii=False)
            logger.info(f"版本检查配置已保存到: {version_check_path}")
        except Exception as e:
            logger.error(f"保存版本检查配置文件失败: {str(e)}")

        logger.info("\n" + "=" * 50)
        logger.info("版本检查配置内容 (可添加到远程版本检查配置中):")
        logger.info("=" * 50)
        logger.info(json.dumps(version_check_info, indent=2, ensure_ascii=False))
        logger.info("=" * 50)

        return {
            "plugin_name": plugin_name,
            "version": version,
            "zip_path": str(zip_path),
            "download_url": download_url,
            "file_size": file_size,
            "md5_hash": md5_hash
        }
