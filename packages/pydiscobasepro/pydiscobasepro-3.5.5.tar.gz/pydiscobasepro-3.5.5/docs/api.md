---
layout: default
title: API Reference
nav_order: 3
---

<div class="page-header">
  <h1><i class="fas fa-code"></i> API Reference</h1>
  <p class="page-subtitle">Complete API documentation for PyDiscoBasePro classes, methods, and utilities</p>
</div>

## 📚 Table of Contents

<div class="api-toc">
  <div class="toc-section">
    <h3>Core Framework</h3>
    <ul>
      <li><a href="#pydiscobasepro">PyDiscoBasePro</a></li>
      <li><a href="#database">Database</a></li>
      <li><a href="#cache">Cache</a></li>
      <li><a href="#security">Security</a></li>
    </ul>
  </div>

  <div class="toc-section">
    <h3>Handlers</h3>
    <ul>
      <li><a href="#commandhandler">CommandHandler</a></li>
      <li><a href="#eventhandler">EventHandler</a></li>
      <li><a href="#componenthandler">ComponentHandler</a></li>
      <li><a href="#pluginhandler">PluginHandler</a></li>
    </ul>
  </div>

  <div class="toc-section">
    <h3>Utilities</h3>
    <ul>
      <li><a href="#logging">Logging</a></li>
      <li><a href="#metrics">Metrics</a></li>
      <li><a href="#config">Configuration</a></li>
      <li><a href="#cli">CLI Tools</a></li>
    </ul>
  </div>
</div>

## 🏗️ Core Framework

### PyDiscoBasePro {#pydiscobasepro}

The main bot class that orchestrates all framework components.

```python
from pydiscobasepro import PyDiscoBasePro

class PyDiscoBasePro:
    def __init__(
        self,
        token: str,
        prefix: str = "!",
        intents: discord.Intents = None,
        database_uri: str = None,
        config_path: str = "config/config.json",
        auto_load: bool = True
    ):
        """
        Initialize the PyDiscoBasePro bot.

        Args:
            token: Discord bot token
            prefix: Command prefix for text commands
            intents: Discord intents configuration
            database_uri: MongoDB connection URI
            config_path: Path to configuration file
            auto_load: Automatically load commands/events on startup
        """

    async def start(self) -> None:
        """Start the bot and all services."""
        pass

    async def load_all(self) -> None:
        """Load all commands, events, and plugins."""
        pass

    async def reload_all(self) -> None:
        """Reload all components without restarting."""
        pass

    def get_command(self, name: str) -> Optional[Command]:
        """Get a loaded command by name."""
        pass

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a loaded plugin by name."""
        pass
```

#### Example Usage

```python
import asyncio
from pydiscobasepro import PyDiscoBasePro

async def main():
    bot = PyDiscoBasePro(
        token="YOUR_BOT_TOKEN",
        prefix="!",
        database_uri="mongodb://localhost:27017/mybot"
    )

    # Load all components
    await bot.load_all()

    # Start the bot
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Database {#database}

Comprehensive MongoDB database interface with ORM-like operations.

```python
from pydiscobasepro.core.database import Database

