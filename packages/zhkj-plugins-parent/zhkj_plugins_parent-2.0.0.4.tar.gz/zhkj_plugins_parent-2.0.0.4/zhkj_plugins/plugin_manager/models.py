from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class VersionInfo:
    version: str
    download_url: str
    release_notes: str
    release_date: str
    file_size: int
    md5_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionInfo':
        return cls(**data)

@dataclass
class PluginConfig:
    """插件配置信息"""
    name: str
    current_version: str
    extract_folder: str
    app_relative_path: str
    plugin_type: str = 'app'
    dependencies: Dict[str, str] = None
    startup_args: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = {}
        if self.startup_args is None:
            self.startup_args = []
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PluginConfig':
        return cls(**data)
