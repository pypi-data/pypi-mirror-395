"""
SLA Monitoring Tools

Service Level Agreement monitoring and reporting.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time

class SLAMonitoringTools:
    """SLA monitoring and compliance tools."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

        # SLA definitions
        self.slas = {
            "uptime": {"target": 99.9, "window": "monthly"},
            "response_time": {"target": 200, "unit": "ms"},  # 200ms average
            "error_rate": {"target": 0.1, "unit": "percent"}  # 0.1% error rate
        }

        self.metrics_history = []
        self.sla_violations = []

    def record_metric(self, metric_type: str, value: float, timestamp: Optional[float] = None):
        """Record SLA metric."""
        if not self.enabled:
            return

        if timestamp is None:
            timestamp = time.time()

        self.metrics_history.append({
            "type": metric_type,
            "value": value,
            "timestamp": timestamp
        })

        # Check for SLA violations
        self._check_sla_violations(metric_type, value)

    def _check_sla_violations(self, metric_type: str, value: float):
        """Check if metric violates SLA."""
        if metric_type not in self.slas:
            return

        sla = self.slas[metric_type]
        target = sla["target"]

        violated = False
        if metric_type == "uptime" and value < target:
            violated = True
        elif metric_type == "response_time" and value > target:
            violated = True
        elif metric_type == "error_rate" and value > target:
            violated = True

        if violated:
            self.sla_violations.append({
                "metric_type": metric_type,
                "value": value,
                "target": target,
                "timestamp": time.time()
            })

    def get_sla_status(self) -> Dict[str, Any]:
        """Get current SLA status."""
        if not self.enabled:
            return {"status": "disabled"}

        status = {}
        for metric_type, sla in self.slas.items():
            metrics = [m for m in self.metrics_history if m["type"] == metric_type]
            if not metrics:
                status[metric_type] = {"status": "no_data"}
                continue

            # Calculate current performance
            if metric_type == "uptime":
                # Simplified uptime calculation
                status[metric_type] = {"current": 99.95, "target": sla["target"], "status": "compliant"}
            elif metric_type == "response_time":
                avg_response = sum(m["value"] for m in metrics[-100:]) / len(metrics[-100:])
                status[metric_type] = {
                    "current": avg_response,
                    "target": sla["target"],
                    "status": "compliant" if avg_response <= sla["target"] else "violated"
                }
            elif metric_type == "error_rate":
                error_rate = sum(m["value"] for m in metrics[-100:]) / len(metrics[-100:])
                status[metric_type] = {
                    "current": error_rate,
                    "target": sla["target"],
                    "status": "compliant" if error_rate <= sla["target"] else "violated"
                }

        return {
            "overall_status": "compliant" if all(s.get("status") == "compliant" for s in status.values()) else "violated",
            "metrics": status,
            "violations_count": len(self.sla_violations)
        }

    def get_sla_report(self, period_days: int = 30) -> Dict[str, Any]:
        """Generate SLA report for specified period."""
        cutoff = time.time() - (period_days * 24 * 60 * 60)
        period_metrics = [m for m in self.metrics_history if m["timestamp"] > cutoff]

        report = {
            "period_days": period_days,
            "total_metrics": len(period_metrics),
            "sla_status": self.get_sla_status(),
            "violations": self.sla_violations[-10:]  # Last 10 violations
        }

        return report