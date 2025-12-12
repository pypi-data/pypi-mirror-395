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

- `SonoraException` - Base exception
- `LavalinkException` - Lavalink protocol errors
- `NodeException` - Node connection errors
- `PlayerException` - Player operation errors
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