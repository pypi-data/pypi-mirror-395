import logging

logger = logging.getLogger(__name__)

import threading
import time
import uuid
import asyncio  # <-- 新增导入
import inspect  # <-- 新增导入
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Any, List
# 假设 zhkj_plugins.wrap.singleton 存在
from zhkj_plugins.wrap import singleton


@dataclass
class TaskInfo:
    task_id: str
    progress: int = 0  # 0-100
    status: str = "pending"  # pending/running/finished/failed/timeout
    step: str = ""  # 当前步骤描述
    result: Optional[Any] = None  # 任务结果
    error: Optional[str] = None  # 错误信息
    create_time: float = field(default_factory=time.time)
    update_time: float = field(default_factory=time.time)


class NestedProgressCallback:
    """嵌套进度回调类"""

    def __init__(self, parent_callback: Optional[Callable[[float, str], None]],
                 start_percent: float, end_percent: float, parent_step: str = ""):
        """
        :param parent_callback: 父进度回调函数
        :param start_percent: 子进度开始的百分比
        :param end_percent: 子进度结束的百分比
        :param parent_step: 父步骤描述
        """
        self.parent_callback = parent_callback or (lambda progress, step: ())
        self.start_percent = start_percent
        self.end_percent = end_percent
        self.parent_step = parent_step
        self.range_size = end_percent - start_percent

    def __call__(self, progress: float, step: str = ""):
        """更新嵌套进度"""
        progress = max(0.0, min(100.0, progress))  # 确保进度在0-100之间

        # 计算在总进度中的位置
        total_progress = self.start_percent + int(self.range_size * progress / 100)

        # 构建完整的步骤描述
        full_step = self.parent_step
        if step:
            if full_step:
                full_step += f" > {step}"
            else:
                full_step = step

        # 调用父回调
        self.parent_callback(total_progress, full_step)

    def create_sub_callback(self, sub_start: float, sub_end: float, sub_step: str = ""):
        """创建子进度回调（支持多级嵌套）"""
        # 计算在父进度范围内的起始和结束位置
        absolute_start = self.start_percent + int(self.range_size * sub_start / 100)
        absolute_end = self.start_percent + int(self.range_size * sub_end / 100)

        # 构建步骤描述
        full_step = self.parent_step
        if sub_step:
            if full_step:
                full_step += f" > {sub_step}"
            else:
                full_step = sub_step

        return NestedProgressCallback(
            self.parent_callback, absolute_start, absolute_end, full_step
        )


