import threading
from typing import List, Dict, Set, Optional, Tuple, Any
from pathlib import Path
import logging

from .dependency_models import DependencyInfo, DependencyRelation, PluginDependencyGraph
from .dependency_resolver import DependencyResolver
from ..models import PluginConfig
from ..version_manager import VersionManager

logger = logging.getLogger("PluginManager.DependencyManager")


class DependencyManager:
    """插件依赖管理器"""

    def __init__(self, version_manager: VersionManager, plugin_install_dir: Path):
        self.version_manager = version_manager
        self.plugin_install_dir = plugin_install_dir
        self.resolver = DependencyResolver(version_manager)
        self._lock = threading.RLock()

        # 缓存已安装插件的依赖信息
        self._dependency_cache: Dict[str, List[DependencyInfo]] = {}

    def load_plugin_dependencies(self, plugin_config: PluginConfig) -> List[DependencyInfo]:
        """加载插件的依赖配置"""
        plugin_name = plugin_config.name

        with self._lock:
            if plugin_name in self._dependency_cache:
                return self._dependency_cache[plugin_name]

            dependencies = []

            # 从插件配置中解析依赖
            if hasattr(plugin_config, 'dependencies') and plugin_config.dependencies:
                for dep_name, dep_constraint in plugin_config.dependencies.items():
                    # 解析依赖关系类型
                    relation = DependencyRelation.REQUIRES
                    if dep_constraint.startswith("recommends:"):
                        relation = DependencyRelation.RECOMMENDS
                        dep_constraint = dep_constraint[11:]
                    elif dep_constraint.startswith("conflicts:"):
                        relation = DependencyRelation.CONFLICTS
                        dep_constraint = dep_constraint[10:]
                    elif dep_constraint.startswith("optional:"):
                        relation = DependencyRelation.OPTIONAL
                        dep_constraint = dep_constraint[9:]

                    dependency = DependencyInfo(
                        plugin_name=dep_name,
                        version_constraint=dep_constraint,
                        relation=relation
                    )
                    dependencies.append(dependency)

            self._dependency_cache[plugin_name] = dependencies
            return dependencies

    def register_plugin_dependencies(self, plugin_config: PluginConfig):
        """注册插件的依赖关系到解析器"""
        dependencies = self.load_plugin_dependencies(plugin_config)
        self.resolver.dependency_graph.add_plugin(
            plugin_config.name,
            plugin_config.current_version,
            dependencies
        )
        logger.info(f"注册插件 {plugin_config.name} 的依赖关系: {len(dependencies)} 个依赖")

    def unregister_plugin_dependencies(self, plugin_name: str):
        """取消注册插件的依赖关系"""
        with self._lock:
            self.resolver.dependency_graph.remove_plugin(plugin_name)
            if plugin_name in self._dependency_cache:
                del self._dependency_cache[plugin_name]
            logger.info(f"取消注册插件 {plugin_name} 的依赖关系")

    def can_safely_uninstall(self, plugin_name: str) -> Tuple[bool, List[str]]:
        """检查插件是否可以安全卸载"""
        with self._lock:
            dependents = self.resolver.dependency_graph.get_dependents(plugin_name)
            can_uninstall = not bool(dependents)
            return can_uninstall, dependents

    def get_safe_uninstall_plan(self, plugin_name: str) -> List[str]:
        """获取安全卸载计划"""
        with self._lock:
            return self.resolver.get_uninstall_order(plugin_name)

    def get_dependency_install_order(self, plugin_name: str, installed_plugins: Dict[str, str]) -> List[str]:
        """获取依赖安装顺序"""
        with self._lock:
            return self.resolver.get_install_order(plugin_name, installed_plugins)

    def validate_plugin_dependencies(self, plugin_name: str, installed_plugins: Dict[str, str]) -> bool:
        """验证插件依赖是否满足"""
        with self._lock:
            return self.resolver.validate_dependencies(plugin_name, installed_plugins)

    def get_dependency_tree(self, plugin_name: str, installed_plugins: Dict[str, str]) -> str:
        """获取依赖树"""
        with self._lock:
            return self.resolver.get_dependency_tree(plugin_name, installed_plugins)

    def analyze_dependency_impact(self, plugin_name: str) -> Dict[str, Any]:
        """分析依赖影响"""
        with self._lock:
            dependents = self.resolver.dependency_graph.get_dependents(plugin_name)
            dependencies = self.resolver.dependency_graph.get_dependencies(plugin_name)

            return {
                "plugin": plugin_name,
                "direct_dependents": dependents,
                "direct_dependencies": [dep.plugin_name for dep in dependencies],
                "can_safely_uninstall": not bool(dependents),
                "impact_level": "high" if dependents else "low"
            }

    def find_circular_dependencies(self) -> List[List[str]]:
        """查找循环依赖"""
        circular_deps = []
        visited = set()

        for plugin_name in self.resolver.dependency_graph.nodes:
            if plugin_name not in visited:
                resolution = self.resolver.resolve_dependencies(
                    plugin_name,
                    self.resolver.dependency_graph.plugin_versions
                )
                if resolution.status.name == "CIRCULAR" and resolution.circular_dependencies:
                    circular_deps.append(resolution.circular_dependencies)
                    visited.update(resolution.circular_dependencies)

        return circular_deps

    def get_orphaned_dependencies(self, installed_plugins: List[str]) -> List[str]:
        """查找孤儿依赖（没有被任何插件直接依赖的已安装插件）"""
        with self._lock:
            orphaned = []
            for plugin in installed_plugins:
                # 检查插件是否被其他插件依赖
                dependents = self.resolver.dependency_graph.get_dependents(plugin)
                # 检查插件是否有依赖其他插件（如果是叶子节点）
                dependencies = self.resolver.dependency_graph.get_dependencies(plugin)

                # 如果没有被依赖且自身没有依赖其他插件，可能是孤儿
                if not dependents and not dependencies:
                    orphaned.append(plugin)

            return orphaned

    def cleanup_orphaned_dependencies(self, installed_plugins: List[str]) -> List[str]:
        """清理孤儿依赖"""
        orphaned = self.get_orphaned_dependencies(installed_plugins)
        logger.info(f"发现 {len(orphaned)} 个孤儿依赖: {', '.join(orphaned)}")
        return orphaned

    def batch_validate_dependencies(self, plugins: List[PluginConfig]) -> Dict[str, bool]:
        """批量验证插件依赖"""
        results = {}
        installed_plugins = {plugin.name: plugin.current_version for plugin in plugins}

        for plugin in plugins:
            results[plugin.name] = self.validate_plugin_dependencies(
                plugin.name, installed_plugins
            )

        return results

    def get_dependency_report(self, plugins: List[PluginConfig]) -> Dict[str, Any]:
        """生成依赖关系报告"""
        with self._lock:
            installed_plugins = {plugin.name: plugin.current_version for plugin in plugins}

            report = {
                "total_plugins": len(plugins),
                "dependency_validation": self.batch_validate_dependencies(plugins),
                "circular_dependencies": self.find_circular_dependencies(),
                "orphaned_dependencies": self.get_orphaned_dependencies([p.name for p in plugins]),
                "dependency_graph": {
                    "nodes": list(self.resolver.dependency_graph.nodes.keys()),
                    "edges": [
                        f"{source} -> {dep.plugin_name}"
                        for source, deps in self.resolver.dependency_graph.nodes.items()
                        for dep in deps
                    ]
                }
            }

            return report