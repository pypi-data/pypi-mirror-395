# Migration from Riffy

This guide helps you migrate from Riffy (JavaScript) to Sonora (Python).

## Key Differences

| Feature | Riffy | Sonora |
|---------|-------|--------|
| Language | JavaScript/TypeScript | Python |
| Lavalink Version | v3 & v4 | v3 & v4 |
| Async/Await | ✅ | ✅ |
| Type Safety | TypeScript optional | Full PEP 561 typing |
| Plugin System | Limited | Extensible |
| Queue Management | Basic | Advanced with history |
| Filters | Basic | Comprehensive DSP |

## Installation

```bash
# Riffy
npm install riffy

# Sonora
pip install py-sonora
```

## Basic Setup

### Riffy
```javascript
const { Riffy } = require("riffy");
const { Client } = require("discord.js");

const client = new Client();
const riffy = new Riffy(client, [
    {
        host: "127.0.0.1",
        port: 2333,
        password: "youshallnotpass"
    }
]);
```

### Sonora
```python
from sonora import SonoraClient
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
sonora = SonoraClient(
    lavalink_nodes=[{
        "host": "127.0.0.1",
        "port": 2333,
        "password": "youshallnotpass"
    }]
)
```

## Event Handling

### Riffy
```javascript
riffy.on("nodeConnect", (node) => {
    console.log(`Node ${node.name} connected`);
});

riffy.on("trackStart", (player, track) => {
    console.log(`Playing ${track.title}`);
});
```

### Sonora
```python
from sonora import event_manager, EventType

@event_manager.on(EventType.NODE_READY)
async def on_node_ready(event):
    print(f"Node connected: {event.data}")

@event_manager.on(EventType.TRACK_START)
async def on_track_start(event):
    track = event.data['track']
    print(f"Playing {track.title}")
```

## Player Operations

### Riffy
```javascript
// Create player
const player = riffy.createPlayer({
    guildId: message.guild.id,
    voiceChannel: message.member.voice.channel.id,
    textChannel: message.channel.id
});

// Play track
const resolve = await riffy.resolve({ query: "your song", source: "youtube" });
await player.play(resolve);

// Control playback
await player.pause();
await player.resume();
await player.stop();
await player.setVolume(50);
```

### Sonora
```python
# Get player (auto-created)
player = await sonora.get_player(ctx.guild.id)

# Connect to voice (usually handled by integration)
await player.connect(channel_id, session_id, token)

# Play track
track = await sonora.load_track("ytsearch:your song")
await player.play(track)

# Control playback
await player.pause()
await player.resume()
await player.stop()
await player.set_volume(50)
```

## Queue Management

### Riffy
```javascript
// Add to queue
await player.queue.add(resolve);

// Skip track
await player.skip();

// Clear queue
player.queue.clear();
```

### Sonora
```python
# Add to queue
player.queue.add(track)

# Skip with auto-playback
await player.skip()

# Advanced queue operations
player.queue.shuffle()
player.queue.move(0, 1)  # Move track from position 0 to 1
tracks = player.queue.get_view("history", limit=10)
```

## Filters and Effects

### Riffy
```javascript
// Basic filters
await player.filters.setEqualizer([
    { band: 0, gain: 0.5 },
    { band: 1, gain: 0.3 }
]);

await player.filters.setKaraoke(true);
```

### Sonora
```python
# Advanced filters
from sonora import Equalizer, Karaoke

eq = Equalizer()
eq.set_band(0, 0.5)
eq.set_band(1, 0.3)
player.filters.set_filter(eq)

karaoke = Karaoke()
player.filters.set_filter(karaoke)

# Apply and send to Lavalink
await player.set_filters()

# Presets
player.filters.nightcore()
player.filters.bass_boost("high")
```

## Search and Loading

### Riffy
```javascript
const resolve = await riffy.resolve({
    query: "your search",
    source: "youtube"
});
```

### Sonora
```python
# Direct loading
track = await sonora.load_track("ytsearch:your search")

# Or use plugins
from sonora.plugins import YouTubePlugin
youtube = YouTubePlugin()
results = await youtube.search("your search")
```

## Node Management

### Riffy
```javascript
const nodes = [
    { host: "node1", port: 2333, password: "pass1" },
    { host: "node2", port: 2333, password: "pass2" }
];

const riffy = new Riffy(client, nodes);
```

### Sonora
```python
# Same node configuration
nodes = [
    {"host": "node1", "port": 2333, "password": "pass1"},
    {"host": "node2", "port": 2333, "password": "pass2"}
]

sonora = SonoraClient(
    lavalink_nodes=nodes,
    node_pooling=True  # Automatic load balancing
)
```

## Error Handling

### Riffy
```javascript
riffy.on("trackError", (player, track, error) => {
    console.error(`Error playing ${track.title}: ${error.message}`);
});
```

### Sonora
```python
@event_manager.on(EventType.TRACK_EXCEPTION)
async def on_track_error(event):
    player = event.data['player']
    track = event.data['track']
    error = event.data['error']
    print(f"Error playing {track.title}: {error}")
```

## Discord Integration

### Riffy
```javascript
// Automatic voice handling
client.on("voiceStateUpdate", (oldState, newState) => {
    // Handled automatically by Riffy
});
```

### Sonora
```python
# Use integration helpers
from sonora.integrations import DiscordPyIntegration

integration = DiscordPyIntegration(bot, sonora)
integration.attach()  # Handles voice events automatically
```

## Configuration

### Riffy
```javascript
const riffy = new Riffy(client, nodes, {
    defaultSearchEngine: "youtube",
    sendWS: true
});
```

### Sonora
```python
sonora = SonoraClient(
    lavalink_nodes=nodes,
    node_pooling=True,
    reconnect_policy={
        "max_retries": 5,
        "backoff": "exponential"
    }
)
```

## Common Patterns Migration

### Command Handler (Riffy → Sonora)

**Riffy:**
```javascript
module.exports = {
    name: 'play',
    execute: async (message, args) => {
        const query = args.join(' ');
        const resolve = await riffy.resolve({ query, source: "youtube" });

        const player = riffy.createPlayer({
            guildId: message.guild.id,
            voiceChannel: message.member.voice.channel.id,
            textChannel: message.channel.id
        });

        await player.queue.add(resolve);
        await message.reply(`Added ${resolve.title} to queue`);
    }
};
```

**Sonora:**
```python
@bot.command()
async def play(ctx, *, query):
    player = await sonora.get_player(ctx.guild.id)

    track = await sonora.load_track(f"ytsearch:{query}")
    if not track:
        return await ctx.send("No results found!")

    player.queue.add(track)
    await ctx.send(f"🎵 Added **{track.title}** to queue")

    # Auto-play if nothing is playing
    if not player.queue.current:
        await player.skip()
```

## Performance Considerations

- **Sonora** uses asyncio throughout for better performance
- **Memory usage** is optimized with proper object pooling
- **Connection handling** includes automatic reconnection
- **Queue operations** are O(1) for most operations

## Need Help?

- Check the [API Reference](api.md) for detailed documentation
- Join our [Discord server](https://discord.gg/sonora)
- View [examples](../examples/) in the repository