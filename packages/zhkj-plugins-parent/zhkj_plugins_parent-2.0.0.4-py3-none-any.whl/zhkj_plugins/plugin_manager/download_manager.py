import json

import requests
import hashlib
import time
from pathlib import Path
from typing import Optional, Callable
import logging

from zhkj_plugins.wrap import singleton

logger = logging.getLogger("PluginManager.DownloadManager")


@singleton
class DownloadManager:
    def __init__(self):
        pass

    def download(self, url: str, save_path: str,
                 timeout: int = 30,
                 max_retries: int = 3) -> Optional[str]:
        """下载插件配置文件并解析为 PluginConfig 对象"""
        save_path_obj = Path(save_path)
        # 确保保存目录存在
        self._ensure_dir(save_path_obj.parent)

        for attempt in range(max_retries):
            try:
                logger.info(f"开始下载插件配置 (尝试 {attempt + 1}/{max_retries}): {url}")

                # 发送 GET 请求开始下载（流式传输）
                with requests.get(url, stream=True, timeout=timeout) as response:
                    response.raise_for_status()

                    with open(save_path, 'wb') as f:
                        f.write(response.content)

                    return save_path

            except requests.RequestException as e:
                logger.warning(f"下载插件配置失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    sleep_time = 2 ** attempt  # 指数退避
                    logger.info(f"{sleep_time}秒后重试...")
                    time.sleep(sleep_time)
            except Exception as e:
                logger.error(f"下载过程中发生未知错误: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)

        logger.error(f"下载插件配置失败，已重试 {max_retries} 次: {url}")
        return None

    def download_with_progress(
            self,
            url: str,
            save_path: str,
            progress_callback: Optional[Callable[[int, int, float], None]] = None,
            chunk_size: int = 8192,
            timeout: int = 600,
            max_retries: int = 3
    ) -> bool:
        """带进度回调的文件下载函数"""
        save_path_obj = Path(save_path)

        for attempt in range(max_retries):
            try:
                # 确保保存目录存在
                self._ensure_dir(save_path_obj.parent)

                # 发送 HEAD 请求获取文件总大小
                head_response = requests.head(url, timeout=timeout)
                head_response.raise_for_status()
                total_size = int(head_response.headers.get('Content-Length', 0))

                # 发送 GET 请求开始下载（流式传输）
                with requests.get(url, stream=True, timeout=timeout) as response:
                    response.raise_for_status()

                    if total_size == 0:
                        total_size = int(response.headers.get('Content-Length', 0))

                    downloaded_size = 0
                    start_time = time.time()
                    last_time = start_time
                    last_downloaded = 0

                    with open(save_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded_size += len(chunk)

                                current_time = time.time()
                                time_diff = current_time - last_time
                                if time_diff > 0.1:
                                    speed = (downloaded_size - last_downloaded) / (time_diff * 1024)
                                    last_time = current_time
                                    last_downloaded = downloaded_size

                                    if progress_callback:
                                        try:
                                            progress_callback(downloaded_size, total_size, speed)
                                        except Exception as e:
                                            logger.warning(f"进度回调执行失败: {str(e)}")

                    if progress_callback:
                        total_time = time.time() - start_time
                        avg_speed = (downloaded_size / (total_time * 1024)) if total_time > 0 else 0
                        try:
                            progress_callback(downloaded_size, total_size, avg_speed)
                        except Exception as e:
                            logger.warning(f"最终进度回调执行失败: {str(e)}")

                logger.info(f"下载完成: {save_path}")
                return True

            except requests.RequestException as e:
                logger.warning(f"下载失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"下载失败，已达到最大重试次数: {url}, {str(e)}")
                    if save_path_obj.exists():
                        save_path_obj.unlink()  # 删除可能不完整的文件
                    return False
                time.sleep(2 ** attempt)  # 指数退避
            except Exception as e:
                logger.error(f"下载过程中发生未知错误: {str(e)}")
                if save_path_obj.exists():
                    save_path_obj.unlink()
                return False

        return False

    def calculate_file_md5(self, file_path: Path) -> str:
        """计算文件的MD5哈希值"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"计算文件MD5失败 {file_path}: {str(e)}")
            return ""

    def _ensure_dir(self, dir_path: Path) -> bool:
        """确保目录存在"""
        try:
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"创建目录: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"创建目录失败 {dir_path}: {str(e)}")
            return False
