import yaml
import json
from pathlib import Path
from typing import Dict, Any
import logging
from zhkj_plugins.exceptions import PluginManagerError

logger = logging.getLogger("PluginManager.ConfigManager")


class ConfigManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_yaml_config()

    @property
    def config_url(self):
        if 'version_checks_url' in self.config:
            return self.config['version_checks_url'].rsplit('/', 1)[0]
        return None

    def _load_yaml_config(self) -> Dict[str, Any]:
        """加载并解析 YAML 配置文件"""
        config = None
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
                    logger.info(f"成功加载配置文件: {self.config_path}")
            except yaml.YAMLError as e:
                logger.error(f"YAML 配置解析错误: {str(e)}")
                raise PluginManagerError(f"YAML 配置解析错误: {str(e)}")
            except Exception as e:
                logger.error(f"加载配置文件失败: {str(e)}")
                raise PluginManagerError(f"加载配置文件失败: {str(e)}")
        if config is None:
            config = {
                'plugin_install_dir': 'plugins',
                'auto_check_updates': True,
                'version_checks_url': '',
                'settings_url': '',
                'settings_update_interval': 600,
                'settings_update_timeout': 10,
                'settings_plugins_version_key': 'plugins_version'
            }
        return config

    def _save_config_to_file(self, config: Dict[str, Any]) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, indent=2)
            logger.info(f"配置文件已保存: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
            return False

    def get(self, key: str, default=None):
        """获取配置值"""
        return self.config.get(key, default)

    def update(self, updates: Dict[str, Any], store=False) -> bool:
        """更新配置"""
        self.config.update(updates)
        if store:
            return self._save_config_to_file(self.config)
        else:
            return True
