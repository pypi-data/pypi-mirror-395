---
title: Monitoring & Metrics
description: Comprehensive monitoring and metrics for Sonora v1.2.7
---

# 📊 Monitoring & Metrics

Sonora v1.2.7 provides comprehensive monitoring capabilities to track performance, health, and usage patterns of your music bot infrastructure.

## Built-in Metrics

### Performance Metrics

```python
from sonora import performance_monitor

# Get current performance stats
stats = performance_monitor.get_stats()

print(f"Uptime: {stats['uptime']:.1f}s")
print(f"Total requests: {stats.get('counters', {}).get('requests', 0)}")
print(f"Active connections: {stats.get('gauges', {}).get('connections', 0)}")

# Average response times
for key, avg_time in stats.items():
    if key.endswith('_duration_avg'):
        operation = key.replace('_duration_avg', '')
        print(f"{operation}: {avg_time:.3f}s avg")
```

### System Metrics

```python
# Get system resource usage
system_stats = performance_monitor.get_system_stats()

print(f"CPU Usage: {system_stats['cpu_percent']:.1f}%")
print(f"Memory Usage: {system_stats['memory_mb']:.1f} MB")
print(f"Memory Percent: {system_stats['memory_percent']:.1f}%")
print(f"Active Threads: {system_stats['threads']}")
print(f"Open Files: {system_stats['open_files']}")
```

## Custom Metrics

### Counter Metrics

```python
# Track events
performance_monitor.increment_counter("tracks_played")
performance_monitor.increment_counter("tracks_skipped")
performance_monitor.increment_counter("user_commands", 5)

# Track errors
performance_monitor.increment_counter("connection_errors")
performance_monitor.increment_counter("timeout_errors")
```

### Timing Metrics

```python
import time

# Track operation duration
start_time = time.time()
await load_track("query")
duration = time.time() - start_time

performance_monitor.record_timing("track_load", duration)
```

### Gauge Metrics

```python
# Track current values
performance_monitor.set_gauge("active_guilds", 150)
performance_monitor.set_gauge("queued_tracks", 45)
performance_monitor.set_gauge("cpu_usage", 65.5)
```

## Real-time Monitoring

### Live Dashboard

```python
import asyncio
from sonora import performance_monitor

async def monitoring_dashboard():
    """Real-time monitoring dashboard"""
    while True:
        # Clear screen
        print("\033[2J\033[H")  # ANSI clear screen

        # Header
        print("🎵 Sonora Monitoring Dashboard")
        print("=" * 50)

        # Performance stats
        stats = performance_monitor.get_stats()
        system = performance_monitor.get_system_stats()

        print(f"⏱️  Uptime: {stats['uptime']:.1f}s")
        print(f"🖥️  CPU: {system['cpu_percent']:.1f}%")
        print(f"💾 Memory: {system['memory_mb']:.1f} MB")

        # Counters
        counters = stats.get('counters', {})
        if counters:
            print("\n📊 Counters:")
            for name, value in counters.items():
                print(f"  {name}: {value}")

        # Gauges
        gauges = stats.get('gauges', {})
        if gauges:
            print("\n📈 Gauges:")
            for name, value in gauges.items():
                print(f"  {name}: {value}")

        # Recent timings
        print("\n⏱️  Recent Operations:")
        for key, value in stats.items():
            if key.endswith('_duration_avg') and isinstance(value, (int, float)):
                operation = key.replace('_duration_avg', '')
                print(f"  {operation}: {value:.3f}s avg")

        await asyncio.sleep(5)  # Update every 5 seconds

# Start monitoring
asyncio.create_task(monitoring_dashboard())
```

## Health Checks

### Lavalink Health Monitoring

