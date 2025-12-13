import threading
import time
from contextlib import contextmanager
from enum import Enum
from typing import Dict, Callable, Any, Optional, Union, List
from datetime import datetime
import logging
import functools
import inspect


class MethodStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"


class ReentrantMultiKeyLock:
    def __init__(self):
        self._locks = {}
        self._global_lock = threading.RLock()  # 使用可重入锁

    @contextmanager
    def acquire(self, key: str, timeout: float = 600.0):
        """完整的上下文管理器实现"""
        current_thread = threading.get_ident()
        acquired = False

        try:
            with self._global_lock:
                if key in self._locks:
                    lock_obj, count, owner = self._locks[key]
                    if owner == current_thread:
                        # 重入：增加计数
                        self._locks[key] = (lock_obj, count + 1, owner)
                        acquired = True
                    else:
                        # 其他线程持有，记录锁对象用于后续获取
                        pass
                else:
                    # 新锁：创建并立即获取
                    lock_obj = threading.Lock()
                    acquired = lock_obj.acquire(timeout=0)  # 非阻塞尝试
                    if acquired:
                        self._locks[key] = (lock_obj, 1, current_thread)

            # 非重入且未立即获取的情况
            if not acquired:
                acquired = lock_obj.acquire(timeout=timeout)
                if acquired:
                    with self._global_lock:
                        self._locks[key] = (lock_obj, 1, current_thread)
                else:
                    raise TimeoutError(f"Failed to acquire lock for key: {key}")

            yield acquired # 执行用户代码

        finally:
            # 释放逻辑（需要补充）
            if acquired:
                self._release(key)

    def _release(self, key: str):
        """释放锁的内部方法"""
        with self._global_lock:
            if key in self._locks:
                lock_obj, count, owner = self._locks[key]
                if owner == threading.get_ident():
                    if count > 1:
                        # 减少重入计数
                        self._locks[key] = (lock_obj, count - 1, owner)
                    else:
                        # 完全释放
                        lock_obj.release()
                        del self._locks[key]

# 全局单例
method_mutex = ReentrantMultiKeyLock()


def _get_mutex_key(func: Callable, key: Union[str, Callable, None], args: tuple, kwargs: dict) -> str:
    """安全生成互斥key，逻辑清晰无歧义"""
    try:
        if key is None:
            # 场景1：未指定key → 模块.函数名
            return f"{func.__module__}.{func.__name__}"
        elif isinstance(key, str):
            # 场景2：字符串key → 直接使用
            return key
        elif callable(key):
            # 场景3：可调用key生成器 → 执行生成
            result = key(*args, **kwargs)
            if not isinstance(result, str):
                logging.warning(f"[Thread-{threading.get_ident()}] Key generator for {func.__name__} returned {type(result)}, converted to string")
                result = str(result)
            return result
        else:
            # 场景4：非法类型 → 默认key
            default_key = f"{func.__module__}.{func.__name__}.invalid"
            logging.warning(f"[Thread-{threading.get_ident()}] Invalid key type {type(key)} for {func.__name__}, using default: {default_key}")
            return default_key
    except Exception as e:
        default_key = f"{func.__module__}.{func.__name__}.error"
        logging.warning(f"[Thread-{threading.get_ident()}] Key generator failed for {func.__name__}: {e}, using default: {default_key}")
        return default_key


def mutex_method(key: Union[str, Callable, None] = None, timeout_seconds: int = 3600):
    """阻塞式互斥装饰器：支持重入、异常安全、无歧义"""
    # 处理无参数装饰（@mutex_method）
    if callable(key) and not isinstance(key, (str, type(lambda: None))):
        func = key
        key = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mutex_key = _get_mutex_key(func, key, args, kwargs)
            # 使用上下文管理器安全获取锁
            with method_mutex.acquire(mutex_key, timeout_seconds) as acquired:
                if not acquired:
                    raise RuntimeError(
                        f"[Thread-{threading.get_ident()}] Mutex key '{mutex_key}' is locked, "
                        f"cannot execute {func.__name__} (timeout: {timeout_seconds}s)"
                    )
                return func(*args, **kwargs)
        return wrapper

    # 处理带参数装饰（@mutex_method(key=..., timeout_seconds=...)）
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mutex_key = _get_mutex_key(func, key, args, kwargs)
            with method_mutex.acquire(mutex_key, timeout_seconds) as acquired:
                if not acquired:
                    raise RuntimeError(
                        f"[Thread-{threading.get_ident()}] Mutex key '{mutex_key}' is locked, "
                        f"cannot execute {func.__name__} (timeout: {timeout_seconds}s)"
                    )
                return func(*args, **kwargs)
        return wrapper
    return decorator


