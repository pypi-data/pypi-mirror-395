"""
Built-in System Metrics

Comprehensive system metrics collection.
"""

import psutil
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

class BuiltInSystemMetrics:
    """Built-in system metrics collection."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.collection_interval = config.get("interval", 60)

        self._metrics = {}
        self._start_time = datetime.now()

    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics."""
        if not self.enabled:
            return {}

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - self._start_time).total_seconds()
        }

        # CPU metrics
        cpu_metrics = await self._collect_cpu_metrics()
        metrics.update(cpu_metrics)

        # Memory metrics
        memory_metrics = await self._collect_memory_metrics()
        metrics.update(memory_metrics)

        # Disk metrics
        disk_metrics = await self._collect_disk_metrics()
        metrics.update(disk_metrics)

        # Network metrics
        network_metrics = await self._collect_network_metrics()
        metrics.update(network_metrics)

        # System info
        system_metrics = await self._collect_system_metrics()
        metrics.update(system_metrics)

        self._metrics = metrics
        return metrics

    async def _collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect CPU metrics."""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "cpu_freq_current": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "cpu_times": psutil.cpu_times()._asdict()
        }

    async def _collect_memory_metrics(self) -> Dict[str, Any]:
        """Collect memory metrics."""
        memory = psutil.virtual_memory()
        return {
            "memory_percent": memory.percent,
            "memory_used": memory.used,
            "memory_available": memory.available,
            "memory_total": memory.total
        }

    async def _collect_disk_metrics(self) -> Dict[str, Any]:
        """Collect disk metrics."""
        disk = psutil.disk_usage('/')
        return {
            "disk_percent": disk.percent,
            "disk_used": disk.used,
            "disk_free": disk.free,
            "disk_total": disk.total
        }

    async def _collect_network_metrics(self) -> Dict[str, Any]:
        """Collect network metrics."""
        net = psutil.net_io_counters()
        return {
            "network_bytes_sent": net.bytes_sent,
            "network_bytes_recv": net.bytes_recv,
            "network_packets_sent": net.packets_sent,
            "network_packets_recv": net.packets_recv
        }

    async def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect general system metrics."""
        return {
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
            "boot_time": psutil.boot_time(),
            "process_count": len(psutil.pids())
        }

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        return self._metrics.copy()

    async def get_metrics_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get metrics history (would need storage implementation)."""
        # Placeholder - would integrate with metrics storage
        return []