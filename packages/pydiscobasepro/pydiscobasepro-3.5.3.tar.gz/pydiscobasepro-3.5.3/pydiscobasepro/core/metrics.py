"""
Core Metrics Engine

Comprehensive metrics collection, storage, and export functionality.
"""

import asyncio
import psutil
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import json

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class MetricsEngine:
    """Comprehensive metrics collection and management."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = self.config.get("enabled", True)
        self.metrics_history_file = Path.home() / ".pydiscobasepro" / "metrics_history.json"
        self.prometheus_port = self.config.get("prometheus_port", 9090)

        # Metrics storage
        self._metrics = {}
        self._start_time = time.time()
        self._collection_task = None

        # Prometheus integration
        self._prometheus_enabled = False
        if self.config.get("prometheus_enabled", False):
            self._setup_prometheus()

    def _setup_prometheus(self):
        """Setup Prometheus metrics export."""
        try:
            from prometheus_client import start_http_server, Gauge, Counter, Histogram

            # Define metrics
            self.cpu_gauge = Gauge('pydiscobasepro_cpu_percent', 'CPU usage percentage')
            self.memory_gauge = Gauge('pydiscobasepro_memory_percent', 'Memory usage percentage')
            self.commands_counter = Counter('pydiscobasepro_commands_total', 'Total commands executed')
            self.response_time_histogram = Histogram('pydiscobasepro_response_time_seconds', 'Command response times')

            start_http_server(self.prometheus_port)
            self._prometheus_enabled = True
            logger.info(f"Prometheus metrics server started on port {self.prometheus_port}")

        except ImportError:
            logger.warning("prometheus_client not installed, Prometheus export disabled")

    async def start(self):
        """Start metrics collection."""
        if not self.enabled:
            return

        self._collection_task = asyncio.create_task(self._collect_metrics_loop())
        logger.info("Metrics collection started")

    async def stop(self):
        """Stop metrics collection."""
        if self._collection_task:
            self._collection_task.cancel()
            try:
                await self._collection_task
            except asyncio.CancelledError:
                pass
        logger.info("Metrics collection stopped")

    async def _collect_metrics_loop(self):
        """Main metrics collection loop."""
        while True:
            try:
                await self._collect_system_metrics()
                await self._collect_bot_metrics()
                await self._save_metrics_history()

                # Update Prometheus if enabled
                if self._prometheus_enabled:
                    self._update_prometheus_metrics()

                await asyncio.sleep(60)  # Collect every minute

            except Exception as e:
                logger.error(f"Metrics collection error: {e}")
                await asyncio.sleep(60)

    async def _collect_system_metrics(self):
        """Collect system resource metrics."""
        try:
            # CPU
            self._metrics["cpu_percent"] = psutil.cpu_percent(interval=1)
            self._metrics["cpu_count"] = psutil.cpu_count()

            # Memory
            memory = psutil.virtual_memory()
            self._metrics["memory_percent"] = memory.percent
            self._metrics["memory_used_mb"] = memory.used / 1024 / 1024
            self._metrics["memory_total_mb"] = memory.total / 1024 / 1024

            # Disk
            disk = psutil.disk_usage('/')
            self._metrics["disk_percent"] = disk.percent
            self._metrics["disk_used_gb"] = disk.used / 1024 / 1024 / 1024
            self._metrics["disk_total_gb"] = disk.total / 1024 / 1024 / 1024

            # Network (basic)
            net = psutil.net_io_counters()
            self._metrics["network_bytes_sent"] = net.bytes_sent
            self._metrics["network_bytes_recv"] = net.bytes_recv

            # Process info
            process = psutil.Process()
            self._metrics["process_cpu_percent"] = process.cpu_percent()
            self._metrics["process_memory_mb"] = process.memory_info().rss / 1024 / 1024
            self._metrics["process_threads"] = process.num_threads()

        except Exception as e:
            logger.error(f"System metrics collection error: {e}")

    async def _collect_bot_metrics(self):
        """Collect bot-specific metrics."""
        try:
            # These would be populated by the bot instance
            self._metrics["uptime_seconds"] = time.time() - self._start_time
            self._metrics["total_guilds"] = getattr(self, '_bot_guilds', 0)
            self._metrics["total_users"] = getattr(self, '_bot_users', 0)
            self._metrics["active_sessions"] = getattr(self, '_active_sessions', 0)
            self._metrics["total_commands"] = getattr(self, '_total_commands', 0)
            self._metrics["commands_per_minute"] = getattr(self, '_commands_per_minute', 0)
            self._metrics["avg_response_time"] = getattr(self, '_avg_response_time', 0)
            self._metrics["errors_per_hour"] = getattr(self, '_errors_per_hour', 0)
            self._metrics["loaded_plugins"] = getattr(self, '_loaded_plugins', 0)

        except Exception as e:
            logger.error(f"Bot metrics collection error: {e}")

    def update_bot_metrics(self, **metrics):
        """Update bot-specific metrics from external sources."""
        for key, value in metrics.items():
            setattr(self, f"_{key}", value)

    async def _save_metrics_history(self):
        """Save metrics to history file."""
        try:
            # Load existing history
            history = []
            if self.metrics_history_file.exists():
                with open(self.metrics_history_file, 'r') as f:
                    history = json.load(f)

            # Add current metrics
            entry = {
                "timestamp": datetime.now().isoformat(),
                **self._metrics
            }
            history.append(entry)

            # Keep only last 1000 entries
            history = history[-1000:]

            # Save
            with open(self.metrics_history_file, 'w') as f:
                json.dump(history, f, indent=2)

        except Exception as e:
            logger.error(f"Metrics history save error: {e}")

    def _update_prometheus_metrics(self):
        """Update Prometheus metrics."""
        try:
            self.cpu_gauge.set(self._metrics.get("cpu_percent", 0))
            self.memory_gauge.set(self._metrics.get("memory_percent", 0))
            # Add more Prometheus updates as needed

        except Exception as e:
            logger.error(f"Prometheus update error: {e}")

    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        return self._metrics.copy()

    async def get_metrics_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get metrics history for specified hours."""
        try:
            if not self.metrics_history_file.exists():
                return []

            with open(self.metrics_history_file, 'r') as f:
                history = json.load(f)

            # Filter by time
            cutoff = datetime.now().timestamp() - (hours * 3600)
            return [
                entry for entry in history
                if datetime.fromisoformat(entry["timestamp"]).timestamp() > cutoff
            ]

        except Exception as e:
            logger.error(f"Metrics history retrieval error: {e}")
            return []

    async def export_metrics(self) -> Dict[str, Any]:
        """Export metrics data for external use."""
        return {
            "current": await self.get_current_metrics(),
            "history": await self.get_metrics_history(hours=24),
            "metadata": {
                "version": "3.0.0",
                "collection_interval": 60,
                "exported_at": datetime.now().isoformat()
            }
        }

    def get_health_score(self) -> float:
        """Calculate system health score based on metrics."""
        score = 100.0

        # CPU penalty
        cpu = self._metrics.get("cpu_percent", 0)
        if cpu > 80:
            score -= (cpu - 80) * 0.5

        # Memory penalty
        memory = self._metrics.get("memory_percent", 0)
        if memory > 80:
            score -= (memory - 80) * 0.5

        # Error rate penalty
        error_rate = self._metrics.get("errors_per_hour", 0)
        if error_rate > 10:
            score -= min(error_rate, 50) * 0.5

        return max(0.0, min(100.0, score))