class Database:
    def __init__(self, uri: str, database_name: str):
        """
        Initialize database connection.

        Args:
            uri: MongoDB connection URI
            database_name: Database name
        """

    # Connection management
    async def connect(self) -> None:
        """Establish database connection."""
        pass

    async def disconnect(self) -> None:
        """Close database connection."""
        pass

    async def ping(self) -> bool:
        """Test database connectivity."""
        pass

    # Guild operations
    async def get_guild_config(self, guild_id: int) -> Dict[str, Any]:
        """Get configuration for a guild."""
        pass

    async def update_guild_config(self, guild_id: int, config: Dict[str, Any]) -> None:
        """Update guild configuration."""
        pass

    async def delete_guild_config(self, guild_id: int) -> None:
        """Delete guild configuration."""
        pass

    # User operations
    async def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Get user profile data."""
        pass

    async def update_user_profile(self, user_id: int, profile: Dict[str, Any]) -> None:
        """Update user profile."""
        pass

    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics."""
        pass

    # Statistics and analytics
    async def increment_command_usage(self, command_name: str, user_id: int = None) -> None:
        """Increment command usage counter."""
        pass

    async def get_command_stats(self, command_name: str = None) -> Dict[str, Any]:
        """Get command usage statistics."""
        pass

    async def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log an event to the database."""
        pass

    # Bulk operations
    async def bulk_insert(self, collection: str, documents: List[Dict]) -> None:
        """Insert multiple documents."""
        pass

    async def bulk_update(self, collection: str, updates: List[Dict]) -> None:
        """Update multiple documents."""
        pass

    # Utility methods
    def get_collection(self, name: str):
        """Get a MongoDB collection."""
        pass

    async def create_indexes(self) -> None:
        """Create necessary database indexes."""
        pass
```

#### Database Schema Examples

```javascript
// Guild configuration
{
  _id: ObjectId,
  guild_id: 123456789012345678,
  prefix: "!",
  welcome_channel: 987654321098765432,
  log_channel: 876543210987654321,
  auto_mod: {
    enabled: true,
    filters: ["spam", "links"],
    actions: ["warn", "mute"]
  },
  created_at: ISODate,
  updated_at: ISODate
}

// User profile
{
  _id: ObjectId,
  user_id: 123456789012345678,
  username: "user#1234",
  experience: 1500,
  level: 5,
  badges: ["early_supporter", "moderator"],
  preferences: {
    theme: "dark",
    notifications: true
  },
  joined_at: ISODate,
  last_active: ISODate
}

// Command statistics
{
  _id: ObjectId,
  command_name: "play",
  usage_count: 1250,
  last_used: ISODate,
  users: [123456789, 987654321],
  guilds: [111111111, 222222222]
}
```

### Cache {#cache}

High-performance caching system with multiple backends.

```python
from pydiscobasepro.core.cache import CacheManager

class CacheManager:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize cache manager.

        Args:
            config: Cache configuration
        """

    # Basic operations
    async def get(self, key: str) -> Any:
        """Get value from cache."""
        pass

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value in cache with optional TTL."""
        pass

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        pass

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass

    async def expire(self, key: str, ttl: int) -> None:
        """Set expiration time for key."""
        pass

    # Advanced operations
    async def get_or_set(self, key: str, default_func, ttl: int = None) -> Any:
        """Get value or set default if not exists."""
        pass

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment numeric value."""
        pass

    async def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement numeric value."""
        pass

    # Bulk operations
    async def mget(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values."""
        pass

    async def mset(self, key_values: Dict[str, Any], ttl: int = None) -> None:
        """Set multiple values."""
        pass

    async def mdelete(self, keys: List[str]) -> int:
        """Delete multiple keys."""
        pass

    # Cache management
    async def clear(self) -> None:
        """Clear all cache data."""
        pass

    async def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        pass

    async def ping(self) -> bool:
        """Test cache connectivity."""
        pass
```

### Security {#security}

Enterprise-grade security features and utilities.

```python
from pydiscobasepro.core.security import SecurityManager

