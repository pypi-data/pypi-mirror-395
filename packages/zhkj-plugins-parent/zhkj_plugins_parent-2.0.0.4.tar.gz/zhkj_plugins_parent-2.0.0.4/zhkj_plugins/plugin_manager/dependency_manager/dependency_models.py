from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger("PluginManager.Dependency")


class DependencyRelation(Enum):
    """依赖关系类型"""
    REQUIRES = "requires"  # 必需依赖
    RECOMMENDS = "recommends"  # 推荐依赖
    CONFLICTS = "conflicts"  # 冲突依赖
    OPTIONAL = "optional"  # 可选依赖


class DependencyStatus(Enum):
    """依赖状态"""
    SATISFIED = "satisfied"  # 依赖已满足
    MISSING = "missing"  # 依赖缺失
    CONFLICT = "conflict"  # 依赖冲突
    CIRCULAR = "circular"  # 循环依赖


@dataclass
class DependencyInfo:
    """依赖信息"""
    plugin_name: str
    version_constraint: str
    relation: DependencyRelation
    description: str = ""
    optional: bool = False

    def __str__(self):
        return f"{self.plugin_name}{self.version_constraint} ({self.relation.value})"


@dataclass
class DependencyResolution:
    """依赖解析结果"""
    plugin_name: str
    status: DependencyStatus
    dependencies: List['DependencyResolution'] = field(default_factory=list)
    conflict_with: Optional[str] = None
    missing_dependencies: List[str] = field(default_factory=list)
    circular_dependencies: List[str] = field(default_factory=list)

    def is_satisfied(self) -> bool:
        """检查依赖是否全部满足"""
        if self.status != DependencyStatus.SATISFIED:
            return False
        return all(dep.is_satisfied() for dep in self.dependencies)


@dataclass
class PluginDependencyGraph:
    """插件依赖图"""
    nodes: Dict[str, List[DependencyInfo]] = field(default_factory=dict)  # 插件 -> 依赖列表
    reverse_nodes: Dict[str, List[str]] = field(default_factory=dict)  # 被依赖插件 -> 依赖它的插件列表
    plugin_versions: Dict[str, str] = field(default_factory=dict)  # 插件当前版本

    def add_plugin(self, plugin_name: str, version: str, dependencies: List[DependencyInfo]):
        """添加插件及其依赖"""
        self.nodes[plugin_name] = dependencies
        self.plugin_versions[plugin_name] = version

        # 更新反向依赖图
        for dep in dependencies:
            if dep.plugin_name not in self.reverse_nodes:
                self.reverse_nodes[dep.plugin_name] = []
            if plugin_name not in self.reverse_nodes[dep.plugin_name]:
                self.reverse_nodes[dep.plugin_name].append(plugin_name)

    def remove_plugin(self, plugin_name: str):
        """移除插件"""
        if plugin_name in self.nodes:
            # 从反向依赖图中移除
            for dep in self.nodes[plugin_name]:
                if dep.plugin_name in self.reverse_nodes:
                    if plugin_name in self.reverse_nodes[dep.plugin_name]:
                        self.reverse_nodes[dep.plugin_name].remove(plugin_name)
                    if not self.reverse_nodes[dep.plugin_name]:
                        del self.reverse_nodes[dep.plugin_name]

            del self.nodes[plugin_name]

        if plugin_name in self.plugin_versions:
            del self.plugin_versions[plugin_name]

        # 从反向依赖图中移除该插件作为被依赖项的记录
        if plugin_name in self.reverse_nodes:
            del self.reverse_nodes[plugin_name]

    def get_dependents(self, plugin_name: str) -> List[str]:
        """获取依赖该插件的所有插件"""
        return self.reverse_nodes.get(plugin_name, [])

    def get_dependencies(self, plugin_name: str) -> List[DependencyInfo]:
        """获取插件的所有依赖"""
        return self.nodes.get(plugin_name, [])

    def has_dependents(self, plugin_name: str) -> bool:
        """检查插件是否有其他插件依赖它"""
        return bool(self.reverse_nodes.get(plugin_name))