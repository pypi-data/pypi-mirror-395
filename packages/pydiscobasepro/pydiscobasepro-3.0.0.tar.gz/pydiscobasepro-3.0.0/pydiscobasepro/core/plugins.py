"""
Core Plugin Management System

Hot-load plugin system with sandboxing, dependency resolution, and marketplace.
"""

import asyncio
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
import inspect

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class PluginManager:
    """Advanced plugin management system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plugins_dir = Path("plugins")
        self.plugins_dir.mkdir(exist_ok=True)
        self.marketplace_dir = Path.home() / ".pydiscobasepro" / "marketplace"
        self.marketplace_dir.mkdir(exist_ok=True)

        self.plugins: Dict[str, Any] = {}
        self.plugin_metadata: Dict[str, Dict[str, Any]] = {}
        self.plugin_dependencies: Dict[str, Set[str]] = {}
        self.sandbox_enabled = config.get("sandbox_enabled", True)
        self.max_plugins = config.get("max_plugins", 50)

        # Execution environment
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._load_queue: asyncio.Queue = asyncio.Queue()

    async def initialize(self):
        """Initialize plugin system."""
        if self.config.get("auto_load", True):
            await self.load_all_plugins()

    async def load_all_plugins(self):
        """Load all available plugins."""
        if len(self.plugins) >= self.max_plugins:
            logger.warning(f"Maximum plugins limit ({self.max_plugins}) reached")
            return

        plugin_files = list(self.plugins_dir.glob("*.py"))
        if not plugin_files:
            logger.info("No plugins found to load")
            return

        logger.info(f"Loading {len(plugin_files)} plugins...")

        for plugin_file in plugin_files:
            if plugin_file.name.startswith('_'):
                continue

            await self._load_queue.put(plugin_file)

        # Process load queue
        tasks = []
        for _ in range(min(4, len(plugin_files))):
            tasks.append(asyncio.create_task(self._process_load_queue()))

        await asyncio.gather(*tasks)

        logger.info(f"Loaded {len(self.plugins)} plugins successfully")

    async def _process_load_queue(self):
        """Process plugin loading queue."""
        while not self._load_queue.empty():
            plugin_file = await self._load_queue.get()
            try:
                await self.load_plugin(plugin_file)
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file}: {e}")
            finally:
                self._load_queue.task_done()

    async def load_plugin(self, plugin_file: Path) -> bool:
        """Load a single plugin with dependency resolution."""
        plugin_name = plugin_file.stem

        if plugin_name in self.plugins:
            return True

        try:
            # Load plugin metadata first
            metadata = await self._load_plugin_metadata(plugin_file)
            if not metadata:
                return False

            # Check dependencies
            if not await self._resolve_dependencies(metadata):
                logger.warning(f"Dependencies not satisfied for plugin {plugin_name}")
                return False

            # Load the plugin
            plugin = await self._load_plugin_module(plugin_file, metadata)
            if not plugin:
                return False

            # Register plugin
            self.plugins[plugin_name] = plugin
            self.plugin_metadata[plugin_name] = metadata

            # Call plugin initialize if available
            if hasattr(plugin, 'initialize'):
                try:
                    await plugin.initialize()
                except Exception as e:
                    logger.error(f"Plugin {plugin_name} initialization failed: {e}")
                    await self.unload_plugin(plugin_name)
                    return False

            logger.info(f"Plugin {plugin_name} loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}")
            return False

    async def _load_plugin_metadata(self, plugin_file: Path) -> Optional[Dict[str, Any]]:
        """Load plugin metadata without executing code."""
        try:
            with open(plugin_file, 'r') as f:
                content = f.read()

            # Extract metadata from comments or docstrings
            metadata = {
                "name": plugin_file.stem,
                "version": "1.0.0",
                "dependencies": [],
                "permissions": [],
                "file": str(plugin_file),
                "hash": hashlib.sha256(content.encode()).hexdigest()
            }

            # Try to extract metadata from AST
            import ast
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Look for plugin class
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            if len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
                                attr_name = item.targets[0].id
                                if attr_name in ["REQUIRED_PERMISSIONS", "DEPENDENCIES", "VERSION"]:
                                    if isinstance(item.value, ast.List):
                                        metadata[attr_name.lower()] = [elt.s for elt in item.value.elts if isinstance(elt, ast.Str)]
                                    elif isinstance(item.value, ast.Str):
                                        metadata[attr_name.lower()] = item.value.s

            return metadata

        except Exception as e:
            logger.error(f"Failed to load metadata for {plugin_file}: {e}")
            return None

    async def _resolve_dependencies(self, metadata: Dict[str, Any]) -> bool:
        """Resolve plugin dependencies."""
        dependencies = metadata.get("dependencies", [])

        for dep in dependencies:
            if dep not in self.plugins:
                # Try to load dependency first
                dep_file = self.plugins_dir / f"{dep}.py"
                if dep_file.exists():
                    if not await self.load_plugin(dep_file):
                        return False
                else:
                    logger.error(f"Dependency {dep} not found for plugin {metadata['name']}")
                    return False

        return True

    async def _load_plugin_module(self, plugin_file: Path, metadata: Dict[str, Any]) -> Optional[Any]:
        """Load plugin module with sandboxing."""
        try:
            spec = importlib.util.spec_from_file_location(metadata["name"], plugin_file)
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)

            if self.sandbox_enabled:
                # Execute in sandboxed environment
                await self._execute_in_sandbox(spec.loader, module, metadata)
            else:
                spec.loader.exec_module(module)

            # Validate plugin interface
            if not hasattr(module, 'register'):
                logger.warning(f"Plugin {metadata['name']} missing register function")
                return None

            return module

        except Exception as e:
            logger.error(f"Error loading plugin module {metadata['name']}: {e}")
            return None

    async def _execute_in_sandbox(self, loader, module, metadata: Dict[str, Any]):
        """Execute plugin in sandboxed environment."""
        # Create restricted globals
        restricted_builtins = {
            'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
            'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
            'range': range, 'enumerate': enumerate, 'zip': zip,
            'sorted': sorted, 'reversed': reversed, 'sum': sum,
            'min': min, 'max': max, 'abs': abs, 'round': round,
            'print': print, 'isinstance': isinstance, 'hasattr': hasattr,
            'getattr': getattr, 'setattr': setattr
        }

        restricted_globals = {
            '__builtins__': restricted_builtins,
            '__name__': module.__name__,
            '__file__': module.__file__,
            'asyncio': asyncio,
            'logger': logger,
        }

        # Execute with restricted environment
        code = loader.get_code(module.__name__)
        exec(code, restricted_globals)

        # Copy safe attributes to module
        for name, value in restricted_globals.items():
            if not name.startswith('_'):
                setattr(module, name, value)

    async def unload_plugin(self, plugin_name: str):
        """Unload a plugin."""
        if plugin_name not in self.plugins:
            return

        plugin = self.plugins[plugin_name]

        # Call cleanup if available
        if hasattr(plugin, 'cleanup'):
            try:
                await plugin.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up plugin {plugin_name}: {e}")

        # Remove from registry
        del self.plugins[plugin_name]
        del self.plugin_metadata[plugin_name]

        # Remove from sys.modules
        module_name = f"plugins.{plugin_name}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        logger.info(f"Plugin {plugin_name} unloaded")

    async def reload_plugin(self, plugin_file: Path):
        """Reload a plugin."""
        plugin_name = plugin_file.stem
        await self.unload_plugin(plugin_name)
        await self.load_plugin(plugin_file)

    async def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed plugin information."""
        if plugin_name not in self.plugins:
            return None

        metadata = self.plugin_metadata[plugin_name]
        plugin = self.plugins[plugin_name]

        info = {
            "name": plugin_name,
            "version": metadata.get("version", "1.0.0"),
            "file": metadata["file"],
            "hash": metadata["hash"],
            "dependencies": metadata.get("dependencies", []),
            "permissions": metadata.get("permissions", []),
            "functions": [],
            "classes": []
        }

        # Inspect plugin for functions and classes
        for name, obj in inspect.getmembers(plugin):
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                info["functions"].append(name)
            elif inspect.isclass(obj):
                info["classes"].append(name)

        return info

    async def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins with metadata."""
        plugin_list = []
        for name, metadata in self.plugin_metadata.items():
            plugin_list.append({
                "name": name,
                "version": metadata.get("version", "1.0.0"),
                "status": "loaded" if name in self.plugins else "error",
                "dependencies": metadata.get("dependencies", []),
                "permissions": metadata.get("permissions", [])
            })
        return plugin_list

    async def check_plugin_health(self, plugin_name: str) -> Dict[str, Any]:
        """Check health of a specific plugin."""
        if plugin_name not in self.plugins:
            return {"status": "not_loaded"}

        plugin = self.plugins[plugin_name]
        metadata = self.plugin_metadata[plugin_name]

        health = {
            "status": "healthy",
            "checks": {
                "has_register": hasattr(plugin, 'register'),
                "has_initialize": hasattr(plugin, 'initialize'),
                "has_cleanup": hasattr(plugin, 'cleanup'),
                "dependencies_satisfied": await self._check_dependencies_satisfied(metadata),
                "file_integrity": await self._check_file_integrity(plugin_name, metadata)
            }
        }

        # Determine overall status
        if not all(health["checks"].values()):
            health["status"] = "unhealthy"

        return health

    async def _check_dependencies_satisfied(self, metadata: Dict[str, Any]) -> bool:
        """Check if plugin dependencies are satisfied."""
        dependencies = metadata.get("dependencies", [])
        return all(dep in self.plugins for dep in dependencies)

    async def _check_file_integrity(self, plugin_name: str, metadata: Dict[str, Any]) -> bool:
        """Check if plugin file has been modified."""
        plugin_file = Path(metadata["file"])
        if not plugin_file.exists():
            return False

        current_hash = hashlib.sha256(plugin_file.read_bytes()).hexdigest()
        stored_hash = metadata.get("hash", "")

        return current_hash == stored_hash

    async def update_plugin_from_marketplace(self, plugin_name: str):
        """Update plugin from marketplace."""
        marketplace_file = self.marketplace_dir / f"{plugin_name}.py"
        if not marketplace_file.exists():
            logger.error(f"Plugin {plugin_name} not found in marketplace")
            return

        # Backup current version
        current_file = self.plugins_dir / f"{plugin_name}.py"
        if current_file.exists():
            backup_file = current_file.with_suffix('.py.backup')
            current_file.rename(backup_file)

        # Install new version
        marketplace_file.copy(current_file)

        # Reload plugin
        await self.reload_plugin(current_file)

        logger.info(f"Plugin {plugin_name} updated from marketplace")

    async def cleanup(self):
        """Cleanup all plugins."""
        for plugin_name in list(self.plugins.keys()):
            await self.unload_plugin(plugin_name)

        self.executor.shutdown(wait=True)