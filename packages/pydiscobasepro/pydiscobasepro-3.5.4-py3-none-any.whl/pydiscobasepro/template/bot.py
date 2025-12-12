import json
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from watchfiles import awatch

from database import Database
from handlers import CommandHandler, EventHandler, ComponentHandler
from utils import setup_logging
from dashboard import Dashboard

# Load config
config_path = Path("config/config.json")
if not config_path.exists():
    logger.error("config/config.json not found. Please create it with your bot token.")
    sys.exit(1)

with open(config_path, "r") as f:
    config = json.load(f)

# Setup logging
setup_logging(config["logging"])

# Setup intents
intents = discord.Intents.default()
for intent, enabled in config["intents"].items():
    if hasattr(intents, intent):
        setattr(intents, intent, enabled)

# Initialize bot
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

# Database
db_client = AsyncIOMotorClient(config["mongodb"]["uri"])
database = Database(db_client[config["mongodb"]["database"]])

# Handlers
command_handler = CommandHandler(bot, database)
event_handler = EventHandler(bot, database)
component_handler = ComponentHandler(bot, database)

# Dashboard
dashboard = Dashboard(bot, database, config["dashboard"]) if config["dashboard"]["enabled"] else None

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await command_handler.load_commands()
    await event_handler.load_events()
    await component_handler.load_components()
    if dashboard:
        await dashboard.run()
    # Start hot-reloading
    bot.loop.create_task(hot_reload())

async def hot_reload():
    paths = ["commands", "events", "components"]
    async for changes in awatch(*paths):
        for change in changes:
            path, action = change
            if path.suffix == ".py":
                if "commands" in str(path):
                    await command_handler.reload_commands()
                elif "events" in str(path):
                    await event_handler.reload_events()
                elif "components" in str(path):
                    await component_handler.reload_components()

if __name__ == "__main__":
    bot.run(config["token"])