```python
from sonora import SonoraClient
import aiohttp
import asyncio

class HealthChecker:
    def __init__(self, client: SonoraClient):
        self.client = client
        self.last_check = 0
        self.check_interval = 60  # Check every minute
        self.failures = 0
        self.max_failures = 3

    async def check_lavalink_health(self) -> dict:
        """Check Lavalink node health"""
        results = {}

        for node in self.client.nodes:
            try:
                # Test connection
                start_time = time.time()
                # This would be a real health check
                # For now, simulate
                await asyncio.sleep(0.1)  # Simulate network call
                response_time = time.time() - start_time

                results[node.host] = {
                    "status": "healthy",
                    "response_time": response_time,
                    "connected": node.connected,
                    "players": len(node.players) if hasattr(node, 'players') else 0
                }

            except Exception as e:
                results[node.host] = {
                    "status": "unhealthy",
                    "error": str(e)
                }

        return results

    async def monitor_health(self):
        """Continuous health monitoring"""
        while True:
            try:
                health = await self.check_lavalink_health()

                unhealthy_nodes = [
                    node for node, status in health.items()
                    if status["status"] != "healthy"
                ]

                if unhealthy_nodes:
                    print(f"⚠️  Unhealthy nodes: {unhealthy_nodes}")
                    self.failures += 1

                    if self.failures >= self.max_failures:
                        print("🚨 Multiple health check failures - triggering alert")
                        await self.alert_admin(health)
                        self.failures = 0
                else:
                    self.failures = 0
                    print("✅ All nodes healthy")

            except Exception as e:
                print(f"Health check error: {e}")

            await asyncio.sleep(self.check_interval)

    async def alert_admin(self, health_status: dict):
        """Send alert to administrators"""
        # This would integrate with your alerting system
        # Email, Slack, Discord webhook, etc.
        print("🚨 ALERT: Lavalink health issues detected!")
        for node, status in health_status.items():
            print(f"  {node}: {status}")
```

## Event Monitoring

### Track Playback Events

```python
from sonora import event_manager, EventType

class PlaybackMonitor:
    def __init__(self):
        self.playback_stats = {
            "tracks_started": 0,
            "tracks_ended": 0,
            "tracks_skipped": 0,
            "total_playtime": 0,
            "errors": 0
        }
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Set up event monitoring"""

        @event_manager.on(EventType.TRACK_START)
        async def on_track_start(event):
            self.playback_stats["tracks_started"] += 1
            track = event.data.get("track")
            if track:
                print(f"🎵 Started: {track.title} by {track.author}")

        @event_manager.on(EventType.TRACK_END)
        async def on_track_end(event):
            self.playback_stats["tracks_ended"] += 1
            reason = event.data.get("reason", "unknown")
            track = event.data.get("track")

            if track and hasattr(track, 'length'):
                self.playback_stats["total_playtime"] += track.length / 1000  # Convert to seconds

            print(f"🏁 Track ended: {reason}")

        @event_manager.on(EventType.TRACK_EXCEPTION)
        async def on_track_error(event):
            self.playback_stats["errors"] += 1
            error = event.data.get("error")
            print(f"❌ Track error: {error}")

    def get_stats(self) -> dict:
        """Get playback statistics"""
        return self.playback_stats.copy()

    def reset_stats(self):
        """Reset statistics"""
        for key in self.playback_stats:
            self.playback_stats[key] = 0

# Global monitor
playback_monitor = PlaybackMonitor()
```

### Queue Monitoring

```python
class QueueMonitor:
    def __init__(self):
        self.queue_stats = {
            "tracks_added": 0,
            "tracks_removed": 0,
            "queue_cleared": 0,
            "shuffle_used": 0,
            "max_queue_size": 0
        }

    async def monitor_queue(self, player):
        """Monitor queue changes"""
        while True:
            queue_size = len(player.queue.upcoming)
            self.queue_stats["max_queue_size"] = max(
                self.queue_stats["max_queue_size"],
                queue_size
            )

            await asyncio.sleep(60)  # Check every minute

    def get_stats(self) -> dict:
        """Get queue statistics"""
        return self.queue_stats.copy()
```

## Performance Profiling

### Built-in Profiler

```python
from sonora import performance_profiler

# Start profiling
performance_profiler.start_profiling()

# Run your operations
await play_multiple_tracks()

# Stop and analyze
results = performance_profiler.stop_profiling()

print("=== Performance Profile ===")
print(f"Execution time: {results['execution_time']:.2f}s")
print(f"Peak memory: {results['memory_peak_mb']:.1f} MB")

print("\nTop functions by time:")
profile_lines = results['profile_stats'].split('\n')
for line in profile_lines[:10]:
    if line.strip() and not line.startswith(' '):
        print(f"  {line.strip()}")
```

### Custom Profiling

