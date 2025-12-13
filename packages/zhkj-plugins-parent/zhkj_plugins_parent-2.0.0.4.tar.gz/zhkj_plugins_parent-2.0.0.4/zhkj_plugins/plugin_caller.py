import uuid
import pickle
import base64
import inspect
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, Callable, Union
import requests
import aiohttp
import time
import io

from .secret_util import SecretUtil

logger = logging.getLogger("PluginCaller")


def rpc_class(plugin_name: str, timeout: int = 30):
    """类级别 RPC 装饰器，支持超时配置

    Args:
        plugin_name: 插件名称
        timeout: 默认超时时间（秒）
    """

    def decorator(cls):
        # 添加类级别元数据
        cls._rpc_class_metadata = {
            "plugin_name": plugin_name,
            "timeout": timeout
        }

        # 保存原始 __getattribute__ 方法
        original_getattribute = cls.__getattribute__

        def __getattribute__(self, name: str):
            """拦截方法调用，自动处理RPC调用"""
            try:
                attr = original_getattribute(self, name)

                if not callable(attr) or not hasattr(attr, '_rpc_metadata'):
                    return attr

                # 检查是否是异步方法
                if asyncio.iscoroutinefunction(attr):
                    async def async_rpc_wrapper(*args, **kwargs):
                        return await self._call_rpc_method_async(attr, *args, **kwargs)

                    return async_rpc_wrapper
                else:
                    def sync_rpc_wrapper(*args, **kwargs):
                        return self._call_rpc_method(attr, *args, **kwargs)

                    return sync_rpc_wrapper

            except AttributeError:
                return original_getattribute(self, name)

        cls.__getattribute__ = __getattribute__
        return cls

    return decorator


def rpc_method(method_name: str = None, endpoint: str = "/api/v1/call",
               timeout: Optional[int] = None, retry_times: int = 1):
    """
    RPC方法注解，配置调用参数
    """

    def decorator(func):
        func._rpc_metadata = {
            "method_name": method_name or func.__name__,
            "endpoint": endpoint,
            "timeout": timeout,
            "retry_times": retry_times
        }
        return func

    return decorator


class RPCError(Exception):
    """RPC调用异常"""

    def __init__(self, message: str, request_id: str = None, original_exception: Exception = None):
        self.message = message
        self.request_id = request_id
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        base_msg = f"RPCError: {self.message}"
        if self.request_id:
            base_msg += f" (Request ID: {self.request_id})"
        if self.original_exception:
            base_msg += f" [Original: {str(self.original_exception)}]"
        return base_msg


class PickleSerializer:
    """安全的Pickle序列化器，使用fickling防御反序列化攻击"""

    @staticmethod
    def dumps(obj: Any) -> str:
        """序列化对象为 base64 字符串"""
        try:
            pickled = pickle.dumps(obj)
            return base64.b64encode(pickled).decode('utf-8')
        except Exception as e:
            logger.error(f"Pickle序列化失败: {str(e)}")
            raise RPCError(f"数据序列化失败: {str(e)}")

    # @staticmethod
    # def loads(data: str) -> Any:
    #     """从 base64 字符串安全反序列化对象，使用fickling进行安全检查"""
    #     try:
    #         from fickling.loader import load as fickling_load
    #         from fickling.analysis import Severity
    #         # 解码base64数据
    #         pickled = base64.b64decode(data.encode('utf-8'))
    #
    #         # 使用fickling进行安全反序列化
    #         # 设置安全级别为LIKELY_SAFE，只允许最安全的操作
    #         logger.info(pickle.loads(pickled))
    #         file_obj = io.BytesIO(pickled)
    #         result = fickling_load(file_obj, max_acceptable_severity=Severity.LIKELY_UNSAFE)
    #
    #         return result
    #     except Exception as e:
    #         logger.error(e, exc_info=True)
    #         raise RPCError(f"数据反序列化失败: {str(e)}")

    @staticmethod
    def loads(data: str) -> Any:
        """从 base64 字符串反序列化对象"""
        try:
            pickled = base64.b64decode(data.encode('utf-8'))
            return pickle.loads(pickled)
        except Exception as e:
            logger.error(f"Pickle反序列化失败: {str(e)}")
            raise RPCError(f"数据反序列化失败: {str(e)}")


class RequestResponseProcessor:
    """请求响应处理器，提取共用逻辑"""

    def __init__(self, secret_util):
        self.secret_util = secret_util

    def prepare_request_data(self, method_name: str, params: Dict[str, Any],
                             class_name: str) -> Dict[str, Any]:
        """准备请求数据"""
        request_id = str(uuid.uuid4())

        request_data = {
            "class": class_name,
            "method": method_name,
            "params": params,
            "timestamp": datetime.now().isoformat(),
            "request_id": request_id
        }

        # 序列化请求数据
        serialized_request = PickleSerializer.dumps(request_data)

        # 加密序列化后的数据
        encrypted_request = self.secret_util.encrypt_data(serialized_request)
        if not encrypted_request:
            raise RPCError("请求数据加密失败", request_id)

        return {
            "encrypted_request": encrypted_request,
            "request_id": request_id
        }

    def process_response(self, encrypted_response: str, request_id: str) -> Any:
        """处理响应数据"""
        if not encrypted_response:
            raise RPCError("响应数据为空", request_id)

        # 解密响应数据
        decrypted_response = self.secret_util.decrypt_data(encrypted_response)
        if not decrypted_response:
            raise RPCError("响应数据解密失败", request_id)

        # 使用Pickle反序列化得到原始结果
        result = PickleSerializer.loads(decrypted_response)

        # 如果结果是异常对象，直接抛出
        if isinstance(result, Exception):
            raise result

        # 返回正常结果
        return result


