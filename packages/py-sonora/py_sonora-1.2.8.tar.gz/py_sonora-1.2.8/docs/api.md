# API Reference

This page contains the complete API reference for Sonora.

## SonoraClient

The main client class for interacting with Sonora.

```python
from sonora import SonoraClient

client = SonoraClient(
    lavalink_nodes=[{
        "host": "127.0.0.1",
        "port": 2333,
        "password": "youshallnotpass"
    }],
    node_pooling=True,
    reconnect_policy={"max_retries": 5, "backoff": "exponential"}
)
```

### Methods

#### `async def start()`
Starts the client and connects to Lavalink nodes.

#### `async def close()`
Closes the client and disconnects from all nodes.

#### `async def get_player(guild_id: int) -> Player`
Gets or creates a player for the specified guild.

#### `async def load_track(query: str) -> Track | None`
Loads a track from Lavalink using the provided query.

---

## Player

Represents a per-guild music player with advanced queue management.

### Properties

- `guild_id: int` - The guild ID this player belongs to
- `queue: Queue` - The player's music queue
- `volume: int` - Current volume (0-100)
- `paused: bool` - Whether playback is paused
- `position: int` - Current playback position in milliseconds

### Methods

#### `async def connect(channel_id: int, session_id: str, token: str)`
Connects to a voice channel.

#### `async def disconnect()`
Disconnects from the voice channel.

#### `async def play(track: Track)`
Starts playing the specified track.

#### `async def pause()`
Pauses playback.

#### `async def resume()`
Resumes playback.

#### `async def stop()`
Stops playback and clears the current track.

#### `async def seek(position: int)`
Seeks to a specific position in the current track.

#### `async def set_volume(volume: int)`
Sets the player volume (0-100).

#### `async def skip() -> Track | None`
Skips to the next track in the queue.

#### `async def skip_to(position: int) -> Track | None`
Skips to a specific position in the queue.

---

## Queue

Advanced queue management with history and multiple views.

### Properties

- `current: Track | None` - Currently playing track
- `length: int` - Number of tracks in the queue
- `is_empty: bool` - Whether the queue is empty

### Methods

#### `add(track: Track, position: int | None = None)`
Adds a track to the queue.

#### `remove(position: int) -> Track`
Removes a track from the queue.

#### `clear()`
Clears all tracks from the queue.

#### `shuffle()`
Shuffles the queue.

#### `skip_to(position: int) -> Track`
Skips to a specific position in the queue.

#### `get_view(view_type: str, limit: int | None = None) -> List[Track]`
Gets a view of the queue (upcoming, history, all).

---

## Filters

Audio filters and effects for enhancing playback.

### Available Filters

#### Equalizer
15-band equalizer with gain control.

```python
from sonora import Equalizer

eq = Equalizer()
eq.set_band(0, 0.5)  # Boost bass
eq.set_band(14, -0.2)  # Cut treble
```

#### Karaoke
Vocal removal filter.

```python
from sonora import Karaoke

karaoke = Karaoke(level=1.0)
```

#### Timescale
Speed and pitch control.

```python
from sonora import Timescale

# Nightcore effect
nightcore = Timescale(speed=1.2, pitch=1.1)

# Vaporwave effect
vaporwave = Timescale(speed=0.8, pitch=1.1)
```

### Preset Filters

#### Bass Boost
```python
player.filters.bass_boost("high")  # low, medium, high
```

#### Nightcore
```python
player.filters.nightcore()
```

#### Vaporwave
```python
player.filters.vaporwave()
```

---

## Events

Sonora provides a comprehensive event system for tracking player state.

### Available Events

- `TRACK_START` - Fired when a track begins playing
- `TRACK_END` - Fired when a track ends
- `TRACK_EXCEPTION` - Fired when a track encounters an error
- `PLAYER_UPDATE` - Fired when player state changes
- `QUEUE_EMPTY` - Fired when the queue becomes empty
- `VOICE_UPDATE` - Fired when voice connection state changes

### Usage

