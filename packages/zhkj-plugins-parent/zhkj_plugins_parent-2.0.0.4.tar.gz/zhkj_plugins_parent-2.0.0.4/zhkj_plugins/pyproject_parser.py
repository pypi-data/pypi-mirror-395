import toml
from pathlib import Path
from typing import Dict, Optional, List, Any


class PyprojectParser:
    """pyproject.toml 文件解析工具类（适配规范字段）"""

    def __init__(self, pyproject_path: Optional[Path] = None):
        self.pyproject_path = self._find_pyproject(pyproject_path)
        self._data = self._load_pyproject()

    def _find_pyproject(self, custom_path: Optional[Path]) -> Path:
        if custom_path:
            path = custom_path.resolve()
            if path.exists() and path.name == "pyproject.toml":
                return path
            raise FileNotFoundError(f"指定路径不存在 pyproject.toml: {custom_path}")

        # 从当前文件目录向上查找
        current_dir = Path(__file__).resolve().parent
        while current_dir != current_dir.parent:
            candidate = current_dir / "pyproject.toml"
            if candidate.exists():
                return candidate
            current_dir = current_dir.parent

        raise FileNotFoundError("未在项目目录中找到 pyproject.toml")

    def _load_pyproject(self) -> Dict[str, Any]:
        try:
            with open(self.pyproject_path, "r", encoding="utf-8") as f:
                return toml.load(f)
        except Exception as e:
            raise RuntimeError(f"解析 pyproject.toml 失败: {str(e)}")

    @property
    def project_name(self) -> str:
        return self._data.get("project", {}).get("name", "未知项目")

    @property
    def current_version(self) -> str:
        version = self._data.get("project", {}).get("version")
        if not version:
            raise ValueError("pyproject.toml 中未配置 version 字段")
        return version

    @property
    def all_dependencies(self) -> List[str]:
        return self._data.get("project", {}).get("dependencies", [])

    @property
    def dev_dependencies(self) -> List[str]:
        return self._data.get("project", {}).get("optional-dependencies", {}).get("dev", [])

    def _parse_version_descriptions(self) -> Dict[str, str]:
        """从 tool.version-info.descriptions 解析版本描述"""
        desc_text = self._data.get("tool", {}).get("version-info", {}).get("descriptions", "")
        if not desc_text:
            return {}

        version_desc = {}
        for line in desc_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                version, desc = line.split(":", 1)
                version_desc[version.strip()] = desc.strip()
        return version_desc

    def get_version_description(self, version: Optional[str] = None) -> str:
        target_version = version or self.current_version
        all_desc = self._parse_version_descriptions()
        return all_desc.get(target_version, f"Release {target_version}")

    def reload(self) -> None:
        """重新加载配置"""
        self._data = self._load_pyproject()


# 使用示例
if __name__ == "__main__":
    try:
        parser = PyprojectParser()
        print(f"项目名称: {parser.project_name}")
        print(f"当前版本: {parser.current_version}")
        print(f"当前版本描述: {parser.get_version_description()}")
        print(f"1.0.1版本描述: {parser.get_version_description('1.0.1')}")
    except Exception as e:
        print(f"操作失败: {str(e)}")