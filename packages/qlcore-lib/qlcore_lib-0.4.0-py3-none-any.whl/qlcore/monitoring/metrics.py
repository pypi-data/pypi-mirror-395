from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Dict, Any
from collections import defaultdict
from functools import wraps
import time
import threading

from ..utils.logging import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """Collect and aggregate performance metrics.

    Thread-safe metrics collection.
    """

    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
        self.timings: Dict[str, list[float]] = defaultdict(list)
        self.gauges: Dict[str, float] = {}
        self._lock = threading.Lock()

    def increment(self, metric: str, value: int = 1) -> None:
        """Increment a counter metric.

        Args:
            metric: Metric name
            value: Amount to increment by
        """
        with self._lock:
            self.counters[metric] += value

    def record_timing(self, metric: str, duration_ms: float) -> None:
        """Record a timing metric.

        Args:
            metric: Metric name
            duration_ms: Duration in milliseconds
        """
        with self._lock:
            self.timings[metric].append(duration_ms)

    def set_gauge(self, metric: str, value: float) -> None:
        """Set a gauge metric.

        Args:
            metric: Metric name
            value: Current value
        """
        with self._lock:
            self.gauges[metric] = value

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics.

        Returns:
            Dictionary of metric statistics
        """
        with self._lock:
            timing_stats: Dict[str, Dict[str, float | int]] = {}

            # Compute timing statistics
            for metric, timings in self.timings.items():
                if timings:
                    timing_stats[metric] = {
                        "count": len(timings),
                        "min": min(timings),
                        "max": max(timings),
                        "avg": sum(timings) / len(timings),
                        "total": sum(timings),
                    }

            stats: Dict[str, Any] = {
                "counters": dict(self.counters),
                "gauges": dict(self.gauges),
                "timings": timing_stats,
            }

            return stats

    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self.counters.clear()
            self.timings.clear()
            self.gauges.clear()


# Thread-local metrics collector
_local = threading.local()
_lock = threading.Lock()


def get_metrics() -> MetricsCollector:
    """Get the thread-local metrics collector."""
    if not hasattr(_local, "metrics"):
        _local.metrics = MetricsCollector()
    return _local.metrics


def reset_metrics() -> None:
    """Reset metrics for current thread (useful for testing)."""
    if hasattr(_local, "metrics"):
        _local.metrics.reset()


@contextmanager
def timed_operation(metric_name: str) -> Generator[None, None, None]:
    """Context manager for timing operations.

    Args:
        metric_name: Name of the metric

    Example:
        with timed_operation("portfolio_pnl"):
            pnl = calculate_portfolio_pnl(...)
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000  # Convert to ms
        get_metrics().record_timing(metric_name, elapsed)

        if elapsed > 1000:  # Log slow operations (>1s)
            logger.warning(
                "Slow operation detected", operation=metric_name, duration_ms=elapsed
            )


def metric(metric_name: str):
    """Decorator to automatically time a function.

    Args:
        metric_name: Name of the metric

    Example:
        @metric("calculate_pnl")
        def calculate_pnl(...):
            # ... implementation
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with timed_operation(metric_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator
