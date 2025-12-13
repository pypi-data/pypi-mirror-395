"""
Performance metrics collection.

Provides simple, low-overhead metrics tracking for ParquetFrame operations.
"""

import threading
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Metric:
    """A single metric data point."""

    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MetricsCollector:
    """
    Collects and aggregates performance metrics.

    Thread-safe singleton-like usage intended via global instance.
    """

    def __init__(self):
        self._metrics: list[Metric] = []
        self._lock = threading.Lock()
        self._enabled = True

    def enable(self):
        """Enable metrics collection."""
        self._enabled = True

    def disable(self):
        """Disable metrics collection."""
        self._enabled = False

    def record(self, name: str, value: float, **tags: Any):
        """
        Record a metric value.

        Args:
            name: Metric name
            value: Metric value
            **tags: Additional tags/labels
        """
        if not self._enabled:
            return

        # Convert tags to strings
        str_tags = {k: str(v) for k, v in tags.items()}

        metric = Metric(name=name, value=value, tags=str_tags)

        with self._lock:
            self._metrics.append(metric)

    @contextmanager
    def timer(self, name: str, **tags: Any):
        """
        Context manager to time a block of code.

        Args:
            name: Metric name for the duration
            **tags: Additional tags
        """
        start = time.perf_counter()
        try:
            yield
        finally:
            duration = time.perf_counter() - start
            self.record(name, duration, **tags)

    def get_summary(self) -> dict[str, dict[str, float]]:
        """
        Get summary statistics for collected metrics.

        Returns:
            Dict mapping metric names to stats (count, avg, min, max)
        """
        with self._lock:
            # Group by name
            grouped = defaultdict(list)
            for m in self._metrics:
                grouped[m.name].append(m.value)

        summary = {}
        for name, values in grouped.items():
            summary[name] = {
                "count": len(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "sum": sum(values),
            }

        return summary

    def clear(self):
        """Clear all collected metrics."""
        with self._lock:
            self._metrics.clear()


# Global instance
_global_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector."""
    return _global_collector


__all__ = ["MetricsCollector", "get_metrics_collector"]
