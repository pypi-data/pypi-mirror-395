from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any

class GuildConfig:
    def __init__(self, guild_id: int, prefix: str = "!", welcome_channel: Optional[int] = None, log_channel: Optional[int] = None):
        self.guild_id = guild_id
        self.prefix = prefix
        self.welcome_channel = welcome_channel
        self.log_channel = log_channel

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.guild_id,
            "prefix": self.prefix,
            "welcome_channel": self.welcome_channel,
            "log_channel": self.log_channel
        }

class UserProfile:
    def __init__(self, user_id: int, xp: int = 0, level: int = 1, coins: int = 0):
        self.user_id = user_id
        self.xp = xp
        self.level = level
        self.coins = coins

    def to_dict(self) -> Dict[str, Any]:
        return {
            "_id": self.user_id,
            "xp": self.xp,
            "level": self.level,
            "coins": self.coins
        }

class Database:
    def __init__(self, db):
        self.db = db
        self.guilds = self.db.guilds
        self.users = self.db.users
        self.settings = self.db.settings
        self.command_stats = self.db.command_stats

    # Guild operations
    async def get_guild_config(self, guild_id: int) -> Optional[GuildConfig]:
        data = await self.guilds.find_one({"_id": guild_id})
        if data:
            return GuildConfig(**data)
        return None

    async def update_guild_config(self, config: GuildConfig):
        await self.guilds.update_one({"_id": config.guild_id}, {"$set": config.to_dict()}, upsert=True)

    # User operations
    async def get_user_profile(self, user_id: int) -> Optional[UserProfile]:
        data = await self.users.find_one({"_id": user_id})
        if data:
            return UserProfile(**data)
        return None

    async def update_user_profile(self, profile: UserProfile):
        await self.users.update_one({"_id": profile.user_id}, {"$set": profile.to_dict()}, upsert=True)

    # Command stats
    async def increment_command_usage(self, command_name: str):
        await self.command_stats.update_one(
            {"command": command_name},
            {"$inc": {"usage": 1}},
            upsert=True
        )

    async def get_command_stats(self, command_name: str) -> int:
        stat = await self.command_stats.find_one({"command": command_name})
        return stat["usage"] if stat else 0

    # Legacy methods for compatibility
    async def get_guild(self, guild_id):
        return await self.guilds.find_one({"_id": guild_id})

    async def update_guild(self, guild_id, data):
        await self.guilds.update_one({"_id": guild_id}, {"$set": data}, upsert=True)

    async def get_user(self, user_id):
        return await self.users.find_one({"_id": user_id})

    async def update_user(self, user_id, data):
        await self.users.update_one({"_id": user_id}, {"$set": data}, upsert=True)

    async def get_setting(self, key):
        setting = await self.settings.find_one({"key": key})
        return setting["value"] if setting else None

    async def set_setting(self, key, value):
        await self.settings.update_one({"key": key}, {"$set": {"value": value}}, upsert=True)