import re
from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path
import logging

from .dependency_models import (
    DependencyInfo, DependencyResolution, DependencyStatus,
    DependencyRelation, PluginDependencyGraph
)
from ..version_manager import VersionManager

logger = logging.getLogger("PluginManager.DependencyResolver")


class DependencyResolver:
    """依赖解析器"""

    def __init__(self, version_manager: VersionManager):
        self.version_manager = version_manager
        self.dependency_graph = PluginDependencyGraph()
        self._visited: Set[str] = set()
        self._current_path: List[str] = []

    def add_plugin_dependencies(self, plugin_name: str, version: str, dependencies: List[DependencyInfo]):
        """添加插件依赖关系到依赖图"""
        self.dependency_graph.add_plugin(plugin_name, version, dependencies)
        logger.debug(f"添加插件 {plugin_name} v{version} 的依赖关系")

    def resolve_dependencies(self, plugin_name: str, installed_plugins: Dict[str, str]) -> DependencyResolution:
        """解析插件的依赖关系"""
        self._visited.clear()
        self._current_path.clear()
        return self._resolve_plugin_dependencies(plugin_name, installed_plugins)

    def _resolve_plugin_dependencies(self, plugin_name: str, installed_plugins: Dict[str, str]) -> DependencyResolution:
        """递归解析插件依赖"""
        if plugin_name in self._current_path:
            # 检测到循环依赖
            cycle_path = self._current_path + [plugin_name]
            cycle_str = " -> ".join(cycle_path)
            logger.warning(f"检测到循环依赖: {cycle_str}")
            return DependencyResolution(
                plugin_name=plugin_name,
                status=DependencyStatus.CIRCULAR,
                circular_dependencies=cycle_path
            )

        if plugin_name in self._visited:
            # 已经访问过，返回成功（避免重复处理）
            return DependencyResolution(
                plugin_name=plugin_name,
                status=DependencyStatus.SATISFIED
            )

        self._visited.add(plugin_name)
        self._current_path.append(plugin_name)

        # 获取插件的依赖
        dependencies = self.dependency_graph.get_dependencies(plugin_name)
        resolution = DependencyResolution(
            plugin_name=plugin_name,
            status=DependencyStatus.SATISFIED
        )

        for dep_info in dependencies:
            dep_name = dep_info.plugin_name

            # 检查依赖是否安装
            if dep_name not in installed_plugins:
                if dep_info.relation == DependencyRelation.REQUIRES and not dep_info.optional:
                    resolution.status = DependencyStatus.MISSING
                    resolution.missing_dependencies.append(dep_name)
                    logger.warning(f"插件 {plugin_name} 缺少必需依赖: {dep_name}")
                continue

            # 检查版本约束
            installed_version = installed_plugins[dep_name]
            if not self._check_version_constraint(installed_version, dep_info.version_constraint):
                if dep_info.relation == DependencyRelation.REQUIRES and not dep_info.optional:
                    resolution.status = DependencyStatus.MISSING
                    resolution.missing_dependencies.append(
                        f"{dep_name} (需要 {dep_info.version_constraint}, 当前 {installed_version})"
                    )
                    logger.warning(
                        f"插件 {plugin_name} 依赖版本不匹配: "
                        f"{dep_name} {dep_info.version_constraint} != {installed_version}"
                    )
                continue

            # 检查冲突依赖
            if dep_info.relation == DependencyRelation.CONFLICTS:
                resolution.status = DependencyStatus.CONFLICT
                resolution.conflict_with = dep_name
                logger.warning(f"插件 {plugin_name} 与 {dep_name} 冲突")
                break

            # 递归解析依赖的依赖
            dep_resolution = self._resolve_plugin_dependencies(dep_name, installed_plugins)
            resolution.dependencies.append(dep_resolution)

            if not dep_resolution.is_satisfied():
                resolution.status = dep_resolution.status

        self._current_path.pop()
        return resolution

    def _check_version_constraint(self, version: str, constraint: str) -> bool:
        """检查版本约束"""
        if not constraint or constraint == "*":
            return True

        try:
            # 简单的版本约束检查，支持 >, >=, <, <=, ==, !=
            if constraint.startswith(">="):
                required_version = constraint[2:].strip()
                return self.version_manager._compare_versions(version, required_version) >= 0
            elif constraint.startswith(">"):
                required_version = constraint[1:].strip()
                return self.version_manager._compare_versions(version, required_version) > 0
            elif constraint.startswith("<="):
                required_version = constraint[2:].strip()
                return self.version_manager._compare_versions(version, required_version) <= 0
            elif constraint.startswith("<"):
                required_version = constraint[1:].strip()
                return self.version_manager._compare_versions(version, required_version) < 0
            elif constraint.startswith("=="):
                required_version = constraint[2:].strip()
                return self.version_manager._compare_versions(version, required_version) == 0
            elif constraint.startswith("!="):
                required_version = constraint[2:].strip()
                return self.version_manager._compare_versions(version, required_version) != 0
            else:
                # 默认使用 ==
                return self.version_manager._compare_versions(version, constraint) == 0
        except Exception as e:
            logger.error(f"版本约束检查失败: {version} {constraint} - {str(e)}")
            return False

    def get_install_order(self, plugin_name: str, installed_plugins: Dict[str, str]) -> List[str]:
        """获取插件安装顺序（拓扑排序）"""
        resolution = self.resolve_dependencies(plugin_name, installed_plugins)
        if not resolution.is_satisfied():
            logger.error(f"无法解析依赖关系，无法确定安装顺序: {plugin_name}")
            return []

        # 使用深度优先搜索获取安装顺序（依赖先安装）
        install_order = []
        visited = set()

        def dfs(current_plugin):
            if current_plugin in visited:
                return
            visited.add(current_plugin)

            for dep_info in self.dependency_graph.get_dependencies(current_plugin):
                if (dep_info.relation == DependencyRelation.REQUIRES and
                        not dep_info.optional and
                        dep_info.plugin_name not in installed_plugins):
                    dfs(dep_info.plugin_name)

            if current_plugin not in installed_plugins:
                install_order.append(current_plugin)

        dfs(plugin_name)
        return install_order

    def get_uninstall_order(self, plugin_name: str) -> List[str]:
        """获取插件卸载顺序（反向拓扑排序）"""
        # 检查是否有其他插件依赖此插件
        dependents = self.dependency_graph.get_dependents(plugin_name)
        if dependents:
            logger.warning(f"插件 {plugin_name} 被其他插件依赖: {', '.join(dependents)}")
            return []

        # 收集可以安全卸载的依赖
        uninstall_order = [plugin_name]
        visited = set()

        def find_unused_dependencies(current_plugin):
            if current_plugin in visited:
                return
            visited.add(current_plugin)

            for dep_info in self.dependency_graph.get_dependencies(current_plugin):
                dep_name = dep_info.plugin_name
                # 检查该依赖是否还被其他插件使用
                other_dependents = [
                    p for p in self.dependency_graph.get_dependents(dep_name)
                    if p != current_plugin and p not in uninstall_order
                ]
                if not other_dependents:
                    uninstall_order.append(dep_name)
                    find_unused_dependencies(dep_name)

        find_unused_dependencies(plugin_name)
        return uninstall_order

    def validate_dependencies(self, plugin_name: str, installed_plugins: Dict[str, str]) -> bool:
        """验证插件依赖是否满足"""
        resolution = self.resolve_dependencies(plugin_name, installed_plugins)
        return resolution.is_satisfied()

    def get_dependency_tree(self, plugin_name: str, installed_plugins: Dict[str, str]) -> str:
        """获取依赖树文本表示"""
        resolution = self.resolve_dependencies(plugin_name, installed_plugins)
        return self._format_dependency_tree(resolution)

    def _format_dependency_tree(self, resolution: DependencyResolution, level: int = 0) -> str:
        """格式化依赖树"""
        indent = "  " * level
        status_icon = {
            DependencyStatus.SATISFIED: "✓",
            DependencyStatus.MISSING: "✗",
            DependencyStatus.CONFLICT: "⚡",
            DependencyStatus.CIRCULAR: "↻"
        }.get(resolution.status, "?")

        tree = f"{indent}{status_icon} {resolution.plugin_name}\n"

        for dep in resolution.dependencies:
            tree += self._format_dependency_tree(dep, level + 1)

        return tree