"""
Plugin Permission Control

Fine-grained permission system for plugins.
"""

from typing import Dict, List, Set, Any
from enum import Enum

class PluginPermission(Enum):
    """Plugin permissions."""
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    NETWORK_ACCESS = "network.access"
    DATABASE_ACCESS = "database.access"
    SYSTEM_INFO = "system.info"
    PLUGIN_COMMUNICATE = "plugin.communicate"
    CONFIG_READ = "config.read"
    CONFIG_WRITE = "config.write"

class PluginPermissionControl:
    """Plugin permission management system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plugin_permissions: Dict[str, Set[PluginPermission]] = {}
        self.default_permissions = {
            PluginPermission.FILE_READ,
            PluginPermission.PLUGIN_COMMUNICATE
        }

    def grant_permission(self, plugin_name: str, permission: PluginPermission):
        """Grant permission to plugin."""
        if plugin_name not in self.plugin_permissions:
            self.plugin_permissions[plugin_name] = set(self.default_permissions)

        self.plugin_permissions[plugin_name].add(permission)

    def revoke_permission(self, plugin_name: str, permission: PluginPermission):
        """Revoke permission from plugin."""
        if plugin_name in self.plugin_permissions:
            self.plugin_permissions[plugin_name].discard(permission)

    def has_permission(self, plugin_name: str, permission: PluginPermission) -> bool:
        """Check if plugin has permission."""
        permissions = self.plugin_permissions.get(plugin_name, self.default_permissions)
        return permission in permissions

    def get_plugin_permissions(self, plugin_name: str) -> Set[PluginPermission]:
        """Get all permissions for plugin."""
        return self.plugin_permissions.get(plugin_name, self.default_permissions.copy())