import logging
import threading
import time
from queue import Empty, Queue

logger = logging.getLogger("ProcessOutputMonitor")


class ProcessOutputMonitor:
    """进程输出监控器"""

    def __init__(self, process, plugin_name, success_indicator, timeout=30):
        self.process = process
        self.plugin_name = plugin_name
        self.success_indicator = success_indicator
        self.timeout = timeout
        self.output_queue = Queue()
        self.success = False
        self.monitor_thread = None
        self._stop_monitoring = threading.Event()

    def _read_output(self):
        """在单独线程中读取输出"""
        try:
            while not self._stop_monitoring.is_set() and self.process.poll() is None:
                if (hasattr(self.process, 'stdout') and
                        self.process.stdout is not None):
                    output = self.process.stdout.readline()
                    if output:
                        decoded = output.decode('utf-8', errors='ignore').strip()
                        if decoded:
                            self.output_queue.put(decoded)
                            logger.info(f"插件 {self.plugin_name} 输出: {decoded}")
                            if self.success_indicator in decoded:
                                self.success = True
                                logger.info(f"插件 {self.plugin_name} 启动成功")
                                # 不在这里return，让循环继续
                time.sleep(0.1)
        except Exception as e:
            logger.error(f"监控线程错误: {e}")
        finally:
            try:
                self.process.stdout.close()
            except:
                pass

    def wait_for_success(self):
        """等待成功指示符"""
        if not self.process:
            return False


        self._stop_monitoring.clear()
        self.success = False

        self.monitor_thread = threading.Thread(target=self._read_output)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        start_time = time.time()
        try:
            while time.time() - start_time < self.timeout:
                if self.success:
                    self._stop_monitoring.set()
                    return True

                # 检查进程是否异常退出
                if self.process.poll() is not None:
                    logger.error(f"插件进程异常退出，返回码: {self.process.poll()}")
                    self._stop_monitoring.set()
                    return False

                # 非阻塞地处理队列中的输出
                try:
                    while True:
                        output = self.output_queue.get_nowait()
                        # 输出已经在监控线程中处理过了，这里只是清空队列
                except Empty:
                    pass

                time.sleep(0.1)

            logger.warning(f"等待插件 {self.plugin_name} 启动超时")
            return False
        finally:
            self._stop_monitoring.set()




    # 容易卡死
    def wait_for_success1(self):
        """等待成功指示符"""
        if not self.process:
            return False

        self._stop_monitoring.clear()
        self.success = False

        self.monitor_thread = threading.Thread(target=self._read_output)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

        start_time = time.time()
        try:
            while time.time() - start_time < self.timeout:
                if self.success:
                    self._stop_monitoring.set()
                    return True

                # 检查进程是否异常退出
                if self.process.poll() is not None:
                    logger.error(f"插件进程异常退出，返回码: {self.process.poll()}")
                    self._stop_monitoring.set()
                    return False

                # 非阻塞地处理队列中的输出
                try:
                    while True:
                        output = self.output_queue.get_nowait()
                        # 输出已经在监控线程中处理过了，这里只是清空队列
                except Empty:
                    pass

                time.sleep(0.1)

            logger.warning(f"等待插件 {self.plugin_name} 启动超时")
            return False
        finally:
            self._stop_monitoring.set()


