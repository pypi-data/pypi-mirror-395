---
layout: default
title: Configuration
nav_order: 4
---

<div class="page-header">
  <h1><i class="fas fa-cogs"></i> Configuration Guide</h1>
  <p class="page-subtitle">Complete configuration reference for PyDiscoBasePro with examples and best practices</p>
</div>

## 📁 Configuration Files

<div class="config-files">
  <div class="config-file">
    <h4><code>config/config.json</code></h4>
    <p>Main configuration file for bot settings, database, logging, and features.</p>
  </div>

  <div class="config-file">
    <h4><code>config/secrets.json</code></h4>
    <p>Sensitive configuration like API keys and passwords (auto-encrypted).</p>
  </div>

  <div class="config-file">
    <h4><code>.env</code></h4>
    <p>Environment variables for sensitive data and deployment-specific settings.</p>
  </div>
</div>

## ⚙️ Core Configuration

### Basic Bot Settings

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "description": "My awesome Discord bot powered by PyDiscoBasePro",
  "version": "1.0.0",
  "owner_id": 123456789012345678,
  "support_guild_id": 987654321098765432
}
```

| Setting | Type | Required | Description |
|---------|------|----------|-------------|
| `token` | string | ✅ | Discord bot token from Developer Portal |
| `prefix` | string | ❌ | Command prefix (default: "!") |
| `description` | string | ❌ | Bot description |
| `version` | string | ❌ | Bot version |
| `owner_id` | integer | ❌ | Bot owner's Discord user ID |
| `support_guild_id` | integer | ❌ | Support server guild ID |

### Discord Intents

```json
{
  "intents": {
    "guilds": true,
    "members": true,
    "messages": true,
    "message_content": true,
    "voice_states": true,
    "reactions": true,
    "presences": false,
    "message_typing": false,
    "direct_messages": true,
    "guild_messages": true,
    "guild_reactions": true,
    "guild_voice_states": true,
    "auto_moderation": true
  }
}
```

| Intent | Description | Required for |
|--------|-------------|--------------|
| `guilds` | Guild events | Basic functionality |
| `members` | Member events | User management |
| `messages` | Message events | Commands, moderation |
| `message_content` | Message content | Command parsing |
| `voice_states` | Voice events | Music, voice features |
| `reactions` | Reaction events | Reaction roles, polls |
| `presences` | Presence events | Rich presence features |

## 🗄️ Database Configuration

### MongoDB Settings

```json
{
  "mongodb": {
    "uri": "mongodb://localhost:27017",
    "database": "my_discord_bot",
    "connection_timeout": 5000,
    "server_selection_timeout": 5000,
    "max_pool_size": 10,
    "min_pool_size": 2,
    "max_idle_time": 30000,
    "collections": {
      "users": "users",
      "guilds": "guilds",
      "logs": "logs",
      "commands": "commands",
      "moderation": "moderation"
    }
  }
}
```

### Alternative Databases

```json
{
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "database": "my_bot_db",
    "username": "bot_user",
    "password": "secure_password",
    "ssl_mode": "require"
  }
}
```

```json
{
  "database": {
    "type": "sqlite",
    "path": "data/bot.db",
    "backup_interval": 3600
  }
}
```

## 📊 Logging Configuration

### Basic Logging

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/bot.log",
    "max_size": "10MB",
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S"
  }
}
```