@singleton
class AsyncTaskManager:
    def __init__(self, timeout: int = 3600):
        self.timeout = timeout  # 任务默认超时时间（秒）
        self.tasks: Dict[str, TaskInfo] = {}  # 任务存储：task_id -> TaskInfo
        self.lock = threading.Lock()  # 线程安全锁

    # -------------------------- 修改后的 create_task 方法 --------------------------
    def create_task(self, task_func: Callable, *args, **kwargs) -> str:
        task_id = str(uuid.uuid4())
        is_async = inspect.iscoroutinefunction(task_func)  # <-- 检查是否为异步函数

        with self.lock:
            self.tasks[task_id] = TaskInfo(task_id=task_id, step="初始化任务...")

        def progress_callback(progress: float, step: str = ""):
            progress = max(0.0, min(100.0, progress))
            with self.lock:
                # 仅在任务处于 'running' 状态时更新进度，防止结束后或失败后进度被修改
                if task_id in self.tasks and self.tasks[task_id].status == "running":
                    self.tasks[task_id].progress = int(progress)  # 统一转为整数
                    self.tasks[task_id].step = step
                    self.tasks[task_id].update_time = time.time()

        def _run_task():
            try:
                # 1. 设置任务状态为运行中
                with self.lock:
                    if task_id in self.tasks:
                        self.tasks[task_id].status = "running"
                        self.tasks[task_id].update_time = time.time()

                # 2. 调用任务函数
                final_kwargs = {**kwargs, "progress_callback": progress_callback}

                if is_async:
                    # 异步任务：创建新的事件循环并在其中运行
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    logger.info(f"任务 {task_id} 为异步任务，创建新的事件循环运行。")
                    result = loop.run_until_complete(task_func(*args, **final_kwargs))
                    loop.close()
                else:
                    # 同步任务：直接调用
                    result = task_func(*args, **final_kwargs)

                # 3. 任务成功完成
                with self.lock:
                    if task_id in self.tasks:
                        self.tasks[task_id].status = "finished"
                        self.tasks[task_id].result = result
                        self.tasks[task_id].step = "任务完成"
                        self.tasks[task_id].progress = 100
                        self.tasks[task_id].update_time = time.time()

            except Exception as e:
                # 4. 任务执行失败
                error_msg = str(e)
                logger.error(f"任务 {task_id} 执行失败: {error_msg}", exc_info=True)
                with self.lock:
                    if task_id in self.tasks:
                        self.tasks[task_id].status = "failed"
                        self.tasks[task_id].error = error_msg
                        # 限制错误信息长度，避免 TaskInfo 过大
                        self.tasks[task_id].step = f"执行失败: {error_msg[:100]}..."
                        self.tasks[task_id].update_time = time.time()

            finally:
                # 5. 清理超时任务
                self._clean_timeout_tasks()

        threading.Thread(target=_run_task, daemon=True).start()
        return task_id

    # -------------------------- 原有方法（略） --------------------------
    def get_task_progress(self, task_id: str) -> Optional[TaskInfo]:
        with self.lock:
            self._clean_timeout_tasks()
            return self.tasks.get(task_id)

    def create_nested_callback(self, parent_callback: Callable[[float, str], None],
                               start_percent: float, end_percent: float,
                               parent_step: str = "") -> NestedProgressCallback:
        """
        创建嵌套进度回调
        :param parent_callback: 父进度回调
        :param start_percent: 子进度开始百分比
        :param end_percent: 子进度结束百分比
        :param parent_step: 父步骤描述
        :return: 嵌套进度回调对象
        """
        return NestedProgressCallback(parent_callback, start_percent, end_percent, parent_step)

    def _clean_timeout_tasks(self):
        now = time.time()
        timeout_tasks = [
            tid for tid, task in self.tasks.items()
            if now - task.create_time > self.timeout and task.status not in ("running", "finished")
        ]
        for tid in timeout_tasks:
            self.tasks[tid].status = "timeout"
            self.tasks[tid].step = "任务超时"
            self.tasks[tid].update_time = now

    def wait_for_done(self, task_id: str, check_interval: float = 0.5, wait_timeout: Optional[float] = None,
                      get_task_progress: Optional[Callable[[str], Optional[TaskInfo]]] = None,
                      progress_callback: Optional[Callable[[float, str, str, str], None]] = None) -> TaskInfo:
        """
        阻塞等待任务完成，通过 progress_callback 反馈实时进度（替代控制台打印）
        Args:
            task_id: 要等待的任务ID
            check_interval: 进度检查间隔（秒）
            wait_timeout: 等待超时时间（秒，None表示不限制）
            get_task_progress: 自定义获取任务进度方法
            progress_callback: 进度回调函数，接收4个参数：
                - progress: 进度值（0-100）
                - step: 当前步骤描述
                - task_id: 任务ID（完整）
                - status: 任务状态（pending/running/finished/failed/timeout）
                无回调需求时可传None
        Returns:
            TaskInfo: 任务最终状态信息
        Raises:
            ValueError: 任务ID不存在
            TimeoutError: 等待超时
        """
        # 1. 检查任务是否存在
        if get_task_progress is None:
            get_task_progress = self.get_task_progress

        # 初始获取任务信息时也加入重试机制
        max_retries = 3
        retry_count = 0
        task_info = None
        while retry_count < max_retries:
            task_info = get_task_progress(task_id)
            if task_info:
                break
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(0.1)  # 短间隔重试

        if not task_info:
            raise ValueError(f"任务ID不存在：{task_id}")

        # 2. 初始化回调函数（未传入则用空函数，避免报错）
        if not progress_callback:
            progress_callback = lambda progress, step, task_id, status: None

        # 3. 记录等待开始时间
        start_time = time.time()
        # 首次回调：通知等待开始
        progress_callback(
            progress=task_info.progress,
            step=f"开始等待任务完成（检查间隔：{check_interval}秒）",
            task_id=task_id,
            status=task_info.status
        )
        print(f"开始等待任务完成（任务ID：{task_id}），检查间隔：{check_interval}秒")  # 保留基础提示（可选）

        while True:
            # 4. 获取最新任务状态（带重试机制）
            task_info = None
            retry_count = 0  # 重置重试计数
            while retry_count < max_retries:
                task_info = get_task_progress(task_id)
                if task_info:
                    break  # 成功获取，退出重试循环
                retry_count += 1
                time.sleep(0.1)  # 短间隔重试

            if not task_info:
                # 达到最大重试次数仍失败，判定为任务被清理
                progress_callback(
                    progress=0,
                    step=f"任务已被清理或获取失败，无法继续等待",
                    task_id=task_id,
                    status="cleaned"
                )
                raise ValueError(f"任务ID {task_id} 已被清理或获取失败，无法继续等待")

            # 5. 实时回调进度
            progress_callback(
                progress=task_info.progress,
                step=task_info.step,
                task_id=task_id,
                status=task_info.status,
            )

            # 6. 判断任务是否结束
            if task_info.status in ("finished", "failed", "timeout"):
                # 最终回调：任务结束（补充耗时信息）
                total_time = time.time() - start_time
                progress_callback(
                    progress=task_info.progress,
                    step=f"任务结束 | 耗时：{total_time:.1f}秒 | 结果：{task_info.result or task_info.error}",
                    task_id=task_id,
                    status=task_info.status,
                )
                print(f"\n任务结束 | 最终状态：{task_info.status} | 耗时：{total_time:.1f}秒")  # 保留基础提示（可选）
                return task_info

            # 7. 判断等待是否超时
            if wait_timeout is not None and (time.time() - start_time) > wait_timeout:
                # 超时回调
                progress_callback(
                    progress=task_info.progress,
                    step=f"等待超时（超时时间：{wait_timeout}秒）",
                    task_id=task_id,
                    status="wait_timeout",
                )
                raise TimeoutError(
                    f"等待任务 {task_id} 超时（超时时间：{wait_timeout}秒），"
                    f"当前状态：{task_info.status} | 进度：{task_info.progress}%"
                )

            # 8. 间隔等待后继续检查
            time.sleep(check_interval)

    # -------------------------- 新增：清理方法 --------------------------
    def clean_finished_tasks(self, keep_time: float = 300) -> int:
        """
        清理“已完成/失败/超时”的任务（默认保留5分钟内的任务，避免刚结束就被清理）
        Args:
            keep_time: 保留时间（秒），超过该时间的已结束任务才会被清理
        Returns:
            int: 实际清理的任务数量
        """
        with self.lock:  # 线程安全：加锁避免并发修改
            now = time.time()
            # 筛选需要清理的任务：状态是结束态 + 超过保留时间
            tasks_to_clean = [
                task_id for task_id, task in self.tasks.items()
                if task.status in ("finished", "failed", "timeout")  # 仅清理已结束的任务
                   and (now - task.update_time) > keep_time  # 超过保留时间
            ]

            # 执行清理
            for task_id in tasks_to_clean:
                task = self.tasks[task_id]
                logger.info(f"清理已结束任务：{task_id}（状态：{self.tasks[task_id].status}，结束时间：{task.update_time}）")
                del self.tasks[task_id]

            # 记录清理结果
            cleaned_count = len(tasks_to_clean)
            logger.info(
                f"已完成任务清理完成 | 总结束任务数：{len([t for t in self.tasks.values() if t.status in ('finished', 'failed', 'timeout')])} | 清理数量：{cleaned_count}")
            return cleaned_count

    def clean_specific_task(self, task_id: str, force: bool = False) -> bool:
        """
        指定任务ID清理（默认不允许清理“运行中”的任务，避免数据混乱）
        Args:
            task_id: 要清理的任务ID
            force: 是否强制清理（True：即使任务正在运行也清理；False：仅清理非运行中任务）
        Returns:
            bool: 清理结果（True：清理成功；False：任务不存在或不允许清理）
        """
        with self.lock:  # 线程安全：加锁确保任务状态不被并发修改
            # 1. 检查任务是否存在
            if task_id not in self.tasks:
                logger.warning(f"指定清理的任务不存在：{task_id}，清理失败")
                return False

            # 2. 检查任务状态，判断是否允许清理
            task_info = self.tasks[task_id]
            if not force and task_info.status == "running":
                logger.error(f"任务 {task_id} 正在运行中，不允许非强制清理（如需清理请设置 force=True）")
                return False

            # 3. 执行清理
            del self.tasks[task_id]
            logger.info(f"指定任务清理成功 | 任务ID：{task_id} | 清理时状态：{task_info.status} | 是否强制：{force}")
            return True


