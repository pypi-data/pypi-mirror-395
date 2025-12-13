class InstallDownloadBridge:
    """download_with_progress 所需的 (downloaded, total, speed) -> 嵌套进度"""
    __slots__ = ("_inner_cb",)

    def __init__(self, nested_cb: "NestedProgressCallback"):
        self._inner_cb = nested_cb

    def __call__(self, downloaded: int, total: int, speed: float) -> None:
        if total == 0:  # 无法拿到总长，直接报字节数
            self._inner_cb(0, f"已下载 {downloaded / 1024:.1f} KB | 速度 {speed:.1f} KB/s")
            return

        percent = int(downloaded / total * 100)
        total_mb = total / 1024 / 1024
        down_mb = downloaded / 1024 / 1024
        step = f"{down_mb:.1f}/{total_mb:.1f} MB  速度 {speed:.1f} KB/s"
        self._inner_cb(percent, step)


class SubProgress:
    """把 parent 的 [start, end] 再切成 n 段，支持实时汇报"""

    def __init__(self, parent: "NestedProgressCallback", start: int, end: int, step_name: str, segments: int = 1):
        self.parent = parent.create_sub_callback(start, end, step_name)
        self.segs = segments
        self.idx = 0

    def __call__(self, progress: float, step: str = ""):
        self.update(progress, step)

    def update(self, seg_progress: float, msg: str = ""):
        """
        seg_progress: 0~100  当前 segment 的进度
        """
        overall = (self.idx * 100 + seg_progress) / self.segs
        self.parent(int(overall), msg)

    def next_segment(self):
        self.idx += 1
