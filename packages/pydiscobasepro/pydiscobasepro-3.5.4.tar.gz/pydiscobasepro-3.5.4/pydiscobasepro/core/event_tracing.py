"""
Event Tracing System

Distributed tracing for events and operations.
"""

import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class TraceSpan:
    """Trace span for operations."""
    operation: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    tags: Dict[str, Any] = None
    parent_span: Optional['TraceSpan'] = None
    child_spans: List['TraceSpan'] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = {}
        if self.child_spans is None:
            self.child_spans = []

class EventTracingSystem:
    """Event tracing and distributed tracing system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.current_span: Optional[TraceSpan] = None
        self.completed_traces: List[TraceSpan] = []

    @contextmanager
    def trace_operation(self, operation: str, tags: Optional[Dict[str, Any]] = None):
        """Context manager for tracing operations."""
        if not self.enabled:
            yield
            return

        span = TraceSpan(
            operation=operation,
            start_time=time.time(),
            tags=tags or {},
            parent_span=self.current_span
        )

        if self.current_span:
            self.current_span.child_spans.append(span)

        old_span = self.current_span
        self.current_span = span

        try:
            yield span
        finally:
            span.end_time = time.time()
            span.duration = span.end_time - span.start_time
            self.current_span = old_span

            if not old_span:  # Root span completed
                self.completed_traces.append(span)

    def get_current_trace(self) -> Optional[TraceSpan]:
        """Get current active trace."""
        return self.current_span

    def get_trace_tree(self, span: TraceSpan) -> Dict[str, Any]:
        """Get trace tree structure."""
        return {
            "operation": span.operation,
            "duration": span.duration,
            "tags": span.tags,
            "children": [self.get_trace_tree(child) for child in span.child_spans]
        }