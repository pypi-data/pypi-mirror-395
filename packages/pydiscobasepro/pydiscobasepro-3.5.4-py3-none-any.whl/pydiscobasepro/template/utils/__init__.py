import logging
from pathlib import Path

from loguru import logger

def setup_logging(config):
    # Remove default handler
    logger.remove()
    # Add file handler
    log_file = Path(config["file"])
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(log_file, level=config["level"], rotation="1 day", retention="7 days")
    # Add console handler
    logger.add(logging.StreamHandler(), level=config["level"])
    # Discord logging if channel_id provided
    if config.get("discord_channel_id"):
        # This would need bot instance, so maybe implement later in handlers
        pass

# Other utilities
import asyncio
import random
from datetime import datetime, timedelta

class CooldownManager:
    def __init__(self):
        self.cooldowns = {}

    async def check_cooldown(self, key, duration):
        now = datetime.now()
        if key in self.cooldowns:
            if now < self.cooldowns[key]:
                return False
        self.cooldowns[key] = now + timedelta(seconds=duration)
        return True

cooldown_manager = CooldownManager()

def random_choice(choices):
    return random.choice(choices)

async def api_request(url, method="GET", headers=None, data=None):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=headers, json=data) as resp:
            return await resp.json()