# -------------------------- 增加异步任务示例 --------------------------
async def async_data_fetching_task(progress_callback, url: str, fetch_count: int = 5):
    """
    异步任务示例：模拟并发数据抓取
    """
    progress_callback(0, f"开始异步获取数据: {url}")

    async def fetch_item(session, index):
        await asyncio.sleep(0.5)  # 模拟 IO 操作
        return f"Result_{index}"

    progress_callback(10, "初始化异步操作")

    # 模拟创建 session，实际项目中可能使用 aiohttp 等
    class MockSession:
        async def __aenter__(self): return self

        async def __aexit__(self, exc_type, exc_val, exc_tb): pass

    async with MockSession() as session:
        tasks = [fetch_item(session, i) for i in range(fetch_count)]

        results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            results.append(result)

            progress = 10 + int((i + 1) / fetch_count * 80)  # 10% 到 90%
            progress_callback(progress, f"已获取 {i + 1}/{fetch_count} 个项目，最新结果: {result}")

    progress_callback(90, "数据抓取完成，正在处理结果...")
    await asyncio.sleep(1)  # 模拟最终处理
    progress_callback(100, "任务完成")

    return {"url": url, "fetched_items": fetch_count, "results": results}


# -------------------------- 原有同步任务示例 --------------------------
def complex_task_with_params(progress_callback, data_source: str, model_name: str, epochs: int = 5, **kwargs):
    """
    带参数的复杂任务示例 (同步)
    """
    progress_callback(0, f"开始处理数据源: {data_source}")
    # ... (原有逻辑不变)

    # 使用传入的参数
    progress_callback(10, f"配置模型: {model_name}")
    time.sleep(1)

    # 数据加载阶段 (10-40%)
    data_callback = manager.create_nested_callback(progress_callback, 10, 40, "数据加载")

    data_callback(0, "连接数据源")
    time.sleep(0.5)

    # 模拟加载不同数据源
    if data_source == "database":
        data_callback(50, "执行SQL查询")
        time.sleep(1)
    elif data_source == "file":
        data_callback(50, "读取文件")
        time.sleep(0.8)
    else:
        data_callback(50, "获取数据")
        time.sleep(0.5)

    data_callback(100, "数据加载完成")

    # 训练阶段 (40-90%)
    training_callback = manager.create_nested_callback(progress_callback, 40, 90, f"训练模型 {model_name}")

    for epoch in range(epochs):
        epoch_callback = training_callback.create_sub_callback(
            epoch * 100 // epochs, (epoch + 1) * 100 // epochs, f"第{epoch + 1}轮"
        )

        for batch in range(10):
            epoch_callback(batch * 10, f"批次{batch + 1}")
            time.sleep(0.05)

        epoch_callback(100, f"第{epoch + 1}轮完成")

    training_callback(100, "训练完成")

    # 评估阶段 (90-100%)
    progress_callback(90, "评估模型")
    time.sleep(1)
    progress_callback(100, "任务完成")

    # 返回结果，包含传入的参数信息
    return {
        "data_source": data_source,
        "model_name": model_name,
        "epochs": epochs,
        "additional_params": kwargs,
        "accuracy": 0.95,
        "loss": 0.1
    }