```python
from sonora import event_manager, EventType

@event_manager.on(EventType.TRACK_START)
async def on_track_start(event):
    print(f"Now playing: {event.data['track'].title}")

# Or use async context manager
async with event_manager:
    # Events will be processed here
    pass
```

---

## Nodes

Lavalink node management and load balancing.

### Node Configuration

```python
node_config = {
    "host": "127.0.0.1",
    "port": 2333,
    "password": "youshallnotpass",
    "secure": False,  # Use wss:// for secure connections
    "region": "us-east"  # Optional region hint
}
```

### Node Pooling

Sonora supports automatic load balancing across multiple nodes:

```python
client = SonoraClient(
    lavalink_nodes=[
        {"host": "node1.example.com", "port": 2333, "password": "pass1"},
        {"host": "node2.example.com", "port": 2333, "password": "pass2"},
    ],
    node_pooling=True
)
```

---

## Plugins

Extend Sonora with custom search providers and DSP modules.

### Creating a Plugin

```python
from sonora.plugins import BasePlugin

class MyPlugin(BasePlugin):
    async def search(self, query: str) -> List[Track]:
        # Implement custom search logic
        pass

    async def load_track(self, url: str) -> Track | None:
        # Implement custom track loading
        pass
```

### Built-in Plugins

#### YouTube Plugin
```python
from sonora.plugins import YouTubePlugin

youtube = YouTubePlugin(api_key="your_youtube_api_key")
results = await youtube.search("your query")
```

---

## CLI Tools

Sonora includes command-line utilities for development and debugging.

### sonoractl

```bash
# Check environment
sonoractl doctor

# Health check Lavalink node
sonoractl health-check --host 127.0.0.1 --port 2333 --password yourpass

# Start debug monitor
sonoractl debug

# Generate bot template
sonoractl create-bot discord.py mybot

# Show metrics
sonoractl show-stats
```

---

## Exceptions

Sonora provides specific exception types for different error conditions.

- `SonoraError` - Base exception
- `LavalinkException` - Lavalink protocol errors
- `NodeException` - Node connection errors
- `PlayerException` - Player operation errors

---

# v1.2.7 Enterprise Features API

## 🔐 Security API

### CredentialVault

Enterprise-grade encrypted credential storage.

```python
from sonora import CredentialVault

# Create vault with master key
vault = CredentialVault(master_key="your-secure-key")

# Store encrypted credentials
vault.store_credential("lavalink_password", "secret123")
vault.store_credential("youtube_api_key", "api_key_here")

# Retrieve credentials
password = vault.retrieve_credential("lavalink_password")

# Rotate master key
vault.rotate_master_key("new-master-key")
```

### PluginFirewall

Advanced plugin execution security.

```python
from sonora import PluginFirewall

firewall = PluginFirewall()

# Validate plugin code
code = "import os; os.system('rm -rf /')"
issues = firewall.validate_code(code)
# Returns: ["Blocked function call: system"]

# Create secure execution environment
sandbox = firewall.create_sandbox()
# Returns restricted builtins dict
```

## 🛠 High-Level SDKs

### SonoraMusicBotSDK

Pre-built music bot commands and utilities.

```python
from sonora import SonoraMusicBotSDK

# Initialize SDK
sdk = SonoraMusicBotSDK([
    {"host": "127.0.0.1", "port": 2333, "password": "pass"}
])

await sdk.start()

# Execute commands
result = await sdk.execute_command(guild_id, "play", "Never Gonna Give You Up")
# Returns: "🎵 Now playing: Never Gonna Give You Up by Rick Astley"

result = await sdk.execute_command(guild_id, "queue")
# Returns formatted queue display

await sdk.shutdown()
```

### SonoraVoiceSDK

Voice-only streaming and monitoring.

```python
from sonora import SonoraVoiceSDK

# Initialize voice SDK
voice_sdk = SonoraVoiceSDK([
    {"host": "127.0.0.1", "port": 2333, "password": "pass"}
], mode="streaming")

await voice_sdk.start()

# Connect to voice channel
await voice_sdk.connect_voice(guild_id, channel_id, session_id, token)

# Get voice statistics
stats = await voice_sdk.get_voice_stats(guild_id)
# Returns: {"connected": True, "volume": 100, "ping": 45}

await voice_sdk.disconnect_voice(guild_id)
await voice_sdk.shutdown()
```

