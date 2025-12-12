"""
RBAC (Role-Based Access Control) System

Comprehensive role-based access control with permissions and policies.
"""

import hashlib
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class Permission(Enum):
    """System permissions."""
    # Bot management
    BOT_START = "bot.start"
    BOT_STOP = "bot.stop"
    BOT_RESTART = "bot.restart"
    BOT_CONFIG = "bot.config"

    # Command management
    COMMAND_CREATE = "command.create"
    COMMAND_EDIT = "command.edit"
    COMMAND_DELETE = "command.delete"
    COMMAND_EXECUTE = "command.execute"

    # User management
    USER_BAN = "user.ban"
    USER_KICK = "user.kick"
    USER_MUTE = "user.mute"
    USER_ROLE_ASSIGN = "user.role_assign"

    # Server management
    SERVER_CONFIG = "server.config"
    SERVER_BACKUP = "server.backup"
    SERVER_RESTORE = "server.restore"

    # Plugin management
    PLUGIN_INSTALL = "plugin.install"
    PLUGIN_REMOVE = "plugin.remove"
    PLUGIN_CONFIG = "plugin.config"

    # System access
    SYSTEM_LOGS = "system.logs"
    SYSTEM_METRICS = "system.metrics"
    SYSTEM_HEALTH = "system.health"

    # Administrative
    ADMIN_FULL_ACCESS = "admin.full_access"

@dataclass
class Role:
    """Represents a user role with permissions."""
    name: str
    description: str
    permissions: Set[Permission]
    inherits_from: Optional[str] = None
    priority: int = 0  # Higher priority roles override lower ones

@dataclass
class User:
    """Represents a user with roles."""
    user_id: str
    username: str
    roles: Set[str]
    custom_permissions: Set[Permission] = None

