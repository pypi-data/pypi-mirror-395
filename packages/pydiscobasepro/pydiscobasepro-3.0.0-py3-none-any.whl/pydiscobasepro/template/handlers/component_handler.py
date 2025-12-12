import importlib
import sys
from pathlib import Path

from loguru import logger

class ComponentHandler:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.components = {}
        self.components_path = Path("components")

    async def load_components(self):
        for file in self.components_path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            await self.load_component(file.stem)

    async def load_component(self, name):
        try:
            module_name = f"components.{name}"
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            component_class = getattr(module, name.capitalize())
            component_instance = component_class(self.bot, self.database)
            self.components[name] = component_instance
            # Components register their listeners
            logger.info(f"Loaded component: {name}")
        except Exception as e:
            logger.error(f"Failed to load component {name}: {e}")

    async def reload_components(self):
        for name in list(self.components.keys()):
            await self.unload_component(name)
        await self.load_components()

    async def unload_component(self, name):
        if name in self.components:
            del self.components[name]
            module_name = f"components.{name}"
            if module_name in sys.modules:
                del sys.modules[module_name]
            logger.info(f"Unloaded component: {name}")