## 💾 Session Management

### SessionSnapshot

Complete state persistence and recovery.

```python
from sonora import SessionSnapshot, snapshot_manager

# Create snapshot of current player state
snapshot = snapshot_manager.create_snapshot(player)

# Save to file
filepath = snapshot_manager.save_snapshot(snapshot, "guild_123_backup.json")

# Load and restore
loaded_snapshot = snapshot_manager.load_snapshot(filepath)
await snapshot_manager.restore_snapshot(loaded_snapshot, player)
```

### SnapshotManager

Automated session management.

```python
from sonora import snapshot_manager

# Start automatic snapshots (every 5 minutes)
await snapshot_manager.start_auto_snapshot()

# List available snapshots
snapshots = snapshot_manager.list_snapshots(guild_id=123)

# Manual snapshot
snapshot = snapshot_manager.create_snapshot(player)
snapshot_manager.save_snapshot(snapshot)

# Cleanup
await snapshot_manager.stop_auto_snapshot()
```

## 🧪 Testing & Simulation

### ProtocolSimulator

Offline Lavalink protocol simulation.

```python
from sonora import protocol_simulator

# Start simulator
await protocol_simulator.start()

# Enable fault injection for testing
protocol_simulator.enable_fault_injection({
    "packet_loss": 0.05,      # 5% packet loss
    "latency_spike": 0.1,     # 10% latency spikes
    "connection_drop": 0.02   # 2% connection drops
})

# Use simulator like normal Lavalink node
# All operations work offline for testing

await protocol_simulator.stop()
```

### MockFactory

Deterministic test object generation.

```python
from sonora import mock_factory

# Create mock tracks
track1 = mock_factory.create_mock_track(
    title="Test Track",
    author="Test Artist",
    length=180000
)

# Create mock playlists
playlist = mock_factory.create_mock_playlist("Test Playlist", 5)

# Create search results
results = mock_factory.create_mock_search_results("test query", 10)
```

## 🔍 Diagnostics & Profiling

### PerformanceProfiler

Built-in performance analysis.

```python
from sonora import performance_profiler

# Start profiling
performance_profiler.start_profiling()

# Run your code...
await some_async_operation()

# Stop and get results
results = performance_profiler.stop_profiling()
print(f"Execution time: {results['execution_time']:.2f}s")
print(f"Memory peak: {results['memory_peak_mb']:.1f} MB")
print("Top functions:", results['profile_stats'])
```

### StructuredLogger

JSON logging for debugging.

```python
from sonora import structured_logger

# Enable structured logging
structured_logger.enable()

# Logs are now in JSON format
# Can be exported for analysis
logs = structured_logger.get_logs(event_type="track_start", limit=10)
structured_logger.export_logs("debug_logs.json")
```

### WiretapDebugger

Protocol-level debugging.

```python
from sonora import wiretap_debugger

# Start capturing packets
wiretap_debugger.enable()

# Run operations...
await player.play(track)

# Stop and inspect
wiretap_debugger.disable()
packets = wiretap_debugger.get_captured_packets(20)
for packet in packets:
    print(f"Operation: {packet.get('op')}, Data: {packet.get('data')}")
```

### PlayerIntrospector

Decision analysis and debugging.

```python
from sonora import player_introspector

# Logs are automatically recorded
decisions = player_introspector.get_decisions("autoplay_strategy", limit=5)

# Analyze patterns
analysis = player_introspector.analyze_decision_patterns()
print("Decision patterns:", analysis)
```

### PlaybackTimelineDebugger

Event timeline analysis.

```python
from sonora import timeline_debugger

# Events are automatically recorded
timeline = timeline_debugger.get_timeline(
    guild_id=123,
    event_types=["track_start", "track_end"],
    time_range=(time.time() - 3600, time.time())  # Last hour
)

# Generate report
report = timeline_debugger.generate_timeline_report(123)
print(f"Total events: {report['total_events']}")
print(f"Avg time between events: {report['avg_time_between_events']:.2f}s")
```