def simple_processing_task(progress_callback, input_data: list, processing_option: str = "default"):
    """
    简单处理任务示例 (同步)
    """
    total_items = len(input_data)

    for i, item in enumerate(input_data):
        progress = (i + 1) * 100 // total_items
        progress_callback(progress, f"处理 {processing_option}: {item}")
        time.sleep(0.2)

    return {
        "processed_items": total_items,
        "processing_option": processing_option,
        "result": f"成功处理了 {total_items} 个数据项"
    }


# 使用示例
if __name__ == "__main__":
    # 配置基础日志，以便看到 logger.info 的输出
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    manager = AsyncTaskManager(timeout=60)  # 设置一个较短的超时时间方便测试

    # 示例1: 创建带参数的复杂同步任务
    print("=== 示例1: 复杂同步任务 ===")
    task_id1 = manager.create_task(
        complex_task_with_params,
        data_source="database",
        model_name="resnet50",
        epochs=3,
        batch_size=32,
        learning_rate=0.001
    )
    print(f"复杂任务已创建: {task_id1}")

    # 示例2: 创建简单处理同步任务
    print("\n=== 示例2: 简单同步任务 ===")
    task_id2 = manager.create_task(
        simple_processing_task,
        input_data=["item1", "item2", "item3", "item4", "item5"],
        processing_option="fast_mode"
    )
    print(f"简单任务已创建: {task_id2}")

    # 示例3: 创建异步任务
    print("\n=== 示例3: 异步任务 ===")
    task_id3 = manager.create_task(
        async_data_fetching_task,
        url="https://api.example.com/data",
        fetch_count=8
    )
    print(f"异步任务已创建: {task_id3}")

    # 监控任务1进度
    print("\n监控复杂任务进度 (task_id1):")


    # 定义进度回调函数
    def console_progress_callback(progress, step, task_id, status):
        # 实时打印进度，使用 \r 实现单行刷新
        print(f"\r[Task {task_id[:8]}] {status}: {progress}% - {step:<60}", end="")


    try:
        final_info1 = manager.wait_for_done(task_id1, check_interval=0.2, progress_callback=console_progress_callback)
        print(f"\n任务 {task_id1} 结束。状态: {final_info1.status}")
    except Exception as e:
        print(f"\n等待任务 {task_id1} 出现异常: {e}")

    print("\n" + "=" * 50 + "\n")

    # 监控任务3进度 (异步任务)
    print("\n监控异步任务进度 (task_id3):")
    try:
        final_info3 = manager.wait_for_done(task_id3, check_interval=0.3, progress_callback=console_progress_callback)
        print(f"\n任务 {task_id3} 结束。状态: {final_info3.status}")
        # print(f"异步任务结果：{final_info3.result}")
    except Exception as e:
        print(f"\n等待任务 {task_id3} 出现异常: {e}")

    # 等待任务2完成
    print("\n" + "=" * 50 + "\n")
    print("\n等待简单任务完成 (task_id2):")
    manager.wait_for_done(task_id2, check_interval=0.5)

    # 验证任务清理
    print("\n清理已完成任务...")
    time.sleep(5)  # 保证任务 update_time > keep_time=300 (如果任务运行时间太短)
    cleaned_count = manager.clean_finished_tasks(keep_time=1)  # 设置 keep_time=1秒 方便清理
    print(f"实际清理任务数量: {cleaned_count}")

    # 强制清理不存在的任务
    print("\n强制清理不存在的任务:")
    success = manager.clean_specific_task("non-existent-task-id", force=True)
    print(f"清理结果: {success}")

    # 确保主线程不会立即退出
    print("\n所有任务演示完毕。")