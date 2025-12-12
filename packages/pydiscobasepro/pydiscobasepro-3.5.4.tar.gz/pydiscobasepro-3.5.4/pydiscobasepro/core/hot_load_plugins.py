"""
Hot-load Plugin System

Dynamic plugin loading and management with sandboxing.
"""

import asyncio
import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class HotLoadPluginSystem:
    """Hot-load plugin system with sandboxing and dependency management."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plugins_dir = Path("plugins")
        self.plugins_dir.mkdir(exist_ok=True)

        self.plugins: Dict[str, Any] = {}
        self.plugin_metadata: Dict[str, Dict[str, Any]] = {}
        self.plugin_dependencies: Dict[str, Dict[str, List[str]]] = {}
        self.sandbox_enabled = config.get("sandbox_enabled", True)

        self.executor = ThreadPoolExecutor(max_workers=4)
        self._load_queue: asyncio.Queue = asyncio.Queue()

    async def initialize(self):
        """Initialize the plugin system."""
        if self.config.get("auto_load", True):
            await self.load_all_plugins()

    async def load_all_plugins(self):
        """Load all available plugins."""
        plugin_files = list(self.plugins_dir.glob("*.py"))
        if not plugin_files:
            return

        for plugin_file in plugin_files:
            if plugin_file.name.startswith('_'):
                continue
            await self._load_queue.put(plugin_file)

        # Process load queue
        tasks = []
        for _ in range(min(4, len(plugin_files))):
            task = asyncio.create_task(self._process_load_queue())

        await asyncio.gather(*tasks)

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
        """Load a single plugin."""
        plugin_name = plugin_file.stem

        if plugin_name in self.plugins:
            return True

        try:
            # Load plugin metadata
            metadata = await self._load_plugin_metadata(plugin_file)
            if not metadata:
                return False

            # Check dependencies
            if not await self._check_dependencies(metadata):
                return False

            # Load plugin module
            plugin = await self._load_plugin_module(plugin_file, metadata)
            if not plugin:
                return False

            # Register plugin
            self.plugins[plugin_name] = plugin
            self.plugin_metadata[plugin_name] = metadata

            # Initialize plugin
            if hasattr(plugin, 'initialize'):
                try:
                    await plugin.initialize()
                except Exception as e:
                    logger.error(f"Plugin initialization failed: {e}")
                    await self.unload_plugin(plugin_name)
                    return False

            logger.info(f"Plugin loaded: {plugin_name}")
            return True

        except Exception as e:
            logger.error(f"Plugin load error: {e}")
            return False

    async def _load_plugin_metadata(self, plugin_file: Path) -> Optional[Dict[str, Any]]:
        """Load plugin metadata."""
        try:
            with open(plugin_file, 'r') as f:
                content = f.read()

            metadata = {
                "name": plugin_file.stem,
                "version": "1.0.0",
                "dependencies": [],
                "permissions": [],
                "file": str(plugin_file),
                "hash": hashlib.sha256(content.encode()).hexdigest()
            }

            # Parse metadata from code
            import ast
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id == "DEPENDENCIES" and isinstance(node.value, ast.List):
                                metadata["dependencies"] = [elt.s for elt in node.value.elts if isinstance(elt, ast.Str)]
                            elif target.id == "REQUIRED_PERMISSIONS" and isinstance(node.value, ast.List):
                                metadata["permissions"] = [elt.s for elt in node.value.elts if isinstance(elt, ast.Str)]

            return metadata
        except Exception as e:
            logger.error(f"Metadata load error: {e}")
            return None

    async def _check_dependencies(self, metadata: Dict[str, Any]) -> bool:
        """Check plugin dependencies."""
        dependencies = metadata.get("dependencies", [])
        for dep in dependencies:
            if dep not in self.plugins:
                logger.warning(f"Dependency not satisfied: {dep}")
                return False
        return True

    async def _load_plugin_module(self, plugin_file: Path, metadata: Dict[str, Any]) -> Optional[Any]:
        """Load plugin module with sandboxing."""
        try:
            spec = importlib.util.spec_from_file_location(metadata["name"], plugin_file)
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)

            if self.sandbox_enabled:
                await self._execute_in_sandbox(spec.loader, module)
            else:
                spec.loader.exec_module(module)

            if not hasattr(module, 'register'):
                logger.warning(f"Plugin missing register function: {metadata['name']}")
                return None

            return module

        except Exception as e:
            logger.error(f"Module load error: {e}")
            return None

    async def _execute_in_sandbox(self, loader, module):
        """Execute plugin in sandbox."""
        restricted_globals = {
            '__builtins__': {
                'len': len, 'str': str, 'int': int, 'float': float, 'bool': bool,
                'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
                'range': range, 'enumerate': enumerate, 'zip': zip,
                'sorted': sorted, 'reversed': reversed, 'sum': sum,
                'min': min, 'max': max, 'abs': abs, 'round': round,
                'print': print, 'isinstance': isinstance, 'hasattr': hasattr
            },
            '__name__': module.__name__,
            '__file__': module.__file__,
            'asyncio': asyncio,
            'logger': logger
        }

        code = loader.get_code(module.__name__)
        exec(code, restricted_globals)

        for name, value in restricted_globals.items():
            if not name.startswith('_'):
                setattr(module, name, value)

    async def unload_plugin(self, plugin_name: str):
        """Unload a plugin."""
        if plugin_name not in self.plugins:
            return

        plugin = self.plugins[plugin_name]

        if hasattr(plugin, 'cleanup'):
            try:
                await plugin.cleanup()
            except Exception as e:
                logger.error(f"Plugin cleanup error: {e}")

        del self.plugins[plugin_name]
        del self.plugin_metadata[plugin_name]

        module_name = f"plugins.{plugin_name}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        logger.info(f"Plugin unloaded: {plugin_name}")

    async def reload_plugin(self, plugin_file: Path):
        """Reload a plugin."""
        plugin_name = plugin_file.stem
        await self.unload_plugin(plugin_name)
        await self.load_plugin(plugin_file)

    async def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get plugin information."""
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
            "permissions": metadata.get("permissions", [])
        }

        # Inspect plugin
        import inspect
        functions = []
        classes = []
        for name, obj in inspect.getmembers(plugin):
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                functions.append(name)
            elif inspect.isclass(obj):
                classes.append(name)

        info["functions"] = functions
        info["classes"] = classes

        return info

    async def list_plugins(self) -> List[Dict[str, Any]]:
        """List all plugins."""
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

    async def cleanup(self):
        """Cleanup all plugins."""
        for plugin_name in list(self.plugins.keys()):
            await self.unload_plugin(plugin_name)

        self.executor.shutdown(wait=True)