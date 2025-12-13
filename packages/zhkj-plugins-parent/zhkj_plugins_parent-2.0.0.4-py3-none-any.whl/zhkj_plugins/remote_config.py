import os

from typing import List

import json
import requests
import threading
import time
from typing import Dict, Optional, Any, Callable

from zhkj_plugins.wrap import singleton


@singleton
class RemoteSettings:
    def __init__(self,
                 remote_url: str,
                 update_interval,
                 timeout: int,
                 initial_config: Optional[Dict] = None,
                 default_config: Optional[Dict] = None,
                 env_file: str = ".env"):
        self.remote_url = remote_url
        self.update_interval = update_interval
        self.timeout = timeout
        self._config = initial_config or {}
        self._default_config = default_config or {}
        self._last_updated = 0
        self._updating = False  # 标记是否正在更新

        # 使用单个可重入锁简化实现
        self._lock = threading.RLock()

        # -------------------------- 新增：加载环境变量 --------------------------
        self._env_file = env_file
        # 1. 读取.env文件（不污染系统环境变量），键为文件中定义的格式（建议大写下划线）
        env_from_file = self._load_env_file()
        # 2. 读取系统环境变量
        env_from_system = dict(os.environ)
        # 3. 合并：.env变量覆盖系统变量（确保.env优先级更高）
        self._env_config = {**env_from_system, **env_from_file}
        # ----------------------------------------------------------------------

        # 首次更新
        self.update()

    def _load_env_file(self) -> Dict[str, str]:
        """
        自定义解析.env文件，支持格式：
        - KEY=VALUE（基本格式）
        - KEY="VALUE WITH SPACE"（双引号值，自动去除引号）
        - KEY='VALUE WITH SPACE'（单引号值，自动去除引号）
        - # 注释行（忽略）
        - 空行（忽略）
        - 键值对前后空格（自动去除，如 KEY = VALUE → KEY=VALUE）
        """
        env_dict = {}
        # 处理文件不存在的情况（无.env文件则返回空字典）
        if not os.path.exists(self._env_file):
            print(f"提示：.env文件 {self._env_file} 不存在，跳过加载")
            return env_dict

        # 读取文件并逐行解析
        try:
            with open(self._env_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):  # line_num用于定位错误行
                    # 1. 去除行首尾空格（处理空行、行尾换行符）
                    stripped_line = line.strip()
                    # 2. 忽略空行和注释行（#开头）
                    if not stripped_line or stripped_line.startswith("#"):
                        continue
                    # 3. 分割键值对（只按第一个"="分割，避免值中包含"="的情况，如URL）
                    if "=" not in stripped_line:
                        print(f"警告：.env第{line_num}行格式错误（无'='），跳过该行：{line}")
                        continue
                    key, value = stripped_line.split("=", 1)  # split("=", 1)：只分割一次
                    # 4. 去除键的前后空格（如 " KEY " → "KEY"）
                    key = key.strip()
                    # 5. 处理值的前后空格和引号（如 " 'value' " → "value"）
                    value = value.strip()
                    # 去除值的单/双引号（如 "abc" → abc，'abc' → abc）
                    if (value.startswith('"') and value.endswith('"')) or (
                            value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]  # 去掉首尾引号

                    # 6. 加入字典（键重复时，后定义的覆盖前定义的，符合.env常规逻辑）
                    env_dict[key] = value
            return env_dict
        except Exception as e:
            print(f"错误：解析.env文件 {self._env_file} 失败，原因：{str(e)}")
            return env_dict

    def _fetch_remote_config(self) -> Optional[Dict]:
        """从远程获取配置"""
        try:
            response = requests.get(
                self.remote_url,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {str(e)}")
        except Exception as e:
            print(f"获取远程配置失败: {str(e)}")
        return None

    def _parse_config(self, remote_config: Dict) -> Dict:
        """解析远程配置，子类可重写此方法以支持不同格式"""
        settings = remote_config.get("data", {})
        return {key: settings[key]["content"] for key in settings}

    def update(self) -> bool:
        """更新配置（写操作）"""
        # 如果已经在更新中，直接返回
        if self._updating:
            return False

        # 标记为正在更新
        self._updating = True
        try:
            new_config = self._fetch_remote_config()
            if new_config:
                try:
                    new_data = self._parse_config(new_config)
                    with self._lock:
                        self._config = new_data
                        self._last_updated = time.time()
                    return True
                except Exception as e:
                    print(f"解析配置失败: {str(e)}")
            return False
        finally:
            self._updating = False

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置（读操作）"""
        if key in self._env_config:
            return self._env_config.get(key)  # 环境变量值为字符串，后续类型方法会处理
        # 检查是否需要更新（无锁快速检查）
        if self._should_update() and not self._updating:
            threading.Thread(target=self.update, daemon=True).start()

        # 读锁保证读取时配置不会被修改
        with self._lock:
            if key in self._config:
                return self._config.get(key, None)
            else:
                return self._default_config.get(key, default)

    def get_int(self, key, default: Any = None) -> Optional[int]:
        try:
            value = self.get(key, default)
            return int(value)
        except:
            return None

    def get_float(self, key, default: Any = None) -> Optional[float]:
        try:
            value = self.get(key, default)
            return float(value)
        except:
            return None

    def get_list(self, key, default: Any = None) -> Optional[List[Any]]:
        try:
            value = self.get(key, default)
            obj = json.loads(value)
            if isinstance(obj, list):
                return obj
            else:
                return None
        except:
            return None

    def get_dict(self, key, default: Any = None) -> Optional[Dict[str, Any]]:
        try:
            value = self.get(key, default)
            obj = json.loads(value)
            if isinstance(obj, dict):
                return obj
            else:
                return None
        except:
            return None

    def get_bool(self, key, default: Any = None) -> Optional[bool]:
        try:
            value = self.get(key, default)
            # 定义应该转换为 True 的值
            true_values = [True, 1, "1", "true", "True"]
            # 定义应该转换为 False 的值
            false_values = [False, "False", "false", 0, "0", None, ""]

            if value in true_values:
                return True
            elif value in false_values:
                return False
            elif value is not None:
                return True
            else:
                return False
        except:
            return None

    def _should_update(self) -> bool:
        return time.time() - self._last_updated >= self.update_interval

    def get_last_updated(self) -> int:
        return self._last_updated


# 使用示例
if __name__ == "__main__":
    # 示例远程配置URL

    try:
        # 模拟程序运行，定期获取配置
        while True:
            print("\n当前配置:")
            print(f"智能成片-任务总数: {RemoteSettings(update_interval=30).get('smart_mix_cut_task_count')}")
            print(f"智能成片-任务间隔: {RemoteSettings().get('smart_mix_cut_task_interval')}")
            print(json.loads(RemoteSettings().get(Constants.SMART_MIX_CUT_SELLING_LIST, '["特惠"]'))[0])
            print(f"最后更新时间: {time.ctime(RemoteSettings().get_last_updated())}")
            print(f"{RemoteSettings().get_list('smart_mix_cut_downloading_video_duration_5_9', '[10,20]')}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("程序退出...")
