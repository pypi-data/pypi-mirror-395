"""Tests for performance monitoring."""

import asyncio
import time

import pytest

from sonora.performance import (
    AsyncProfiler,
    BackpressureController,
    PerformanceMonitor,
)


class TestPerformanceMonitor:
    """Test performance monitoring."""

    def test_timing_recording(self):
        """Test timing recording."""
        monitor = PerformanceMonitor()

        monitor.record_timing("test_operation", 0.5)
        monitor.record_timing("test_operation", 1.0)

        stats = monitor.get_stats()
        assert "test_operation_duration_avg" in stats
        assert stats["test_operation_duration_avg"] == 0.75

    def test_counter_increment(self):
        """Test counter incrementing."""
        monitor = PerformanceMonitor()

        monitor.increment_counter("requests")
        monitor.increment_counter("requests", 5)

        stats = monitor.get_stats()
        assert stats["counters"]["requests"] == 6

    def test_gauge_setting(self):
        """Test gauge values."""
        monitor = PerformanceMonitor()

        monitor.set_gauge("active_connections", 10)

        stats = monitor.get_stats()
        assert stats["gauges"]["active_connections"] == 10

    def test_histogram_recording(self):
        """Test histogram recording."""
        monitor = PerformanceMonitor()

        monitor.record_histogram("response_times", 0.1)
        monitor.record_histogram("response_times", 0.2)
        monitor.record_histogram("response_times", 0.3)

        stats = monitor.get_stats()
        assert "response_times_p50" in stats
        assert stats["response_times_p50"] == 0.2


class TestAsyncProfiler:
    """Test async profiling."""

    @pytest.mark.asyncio
    async def test_profile_async(self):
        """Test async profiling."""
        profiler = AsyncProfiler()

        async def dummy_coro():
            await asyncio.sleep(0.01)
            return "result"

        result = await profiler.profile_async("test_task", dummy_coro())
        assert result == "result"

        stats = profiler.get_task_stats()
        assert "test_task" in stats
        assert stats["test_task"]["count"] == 1

    def test_task_timing(self):
        """Test manual task timing."""
        profiler = AsyncProfiler()

        profiler.start_task("manual_task")
        time.sleep(0.01)  # Simulate work
        duration = profiler.end_task("manual_task")

        assert duration > 0
        assert duration < 0.1  # Should be quick

        stats = profiler.get_task_stats()
        assert "manual_task" in stats


class TestBackpressureController:
    """Test backpressure control."""

    @pytest.mark.asyncio
    async def test_backpressure_execution(self):
        """Test backpressure-controlled execution."""
        controller = BackpressureController(max_concurrent=2, queue_size=3)

        async def dummy_task():
            await asyncio.sleep(0.01)
            return "done"

        # Execute tasks
        results = await asyncio.gather(*[
            controller.execute(dummy_task()) for _ in range(3)
        ])

        assert len(results) == 3
        assert all(r == "done" for r in results)

    @pytest.mark.asyncio
    async def test_backpressure_dropping(self):
        """Test request dropping under backpressure."""
        controller = BackpressureController(max_concurrent=1, queue_size=1)

        async def slow_task():
            await asyncio.sleep(0.1)
            return "done"

        # Start a slow task
        task1 = asyncio.create_task(controller.execute(slow_task()))

        # Try to execute more tasks - some should be dropped
        results = []
        for _ in range(5):
            result = await controller.execute(slow_task())
            results.append(result)

        # Some results should be None (dropped)
        assert any(r is None for r in results)

        stats = controller.get_stats()
        assert stats["dropped"] > 0