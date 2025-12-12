"""
Plugin Dependency Resolver

Automatic dependency resolution and loading for plugins.
"""

from typing import Dict, List, Set, Any, Optional
import asyncio

class PluginDependencyResolver:
    """Plugin dependency resolution system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.reverse_dependencies: Dict[str, Set[str]] = {}

    def add_plugin_dependencies(self, plugin_name: str, dependencies: List[str]):
        """Add plugin dependencies."""
        self.dependency_graph[plugin_name] = set(dependencies)

        for dep in dependencies:
            if dep not in self.reverse_dependencies:
                self.reverse_dependencies[dep] = set()
            self.reverse_dependencies[dep].add(plugin_name)

    def resolve_dependencies(self, plugin_name: str) -> List[str]:
        """Resolve dependency loading order."""
        visited = set()
        order = []

        def visit(name: str):
            if name in visited:
                return
            visited.add(name)

            for dep in self.dependency_graph.get(name, set()):
                visit(dep)

            order.append(name)

        visit(plugin_name)
        return order[:-1]  # Exclude the plugin itself

    def check_circular_dependencies(self) -> List[List[str]]:
        """Check for circular dependencies."""
        cycles = []

        def find_cycles(node: str, path: List[str], visited: Set[str]):
            if node in path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return

            if node in visited:
                return

            visited.add(node)
            path.append(node)

            for dep in self.dependency_graph.get(node, set()):
                find_cycles(dep, path, visited)

            path.pop()

        visited = set()
        for plugin in self.dependency_graph:
            find_cycles(plugin, [], visited)

        return cycles

    def get_dependent_plugins(self, plugin_name: str) -> Set[str]:
        """Get plugins that depend on the given plugin."""
        return self.reverse_dependencies.get(plugin_name, set())