### Advanced Logging

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/bot.log",
    "max_size": "50MB",
    "backup_count": 10,
    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",

    "handlers": {
      "console": {
        "enabled": true,
        "level": "INFO",
        "format": "%(levelname)s: %(message)s"
      },
      "file": {
        "enabled": true,
        "level": "DEBUG",
        "max_size": "100MB",
        "backup_count": 20
      },
      "discord": {
        "enabled": false,
        "webhook_url": "https://discord.com/api/webhooks/...",
        "level": "ERROR"
      }
    },

    "encryption": {
      "enabled": true,
      "key_rotation_days": 30
    },

    "structured": {
      "enabled": true,
      "include_context": true,
      "include_stack_traces": true
    }
  }
}
```

## 🔒 Security Configuration

### Rate Limiting

```json
{
  "security": {
    "rate_limit": {
      "enabled": true,
      "global_limit": 100,
      "global_window": 60,
      "user_limit": 30,
      "user_window": 60,
      "guild_limit": 500,
      "guild_window": 60,
      "command_cooldowns": {
        "ping": 5,
        "help": 10,
        "admin": 30
      }
    },

    "encryption": {
      "enabled": true,
      "algorithm": "AES-256-GCM",
      "key_rotation_days": 30
    },

    "input_validation": {
      "enabled": true,
      "max_message_length": 2000,
      "allowed_domains": ["discord.gg", "github.com"],
      "blocked_words": ["spam", "advertisement"]
    },

    "audit": {
      "enabled": true,
      "log_admin_actions": true,
      "log_sensitive_commands": true,
      "retention_days": 90
    }
  }
}
```

### Access Control

```json
{
  "permissions": {
    "default_role": "user",
    "roles": {
      "admin": {
        "permissions": ["*"],
        "inherit": []
      },
      "moderator": {
        "permissions": ["kick", "ban", "mute", "manage_messages"],
        "inherit": ["user"]
      },
      "user": {
        "permissions": ["use_commands", "send_messages"],
        "inherit": []
      }
    },

    "command_permissions": {
      "ban": ["admin", "moderator"],
      "kick": ["admin", "moderator"],
      "mute": ["admin", "moderator"],
      "play_music": ["user"],
      "admin_only": ["admin"]
    }
  }
}
```

## 🌐 Web Dashboard Configuration

### Dashboard Settings

```json
{
  "dashboard": {
    "enabled": true,
    "host": "0.0.0.0",
    "port": 8080,
    "ssl": {
      "enabled": false,
      "cert_file": "certs/cert.pem",
      "key_file": "certs/key.pem"
    },
    "auth": {
      "enabled": true,
      "session_timeout": 3600,
      "max_login_attempts": 5,
      "lockout_duration": 900
    },
    "cors": {
      "enabled": true,
      "origins": ["*"],
      "methods": ["GET", "POST", "PUT", "DELETE"],
      "headers": ["Content-Type", "Authorization"]
    }
  }
}
```

### Dashboard Features

```json
{
  "dashboard_features": {
    "metrics": {
      "enabled": true,
      "refresh_interval": 30,
      "historical_data_days": 30
    },
    "logs": {
      "enabled": true,
      "max_lines": 1000,
      "auto_scroll": true
    },
    "commands": {
      "enabled": true,
      "allow_execution": false,
      "command_history": 100
    },
    "users": {
      "enabled": true,
      "show_sensitive_data": false,
      "export_data": true
    },
    "guilds": {
      "enabled": true,
      "show_member_count": true,
      "show_channels": true
    }
  }
}
```

## 🔌 Plugin Configuration

### Plugin System

```json
{
  "plugins": {
    "enabled": true,
    "sandbox_enabled": true,
    "auto_update": true,
    "update_interval_hours": 24,
    "marketplace_url": "https://plugins.pydiscobasepro.com",

    "security": {
      "allowed_imports": ["discord", "asyncio", "json"],
      "blocked_modules": ["os", "sys", "subprocess"],
      "max_memory_mb": 50,
      "max_execution_time": 30
    },

    "directories": {
      "plugins": "plugins/",
      "cache": "plugins/cache/",
      "logs": "plugins/logs/"
    }
  }
}
```

### Plugin Marketplace

```json
{
  "marketplace": {
    "enabled": true,
    "api_url": "https://api.plugins.pydiscobasepro.com",
    "auth_token": "your_marketplace_token",
    "auto_install_updates": false,
    "trusted_publishers": [
      "pydiscobasepro",
      "community-trusted"
    ]
  }
}
```

## 📈 Monitoring & Metrics

### Metrics Configuration

```json
{
  "metrics": {
    "enabled": true,
    "collection_interval": 60,
    "retention_days": 30,

    "prometheus": {
      "enabled": false,
      "port": 9090,
      "path": "/metrics"
    },

    "influxdb": {
      "enabled": false,
      "url": "http://localhost:8086",
      "token": "your-influx-token",
      "org": "your-org",
      "bucket": "discord_bot"
    },

    "custom_metrics": {
      "command_usage": true,
      "error_rates": true,
      "performance": true,
      "user_engagement": true
    }
  }
}
```

### Health Checks

```json
{
  "health_checks": {
    "enabled": true,
    "interval_seconds": 300,
    "timeout_seconds": 30,

    "checks": {
      "database": {
        "enabled": true,
        "query": "db.stats()"
      },
      "discord_api": {
        "enabled": true,
        "endpoint": "/users/@me"
      },
      "memory_usage": {
        "enabled": true,
        "max_percent": 85
      },
      "cpu_usage": {
        "enabled": true,
        "max_percent": 90
      }
    },

    "alerts": {
      "discord_webhook": "https://discord.com/api/webhooks/...",
      "email": "admin@example.com",
      "slack_webhook": "https://hooks.slack.com/..."
    }
  }
}
```

## 🚀 Performance Configuration

### Caching

```json
{
  "cache": {
    "enabled": true,
    "backend": "redis",
    "ttl": 3600,
    "max_memory_items": 10000,

    "redis": {
      "host": "localhost",
      "port": 6379,
      "password": null,
      "db": 0,
      "ssl": false
    },

    "memory": {
      "max_size_mb": 100,
      "eviction_policy": "lru"
    },

    "strategies": {
      "user_data": 1800,
      "guild_config": 3600,
      "command_results": 300,
      "api_responses": 600
    }
  }
}
```

### Optimization

```json
{
  "optimization": {
    "command_caching": true,
    "lazy_loading": true,
    "connection_pooling": true,
    "query_optimization": true,

    "concurrency": {
      "max_workers": 4,
      "thread_pool_size": 8,
      "async_timeout": 30
    },

    "memory": {
      "gc_threshold": 100000,
      "cache_cleanup_interval": 300,
      "max_cache_size_mb": 200
    }
  }
}
```

## 🔧 Development Configuration

### Development Mode

```json
{
  "development": {
    "enabled": true,
    "debug_mode": true,
    "auto_reload": true,
    "reload_delay": 1.0,
    "log_level": "DEBUG",

    "hot_reload": {
      "commands": true,
      "events": true,
      "plugins": false,
      "config": true
    },

    "testing": {
      "mock_discord": true,
      "mock_database": true,
      "verbose_assertions": true
    }
  }
}
```

### Testing Configuration

```json
{
  "testing": {
    "enabled": true,
    "test_directory": "tests/",
    "coverage_enabled": true,
    "coverage_min_percent": 80,

    "framework": {
      "pytest": {
        "args": ["-v", "--tb=short"],
        "markers": ["slow", "integration", "unit"]
      }
    },

    "mocks": {
      "discord_api": true,
      "database": true,
      "external_apis": true
    },

    "performance": {
      "benchmark_enabled": true,
      "profile_memory": true,
      "profile_cpu": true
    }
  }
}
```

## 🌐 Environment Variables

### Environment Configuration

```bash
# Bot Configuration
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!
BOT_DESCRIPTION="My Discord Bot"

