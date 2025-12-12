"""
Plugin Marketplace Structure

Plugin discovery and installation from marketplace.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import aiohttp

class PluginMarketplace:
    """Plugin marketplace for discovery and installation."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.marketplace_url = config.get("marketplace_url", "https://api.pydiscobasepro.com/plugins")
        self.local_marketplace_dir = Path.home() / ".pydiscobasepro" / "marketplace"
        self.local_marketplace_dir.mkdir(exist_ok=True)

        self.available_plugins: Dict[str, Dict[str, Any]] = {}
        self.installed_plugins: Set[str] = set()

    async def refresh_catalog(self):
        """Refresh plugin catalog from marketplace."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.marketplace_url}/catalog") as response:
                    if response.status == 200:
                        self.available_plugins = await response.json()
                        self._save_local_catalog()
                    else:
                        self._load_local_catalog()
        except Exception:
            self._load_local_catalog()

    def _save_local_catalog(self):
        """Save catalog locally."""
        try:
            with open(self.local_marketplace_dir / "catalog.json", 'w') as f:
                json.dump(self.available_plugins, f, indent=2)
        except Exception:
            pass

    def _load_local_catalog(self):
        """Load catalog from local cache."""
        try:
            with open(self.local_marketplace_dir / "catalog.json", 'r') as f:
                self.available_plugins = json.load(f)
        except Exception:
            self.available_plugins = {}

    async def search_plugins(self, query: str) -> List[Dict[str, Any]]:
        """Search plugins in marketplace."""
        results = []
        query_lower = query.lower()

        for plugin_id, plugin_info in self.available_plugins.items():
            if (query_lower in plugin_id.lower() or
                query_lower in plugin_info.get("name", "").lower() or
                query_lower in plugin_info.get("description", "").lower()):
                results.append(plugin_info)

        return results

    async def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed plugin information."""
        return self.available_plugins.get(plugin_id)

    async def download_plugin(self, plugin_id: str, version: Optional[str] = None) -> Optional[Path]:
        """Download plugin from marketplace."""
        plugin_info = self.available_plugins.get(plugin_id)
        if not plugin_info:
            return None

        download_url = plugin_info.get("download_url")
        if not download_url:
            return None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status == 200:
                        content = await response.read()

                        plugin_file = self.local_marketplace_dir / f"{plugin_id}.py"
                        with open(plugin_file, 'wb') as f:
                            f.write(content)

                        return plugin_file
        except Exception:
            return None

    def get_installed_plugins(self) -> Set[str]:
        """Get list of installed plugins."""
        return self.installed_plugins.copy()

    def mark_plugin_installed(self, plugin_id: str):
        """Mark plugin as installed."""
        self.installed_plugins.add(plugin_id)

    def mark_plugin_uninstalled(self, plugin_id: str):
        """Mark plugin as uninstalled."""
        self.installed_plugins.discard(plugin_id)