def nonblocking_mutex_method(key: Union[str, Callable, None] = None, timeout_seconds: int = 3600,
                             default_return: Any = None):
    """非阻塞式互斥装饰器：同一key重复调用返回默认值"""
    if callable(key) and not isinstance(key, (str, type(lambda: None))):
        func = key
        key = None
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mutex_key = _get_mutex_key(func, key, args, kwargs)
            if method_mutex.acquire(mutex_key, timeout_seconds):
                try:
                    return func(*args, **kwargs)
                finally:
                    method_mutex.release(mutex_key)
            return default_return
        return wrapper

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mutex_key = _get_mutex_key(func, key, args, kwargs)
            if method_mutex.acquire(mutex_key, timeout_seconds):
                try:
                    return func(*args, **kwargs)
                finally:
                    method_mutex.release(mutex_key)
            logging.warning(f"[Thread-{threading.get_ident()}] Non-blocking: {func.__name__} skipped (key '{mutex_key}' locked)")
            return default_return
        return wrapper
    return decorator


# ------------------------------ Key生成器（新增key_from_params）------------------------------
def key_from_args(*arg_indices, separator: str = "_"):
    """按参数索引生成key（原有功能）"""
    def generator(*args, **kwargs):
        parts = []
        for idx in arg_indices:
            parts.append(str(args[idx]) if idx < len(args) else f"arg{idx}_missing")
        return separator.join(parts)
    return generator


def simple_key(prefix: str, *arg_indices, **kwarg_names):
    """前缀+参数索引+关键字参数生成key（原有功能）"""
    def generator(*args, **kwargs):
        parts = [prefix]
        # 位置参数
        for idx in arg_indices:
            if idx < len(args):
                parts.append(str(args[idx]))
        # 关键字参数（kwarg_names的值为参数名，如project="project"）
        for param_name in kwarg_names.values():
            if param_name in kwargs:
                parts.append(str(kwargs[param_name]))
        return "_".join(parts)
    return generator


def key_from_param_names(*param_names, separator: str = "_"):
    """按参数名生成key（原有功能，需回溯栈帧）"""
    def generator(*args, **kwargs):
        frame = inspect.currentframe().f_back.f_back.f_back  # 回溯到被装饰函数
        local_vars = frame.f_locals if frame else {}
        parts = []
        for param in param_names:
            if param in local_vars:
                parts.append(str(local_vars[param]))
            elif param in kwargs:
                parts.append(str(kwargs[param]))
            else:
                parts.append(f"{param}_missing")
        return separator.join(parts)
    return generator


def key_from_params(*param_names, prefix: str = "", separator: str = "_"):
    """
    新增：按参数名提取值并拼接key（推荐使用，无需关心参数位置）
    Args:
        *param_names: 要包含的参数名（位置参数、关键字参数均可）
        prefix: key前缀（可选）
        separator: 参数值分隔符（默认"_"）
    示例：
        @mutex_method(key=key_from_params("user_id", "project", prefix="order"))
        def create_order(user_id: int, project: str, amount: float): ...
        → 调用 create_order(123, "test", 100) → key = "order_123_test"
    """
    def generator(*args, **kwargs):
        # 获取函数签名，解析参数名与位置的映射
        func = inspect.currentframe().f_back.f_back.f_back.f_code  # 回溯到被装饰函数
        param_spec = inspect.getfullargspec(func)
        param_names_list = param_spec.args  # 函数定义的参数名列表

        key_parts = [prefix] if prefix else []  # 前缀（可选）

        for param_name in param_names:
            # 1. 先从位置参数中找（根据参数名对应的索引）
            if param_name in param_names_list:
                param_idx = param_names_list.index(param_name)
                if param_idx < len(args):
                    key_parts.append(str(args[param_idx]))
                    continue
            # 2. 再从关键字参数中找
            if param_name in kwargs:
                key_parts.append(str(kwargs[param_name]))
                continue
            # 3. 参数缺失，用占位符
            key_parts.append(f"{param_name}_missing")

        # 移除空字符串（避免前缀为空时出现多余分隔符）
        key_parts = [part for part in key_parts if part]
        return separator.join(key_parts)
    return generator