### ReproduciblePlaybackEngine

Session recording and replay.

```python
from sonora import playback_engine

# Start recording
playback_engine.start_recording("test_session_001")

# Run playback operations...
await player.play(track1)
await player.skip()
await player.play(track2)

# Stop recording
session_id = playback_engine.stop_recording()

# Replay session (for debugging)
await playback_engine.replay_session(session_id, speed=2.0)

# List sessions
sessions = playback_engine.list_sessions()
```

## ⚡ Performance Monitoring

### PerformanceMonitor

Real-time metrics collection.

```python
from sonora import performance_monitor

# Record custom metrics
performance_monitor.record_timing("track_load", 0.234)
performance_monitor.increment_counter("tracks_played")
performance_monitor.set_gauge("active_players", 15)

# Get current stats
stats = performance_monitor.get_stats()
print(f"Uptime: {stats['uptime']:.1f}s")
print(f"Counters: {stats['counters']}")

# System metrics
system_stats = performance_monitor.get_system_stats()
print(f"CPU: {system_stats['cpu_percent']:.1f}%")
print(f"Memory: {system_stats['memory_mb']:.1f} MB")
```

### AsyncProfiler

Async operation profiling.

```python
from sonora import async_profiler

# Profile async operations
result = await async_profiler.profile_async("load_track", load_track_operation())

# Get profiling stats
stats = async_profiler.get_task_stats()
for task_name, metrics in stats.items():
    print(f"{task_name}: {metrics['avg']:.3f}s avg, {metrics['count']} calls")
```

### BackpressureController

Load management and overload protection.

```python
from sonora import backpressure_controller

# Execute with backpressure control
result = await backpressure_controller.execute(some_heavy_operation())

# Check status
stats = backpressure_controller.get_stats()
print(f"Active: {stats['active']}, Queued: {stats['queued']}, Dropped: {stats['dropped']}")
```

## 🧬 Advanced Configuration

### Autoplay Configuration

```python
from sonora import AutoplayEngine

engine = AutoplayEngine(guild_id)
engine.configure({
    "enabled": True,
    "strategy": "similar_artist",
    "fallback_playlist": "global_fallback",
    "max_history": 50,
    "smart_shuffle": True
})

# Register custom strategies
engine.register_strategy("custom", CustomStrategy())
engine.register_scorer("custom", CustomScorer())
```

### Security Configuration

```python
from sonora import credential_manager, autoplay_security, plugin_security

# Configure credential vault
credential_manager.store_credential("lavalink", "secure_password")

# Configure autoplay security
autoplay_security.add_to_allowlist("youtube.com")
autoplay_security.add_to_denylist("badsite.com")

# Configure plugin security
plugin_security.allowed_modules.add("custom_module")
```

### Simulator Configuration

```python
from sonora import protocol_simulator

# Configure simulation parameters
protocol_simulator.node.latency = 25  # ms
protocol_simulator.node.jitter = 5    # ms
protocol_simulator.node.packet_loss = 0.001  # 0.1%

# Enable fault injection
protocol_simulator.enable_fault_injection({
    "packet_loss": 0.05,
    "latency_spike": 0.1,
    "connection_drop": 0.02
})
```

This comprehensive API reference covers all v1.2.7 enterprise features, providing developers with the tools needed to build secure, high-performance, and maintainable Discord music bots.
- `TrackException` - Track loading/search errors

---

## Configuration

### Environment Variables

- `LAVALINK_HOST` - Lavalink server host (default: 127.0.0.1)
- `LAVALINK_PORT` - Lavalink server port (default: 2333)
- `LAVALINK_PASSWORD` - Lavalink server password
- `DISCORD_TOKEN` - Discord bot token (for examples)

### Client Options

```python
client = SonoraClient(
    lavalink_nodes=[...],
    node_pooling=True,
    reconnect_policy={
        "max_retries": 5,
        "backoff": "exponential",
        "base_delay": 1.0,
        "max_delay": 60.0
    }
)
```