import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import logging
from datetime import datetime

from .models import VersionInfo
from zhkj_plugins.remote_config import RemoteSettings
from zhkj_plugins.exceptions import NetworkError

logger = logging.getLogger("PluginManager.VersionManager")


class VersionManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.version_cache_file = Path(config_manager.get('plugin_install_dir', 'plugins')) / "version_cache.json"
        self.version_cache = self._load_version_cache()
        self._version_checks_cache = {}
        self._version_checks_last_fetch = 0

    def _fetch_version_checks(self) -> Dict[str, Any]:
        """从远程获取版本检查配置"""
        version_checks_url = self.config_manager.get('version_checks_url')
        settings_url = self.config_manager.get('settings_url')

        if not version_checks_url:
            if settings_url:
                try:
                    remote_settings = RemoteSettings(
                        settings_url,
                        self.config_manager.get('settings_update_interval', 600),
                        self.config_manager.get('settings_update_timeout', 10)
                    )
                    return remote_settings.get_dict(
                        self.config_manager.get('settings_plugins_version_key', 'plugins_version')
                    )
                except Exception as e:
                    logger.error(f"获取远程版本检查配置失败: {str(e)}")
                    return {}
            return {}

        try:
            # 检查缓存是否有效（5分钟缓存）
            current_time = time.time()
            if (self._version_checks_cache is not None and
                    current_time - self._version_checks_last_fetch < 300):
                return self._version_checks_cache

            logger.info("正在获取远程版本检查配置...")
            response = requests.get(version_checks_url, timeout=10)
            response.raise_for_status()
            version_checks = response.json()

            # 更新缓存
            self._version_checks_cache = version_checks
            self._version_checks_last_fetch = current_time
            logger.info("远程版本检查配置获取成功")
            return version_checks
        except requests.RequestException as e:
            logger.error(f"获取远程版本检查配置失败: {str(e)}")
            raise NetworkError(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"处理版本检查配置失败: {str(e)}")
            return {}

    def _fetch_version_info(self, plugin_name: str, version: Optional[str] = None) -> Optional[VersionInfo]:
        """从远程获取版本检查配置"""
        version_info = self.get_version_check_info(plugin_name)
        if not version_info or 'download_url' not in version_info:
            logger.error(f"无法获取插件 {plugin_name} 的下载地址")
            raise Exception(f"Missing download URL for plugin: {plugin_name}")

        if version is None:
            version = version_info["latest_version"]

        try:
            logger.info("正在获取远程版本检查配置...")
            response = requests.get(self.config_manager.config_url + f"/{plugin_name}-{version}.json", timeout=10)
            response.raise_for_status()
            version_info = VersionInfo.from_dict(response.json())
            logger.info("远程版本检查配置获取成功")
            return version_info
        except requests.RequestException as e:
            logger.error(f"获取远程版本检查配置失败: {str(e)}")
            raise NetworkError(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"处理版本检查配置失败: {str(e)}")
            return None

    def _fetch_version_histories(self, url) -> Optional[Dict[str, Any]]:
        """获取插件所有版本信息，包括最新版本"""
        try:
            logger.info("正在获取远程版本历史...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            plugin_versions = response.json()

            logger.info("远程版本历史成功")
            return plugin_versions
        except requests.RequestException as e:
            logger.error(f"获取远程版本历史失败: {str(e)}")
            raise NetworkError(f"网络请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"处理版本历史失败: {str(e)}")
            return None

    def get_histories(self, plugin_name: str) -> Optional[List[Dict[str, Any]]]:
        """获取指定插件所有版本信息"""
        try:
            version_info = self.get_version_check_info(plugin_name)
            if not version_info or 'download_url' not in version_info:
                logger.error(f"无法获取插件 {plugin_name} 的下载地址")
                raise Exception(f"Missing download URL for plugin: {plugin_name}")
            download_url = version_info.get('download_url')
            version_checks = self._fetch_version_histories(download_url + "/version-history.json")
            return version_checks.get(plugin_name, [])
        except Exception as e:
            logger.error(f"获取插件 {plugin_name} 版本检查信息失败: {str(e)}")
            return None

    def get_version_check_info(self, plugin_name: str) -> Dict[str, Any]:
        """获取指定插件的版本检查信息"""
        try:
            version_checks = self._fetch_version_checks()
            return version_checks.get(plugin_name, {})
        except Exception as e:
            logger.error(f"获取插件 {plugin_name} 版本检查信息失败: {str(e)}")
            return {}

    def get_version_info(self, plugin_name: str, version: Optional[str] = None) -> Optional[VersionInfo]:
        """获取指定插件版本信息"""
        try:
            return self._fetch_version_info(plugin_name, version)
        except Exception as e:
            logger.error(f"获取插件 {plugin_name} 版本信息失败: {str(e)}")
            return {}

    def _load_version_cache(self) -> Dict[str, Any]:
        """加载版本缓存"""
        if not self.version_cache_file.exists():
            return {}

        try:
            with open(self.version_cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                logger.info("成功加载版本缓存")
                return cache
        except Exception as e:
            logger.error(f"加载版本缓存失败: {str(e)}")
            return {}

    def save_version_cache(self) -> bool:
        """保存版本缓存"""
        try:
            with open(self.version_cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.version_cache, f, indent=2, ensure_ascii=False)
            logger.info("版本缓存保存成功")
            return True
        except Exception as e:
            logger.error(f"保存版本缓存失败: {str(e)}")
            return False

    def _compare_versions(self, version1: str, version2: str) -> int:
        """比较两个版本号"""
        try:
            v1_parts = list(map(int, version1.split('.')))
            v2_parts = list(map(int, version2.split('.')))

            # 补齐版本号长度
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))

            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            return 0
        except Exception as e:
            logger.error(f"版本号比较失败 '{version1}' vs '{version2}': {str(e)}")
            return 0  # 出错时视为相等
