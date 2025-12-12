"""Performance monitoring and profiling for Sonora v1.2.0."""

import asyncio
import time
from collections import defaultdict, deque
from typing import Any, Dict, List, Optional

import psutil


class PerformanceMonitor:
    """Monitor performance metrics for Sonora components."""

    def __init__(self):
        self.start_time = time.time()
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = defaultdict(list)

    def record_timing(self, operation: str, duration: float) -> None:
        """Record timing for an operation."""
        self.metrics[f"{operation}_duration"].append(duration)

    def increment_counter(self, name: str, value: int = 1) -> None:
        """Increment a counter."""
        self.counters[name] += value

    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge value."""
        self.gauges[name] = value

    def record_histogram(self, name: str, value: float) -> None:
        """Record a value in a histogram."""
        self.histograms[name].append(value)
        # Keep only recent values
        if len(self.histograms[name]) > 1000:
            self.histograms[name] = self.histograms[name][-1000:]

    def get_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        stats = {
            "uptime": time.time() - self.start_time,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
        }

        # Calculate averages for timing metrics
        for key, values in self.metrics.items():
            if values:
                stats[f"{key}_avg"] = sum(values) / len(values)
                stats[f"{key}_min"] = min(values)
                stats[f"{key}_max"] = max(values)
                stats[f"{key}_count"] = len(values)

        # Calculate percentiles for histograms
        for key, values in self.histograms.items():
            if values:
                sorted_values = sorted(values)
                n = len(sorted_values)
                stats[f"{key}_p50"] = sorted_values[n // 2]
                stats[f"{key}_p95"] = sorted_values[int(n * 0.95)]
                stats[f"{key}_p99"] = sorted_values[int(n * 0.99)]

        return stats

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-level performance statistics."""
        process = psutil.Process()
        return {
            "cpu_percent": process.cpu_percent(),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "memory_percent": process.memory_percent(),
            "threads": process.num_threads(),
            "open_files": len(process.open_files()),
        }


class AsyncProfiler:
    """Async-aware profiler for performance analysis."""

    def __init__(self):
        self.tasks: Dict[str, List[float]] = defaultdict(list)
        self.active_tasks: Dict[str, float] = {}

    async def profile_async(self, name: str, coro):
        """Profile an async coroutine."""
        start_time = time.time()
        try:
            result = await coro
            duration = time.time() - start_time
            self.tasks[name].append(duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            self.tasks[f"{name}_error"].append(duration)
            raise e

    def start_task(self, name: str) -> None:
        """Start timing a task."""
        self.active_tasks[name] = time.time()

    def end_task(self, name: str) -> float:
        """End timing a task and return duration."""
        if name in self.active_tasks:
            duration = time.time() - self.active_tasks[name]
            self.tasks[name].append(duration)
            del self.active_tasks[name]
            return duration
        return 0.0

    def get_task_stats(self) -> Dict[str, Any]:
        """Get statistics for profiled tasks."""
        stats = {}
        for task_name, durations in self.tasks.items():
            if durations:
                stats[task_name] = {
                    "count": len(durations),
                    "avg": sum(durations) / len(durations),
                    "min": min(durations),
                    "max": max(durations),
                    "total": sum(durations),
                }
        return stats


class BackpressureController:
    """Control backpressure in high-throughput scenarios."""

    def __init__(self, max_concurrent: int = 10, queue_size: int = 100):
        self.max_concurrent = max_concurrent
        self.queue_size = queue_size
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.queue: deque = deque(maxlen=queue_size)
        self.dropped_count = 0

    async def execute(self, coro):
        """Execute a coroutine with backpressure control."""
        # Check if we can acquire semaphore without blocking
        if self.semaphore._value <= 0:
            self.dropped_count += 1
            return None  # Drop request due to backpressure

        async with self.semaphore:
            try:
                result = await coro
                return result
            except Exception as e:
                # Re-raise exceptions
                raise e

    def get_stats(self) -> Dict[str, Any]:
        """Get backpressure statistics."""
        return {
            "active": self.max_concurrent - self.semaphore._value,
            "queued": len(self.queue),
            "dropped": self.dropped_count,
            "max_concurrent": self.max_concurrent,
            "queue_size": self.queue_size,
        }


# Global performance monitoring instances
performance_monitor = PerformanceMonitor()
async_profiler = AsyncProfiler()
backpressure_controller = BackpressureController()