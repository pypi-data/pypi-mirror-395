import time
import threading

from qlcore.monitoring.metrics import (
    MetricsCollector,
    get_metrics,
    timed_operation,
    metric,
    reset_metrics,
)
from qlcore.monitoring.performance import PerformanceMonitor


def test_metrics_collector():
    """Test metrics collection."""
    metrics = MetricsCollector()

    # Test counter
    metrics.increment("fills")
    metrics.increment("fills")
    assert metrics.counters["fills"] == 2

    # Test timing
    metrics.record_timing("operation", 10.5)
    metrics.record_timing("operation", 20.3)
    assert len(metrics.timings["operation"]) == 2

    # Test gauge
    metrics.set_gauge("equity", 100000.0)
    assert metrics.gauges["equity"] == 100000.0

    # Get stats
    stats = metrics.get_stats()
    assert stats["counters"]["fills"] == 2
    assert "operation" in stats["timings"]
    assert stats["timings"]["operation"]["count"] == 2


def test_timed_operation():
    """Test timed operation context manager."""
    reset_metrics()
    metrics = get_metrics()

    with timed_operation("test_operation"):
        time.sleep(0.01)  # 10ms

    stats = metrics.get_stats()
    assert "test_operation" in stats["timings"]
    assert stats["timings"]["test_operation"]["count"] == 1
    assert stats["timings"]["test_operation"]["min"] >= 10  # At least 10ms


def test_metric_decorator():
    """Test metric decorator."""
    reset_metrics()
    metrics = get_metrics()

    @metric("decorated_func")
    def test_func():
        time.sleep(0.01)
        return 42

    result = test_func()
    assert result == 42

    stats = metrics.get_stats()
    assert "decorated_func" in stats["timings"]


def test_performance_monitor():
    """Test performance monitoring."""
    monitor = PerformanceMonitor()
    snapshot = monitor.get_snapshot()

    assert snapshot.timestamp > 0
    # memory_mb and cpu_percent may be None if psutil not installed
    if snapshot.memory_mb is not None:
        assert snapshot.memory_mb > 0


def test_metrics_thread_local():
    """Test that metrics are thread-local."""
    reset_metrics()

    results = {}

    def thread_work(thread_id):
        metrics = get_metrics()
        metrics.increment("counter")
        results[thread_id] = metrics.counters["counter"]

    threads = []
    for i in range(3):
        t = threading.Thread(target=thread_work, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Each thread should have its own counter
    assert all(count == 1 for count in results.values())
