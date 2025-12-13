from pathlib import Path
from typing import Optional, List

import psutil

from .models import PluginConfig


def get_service_port_by_process(plugin_install_dir: Path, plugin: PluginConfig) -> Optional[int]:
    """
    根据进程路径获取其监听的端口号
    :return: 端口号列表（若未找到或无端口则返回空列表）
    """
    proc = get_proc_by_plugin(plugin_install_dir, plugin)
    ports = []
    if proc is not None:
        # 获取进程的网络连接
        connections = proc.connections()
        for conn in connections:
            # 筛选处于监听状态的 TCP 连接
            if conn.status == psutil.CONN_LISTEN and conn.type == 1:
                # 提取端口号（laddr 是 (ip, port) 元组）
                ports.append(conn.laddr[1])
    # 去重并返回
    ports = list(set(ports))
    if len(ports) > 0:
        return ports[0]
    return None


def get_proc_by_plugin(plugin_install_dir: Path, plugin: PluginConfig) -> Optional[psutil.Process]:
    app_abs_path = str((plugin_install_dir / plugin.extract_folder / plugin.app_relative_path).resolve())
    return find_proc_by_path(app_abs_path)


def get_plugin_info(plugin_name: str, plugins: List[PluginConfig]) -> Optional[PluginConfig]:
    """获取插件信息"""
    if plugins is None:
        return None
    return next((p for p in plugins if p.name == plugin_name), None)


def find_proc_by_path(p: str, fields: List[str] = None) -> Optional[psutil.Process]:
    """获取运行中的进程"""
    if fields is None:
        fields = ['exe', 'cmdline', 'pid', 'name']
    for proc in psutil.process_iter(fields):
        try:
            if proc.info['exe'] and str(Path(proc.info['exe']).resolve()) == p:
                return proc
            elif proc.info['cmdline']:
                cmd_path = Path(proc.info['cmdline'][0]).resolve()
                if cmd_path.exists() and str(cmd_path) == p:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return None
