import asyncio
import logging
import importlib
import inspect
import pickle
import base64
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Union, Coroutine

from zhkj_plugins.secret_util import SecretUtil

logger = logging.getLogger(__name__)


class PickleSerializer:
    """Pickle 序列化器"""

    @staticmethod
    def dumps(obj: any) -> str:
        """序列化对象为 base64 字符串"""
        try:
            pickled = pickle.dumps(obj)
            return base64.b64encode(pickled).decode('utf-8')
        except Exception as e:
            logger.error(f"Pickle序列化失败: {str(e)}")
            raise Exception(f"数据序列化失败: {str(e)}")

    @staticmethod
    def loads(data: str) -> any:
        """从 base64 字符串反序列化对象"""
        try:
            pickled = base64.b64decode(data.encode('utf-8'))
            return pickle.loads(pickled)
        except Exception as e:
            logger.error(f"Pickle反序列化失败: {str(e)}")
            raise Exception(f"数据反序列化失败: {str(e)}")


class RPCService:
    """RPC服务核心类，不依赖Flask"""

    def __init__(self, secret_key: bytes):
        self.secret_util = SecretUtil(secret_key)
        self.serializer = PickleSerializer()
        self._loop = None

    def get_or_create_loop(self):
        """获取或创建事件循环"""
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            if self._loop is None:
                self._loop = asyncio.new_event_loop()
            return self._loop

    def process_request(self, encrypted_data: str) -> str:
        """同步包装器"""
        loop = self.get_or_create_loop()

        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self.async_process_request(encrypted_data),
                loop
            )
            return future.result(timeout=30)  # 30秒超时
        else:
            # 启动新的事件循环
            return loop.run_until_complete(
                self.async_process_request(encrypted_data)
            )

    async def async_process_request(self, encrypted_data: str) -> Union[Coroutine, str]:
        """处理RPC请求，返回加密的响应数据"""
        try:
            # 解密数据
            decrypted_data = self.secret_util.decrypt_data(encrypted_data)
            if not decrypted_data:
                return self._create_error_response("数据解密失败")

            # 反序列化请求
            try:
                request_data = self.serializer.loads(decrypted_data)
            except Exception as e:
                return self._create_error_response(f"请求数据反序列化失败: {str(e)}")

            # 提取参数
            class_path = request_data.get('class')
            method_name = request_data.get('method')
            params = request_data.get('params', {})

            # 验证参数
            if not all([class_path, method_name]):
                return self._create_error_response("缺少必要参数: class 或 method")

            # 动态调用
            try:
                result = await self._dynamic_call(class_path, method_name, params)
                return self._create_success_response(result)
            except Exception as e:
                logger.error(f"方法调用异常: {str(e)}")
                return self._create_error_response(str(e))

        except Exception as e:
            logger.error(f"RPC处理异常: {str(e)}")
            return self._create_error_response(f"系统错误: {str(e)}")

    def _create_success_response(self, result: any) -> str:
        """创建成功响应"""
        serialized_result = self.serializer.dumps(result)
        return self.secret_util.encrypt_data(serialized_result)

    def _create_error_response(self, error_msg: str) -> str:
        """创建错误响应"""
        error = Exception(error_msg)
        serialized_error = self.serializer.dumps(error)
        return self.secret_util.encrypt_data(serialized_error)

    async def _dynamic_call(self, class_path: str, method_name: str, params: dict) -> Union[Coroutine, str]:
        """动态调用指定类的方法"""
        try:
            # 动态导入模块和类
            module_name, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            target_class = getattr(module, class_name)

            # 检查方法是否存在
            if not hasattr(target_class, method_name):
                raise AttributeError(f"类 {class_path} 不存在方法 {method_name}")

            method = getattr(target_class, method_name)

            # 检查是否为类方法或静态方法
            if inspect.ismethod(method) or inspect.isfunction(method):
                # 实例化类（如果需要）
                instance = target_class() if not inspect.isclass(method) else target_class

                # 调用方法
                if inspect.iscoroutinefunction(method):
                    # 异步方法
                    return await method(instance, **params)
                else:
                    # 同步方法
                    return method(instance, **params)
            else:
                raise TypeError(f"方法 {method_name} 不可调用")

        except ImportError as e:
            raise Exception(f"无法导入类 {class_path}: {str(e)}")
        except Exception as e:
            raise