```python
import cProfile
import pstats
import io

class CustomProfiler:
    def __init__(self):
        self.profiler = None

    def start(self):
        """Start profiling"""
        self.profiler = cProfile.Profile()
        self.profiler.enable()

    def stop(self) -> dict:
        """Stop profiling and return results"""
        if not self.profiler:
            return {}

        self.profiler.disable()

        # Get stats
        s = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=s)
        stats.sort_stats('cumulative')
        stats.print_stats(20)

        return {
            "profile_output": s.getvalue(),
            "timestamp": time.time()
        }

# Usage
profiler = CustomProfiler()
profiler.start()

# Your code here
await some_operations()

results = profiler.stop()
print(results["profile_output"])
```

## Alerting & Notifications

### Threshold Alerts

```python
class AlertManager:
    def __init__(self):
        self.thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "error_rate": 5.0,  # errors per minute
            "response_time": 5.0  # seconds
        }
        self.alert_cooldown = 300  # 5 minutes between alerts

    async def check_thresholds(self):
        """Check if any metrics exceed thresholds"""
        stats = performance_monitor.get_stats()
        system = performance_monitor.get_system_stats()

        alerts = []

        # CPU alert
        if system['cpu_percent'] > self.thresholds['cpu_percent']:
            alerts.append(f"High CPU usage: {system['cpu_percent']:.1f}%")

        # Memory alert
        if system['memory_percent'] > self.thresholds['memory_percent']:
            alerts.append(f"High memory usage: {system['memory_percent']:.1f}%")

        # Error rate alert (simplified)
        errors = stats.get('counters', {}).get('errors', 0)
        uptime = stats.get('uptime', 1)
        error_rate = (errors / uptime) * 60  # errors per minute

        if error_rate > self.thresholds['error_rate']:
            alerts.append(f"High error rate: {error_rate:.1f} errors/min")

        # Send alerts if any
        if alerts:
            await self.send_alerts(alerts)

    async def send_alerts(self, alerts: list):
        """Send alerts to configured channels"""
        message = "🚨 Sonora Alert\n" + "\n".join(alerts)

        # Send to Discord webhook
        # Send email
        # Send to monitoring system
        print(message)

# Start monitoring
alert_manager = AlertManager()

async def alert_loop():
    while True:
        await alert_manager.check_thresholds()
        await asyncio.sleep(60)  # Check every minute

asyncio.create_task(alert_loop())
```

## Integration with Monitoring Systems

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Define metrics
tracks_played = Counter('sonora_tracks_played_total', 'Total tracks played')
active_guilds = Gauge('sonora_active_guilds', 'Number of active guilds')
track_load_time = Histogram('sonora_track_load_duration', 'Track load duration')

class PrometheusExporter:
    def __init__(self):
        self.setup_metrics()

    def setup_metrics(self):
        """Set up Prometheus metrics"""
        start_http_server(8000)  # Expose metrics on port 8000

    def update_metrics(self):
        """Update Prometheus metrics from Sonora stats"""
        stats = performance_monitor.get_stats()

        # Update counters
        tracks_played.inc(stats.get('counters', {}).get('tracks_played', 0))

        # Update gauges
        active_guilds.set(stats.get('gauges', {}).get('active_guilds', 0))

        # Update histograms (would need to collect timing data)
        # track_load_time.observe(duration)

# Usage
exporter = PrometheusExporter()

# Update metrics periodically
async def metrics_loop():
    while True:
        exporter.update_metrics()
        await asyncio.sleep(30)  # Update every 30 seconds

asyncio.create_task(metrics_loop())
```

### Grafana Dashboards

Create dashboards for visualizing Sonora metrics:

1. **System Metrics**: CPU, memory, disk usage
2. **Playback Stats**: Tracks played, skipped, errors
3. **Queue Metrics**: Queue size, add/remove rates
4. **Performance**: Response times, throughput
5. **Errors**: Error rates by type and time

### Log Aggregation

```python
import logging
from sonora.diagnostics import structured_logger

# Configure structured logging for ELK stack
structured_logger.enable()

# Set up JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": record.created,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)

        return json.dumps(log_entry)

# Configure logger
logger = logging.getLogger('sonora')
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Track started", extra={
    "extra_data": {
        "guild_id": 123,
        "track_title": "Example Song",
        "track_author": "Example Artist"
    }
})
```

This comprehensive monitoring guide enables you to track, analyze, and maintain the health and performance of your Sonora v1.2.7 deployment.