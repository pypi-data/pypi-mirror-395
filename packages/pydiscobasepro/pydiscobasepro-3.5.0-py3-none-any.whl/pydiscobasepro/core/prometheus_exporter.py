"""
Export Metrics to Prometheus

Prometheus metrics export functionality.
"""

from prometheus_client import Gauge, Counter, Histogram, start_http_server
from typing import Dict, Any, Optional

class PrometheusMetricsExporter:
    """Prometheus metrics exporter."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.port = config.get("port", 9090)

        self.metrics = {}

        if self.enabled:
            self._setup_metrics()
            start_http_server(self.port)

    def _setup_metrics(self):
        """Setup Prometheus metrics."""
        # System metrics
        self.cpu_gauge = Gauge('pydiscobasepro_cpu_percent', 'CPU usage percentage')
        self.memory_gauge = Gauge('pydiscobasepro_memory_percent', 'Memory usage percentage')
        self.disk_gauge = Gauge('pydiscobasepro_disk_percent', 'Disk usage percentage')

        # Bot metrics
        self.guilds_gauge = Gauge('pydiscobasepro_guilds_total', 'Total guilds')
        self.users_gauge = Gauge('pydiscobasepro_users_total', 'Total users')
        self.commands_counter = Counter('pydiscobasepro_commands_total', 'Total commands executed')

        # Performance metrics
        self.response_time_histogram = Histogram('pydiscobasepro_response_time_seconds', 'Command response times')

    def update_metrics(self, metrics: Dict[str, Any]):
        """Update Prometheus metrics."""
        if not self.enabled:
            return

        # Update gauges
        self.cpu_gauge.set(metrics.get("cpu_percent", 0))
        self.memory_gauge.set(metrics.get("memory_percent", 0))
        self.disk_gauge.set(metrics.get("disk_percent", 0))
        self.guilds_gauge.set(metrics.get("total_guilds", 0))
        self.users_gauge.set(metrics.get("total_users", 0))

    def increment_commands(self, count: int = 1):
        """Increment commands counter."""
        if self.enabled:
            self.commands_counter.inc(count)

    def observe_response_time(self, duration: float):
        """Observe response time."""
        if self.enabled:
            self.response_time_histogram.observe(duration)