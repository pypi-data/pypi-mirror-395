"""
Core Configuration Manager

Centralized configuration management with environment support and validation.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """Central configuration manager for PyDiscoBasePro."""

    def __init__(self):
        self.config_dir = Path("config")
        self.config_file = self.config_dir / "config.json"
        self.env_prefix = "PYDISCOBASEPRO_"
        self._config = {}

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file and environment."""
        # Start with defaults
        config = self.get_default_config()

        # Load from file if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                self._merge_config(config, file_config)
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}")

        # Override with environment variables
        self._load_env_config(config)

        # Validate configuration
        self._validate_config(config)

        self._config = config
        return config

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "token": "",
            "prefix": "!",
            "intents": {
                "guilds": True,
                "members": True,
                "messages": True,
                "message_content": True,
                "voice_states": True,
                "reactions": True
            },
            "mongodb": {
                "uri": "mongodb://localhost:27017",
                "database": "pydiscobasepro"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/bot.log",
                "discord_channel_id": None
            },
            "dashboard": {
                "enabled": False,
                "host": "0.0.0.0",
                "port": 8080
            },
            "cache": {
                "enabled": True,
                "redis_url": "redis://localhost:6379",
                "ttl": 3600
            },
            "security": {
                "encryption_enabled": True,
                "audit_logging": True,
                "rate_limiting": True
            },
            "plugins": {
                "auto_load": True,
                "sandbox_enabled": True
            },
            "execution": {
                "max_workers": 10,
                "timeout": 30
            },
            "watchdog": {
                "enabled": True,
                "check_interval": 60
            },
            "recovery": {
                "auto_backup": True
            },
            "metrics": {
                "enabled": True,
                "prometheus_port": 9090
            }
        }

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]):
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _load_env_config(self, config: Dict[str, Any]):
        """Load configuration from environment variables."""
        for env_key, env_value in os.environ.items():
            if env_key.startswith(self.env_prefix):
                config_key = env_key[len(self.env_prefix):].lower().replace('_', '.')
                self._set_nested_config(config, config_key, env_value)

    def _set_nested_config(self, config: Dict[str, Any], key_path: str, value: str):
        """Set nested configuration value from key path."""
        keys = key_path.split('.')
        current = config

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Type conversion
        final_key = keys[-1]
        if value.lower() in ('true', 'false'):
            current[final_key] = value.lower() == 'true'
        elif value.isdigit():
            current[final_key] = int(value)
        elif value.replace('.', '').isdigit():
            current[final_key] = float(value)
        else:
            current[final_key] = value

    def _validate_config(self, config: Dict[str, Any]):
        """Validate configuration values."""
        # Required fields
        required = ["token"]
        for req in required:
            if not config.get(req):
                logger.warning(f"Required configuration field missing: {req}")

        # Validate port ranges
        if "dashboard" in config and "port" in config["dashboard"]:
            port = config["dashboard"]["port"]
            if not (1024 <= port <= 65535):
                logger.warning(f"Dashboard port {port} is not in valid range (1024-65535)")

        # Validate URLs
        if "mongodb" in config and "uri" in config["mongodb"]:
            uri = config["mongodb"]["uri"]
            if not uri.startswith(("mongodb://", "mongodb+srv://")):
                logger.warning(f"Invalid MongoDB URI format: {uri}")

    def save_config(self):
        """Save current configuration to file."""
        self.config_dir.mkdir(exist_ok=True)
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key path."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """Set configuration value by key path."""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()

    def reload_config(self):
        """Reload configuration from file."""
        self._config = self.load_config()