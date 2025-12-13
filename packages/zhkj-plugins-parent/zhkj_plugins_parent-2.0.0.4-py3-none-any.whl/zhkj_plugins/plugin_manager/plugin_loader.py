import yaml
from pathlib import Path
from typing import List, Optional
import logging

from .download_manager import DownloadManager
from .models import PluginConfig

logger = logging.getLogger("PluginManager.PluginLoader")


class PluginLoader:
    def __init__(self, plugin_install_dir: Path):
        self.plugin_install_dir = plugin_install_dir

    def load_all_plugins(self) -> List[PluginConfig]:
        """从插件目录加载所有插件的配置"""
        plugins = []

        if not self.plugin_install_dir.exists():
            logger.warning(f"插件目录不存在: {self.plugin_install_dir}")
            return plugins

        try:
            for plugin_dir in self.plugin_install_dir.iterdir():
                if plugin_dir.is_dir() and not plugin_dir.name.startswith("_"):
                    config_file = plugin_dir / "plugin.yaml"
                    if config_file.exists():
                        plugin_config = self.load_plugin_config_from_file(config_file)
                        if plugin_config:
                            plugins.append(plugin_config)
                            logger.info(f"加载插件配置: {plugin_config.name}")
        except Exception as e:
            logger.error(f"扫描插件目录失败: {str(e)}")

        logger.info(f"共加载 {len(plugins)} 个插件配置")
        return plugins

    def load_plugin_config_from_file(self, config_path: Path) -> Optional[PluginConfig]:
        """从文件加载插件配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)

            if config_data and 'name' in config_data:
                plugin_config = PluginConfig(
                    name=config_data['name'],
                    current_version=config_data['current_version'],
                    extract_folder=config_data['extract_folder'],
                    app_relative_path=config_data['app_relative_path'],
                    plugin_type=config_data.get('plugin_type', 'app'),
                    dependencies=config_data.get('dependencies', {}),
                    startup_args=config_data.get('startup_args', []),
                    metadata=config_data.get('metadata', {})
                )
                return plugin_config
            else:
                logger.warning(f"插件配置文件格式错误: {config_path}")
        except Exception as e:
            logger.error(f"加载插件配置文件失败 {config_path}: {str(e)}")

        return None

    def save_plugin_config(self, plugin_config: PluginConfig, plugin_dir: Path = None,
                           file_name: str = "plugin.yaml") -> bool:
        """保存单个插件的配置到其目录下的 plugin.yaml 文件"""
        if plugin_dir is None:
            plugin_dir = self.plugin_install_dir / plugin_config.extract_folder
        config_file = plugin_dir / file_name

        # 确保插件目录存在
        if not self.ensure_dir(plugin_dir):
            return False

        config_data = plugin_config.to_dict()

        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, allow_unicode=True, indent=2)
            logger.info(f"保存插件配置: {plugin_config.name} -> {config_file}")
            return True
        except Exception as e:
            logger.error(f"保存插件配置失败 {plugin_config.name}: {str(e)}")
            return False

    def ensure_dir(self, dir_path: Path) -> bool:
        """确保目录存在"""
        try:
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"创建目录: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"创建目录失败 {dir_path}: {str(e)}")
            return False
