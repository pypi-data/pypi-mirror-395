from .plugin_manager import PluginManager,PortManager
from .plugin_manager.models import PluginConfig
# your_package/__init__.py
from importlib.metadata import version, PackageNotFoundError
from .pyproject_parser import PyprojectParser

try:
    # 读取 pyproject.toml 中定义的版本号（与项目名称对应）
    __version__ = version("zhkj-plugins-parent")  # 注意：此处名称必须与 pyproject.toml 中的 project.name 一致
except PackageNotFoundError:
    # 项目未安装时的容错（如开发阶段）
    __version__ = "0.0.0.dev0"  # 开发版本占位符