"""
Plugin Version Pinning

Version management and compatibility for plugins.
"""

from typing import Dict, Any, Optional
import packaging.version

class PluginVersionPinning:
    """Plugin version pinning and compatibility management."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pinned_versions: Dict[str, str] = {}
        self.compatibility_matrix: Dict[str, Dict[str, bool]] = {}

    def pin_version(self, plugin_name: str, version: str):
        """Pin plugin to specific version."""
        self.pinned_versions[plugin_name] = version

    def unpin_version(self, plugin_name: str):
        """Unpin plugin version."""
        self.pinned_versions.pop(plugin_name, None)

    def get_pinned_version(self, plugin_name: str) -> Optional[str]:
        """Get pinned version for plugin."""
        return self.pinned_versions.get(plugin_name)

    def is_version_compatible(self, plugin_name: str, version: str) -> bool:
        """Check if version is compatible with pinned version."""
        pinned = self.get_pinned_version(plugin_name)
        if not pinned:
            return True

        try:
            return packaging.version.parse(version) >= packaging.version.parse(pinned)
        except Exception:
            return False

    def set_compatibility(self, plugin1: str, plugin2: str, compatible: bool):
        """Set compatibility between plugins."""
        if plugin1 not in self.compatibility_matrix:
            self.compatibility_matrix[plugin1] = {}
        self.compatibility_matrix[plugin1][plugin2] = compatible