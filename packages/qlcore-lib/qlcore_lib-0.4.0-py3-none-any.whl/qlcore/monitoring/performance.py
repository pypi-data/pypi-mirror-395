from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import time

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PerformanceSnapshot:
    """Snapshot of system performance metrics."""

    timestamp: float
    memory_mb: Optional[float]
    cpu_percent: Optional[float]

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "memory_mb": self.memory_mb,
            "cpu_percent": self.cpu_percent,
        }


class PerformanceMonitor:
    """Monitor system performance (optional, requires psutil)."""

    def __init__(self):
        self.has_psutil = False
        self.process = None

        try:
            import psutil

            self.has_psutil = True
            self.process = psutil.Process()
        except ImportError:
            logger.debug("psutil not available, performance monitoring disabled")

    def get_snapshot(self) -> PerformanceSnapshot:
        """Get current performance snapshot.

        Returns:
            Performance snapshot (memory/CPU may be None if psutil unavailable)
        """
        memory_mb = None
        cpu_percent = None

        if self.has_psutil and self.process:
            try:
                memory_info = self.process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB
                cpu_percent = self.process.cpu_percent(interval=0.1)
            except Exception as e:
                logger.debug("Failed to get performance metrics", error=str(e))

        return PerformanceSnapshot(
            timestamp=time.time(),
            memory_mb=memory_mb,
            cpu_percent=cpu_percent,
        )

    def log_snapshot(self) -> None:
        """Log current performance snapshot."""
        snapshot = self.get_snapshot()

        if snapshot.memory_mb is not None:
            logger.info(
                "Performance snapshot",
                memory_mb=snapshot.memory_mb,
                cpu_percent=snapshot.cpu_percent,
            )
        else:
            logger.debug("Performance monitoring unavailable (install psutil)")
