import socket
import threading
from contextlib import contextmanager
from typing import Set
import psutil
from pathlib import Path


def get_free_port() -> int:
    """获取随机可用端口"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            port = s.getsockname()[1]
            return port
    except Exception:
        return 8080  # 备用端口


def get_running_processes() -> Set[str]:
    """获取运行中的进程"""
    processes = set()
    for proc in psutil.process_iter(['exe', 'cmdline']):
        try:
            if proc.info['exe']:
                processes.add(str(Path(proc.info['exe']).resolve()))
            elif proc.info['cmdline']:
                cmd_path = Path(proc.info['cmdline'][0]).resolve()
                if cmd_path.exists():
                    processes.add(str(cmd_path))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes


@contextmanager
def thread_lock(lock: threading.RLock):
    """线程锁上下文管理器"""
    lock.acquire()
    try:
        yield
    finally:
        lock.release()
