import importlib
import sys
from pathlib import Path

from loguru import logger

class EventHandler:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.events = {}
        self.events_path = Path("events")

    async def load_events(self):
        for file in self.events_path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            await self.load_event(file.stem)

    async def load_event(self, name):
        try:
            module_name = f"events.{name}"
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            event_class = getattr(module, name.capitalize())
            event_instance = event_class(self.bot, self.database)
            self.events[name] = event_instance
            # Events are registered via decorators in the class
            logger.info(f"Loaded event: {name}")
        except Exception as e:
            logger.error(f"Failed to load event {name}: {e}")

    async def reload_events(self):
        for name in list(self.events.keys()):
            await self.unload_event(name)
        await self.load_events()

    async def unload_event(self, name):
        if name in self.events:
            del self.events[name]
            module_name = f"events.{name}"
            if module_name in sys.modules:
                del sys.modules[module_name]
            logger.info(f"Unloaded event: {name}")