class SecurityManager:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize security manager.

        Args:
            config: Security configuration
        """

    # Rate limiting
    async def check_rate_limit(self, user_id: int, action: str) -> bool:
        """Check if user is within rate limits."""
        pass

    async def record_action(self, user_id: int, action: str) -> None:
        """Record user action for rate limiting."""
        pass

    # Encryption
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        pass

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        pass

    # Input validation
    def sanitize_input(self, input_str: str) -> str:
        """Sanitize user input."""
        pass

    def validate_command_args(self, args: Dict) -> bool:
        """Validate command arguments."""
        pass

    # Security monitoring
    async def log_security_event(self, event_type: str, data: Dict) -> None:
        """Log security-related events."""
        pass

    async def detect_suspicious_activity(self, user_id: int, actions: List) -> bool:
        """Detect potentially malicious activity."""
        pass

    # Access control
    async def check_permissions(self, user_id: int, permission: str) -> bool:
        """Check user permissions."""
        pass

    async def grant_permission(self, user_id: int, permission: str) -> None:
        """Grant permission to user."""
        pass

    async def revoke_permission(self, user_id: int, permission: str) -> None:
        """Revoke permission from user."""
        pass
```

## 🎛️ Handlers

### CommandHandler {#commandhandler}

Automatic command loading, management, and execution.

```python
from pydiscobasepro.core.handlers import CommandHandler

class CommandHandler:
    def __init__(self, bot, database: Database, config: Dict[str, Any]):
        """
        Initialize command handler.

        Args:
            bot: Discord bot instance
            database: Database instance
            config: Handler configuration
        """

    # Loading operations
    async def load_commands(self, directory: str = "commands") -> int:
        """Load all commands from directory."""
        pass

    async def load_command(self, file_path: str) -> bool:
        """Load a specific command file."""
        pass

    async def reload_commands(self) -> int:
        """Reload all commands."""
        pass

    async def reload_command(self, name: str) -> bool:
        """Reload a specific command."""
        pass

    async def unload_command(self, name: str) -> bool:
        """Unload a command."""
        pass

    # Command management
    def get_command(self, name: str) -> Optional[Command]:
        """Get command by name."""
        pass

    def list_commands(self) -> List[str]:
        """List all loaded commands."""
        pass

    def get_command_info(self, name: str) -> Dict[str, Any]:
        """Get detailed command information."""
        pass

    # Execution
    async def execute_command(self, ctx, command_name: str, *args, **kwargs) -> None:
        """Execute a command."""
        pass

    # Validation
    def validate_command(self, command_class) -> bool:
        """Validate command class structure."""
        pass

    # Error handling
    async def handle_command_error(self, ctx, error: Exception) -> None:
        """Handle command execution errors."""
        pass
```

#### Command Structure

```python
# commands/ping.py
import discord
from discord import app_commands
from pydiscobasepro.core.database import Database

class PingCommand:
    """A simple ping command."""

    def __init__(self, bot, database: Database):
        self.bot = bot
        self.database = database
        self.name = "ping"
        self.description = "Check bot latency"
        self.category = "utility"
        self.cooldown = 5  # seconds

        # Create slash command
        self.slash_command = app_commands.Command(
            name=self.name,
            description=self.description,
            callback=self.run
        )

    async def run(self, interaction: discord.Interaction):
        """Execute the ping command."""
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: {latency}ms",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

        # Log usage
        await self.database.increment_command_usage("ping")

# Export for auto-loading
ping_command = PingCommand
```

### EventHandler {#eventhandler}

Discord event management and processing.

```python
from pydiscobasepro.core.handlers import EventHandler

class EventHandler:
    def __init__(self, bot, database: Database, config: Dict[str, Any]):
        """
        Initialize event handler.

        Args:
            bot: Discord bot instance
            database: Database instance
            config: Handler configuration
        """

    # Loading operations
    async def load_events(self, directory: str = "events") -> int:
        """Load all events from directory."""
        pass

    async def load_event(self, file_path: str) -> bool:
        """Load a specific event file."""
        pass

    async def reload_events(self) -> int:
        """Reload all events."""
        pass

    async def reload_event(self, name: str) -> bool:
        """Reload a specific event."""
        pass

    async def unload_event(self, name: str) -> bool:
        """Unload an event."""
        pass

    # Event management
    def get_event(self, name: str) -> Optional[Event]:
        """Get event by name."""
        pass

    def list_events(self) -> List[str]:
        """List all loaded events."""
        pass

    # Statistics
    async def get_event_stats(self) -> Dict[str, int]:
        """Get event execution statistics."""
        pass

    # Error handling
    async def handle_event_error(self, event_name: str, error: Exception) -> None:
        """Handle event execution errors."""
        pass
```

#### Event Structure

```python
# events/on_ready.py
import discord
from pydiscobasepro.core.database import Database

class OnReadyEvent:
    """Handle bot ready event."""

    def __init__(self, bot, database: Database):
        self.bot = bot
        self.database = database
        self.name = "on_ready"

    async def run(self):
        """Execute when bot becomes ready."""
        print(f"🤖 {self.bot.user} is ready!")

        # Update bot status
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.bot.guilds)} servers"
            )
        )

        # Log startup
        await self.database.log_event("bot_ready", {
            "guilds": len(self.bot.guilds),
            "users": sum(guild.member_count for guild in self.bot.guilds),
            "timestamp": discord.utils.utcnow().isoformat()
        })

# Export for auto-loading
on_ready_event = OnReadyEvent
```

### ComponentHandler {#componenthandler}

Interactive component (buttons, selects) management.

```python
from pydiscobasepro.core.handlers import ComponentHandler

class ComponentHandler:
    def __init__(self, bot, database: Database, config: Dict[str, Any]):
        """
        Initialize component handler.

        Args:
            bot: Discord bot instance
            database: Database instance
            config: Handler configuration
        """

    # Loading operations
    async def load_components(self, directory: str = "components") -> int:
        """Load all components from directory."""
        pass

    async def load_component(self, file_path: str) -> bool:
        """Load a specific component file."""
        pass

    async def reload_components(self) -> int:
        """Reload all components."""
        pass

    # Component management
    def register_button(self, custom_id: str, callback) -> None:
        """Register a button callback."""
        pass

    def register_select(self, custom_id: str, callback) -> None:
        """Register a select menu callback."""
        pass

    def unregister_component(self, custom_id: str) -> None:
        """Unregister a component."""
        pass

    # Utility methods
    def generate_custom_id(self, component_type: str, data: Dict = None) -> str:
        """Generate a unique custom ID."""
        pass

    def parse_custom_id(self, custom_id: str) -> Dict:
        """Parse data from custom ID."""
        pass
```

### PluginHandler {#pluginhandler}

Plugin loading, management, and sandboxing.

```python
from pydiscobasepro.core.handlers import PluginHandler

class PluginHandler:
    def __init__(self, bot, config: Dict[str, Any]):
        """
        Initialize plugin handler.

        Args:
            bot: Discord bot instance
            config: Plugin configuration
        """

    # Plugin operations
    async def load_plugin(self, plugin_path: str) -> bool:
        """Load a plugin from path."""
        pass

    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        pass

    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a plugin."""
        pass

    # Plugin management
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins."""
        pass

    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """Get plugin information."""
        pass

    # Sandbox operations
    def create_sandbox(self, plugin_name: str) -> Sandbox:
        """Create a sandbox environment for plugin."""
        pass

    def execute_in_sandbox(self, plugin_code: str, sandbox: Sandbox) -> Any:
        """Execute plugin code in sandbox."""
        pass

    # Plugin marketplace
    async def search_plugins(self, query: str) -> List[Dict]:
        """Search plugins in marketplace."""
        pass

    async def install_from_marketplace(self, plugin_id: str) -> bool:
        """Install plugin from marketplace."""
        pass

    async def update_plugin(self, plugin_name: str) -> bool:
        """Update plugin to latest version."""
        pass
```

## 🛠️ Utilities

### Logging {#logging}

Structured logging with encryption and rotation.

```python
from pydiscobasepro.core.logging import setup_structured_logging, get_logger

def setup_structured_logging(config: Dict[str, Any] = None) -> None:
    """
    Setup structured logging system.

    Args:
        config: Logging configuration
    """

def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    pass

class StructuredLogger:
    def __init__(self, config: Dict[str, Any]):
        """Initialize structured logger."""

    def log_event(self, level: str, event: str, data: Dict = None) -> None:
        """Log a structured event."""
        pass

    def log_error(self, error: Exception, context: Dict = None) -> None:
        """Log an error with context."""
        pass

    def log_performance(self, operation: str, duration: float, metadata: Dict = None) -> None:
        """Log performance metrics."""
        pass
```

### Metrics {#metrics}

Comprehensive metrics collection and reporting.

```python
from pydiscobasepro.core.metrics import MetricsEngine

class MetricsEngine:
    def __init__(self):
        """Initialize metrics engine."""

    # Counter metrics
    def increment_counter(self, name: str, value: float = 1.0, labels: Dict = None) -> None:
        """Increment a counter metric."""
        pass

    # Gauge metrics
    def set_gauge(self, name: str, value: float, labels: Dict = None) -> None:
        """Set a gauge metric value."""
        pass

    def increment_gauge(self, name: str, value: float = 1.0, labels: Dict = None) -> None:
        """Increment a gauge metric."""
        pass

    def decrement_gauge(self, name: str, value: float = 1.0, labels: Dict = None) -> None:
        """Decrement a gauge metric."""
        pass

    # Histogram metrics
    def observe_histogram(self, name: str, value: float, labels: Dict = None) -> None:
        """Observe a histogram metric."""
        pass

    # Timer metrics
    def start_timer(self, name: str, labels: Dict = None) -> Timer:
        """Start a timer metric."""
        pass

    def time_function(self, name: str):
        """Decorator to time function execution."""
        pass

    # Export methods
    def get_metrics(self) -> Dict:
        """Get all current metrics."""
        pass

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        pass

    def export_json(self) -> str:
        """Export metrics in JSON format."""
        pass
```

### Configuration {#config}

Advanced configuration management.

```python
from pydiscobasepro.cli.config import CLIConfig

class CLIConfig:
    def __init__(self, config_dir: str = None):
        """Initialize configuration manager."""

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        pass

    def save_config(self) -> None:
        """Save configuration to file."""
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        pass

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        pass

    def get_config_dict(self) -> Dict[str, Any]:
        """Get full configuration dictionary."""
        pass

    def validate_config(self) -> List[str]:
        """Validate configuration and return errors."""
        pass

    def export_config(self, format: str = "json") -> str:
        """Export configuration in specified format."""
        pass

    def import_config(self, data: str, format: str = "json") -> None:
        """Import configuration from string."""
        pass
```

### CLI Tools {#cli}

Command-line interface utilities.

```python
from pydiscobasepro.cli.app import create_cli_app

def create_cli_app() -> typer.Typer:
    """Create the main CLI application."""
    pass

# Available CLI commands:
# pydiscobasepro project create <name>
# pydiscobasepro auth login
# pydiscobasepro config show
# pydiscobasepro plugins list
# pydiscobasepro monitoring metrics
# pydiscobasepro devops deploy
# pydiscobasepro testing run
# pydiscobasepro --help
```

## 📖 Examples

### Complete Bot Setup

```python
import asyncio
from pydiscobasepro import PyDiscoBasePro

async def main():
    # Initialize bot with full configuration
    bot = PyDiscoBasePro(
        token="YOUR_BOT_TOKEN",
        prefix="!",
        database_uri="mongodb://localhost:27017/mybot",
        config_path="config/config.json"
    )

    # Setup additional components
    await bot.database.connect()
    await bot.cache.connect()

    # Load all components
    await bot.load_all()

    # Setup monitoring
    bot.metrics.start_timer("bot_uptime")

    # Start the bot
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Command with Database

```python
import discord
from discord import app_commands
from pydiscobasepro.core.database import Database

class LevelCommand:
    def __init__(self, bot, database: Database):
        self.bot = bot
        self.database = database
        self.name = "level"
        self.description = "Check your level and experience"

        self.slash_command = app_commands.Command(
            name=self.name,
            description=self.description,
            callback=self.run
        )

    async def run(self, interaction: discord.Interaction, user: discord.User = None):
        target_user = user or interaction.user

        # Get user profile from database
        profile = await self.database.get_user_profile(target_user.id)

        if not profile:
            # Create new profile
            profile = {
                "experience": 0,
                "level": 1,
                "username": target_user.name
            }
            await self.database.update_user_profile(target_user.id, profile)

        # Calculate level progress
        exp = profile.get("experience", 0)
        level = profile.get("level", 1)
        exp_needed = level * 100  # Simple leveling formula
        progress = (exp % 100) / 100 * 100

        embed = discord.Embed(
            title=f"📊 {target_user.display_name}'s Level",
            color=discord.Color.blue()
        )

        embed.add_field(name="Level", value=str(level), inline=True)
        embed.add_field(name="Experience", value=f"{exp}/{exp_needed}", inline=True)
        embed.add_field(name="Progress", value=f"{progress:.1f}%", inline=True)

        # Progress bar
        filled = int(progress / 10)
        bar = "█" * filled + "░" * (10 - filled)
        embed.add_field(name="Progress Bar", value=f"`{bar}`", inline=False)

        await interaction.response.send_message(embed=embed)

level_command = LevelCommand
```

### Plugin Development

```python
# plugins/weather.py
import aiohttp
from pydiscobasepro.core.plugin import Plugin

class WeatherPlugin(Plugin):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = "weather"
        self.version = "1.0.0"
        self.description = "Weather information plugin"
        self.api_key = None

    async def on_load(self):
        """Called when plugin is loaded."""
        self.api_key = self.config.get("weather.api_key")
        if not self.api_key:
            self.logger.warning("Weather API key not configured")

    async def on_unload(self):
        """Called when plugin is unloaded."""
        pass

    @self.bot.slash_command(name="weather", description="Get weather information")
    async def weather_command(self, interaction: discord.Interaction, city: str):
        if not self.api_key:
            await interaction.response.send_message("Weather API not configured")
            return

        async with aiohttp.ClientSession() as session:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data["main"]["temp"]
                    description = data["weather"][0]["description"]

                    embed = discord.Embed(
                        title=f"Weather in {city}",
                        description=f"{temp}°C - {description.title()}",
                        color=discord.Color.blue()
                    )
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("City not found")

def create_plugin(bot):
    return WeatherPlugin(bot)
```

## 🔗 Related Links

- [Getting Started Guide](getting-started.html)
- [Configuration Reference](configuration.html)
- [Deployment Guide](deployment.html)
- [GitHub Repository](https://github.com/code-xon/pydiscobasepro)
- [Community Discord](https://discord.gg/pydiscobasepro)
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