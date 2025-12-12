import discord
from loguru import logger

class OnReady:
    def __init__(self, bot, database):
        self.bot = bot
        self.database = database

        @self.bot.event
        async def on_ready():
            logger.info("Bot is ready!")
            # Custom logic here