class RBACSystem:
    """Role-Based Access Control system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.roles_file = Path.home() / ".pydiscobasepro" / "rbac_roles.json"
        self.users_file = Path.home() / ".pydiscobasepro" / "rbac_users.json"

        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.permission_cache: Dict[str, Set[Permission]] = {}

        self._setup_default_roles()
        self.load_data()

    def _setup_default_roles(self):
        """Setup default roles."""
        self.roles = {
            "admin": Role(
                name="Administrator",
                description="Full system access",
                permissions={Permission.ADMIN_FULL_ACCESS},
                priority=100
            ),
            "moderator": Role(
                name="Moderator",
                description="Server moderation permissions",
                permissions={
                    Permission.USER_BAN,
                    Permission.USER_KICK,
                    Permission.USER_MUTE,
                    Permission.COMMAND_EXECUTE,
                    Permission.SYSTEM_LOGS
                },
                priority=50
            ),
            "developer": Role(
                name="Developer",
                description="Development and plugin permissions",
                permissions={
                    Permission.COMMAND_CREATE,
                    Permission.COMMAND_EDIT,
                    Permission.PLUGIN_INSTALL,
                    Permission.PLUGIN_CONFIG,
                    Permission.SYSTEM_METRICS
                },
                priority=40
            ),
            "user": Role(
                name="User",
                description="Basic user permissions",
                permissions={
                    Permission.COMMAND_EXECUTE,
                    Permission.SYSTEM_HEALTH
                },
                priority=10
            )
        }

    def load_data(self):
        """Load roles and users from disk."""
        # Load roles
        if self.roles_file.exists():
            try:
                with open(self.roles_file, 'r') as f:
                    roles_data = json.load(f)
                for role_name, role_data in roles_data.items():
                    permissions = {Permission(p) for p in role_data.get("permissions", [])}
                    self.roles[role_name] = Role(
                        name=role_data["name"],
                        description=role_data["description"],
                        permissions=permissions,
                        inherits_from=role_data.get("inherits_from"),
                        priority=role_data.get("priority", 0)
                    )
            except Exception as e:
                logger.error(f"Failed to load roles: {e}")

        # Load users
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    users_data = json.load(f)
                for user_id, user_data in users_data.items():
                    custom_perms = None
                    if "custom_permissions" in user_data:
                        custom_perms = {Permission(p) for p in user_data["custom_permissions"]}

                    self.users[user_id] = User(
                        user_id=user_id,
                        username=user_data["username"],
                        roles=set(user_data.get("roles", [])),
                        custom_permissions=custom_perms
                    )
            except Exception as e:
                logger.error(f"Failed to load users: {e}")

    def save_data(self):
        """Save roles and users to disk."""
        # Save roles
        roles_data = {}
        for role_name, role in self.roles.items():
            roles_data[role_name] = {
                "name": role.name,
                "description": role.description,
                "permissions": [p.value for p in role.permissions],
                "inherits_from": role.inherits_from,
                "priority": role.priority
            }

        try:
            with open(self.roles_file, 'w') as f:
                json.dump(roles_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save roles: {e}")

        # Save users
        users_data = {}
        for user_id, user in self.users.items():
            user_data = {
                "user_id": user.user_id,
                "username": user.username,
                "roles": list(user.roles)
            }
            if user.custom_permissions:
                user_data["custom_permissions"] = [p.value for p in user.custom_permissions]
            users_data[user_id] = user_data

        try:
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save users: {e}")

    def create_role(self, name: str, description: str, permissions: List[Permission],
                   inherits_from: Optional[str] = None, priority: int = 0) -> bool:
        """Create a new role."""
        if name in self.roles:
            return False

        if inherits_from and inherits_from not in self.roles:
            return False

        self.roles[name] = Role(
            name=name,
            description=description,
            permissions=set(permissions),
            inherits_from=inherits_from,
            priority=priority
        )

        self.save_data()
        # Clear permission cache
        self.permission_cache.clear()

        logger.info(f"Role created: {name}")
        return True

    def delete_role(self, name: str) -> bool:
        """Delete a role."""
        if name not in self.roles:
            return False

        # Check if role is in use
        for user in self.users.values():
            if name in user.roles:
                return False

        del self.roles[name]
        self.save_data()
        self.permission_cache.clear()

        logger.info(f"Role deleted: {name}")
        return True

    def assign_role_to_user(self, user_id: str, role_name: str) -> bool:
        """Assign a role to a user."""
        if role_name not in self.roles:
            return False

        if user_id not in self.users:
            # Create user if doesn't exist
            self.users[user_id] = User(
                user_id=user_id,
                username=f"User_{user_id}",
                roles=set()
            )

        self.users[user_id].roles.add(role_name)
        self.save_data()

        # Clear user's permission cache
        self.permission_cache.pop(user_id, None)

        logger.info(f"Role {role_name} assigned to user {user_id}")
        return True

    def revoke_role_from_user(self, user_id: str, role_name: str) -> bool:
        """Revoke a role from a user."""
        if user_id not in self.users:
            return False

        if role_name in self.users[user_id].roles:
            self.users[user_id].roles.remove(role_name)
            self.save_data()
            self.permission_cache.pop(user_id, None)

            logger.info(f"Role {role_name} revoked from user {user_id}")
            return True

        return False

    def grant_permission_to_user(self, user_id: str, permission: Permission) -> bool:
        """Grant a custom permission to a user."""
        if user_id not in self.users:
            self.users[user_id] = User(
                user_id=user_id,
                username=f"User_{user_id}",
                roles=set()
            )

        if self.users[user_id].custom_permissions is None:
            self.users[user_id].custom_permissions = set()

        self.users[user_id].custom_permissions.add(permission)
        self.save_data()
        self.permission_cache.pop(user_id, None)

        logger.info(f"Permission {permission.value} granted to user {user_id}")
        return True

    def revoke_permission_from_user(self, user_id: str, permission: Permission) -> bool:
        """Revoke a custom permission from a user."""
        if user_id not in self.users or not self.users[user_id].custom_permissions:
            return False

        if permission in self.users[user_id].custom_permissions:
            self.users[user_id].custom_permissions.remove(permission)
            self.save_data()
            self.permission_cache.pop(user_id, None)

            logger.info(f"Permission {permission.value} revoked from user {user_id}")
            return True

        return False

    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user."""
        if user_id in self.permission_cache:
            return self.permission_cache[user_id]

        if user_id not in self.users:
            return set()

        user = self.users[user_id]
        permissions = set()

        # Add custom permissions
        if user.custom_permissions:
            permissions.update(user.custom_permissions)

        # Add role permissions
        for role_name in user.roles:
            if role_name in self.roles:
                role = self.roles[role_name]
                permissions.update(role.permissions)

                # Add inherited permissions
                self._add_inherited_permissions(role, permissions)

        # Cache permissions
        self.permission_cache[user_id] = permissions
        return permissions

    def _add_inherited_permissions(self, role: Role, permissions: Set[Permission]):
        """Recursively add inherited permissions."""
        if role.inherits_from:
            parent_role = self.roles.get(role.inherits_from)
            if parent_role:
                permissions.update(parent_role.permissions)
                self._add_inherited_permissions(parent_role, permissions)

    def has_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        user_permissions = self.get_user_permissions(user_id)

        # Check for admin full access
        if Permission.ADMIN_FULL_ACCESS in user_permissions:
            return True

        return permission in user_permissions

    def has_any_permission(self, user_id: str, permissions: List[Permission]) -> bool:
        """Check if user has any of the specified permissions."""
        user_permissions = self.get_user_permissions(user_id)
        return any(perm in user_permissions for perm in permissions)

    def has_all_permissions(self, user_id: str, permissions: List[Permission]) -> bool:
        """Check if user has all of the specified permissions."""
        user_permissions = self.get_user_permissions(user_id)
        return all(perm in user_permissions for perm in permissions)

    def get_user_roles(self, user_id: str) -> Set[str]:
        """Get all roles for a user."""
        if user_id not in self.users:
            return set()
        return self.users[user_id].roles.copy()

    def list_roles(self) -> Dict[str, Dict[str, Any]]:
        """List all roles with their information."""
        roles_info = {}
        for name, role in self.roles.items():
            roles_info[name] = {
                "name": role.name,
                "description": role.description,
                "permissions": [p.value for p in role.permissions],
                "inherits_from": role.inherits_from,
                "priority": role.priority
            }
        return roles_info

    def list_users(self) -> Dict[str, Dict[str, Any]]:
        """List all users with their roles and permissions."""
        users_info = {}
        for user_id, user in self.users.items():
            permissions = self.get_user_permissions(user_id)
            users_info[user_id] = {
                "username": user.username,
                "roles": list(user.roles),
                "permissions": [p.value for p in permissions],
                "custom_permissions": [p.value for p in (user.custom_permissions or set())]
            }
        return users_info

    def create_user(self, user_id: str, username: str, initial_role: Optional[str] = None) -> bool:
        """Create a new user."""
        if user_id in self.users:
            return False

        roles = {initial_role} if initial_role else set()
        self.users[user_id] = User(
            user_id=user_id,
            username=username,
            roles=roles
        )

        self.save_data()
        logger.info(f"User created: {username} ({user_id})")
        return True

    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        if user_id not in self.users:
            return False

        del self.users[user_id]
        self.save_data()
        self.permission_cache.pop(user_id, None)

        logger.info(f"User deleted: {user_id}")
        return True