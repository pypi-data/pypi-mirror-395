"""
Plugin Crash Isolation

Isolate plugin crashes to prevent system-wide failures.
"""

import asyncio
import sys
from typing import Dict, Any, Optional, Callable
import traceback

class PluginCrashIsolation:
    """Plugin crash isolation system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.isolation_enabled = config.get("enabled", True)
        self.crash_handlers: Dict[str, Callable] = {}
        self.crash_counts: Dict[str, int] = {}
        self.max_crashes = config.get("max_crashes", 5)

    def register_crash_handler(self, plugin_name: str, handler: Callable):
        """Register crash handler for plugin."""
        self.crash_handlers[plugin_name] = handler

    async def isolate_plugin_execution(self, plugin_name: str, func: Callable, *args, **kwargs):
        """Execute plugin function with crash isolation."""
        if not self.isolation_enabled:
            return await func(*args, **kwargs)

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await self.handle_plugin_crash(plugin_name, e, func.__name__)
            raise

    async def handle_plugin_crash(self, plugin_name: str, error: Exception, function_name: str):
        """Handle plugin crash."""
        self.crash_counts[plugin_name] = self.crash_counts.get(plugin_name, 0) + 1

        logger.error(f"Plugin {plugin_name} crashed in {function_name}: {error}")
        logger.error(traceback.format_exc())

        # Check if plugin should be disabled
        if self.crash_counts[plugin_name] >= self.max_crashes:
            logger.critical(f"Plugin {plugin_name} disabled due to excessive crashes")
            # Disable plugin logic would go here

        # Call custom crash handler
        if plugin_name in self.crash_handlers:
            try:
                await self.crash_handlers[plugin_name](error, function_name)
            except Exception as handler_error:
                logger.error(f"Crash handler error: {handler_error}")

    def get_crash_stats(self, plugin_name: str) -> Dict[str, Any]:
        """Get crash statistics for plugin."""
        return {
            "crash_count": self.crash_counts.get(plugin_name, 0),
            "max_crashes": self.max_crashes,
            "is_disabled": self.crash_counts.get(plugin_name, 0) >= self.max_crashes
        }