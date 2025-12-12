"""
Execution Timelines

Timeline tracking for operation execution.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import time

class ExecutionTimelines:
    """Execution timeline tracking system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.timelines: Dict[str, List[Dict[str, Any]]] = {}

    def start_operation(self, operation_id: str, operation: str):
        """Start tracking operation."""
        if not self.enabled:
            return

        if operation_id not in self.timelines:
            self.timelines[operation_id] = []

        self.timelines[operation_id].append({
            "operation": operation,
            "start_time": time.time(),
            "end_time": None,
            "duration": None,
            "status": "running"
        })

    def end_operation(self, operation_id: str, status: str = "completed"):
        """End tracking operation."""
        if not self.enabled or operation_id not in self.timelines:
            return

        timeline = self.timelines[operation_id]
        if timeline and timeline[-1]["end_time"] is None:
            timeline[-1]["end_time"] = time.time()
            timeline[-1]["duration"] = timeline[-1]["end_time"] - timeline[-1]["start_time"]
            timeline[-1]["status"] = status

    def get_timeline(self, operation_id: str) -> List[Dict[str, Any]]:
        """Get operation timeline."""
        return self.timelines.get(operation_id, [])

    def get_all_timelines(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all timelines."""
        return self.timelines.copy()