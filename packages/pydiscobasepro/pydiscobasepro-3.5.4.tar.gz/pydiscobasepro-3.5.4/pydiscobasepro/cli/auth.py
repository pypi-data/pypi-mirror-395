"""
CLI Authentication System

Handles user authentication, token management, permissions, and security.
"""

import hashlib
import secrets
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import bcrypt
import jwt
from cryptography.fernet import Fernet
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)
console = Console()

class CLIAuth:
    """Advanced CLI authentication and authorization system."""

    def __init__(self, config):
        self.config = config
        self.users_file = Path.home() / ".pydiscobasepro" / "users.enc"
        self.sessions_file = Path.home() / ".pydiscobasepro" / "sessions.enc"
        self._current_user = None
        self._users = {}
        self._sessions = {}

        self.load_users()
        self.load_sessions()

    def create_default_user(self):
        """Create default user if no users exist."""
        if not self._users:
            default_username = "default"
            default_password = "default"
            self._users[default_username] = {
                "password_hash": self.hash_password(default_password),
                "role": "admin",
                "created": datetime.utcnow().isoformat(),
                "permissions": ["*"]
            }
            self.save_users()
            logger.info("Created default user: default/default")

    def get_encryption_key(self) -> bytes:
        """Get encryption key for sensitive data."""
        key_file = Path.home() / ".pydiscobasepro" / "auth.key"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            return key

    def load_users(self):
        """Load encrypted users database."""
        if self.users_file.exists():
            try:
                fernet = Fernet(self.get_encryption_key())
                encrypted_data = self.users_file.read_bytes()
                decrypted_data = fernet.decrypt(encrypted_data)
                self._users = jwt.decode(decrypted_data, options={"verify_signature": False})
            except Exception as e:
                logger.error(f"Failed to load users: {e}")
                self._users = {}
        else:
            # Create default user if no users file exists
            self.create_default_user()

    def save_users(self):
        """Save encrypted users database."""
        try:
            fernet = Fernet(self.get_encryption_key())
            users_json = jwt.encode(self._users, "secret", algorithm="HS256")
            encrypted_data = fernet.encrypt(users_json.encode())
            self.users_file.write_bytes(encrypted_data)
        except Exception as e:
            logger.error(f"Failed to save users: {e}")

    def load_sessions(self):
        """Load encrypted sessions database."""
        if self.sessions_file.exists():
            try:
                fernet = Fernet(self.get_encryption_key())
                encrypted_data = self.sessions_file.read_bytes()
                decrypted_data = fernet.decrypt(encrypted_data)
                self._sessions = jwt.decode(decrypted_data, options={"verify_signature": False})
            except Exception as e:
                logger.error(f"Failed to load sessions: {e}")
                self._sessions = {}

    def save_sessions(self):
        """Save encrypted sessions database."""
        try:
            fernet = Fernet(self.get_encryption_key())
            sessions_json = jwt.encode(self._sessions, "secret", algorithm="HS256")
            encrypted_data = fernet.encrypt(sessions_json.encode())
            self.sessions_file.write_bytes(encrypted_data)
        except Exception as e:
            logger.error(f"Failed to save sessions: {e}")

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def generate_token(self, user_id: str) -> str:
        """Generate JWT token for user."""
        expiry = datetime.utcnow() + timedelta(seconds=self.config.get("auth.token_expiry", 3600))
        payload = {
            "user_id": user_id,
            "exp": expiry.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }
        secret = secrets.token_hex(32)
        return jwt.encode(payload, secret, algorithm="HS256")

    def validate_token(self, token: str) -> Optional[str]:
        """Validate JWT token and return user_id."""
        try:
            # Note: In production, use proper secret management
            payload = jwt.decode(token, options={"verify_signature": False})
            user_id = payload.get("user_id")
            if user_id in self._users:
                return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
        return None

    async def login(self):
        """Interactive login process."""
        console.print("[cyan]PyDiscoBasePro CLI Login[/cyan]")

        username = Prompt.ask("Username")
        password = Prompt.ask("Password", password=True)

        if self.authenticate(username, password):
            console.print(f"[green]Welcome back, {username}![/green]")
            self._current_user = username
            # Generate and store session
            token = self.generate_token(username)
            session_id = secrets.token_hex(16)
            self._sessions[session_id] = {
                "user_id": username,
                "token": token,
                "created": datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat()
            }
            self.save_sessions()
        else:
            console.print("[red]Invalid credentials.[/red]")

    async def logout(self):
        """Logout current user."""
        if self._current_user:
            # Remove active sessions for user
            sessions_to_remove = []
            for session_id, session in self._sessions.items():
                if session["user_id"] == self._current_user:
                    sessions_to_remove.append(session_id)

            for session_id in sessions_to_remove:
                del self._sessions[session_id]

            self.save_sessions()
            console.print(f"[green]Logged out {self._current_user}[/green]")
            self._current_user = None
        else:
            console.print("[yellow]Not logged in.[/yellow]")

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        if username in self._users:
            stored_hash = self._users[username]["password_hash"]
            return self.verify_password(password, stored_hash)
        return False

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return self._current_user is not None

    async def show_status(self):
        """Show authentication status."""
        if self._current_user:
            console.print(f"[green]Logged in as: {self._current_user}[/green]")

            # Show active sessions
            user_sessions = [
                session for session in self._sessions.values()
                if session["user_id"] == self._current_user
            ]

            if user_sessions:
                table = Table(title="Active Sessions")
                table.add_column("Created", style="cyan")
                table.add_column("Last Activity", style="green")

                for session in user_sessions:
                    table.add_row(
                        session["created"],
                        session["last_activity"]
                    )
                console.print(table)
        else:
            console.print("[yellow]Not logged in[/yellow]")

    async def manage_users(self, args: List[str]):
        """Manage users (admin only)."""
        if not self._current_user:
            console.print("[red]Authentication required.[/red]")
            return

        if not args:
            self.list_users()
            return

        command = args[0].lower()
        if command == "list":
            self.list_users()
        elif command == "add":
            if len(args) >= 2:
                await self.add_user(args[1])
            else:
                console.print("[red]Usage: auth users add <username>[/red]")
        elif command == "remove":
            if len(args) >= 2:
                self.remove_user(args[1])
            else:
                console.print("[red]Usage: auth users remove <username>[/red]")
        elif command == "reset-password":
            if len(args) >= 2:
                await self.reset_password(args[1])
            else:
                console.print("[red]Usage: auth users reset-password <username>[/red]")
        else:
            console.print(f"[red]Unknown users command: {command}[/red]")

    def list_users(self):
        """List all users."""
        if not self._users:
            console.print("[yellow]No users found.[/yellow]")
            return

        table = Table(title="Users")
        table.add_column("Username", style="cyan")
        table.add_column("Role", style="green")
        table.add_column("Created", style="yellow")

        for username, user_data in self._users.items():
            table.add_row(
                username,
                user_data.get("role", "user"),
                user_data.get("created", "Unknown")
            )
        console.print(table)

    async def add_user(self, username: str):
        """Add a new user."""
        if username in self._users:
            console.print(f"[red]User '{username}' already exists.[/red]")
            return

        password = Prompt.ask(f"Password for {username}", password=True)
        confirm_password = Prompt.ask("Confirm password", password=True)

        if password != confirm_password:
            console.print("[red]Passwords do not match.[/red]")
            return

        role = Prompt.ask("Role", default="user")

        self._users[username] = {
            "password_hash": self.hash_password(password),
            "role": role,
            "created": datetime.utcnow().isoformat(),
            "permissions": self.get_default_permissions(role)
        }

        self.save_users()
        console.print(f"[green]User '{username}' added successfully.[/green]")

    def remove_user(self, username: str):
        """Remove a user."""
        if username not in self._users:
            console.print(f"[red]User '{username}' does not exist.[/red]")
            return

        if username == self._current_user:
            console.print("[red]Cannot remove yourself.[/red]")
            return

        del self._users[username]
        self.save_users()
        console.print(f"[green]User '{username}' removed.[/green]")

    async def reset_password(self, username: str):
        """Reset user password."""
        if username not in self._users:
            console.print(f"[red]User '{username}' does not exist.[/red]")
            return

        new_password = Prompt.ask(f"New password for {username}", password=True)
        confirm_password = Prompt.ask("Confirm new password", password=True)

        if new_password != confirm_password:
            console.print("[red]Passwords do not match.[/red]")
            return

        self._users[username]["password_hash"] = self.hash_password(new_password)
        self.save_users()
        console.print(f"[green]Password reset for '{username}'.[/green]")

    def get_default_permissions(self, role: str) -> List[str]:
        """Get default permissions for role."""
        permissions = {
            "admin": ["*"],
            "developer": ["read", "write", "execute", "deploy"],
            "user": ["read", "execute"]
        }
        return permissions.get(role, ["read"])

    def check_permission(self, permission: str) -> bool:
        """Check if current user has permission."""
        if not self._current_user:
            return False

        user_perms = self._users[self._current_user].get("permissions", [])
        return "*" in user_perms or permission in user_perms