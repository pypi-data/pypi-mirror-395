import importlib
import os
import sys
from pathlib import Path

from discord.ext import commands
from loguru import logger

class CommandHandler:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database
        self.commands = {}
        self.commands_path = Path("commands")

    async def load_commands(self):
        for file in self.commands_path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            await self.load_command(file.stem)

    async def load_command(self, name):
        try:
            module_name = f"commands.{name}"
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            command_class = getattr(module, name.capitalize())
            command_instance = command_class(self.bot, self.database)
            self.commands[name] = command_instance
            # Register slash command if has slash metadata
            if hasattr(command_instance, "slash_command"):
                self.bot.tree.add_command(command_instance.slash_command)
            # Register prefix command
            if hasattr(command_instance, "prefix_command"):
                self.bot.add_command(command_instance.prefix_command)
            logger.info(f"Loaded command: {name}")
        except Exception as e:
            logger.error(f"Failed to load command {name}: {e}")

    async def reload_commands(self):
        for name in list(self.commands.keys()):
            await self.unload_command(name)
        await self.load_commands()

    async def unload_command(self, name):
        if name in self.commands:
            # Remove from bot
            if hasattr(self.commands[name], "slash_command"):
                self.bot.tree.remove_command(self.commands[name].slash_command.name)
            if hasattr(self.commands[name], "prefix_command"):
                self.bot.remove_command(self.commands[name].prefix_command.name)
            del self.commands[name]
            # Remove from sys.modules
            module_name = f"commands.{name}"
            if module_name in sys.modules:
                del sys.modules[module_name]
            logger.info(f"Unloaded command: {name}")