# Database
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=my_bot_db

# Security
ENCRYPTION_KEY=your-32-char-encryption-key
JWT_SECRET=your-jwt-secret-key

# Dashboard
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8080
DASHBOARD_SECRET_KEY=your-dashboard-secret

# External APIs
WEATHER_API_KEY=your-weather-api-key
GOOGLE_API_KEY=your-google-api-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# Development
DEBUG_MODE=true
AUTO_RELOAD=true
```

### Environment Override

```json
{
  "environment_override": {
    "enabled": true,
    "prefix": "BOT_",
    "override_existing": false,

    "mappings": {
      "BOT_TOKEN": "token",
      "BOT_PREFIX": "prefix",
      "MONGODB_URI": "mongodb.uri",
      "DATABASE_NAME": "mongodb.database",
      "LOG_LEVEL": "logging.level"
    }
  }
}
```

## 🔄 Configuration Management

### CLI Configuration Commands

```bash
# View current configuration
pydiscobasepro config show

# Set configuration values
pydiscobasepro config set logging.level DEBUG
pydiscobasepro config set dashboard.enabled true

# Get specific values
pydiscobasepro config get mongodb.database

# Export configuration
pydiscobasepro config export --format yaml > config_backup.yaml

# Import configuration
pydiscobasepro config import config_backup.json
```

### Configuration Validation

```json
{
  "validation": {
    "enabled": true,
    "strict_mode": false,
    "schema_version": "1.0",

    "rules": {
      "token": {
        "required": true,
        "type": "string",
        "min_length": 50
      },
      "mongodb.uri": {
        "required": true,
        "type": "string",
        "pattern": "^mongodb://"
      },
      "dashboard.port": {
        "type": "integer",
        "min": 1024,
        "max": 65535
      }
    },

    "warnings": {
      "missing_optional": true,
      "deprecated_keys": true,
      "type_mismatches": true
    }
  }
}
```

## 📋 Complete Example Configuration

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "prefix": "!",
  "description": "Advanced Discord Bot with PyDiscoBasePro",
  "version": "1.0.0",
  "owner_id": 123456789012345678,

  "intents": {
    "guilds": true,
    "members": true,
    "messages": true,
    "message_content": true,
    "voice_states": true,
    "reactions": true
  },

  "mongodb": {
    "uri": "mongodb://localhost:27017",
    "database": "discord_bot",
    "connection_timeout": 5000
  },

  "logging": {
    "level": "INFO",
    "file": "logs/bot.log",
    "max_size": "10MB",
    "backup_count": 5
  },

  "dashboard": {
    "enabled": true,
    "host": "0.0.0.0",
    "port": 8080
  },

  "plugins": {
    "enabled": true,
    "sandbox_enabled": true
  },

  "security": {
    "rate_limit": {
      "enabled": true,
      "user_limit": 30,
      "user_window": 60
    }
  },

  "cache": {
    "enabled": true,
    "ttl": 3600
  },

  "metrics": {
    "enabled": true,
    "collection_interval": 60
  }
}
```

## 🆘 Troubleshooting Configuration

<div class="troubleshooting">
  <details>
    <summary><strong>Configuration file not found?</strong></summary>
    <ul>
      <li>Ensure you're in the correct project directory</li>
      <li>Run <code>pydiscobasepro project create mybot</code> to create a new project</li>
      <li>Check file permissions on the config directory</li>
    </ul>
  </details>

  <details>
    <summary><strong>Database connection failed?</strong></summary>
    <ul>
      <li>Verify MongoDB is running and accessible</li>
      <li>Check the connection URI format</li>
      <li>Ensure network connectivity to database host</li>
      <li>Validate database credentials</li>
    </ul>
  </details>

  <details>
    <summary><strong>Bot permissions issues?</strong></summary>
    <ul>
      <li>Review Discord intents configuration</li>
      <li>Check bot permissions in Discord Developer Portal</li>
      <li>Ensure bot has necessary guild permissions</li>
      <li>Verify bot role hierarchy</li>
    </ul>
  </details>
</div>

## 🔗 Related Documentation

- [Getting Started Guide](getting-started.html)
- [API Reference](api.html)
- [Deployment Guide](deployment.html)
- [CLI Commands Reference](../cli-commands.html)
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