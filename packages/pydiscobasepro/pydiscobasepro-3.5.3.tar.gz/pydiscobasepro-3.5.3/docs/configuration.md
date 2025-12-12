---
layout: default
title: Configuration
nav_order: 4
---

# Configuration Guide

## Basic Configuration

The main configuration file is located at `config/config.json`. Here's a complete example:

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "intents": {
    "guilds": true,
    "members": true,
    "messages": true,
    "message_content": true,
    "voice_states": true,
    "reactions": true,
    "presences": false
  },
  "mongodb": {
    "uri": "mongodb://localhost:27017",
    "database": "pydiscobasepro"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/bot.log",
    "discord_channel_id": null,
    "max_file_size": "10 MB",
    "retention": "7 days"
  },
  "dashboard": {
    "enabled": true,
    "host": "0.0.0.0",
    "port": 8080,
    "auth_required": false
  },
  "features": {
    "auto_register_commands": true,
    "hot_reload": true,
    "error_reporting": true
  }
}
```

## Configuration Options

### Bot Token

Your Discord bot token from the [Developer Portal](https://discord.com/developers/applications).

### Command Prefix

The prefix for traditional commands (e.g., "!help").

### Intents

Discord gateway intents your bot needs. Enable only what's required for security.

- `guilds`: Server information
- `members`: Member information
- `messages`: Message content and events
- `message_content`: Access to message content
- `voice_states`: Voice channel events
- `reactions`: Message reactions

### MongoDB Configuration

Database connection settings.

- `uri`: MongoDB connection string
- `database`: Database name

### Logging Configuration

Control how the bot logs information.

- `level`: DEBUG, INFO, WARNING, ERROR
- `file`: Log file path
- `discord_channel_id`: Channel ID for Discord logging
- `max_file_size`: Maximum log file size
- `retention`: How long to keep log files

### Dashboard Configuration

Web dashboard settings.

- `enabled`: Enable/disable dashboard
- `host`: Server host (0.0.0.0 for all interfaces)
- `port`: Server port
- `auth_required`: Require authentication

## Environment Variables

You can use environment variables for sensitive data:

```bash
export BOT_TOKEN="your_token_here"
export MONGODB_URI="mongodb://localhost:27017"
export DASHBOARD_PORT="8080"
```

Then reference them in your config:

```json
{
  "token": "$BOT_TOKEN",
  "mongodb": {
    "uri": "$MONGODB_URI"
  },
  "dashboard": {
    "port": "$DASHBOARD_PORT"
  }
}
```

## Advanced Configuration

### Custom Command Categories

Organize commands into categories:

```json
"categories": {
  "moderation": ["ban", "kick", "mute"],
  "fun": ["meme", "joke", "game"],
  "utility": ["help", "info", "ping"]
}
```

### Rate Limiting

Configure global rate limits:

```json
"rate_limits": {
  "commands_per_second": 5,
  "messages_per_minute": 60
}
```

### Plugin Configuration

Configure third-party plugins:

```json
"plugins": {
  "music": {
    "enabled": true,
    "max_queue_size": 100
  },
  "moderation": {
    "auto_mod": true,
    "spam_detection": true
  }
}
```

## Configuration Validation

The framework validates your configuration on startup. Common errors:

- **Invalid token**: Check your bot token from Discord Developer Portal
- **Missing intents**: Enable required intents in both config and Developer Portal
- **MongoDB connection failed**: Verify MongoDB is running and URI is correct
- **Permission errors**: Ensure bot has necessary permissions in your server