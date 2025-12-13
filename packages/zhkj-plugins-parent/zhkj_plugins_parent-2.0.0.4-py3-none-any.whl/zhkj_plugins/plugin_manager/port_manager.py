import logging
import threading
from typing import Optional

logger = logging.getLogger("PortManager")

# 单例端口管理器（服务类插件端口记录）
class PortManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.port_map = {}  # {插件名: 端口号}
        return cls._instance

    def get_port(self, plugin_name: str) -> Optional[int]:
        """获取插件端口"""
        with self._lock:
            return self.port_map.get(plugin_name)

    def set_port(self, plugin_name: str, port: int) -> None:
        """设置插件端口"""
        with self._lock:
            self.port_map[plugin_name] = port
            logger.info(f"设置插件端口: {plugin_name} -> {port}")

    def clear_port(self, plugin_name: str) -> None:
        """清理插件端口"""
        with self._lock:
            if plugin_name in self.port_map:
                del self.port_map[plugin_name]
                logger.info(f"清理插件端口: {plugin_name}")

    def clear_all(self) -> None:
        """清理所有端口"""
        with self._lock:
            self.port_map.clear()
            logger.info("清理所有插件端口")