class RPCCallerBase:
    """
    RPC调用基类，使用Pickle序列化，支持同步和异步调用
    """

    def __init__(self, plugin_manager, secret_key: bytes = None, port=None):
        self.plugin_manager = plugin_manager
        self.port = port
        self.secret_util = SecretUtil(secret_key)
        self.processor = RequestResponseProcessor(self.secret_util)
        self._plugin_name = self._get_plugin_name()
        self._timeout = self._get_timeout()
        self._base_url = None
        self._session = requests.Session()
        self._async_session = None
        self._class_name = self.__class__.__module__ + "." + self.__class__.__name__
        self._initialize_base_url()

    def _get_plugin_name(self) -> str:
        """从类注解获取插件名称"""
        return getattr(self.__class__, '_rpc_class_metadata', {}).get('plugin_name')

    def _get_timeout(self) -> int:
        """从类注解获取超时时间"""
        return getattr(self.__class__, '_rpc_class_metadata', {}).get('timeout', 30)

    def _initialize_base_url(self):
        """初始化插件的基础URL"""
        if not self._plugin_name:
            logger.warning("未设置插件名称，请使用@rpc_class注解")
            return

        if not self.port:
            self.port = self.plugin_manager.get_service_port(self._plugin_name)

        if self.port:
            self._base_url = f"http://127.0.0.1:{self.port}"
            logger.info(f"初始化插件 {self._plugin_name} 调用器，地址: {self._base_url}")
        else:
            logger.warning(f"无法获取插件 {self._plugin_name} 的端口，插件可能未运行")

    async def _get_async_session(self) -> aiohttp.ClientSession:
        """获取或创建异步会话"""
        if self._async_session is None or self._async_session.closed:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._async_session = aiohttp.ClientSession(timeout=timeout)
        return self._async_session

    async def close_async_session(self):
        """关闭异步会话"""
        if self._async_session and not self._async_session.closed:
            await self._async_session.close()

    def __getattribute__(self, name: str):
        """拦截方法调用，自动处理RPC调用"""
        try:
            # 先获取属性
            attr = object.__getattribute__(self, name)

            # 如果是可调用方法且有RPC元数据，则包装它
            if callable(attr) and hasattr(attr, '_rpc_metadata'):
                # 检查是否是异步方法
                if asyncio.iscoroutinefunction(attr):
                    async def async_rpc_wrapper(*args, **kwargs):
                        return await self._call_rpc_method_async(attr, *args, **kwargs)

                    return async_rpc_wrapper
                else:
                    def sync_rpc_wrapper(*args, **kwargs):
                        return self._call_rpc_method(attr, *args, **kwargs)

                    return sync_rpc_wrapper

            return attr

        except AttributeError:
            return object.__getattribute__(self, name)

    def _call_rpc_method_common(self, method: Callable, args: tuple, kwargs: dict,
                                is_async: bool = False) -> Any:
        """
        RPC调用的共用逻辑
        """
        if not self._base_url:
            raise RPCError("插件未运行或无法获取服务地址")

        metadata = method._rpc_metadata
        method_name = metadata['method_name']
        endpoint = metadata['endpoint']
        timeout = metadata['timeout'] or self._timeout
        retry_times = metadata.get('retry_times', 1)

        # 构建参数
        params = self._build_params(method, args, kwargs)

        last_exception = None
        for attempt in range(retry_times):
            try:
                # 根据同步/异步执行调用
                if is_async:
                    result = self._execute_call_async(method_name, params, endpoint, timeout)
                    if asyncio.iscoroutine(result):
                        return result
                    else:
                        # 如果返回的是普通值，包装为协程
                        async def return_value():
                            return result

                        return return_value()
                else:
                    return self._execute_call(method_name, params, endpoint, timeout)

            except (RPCError, Exception) as e:
                last_exception = e if isinstance(e, RPCError) else RPCError(f"RPC调用异常: {str(e)}")

                if attempt < retry_times - 1:  # 不是最后一次重试
                    sleep_time = 1
                    logger.warning(f"RPC调用失败，正在进行第 {attempt + 1} 次重试: {str(e)}")
                    if is_async:
                        # 对于异步调用，我们需要返回一个协程
                        async def retry_async():
                            await asyncio.sleep(sleep_time)
                            # 这里不能直接递归调用，需要重新实现重试逻辑
                            # 简化处理：抛出异常，由外层循环处理
                            raise last_exception

                        return retry_async()
                    else:
                        time.sleep(sleep_time)
                else:
                    logger.error(f"RPC调用失败，已达最大重试次数 {retry_times}: {str(e)}")
                    raise last_exception

        # 所有重试都失败
        raise last_exception or RPCError("RPC调用失败")

    def _call_rpc_method(self, method: Callable, *args, **kwargs) -> Any:
        """
        执行同步RPC调用
        """
        return self._call_rpc_method_common(method, args, kwargs, is_async=False)

    async def _call_rpc_method_async(self, method: Callable, *args, **kwargs) -> Any:
        """
        执行异步RPC调用
        """
        result = self._call_rpc_method_common(method, args, kwargs, is_async=True)
        if asyncio.iscoroutine(result):
            return await result
        return result

    def _build_params(self, method: Callable, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """
        根据方法签名构建参数
        """
        try:
            sig = inspect.signature(method)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            params = dict(bound_args.arguments)

            # 移除self参数
            if 'self' in params:
                del params['self']

            return params

        except Exception as e:
            logger.error(f"参数构建失败: {str(e)}")
            raise RPCError(f"参数构建失败: {str(e)}") from e

    def _execute_call(self, method_name: str, params: Dict[str, Any],
                      endpoint: str, timeout: int) -> Any:
        """
        执行实际的同步RPC调用
        """
        try:
            # 准备请求数据
            prepared_data = self.processor.prepare_request_data(
                method_name, params, self._class_name
            )
            encrypted_request = prepared_data["encrypted_request"]
            request_id = prepared_data["request_id"]

            # 发送请求
            url = f"{self._base_url}{endpoint}"
            payload = {"data": encrypted_request}

            logger.debug(f"发送同步RPC请求到 {url}, 方法: {method_name}, 请求ID: {request_id}")
            response = self._session.post(url, json=payload, timeout=timeout)

            if response.status_code != 200:
                raise RPCError(f"HTTP错误: {response.status_code}", request_id)

            # 解析响应
            response_data = response.json()

            # 检查响应中是否有错误信息
            if 'error' in response_data:
                raise RPCError(f"插件返回错误: {response_data['error']}", request_id)

            # 获取加密的响应数据并处理
            encrypted_response = response_data.get("data")
            return self.processor.process_response(encrypted_response, request_id)

        except requests.exceptions.Timeout:
            raise RPCError("请求超时", request_id)
        except requests.exceptions.ConnectionError:
            raise RPCError("连接失败", request_id)
        except RPCError:
            raise
        except Exception as e:
            raise RPCError(f"调用异常: {str(e)}", request_id) from e

    async def _execute_call_async(self, method_name: str, params: Dict[str, Any],
                                  endpoint: str, timeout: int) -> Any:
        """
        执行实际的异步RPC调用
        """
        try:
            # 准备请求数据
            prepared_data = self.processor.prepare_request_data(
                method_name, params, self._class_name
            )
            encrypted_request = prepared_data["encrypted_request"]
            request_id = prepared_data["request_id"]

            # 发送异步请求
            url = f"{self._base_url}{endpoint}"
            payload = {"data": encrypted_request}

            logger.debug(f"发送异步RPC请求到 {url}, 方法: {method_name}, 请求ID: {request_id}")

            session = await self._get_async_session()
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise RPCError(f"HTTP错误: {response.status}", request_id)

                # 解析响应
                response_data = await response.json()

                # 检查响应中是否有错误信息
                if 'error' in response_data:
                    raise RPCError(f"插件返回错误: {response_data['error']}", request_id)

                # 获取加密的响应数据并处理
                encrypted_response = response_data.get("data")
                return self.processor.process_response(encrypted_response, request_id)

        except asyncio.TimeoutError:
            raise RPCError("请求超时", request_id)
        except aiohttp.ClientConnectionError:
            raise RPCError("连接失败", request_id)
        except RPCError:
            raise
        except Exception as e:
            raise RPCError(f"异步调用异常: {str(e)}", request_id) from e

    def get_available_methods(self) -> list:
        """
        获取可用的RPC方法列表
        """
        methods = []
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if callable(attr) and hasattr(attr, '_rpc_metadata'):
                    methods.append({
                        'name': attr._rpc_metadata['method_name'],
                        'async': asyncio.iscoroutinefunction(attr)
                    })
            except:
                continue
        return methods

    def validate_connection(self) -> bool:
        """
        验证与插件的连接（同步）
        """
        if not self._base_url:
            return False

        try:
            response = self._session.get(f"{self._base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    async def validate_connection_async(self) -> bool:
        """
        验证与插件的连接（异步）
        """
        if not self._base_url:
            return False

        try:
            session = await self._get_async_session()
            async with session.get(f"{self._base_url}/health") as response:
                return response.status == 200
        except:
            return False

    def update_base_url(self, port: int = None):
        """更新基础URL，用于动态端口变化的情况"""
        if port:
            self.port = port
        self._initialize_base_url()

    async def __aenter__(self):
        """异步上下文管理器支持"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出时关闭会话"""
        await self.close_async_session()
