"""
CLI Configuration Management

Handles CLI configuration, profiles, encryption, and persistence.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, List
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import yaml
import toml

class CLIConfig:
    """Advanced CLI configuration manager with encryption and profiles."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".pydiscobasepro"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "cli_config.json"
        self.encrypted_config_file = self.config_dir / "cli_config.enc"
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)

        self._config: Dict[str, Any] = {}
        self._encryption_key: Optional[bytes] = None
        self._current_profile = "default"

        self.load_config()

    def get_encryption_key(self) -> bytes:
        """Get or generate encryption key."""
        if self._encryption_key is None:
            key_file = self.config_dir / "encryption.key"
            if key_file.exists():
                self._encryption_key = key_file.read_bytes()
            else:
                # Generate new key
                salt = os.urandom(16)
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                password = os.environ.get("PYDISCOBASEPRO_KEY", "default_key").encode()
                self._encryption_key = base64.urlsafe_b64encode(kdf.derive(password))
                key_file.write_bytes(self._encryption_key)
        return self._encryption_key

    def load_config(self):
        """Load configuration from file."""
        if self.encrypted_config_file.exists():
            try:
                fernet = Fernet(self.get_encryption_key())
                encrypted_data = self.encrypted_config_file.read_bytes()
                decrypted_data = fernet.decrypt(encrypted_data)
                self._config = json.loads(decrypted_data.decode())
            except Exception:
                # Fallback to unencrypted config
                if self.config_file.exists():
                    with open(self.config_file, 'r') as f:
                        self._config = json.load(f)
        elif self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self._config = json.load(f)
        else:
            self._config = self.get_default_config()

    def save_config(self):
        """Save configuration to encrypted file."""
        try:
            fernet = Fernet(self.get_encryption_key())
            config_json = json.dumps(self._config, indent=2)
            encrypted_data = fernet.encrypt(config_json.encode())
            self.encrypted_config_file.write_bytes(encrypted_data)
        except Exception as e:
            # Fallback to unencrypted save
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": "3.0.0",
            "auth": {
                "required": False,
                "token_expiry": 3600,
                "max_sessions": 5
            },
            "security": {
                "encryption_enabled": True,
                "audit_logging": True,
                "brute_force_protection": True,
                "rate_limiting": {
                    "enabled": True,
                    "max_requests": 100,
                    "window_seconds": 60
                }
            },
            "plugins": {
                "auto_load": True,
                "sandbox_enabled": True,
                "max_plugins": 50
            },
            "cache": {
                "enabled": True,
                "redis_url": "redis://localhost:6379",
                "ttl": 3600
            },
            "logging": {
                "level": "INFO",
                "structured": True,
                "encryption": False
            },
            "metrics": {
                "enabled": True,
                "prometheus_port": 9090
            },
            "execution": {
                "max_workers": 10,
                "timeout": 30,
                "retry_attempts": 3
            },
            "watchdog": {
                "enabled": True,
                "check_interval": 60,
                "auto_restart": True
            },
            "recovery": {
                "auto_backup": True,
                "max_snapshots": 10
            },
            "offline_mode": False,
            "current_profile": "default"
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """Set configuration value."""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()

    def get_history_file(self) -> Path:
        """Get command history file path."""
        return self.config_dir / "command_history.txt"

    def show_config(self):
        """Display current configuration."""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()
        table = Table(title="CLI Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        def flatten_config(d, prefix=""):
            for k, v in d.items():
                key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    flatten_config(v, key)
                else:
                    table.add_row(key, str(v))

        flatten_config(self._config)
        console.print(Panel(table, border_style="blue"))

    def manage_profiles(self, args: List[str]):
        """Manage configuration profiles."""
        if not args:
            self.list_profiles()
            return

        command = args[0].lower()
        if command == "list":
            self.list_profiles()
        elif command == "create":
            if len(args) >= 2:
                self.create_profile(args[1])
            else:
                print("Usage: config profiles create <name>")
        elif command == "switch":
            if len(args) >= 2:
                self.switch_profile(args[1])
            else:
                print("Usage: config profiles switch <name>")
        elif command == "delete":
            if len(args) >= 2:
                self.delete_profile(args[1])
            else:
                print("Usage: config profiles delete <name>")
        else:
            print(f"Unknown profile command: {command}")

    def list_profiles(self):
        """List available profiles."""
        profiles = []
        for profile_file in self.profiles_dir.glob("*.json"):
            profiles.append(profile_file.stem)

        from rich.console import Console
        console = Console()
        if profiles:
            console.print("[green]Available profiles:[/green]")
            for profile in profiles:
                marker = " →" if profile == self._current_profile else ""
                console.print(f"  {profile}{marker}")
        else:
            console.print("[yellow]No profiles found.[/yellow]")

    def create_profile(self, name: str):
        """Create a new profile."""
        profile_file = self.profiles_dir / f"{name}.json"
        if profile_file.exists():
            print(f"Profile '{name}' already exists.")
            return

        # Copy current config
        with open(profile_file, 'w') as f:
            json.dump(self._config, f, indent=2)
        print(f"Profile '{name}' created.")

    def switch_profile(self, name: str):
        """Switch to a different profile."""
        profile_file = self.profiles_dir / f"{name}.json"
        if not profile_file.exists():
            print(f"Profile '{name}' does not exist.")
            return

        # Load profile
        with open(profile_file, 'r') as f:
            self._config = json.load(f)
        self._current_profile = name
        self.save_config()
        print(f"Switched to profile '{name}'.")

    def delete_profile(self, name: str):
        """Delete a profile."""
        if name == "default":
            print("Cannot delete default profile.")
            return

        profile_file = self.profiles_dir / f"{name}.json"
        if profile_file.exists():
            profile_file.unlink()
            print(f"Profile '{name}' deleted.")
        else:
            print(f"Profile '{name}' does not exist.")

    def export_config(self, format_type: str = "json") -> str:
        """Export configuration in specified format."""
        if format_type == "json":
            return json.dumps(self._config, indent=2)
        elif format_type == "yaml":
            return yaml.dump(self._config, default_flow_style=False)
        elif format_type == "toml":
            return toml.dumps(self._config)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def import_config(self, data: str, format_type: str = "json"):
        """Import configuration from string."""
        if format_type == "json":
            self._config = json.loads(data)
        elif format_type == "yaml":
            self._config = yaml.safe_load(data)
        elif format_type == "toml":
            self._config = toml.loads(data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        self.save_config()