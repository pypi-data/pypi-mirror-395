---
layout: default
title: API Reference
nav_order: 3
---

# API Reference

## Core Classes

### Database

Main database interface for MongoDB operations.

```python
class Database:
    def __init__(self, db: AsyncIOMotorDatabase)

    # Guild operations
    async def get_guild_config(self, guild_id: int) -> GuildConfig
    async def update_guild_config(self, config: GuildConfig)

    # User operations
    async def get_user_profile(self, user_id: int) -> UserProfile
    async def update_user_profile(self, profile: UserProfile)

    # Statistics
    async def increment_command_usage(self, command_name: str)
    async def get_command_stats(self, command_name: str) -> int
```

### Command Handlers

Automatic loading and management of commands.

```python
class CommandHandler:
    def __init__(self, bot: commands.Bot, database: Database)

    async def load_commands(self)
    async def reload_commands()
    async def load_command(self, name: str)
    async def unload_command(self, name: str)
```

### Event Handlers

Discord event management system.

```python
class EventHandler:
    def __init__(self, bot: commands.Bot, database: Database)

    async def load_events(self)
    async def reload_events()
    async def load_event(self, name: str)
    async def unload_event(self, name: str)
```

## Models

### GuildConfig

```python
class GuildConfig:
    def __init__(self, guild_id: int, prefix: str = "!", welcome_channel: Optional[int] = None, log_channel: Optional[int] = None)

    guild_id: int
    prefix: str
    welcome_channel: Optional[int]
    log_channel: Optional[int]

    def to_dict(self) -> Dict[str, Any]
```

### UserProfile

```python
class UserProfile:
    def __init__(self, user_id: int, xp: int = 0, level: int = 1, coins: int = 0)

    user_id: int
    xp: int
    level: int
    coins: int

    def to_dict(self) -> Dict[str, Any]
```

## Utilities

### CooldownManager

```python
class CooldownManager:
    def __init__(self)

    async def check_cooldown(self, key: str, duration: int) -> bool
```

### API Request Helper

```python
async def api_request(url: str, method: str = "GET", headers: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict
```

## Dashboard

### Dashboard Class

```python
class Dashboard:
    def __init__(self, bot: commands.Bot, database: Database, config: Dict)

    async def run(self)
    # Serves web interface at configured host:port
```