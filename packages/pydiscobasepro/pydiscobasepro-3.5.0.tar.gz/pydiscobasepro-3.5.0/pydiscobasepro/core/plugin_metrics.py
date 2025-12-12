"""
Plugin Metrics Tracking

Performance and usage metrics for plugins.
"""

import time
from typing import Dict, Any, Optional
from collections import defaultdict

class PluginMetricsTracker:
    """Plugin metrics tracking system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

        self.execution_times: Dict[str, list] = defaultdict(list)
        self.call_counts: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.memory_usage: Dict[str, list] = defaultdict(list)

    def track_execution(self, plugin_name: str, function_name: str, execution_time: float):
        """Track function execution."""
        if not self.enabled:
            return

        key = f"{plugin_name}.{function_name}"
        self.execution_times[key].append(execution_time)
        self.call_counts[key] += 1

        # Keep only last 100 measurements
        if len(self.execution_times[key]) > 100:
            self.execution_times[key].pop(0)

    def track_error(self, plugin_name: str, function_name: str):
        """Track function error."""
        if not self.enabled:
            return

        key = f"{plugin_name}.{function_name}"
        self.error_counts[key] += 1

    def get_metrics(self, plugin_name: str) -> Dict[str, Any]:
        """Get metrics for plugin."""
        if not self.enabled:
            return {}

        metrics = {}

        for key, times in self.execution_times.items():
            if key.startswith(f"{plugin_name}."):
                function_name = key.split('.', 1)[1]
                metrics[function_name] = {
                    "call_count": self.call_counts[key],
                    "error_count": self.error_counts[key],
                    "avg_execution_time": sum(times) / len(times) if times else 0,
                    "max_execution_time": max(times) if times else 0,
                    "min_execution_time": min(times) if times else 0
                }

        return metrics