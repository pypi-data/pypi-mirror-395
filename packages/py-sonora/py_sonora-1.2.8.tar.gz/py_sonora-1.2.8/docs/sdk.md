---
title: SDK Usage Guide
description: Using Sonora's high-level SDKs for rapid bot development
---

# 🛠 Sonora SDKs

Sonora v1.2.7 provides high-level SDKs designed to accelerate bot development while maintaining full access to advanced features.

## SonoraMusicBotSDK

The `SonoraMusicBotSDK` provides pre-built command handlers and utilities for music bot development.

### Basic Setup

```python
import discord
from discord.ext import commands
from sonora import SonoraMusicBotSDK

# Initialize SDK
sdk = SonoraMusicBotSDK([
    {"host": "127.0.0.1", "port": 2333, "password": "youshallnotpass"}
])

# Create bot
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    await sdk.start()
    print("🎵 Music bot ready!")

@bot.event
async def on_disconnect():
    await sdk.shutdown()
```

### Built-in Commands

The SDK comes with pre-implemented music commands:

#### Play Command

```python
@bot.command()
async def play(ctx, *, query):
    """Play music with smart autoplay"""
    result = await sdk.execute_command(ctx.guild.id, "play", query)
    await ctx.send(result)
```

**Features:**
- Automatic track resolution
- Queue management
- Smart autoplay integration
- Error handling

#### Queue Management

```python
@bot.command()
async def queue(ctx):
    """Display current queue"""
    result = await sdk.execute_command(ctx.guild.id, "queue")
    await ctx.send(result)

@bot.command()
async def skip(ctx):
    """Skip current track"""
    result = await sdk.execute_command(ctx.guild.id, "skip")
    await ctx.send(result)
```

#### Audio Filters

```python
@bot.command()
async def bassboost(ctx, level="medium"):
    """Apply bass boost filter"""
    result = await sdk.execute_command(ctx.guild.id, "filter", "bassboost", level)
    await ctx.send(result)

@bot.command()
async def nightcore(ctx):
    """Apply nightcore effect"""
    result = await sdk.execute_command(ctx.guild.id, "filter", "nightcore")
    await ctx.send(result)
```

### Custom Commands

Extend the SDK with custom commands:

```python
from sonora import MusicBotCommand

class ShuffleCommand(MusicBotCommand):
    def __init__(self):
        super().__init__("shuffle", "Shuffle the current queue")

    async def execute(self, player, **kwargs):
        """Shuffle queue implementation"""
        try:
            await player.queue.smart_shuffle()
            return f"🔀 Shuffled {len(player.queue.upcoming)} tracks"
        except Exception as e:
            return f"❌ Shuffle failed: {str(e)}"

class VolumeCommand(MusicBotCommand):
    def __init__(self):
        super().__init__("volume", "Set playback volume")

    async def execute(self, player, level=None, **kwargs):
        """Volume control implementation"""
        if level is None:
            return f"🔊 Current volume: {player.volume}%"

        try:
            new_volume = min(200, max(0, int(level)))
            player.volume = new_volume
            await player.set_volume(new_volume)
            return f"🔊 Volume set to {new_volume}%"
        except ValueError:
            return "❌ Invalid volume level. Use 0-200"

# Register custom commands
sdk.register_command(ShuffleCommand())
sdk.register_command(VolumeCommand())

# Use in Discord
@bot.command()
async def shuffle(ctx):
    result = await sdk.execute_command(ctx.guild.id, "shuffle")
    await ctx.send(result)

@bot.command()
async def volume(ctx, level=None):
    result = await sdk.execute_command(ctx.guild.id, "volume", level)
    await ctx.send(result)
```

### Advanced Features

#### Event Handling

```python
from sonora import event_manager, EventType

@event_manager.on(EventType.TRACK_START)
async def on_track_start(event):
    """Handle track start events"""
    guild_id = event.data['guild_id']
    track = event.data['track']

    # Get channel for this guild (you'll need to store this)
    channel = bot.get_channel(your_channel_id)
    if channel:
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{track.title}** by {track.author}",
            color=0x8b5cf6
        )
        embed.set_thumbnail(url=track.thumbnail)
        await channel.send(embed=embed)

@event_manager.on(EventType.QUEUE_EMPTY)
async def on_queue_empty(event):
    """Handle queue empty events"""
    guild_id = event.data['guild_id']
    # Could trigger autoplay or send notification
    pass
```

#### Error Handling

```python
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandInvokeError):
        # SDK command errors are handled by the SDK
        # But you can add custom error handling here
        await ctx.send(f"❌ An error occurred: {str(error)}")
```

## SonoraVoiceSDK

The `SonoraVoiceSDK` provides voice-only streaming capabilities for applications that don't need full music bot features.

### Voice Streaming Setup

```python
from sonora import SonoraVoiceSDK

# Initialize voice SDK
voice_sdk = SonoraVoiceSDK([
    {"host": "127.0.0.1", "port": 2333, "password": "pass"}
], mode="streaming")

await voice_sdk.start()
```

### Voice Connection Management

```python
# Connect to voice channel
await voice_sdk.connect_voice(
    guild_id=123456789,
    channel_id=987654321,
    session_id="session_id_here",
    token="voice_token_here"
)

# Get connection stats
stats = await voice_sdk.get_voice_stats(guild_id)
print(f"Connected: {stats['connected']}")
print(f"Ping: {stats['ping']}ms")

# Disconnect
await voice_sdk.disconnect_voice(guild_id)
```

### Custom Audio Streaming

```python
import asyncio
import wave
import audioop

class AudioStreamer:
    def __init__(self, voice_sdk, guild_id):
        self.voice_sdk = voice_sdk
        self.guild_id = guild_id
        self.is_streaming = False

    async def stream_file(self, file_path):
        """Stream audio file"""
        try:
            # Open WAV file
            with wave.open(file_path, 'rb') as wav_file:
                # Convert to PCM if needed
                if wav_file.getsampwidth() != 2:
                    # Convert to 16-bit PCM
                    pass

                # Read audio data in chunks
                chunk_size = 3840  # 20ms at 48kHz
                data = wav_file.readframes(chunk_size)

                while data and self.is_streaming:
                    # Convert stereo to mono if needed
                    if wav_file.getnchannels() == 2:
                        data = audioop.tomono(data, 2, 0.5, 0.5)

                    # Send to voice SDK
                    await self.voice_sdk.stream_audio(self.guild_id, data)

                    # Read next chunk
                    data = wav_file.readframes(chunk_size)
                    await asyncio.sleep(0.02)  # 20ms delay

        except Exception as e:
            print(f"Streaming error: {e}")

    async def start_streaming(self, file_path):
        """Start streaming"""
        self.is_streaming = True
        await self.stream_file(file_path)

    def stop_streaming(self):
        """Stop streaming"""
        self.is_streaming = False
```

### Voice Monitoring

```python
class VoiceMonitor:
    def __init__(self, voice_sdk):
        self.voice_sdk = voice_sdk
        self.monitoring = False

    async def start_monitoring(self, guild_id):
        """Monitor voice connection health"""
        self.monitoring = True

        while self.monitoring:
            try:
                stats = await self.voice_sdk.get_voice_stats(guild_id)

                if not stats['connected']:
                    print("Voice connection lost!")
                    # Attempt reconnection logic here
                else:
                    print(f"Voice stats: Ping {stats['ping']}ms, Volume {stats['volume']}%")

            except Exception as e:
                print(f"Monitoring error: {e}")

            await asyncio.sleep(30)  # Check every 30 seconds

    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
```

## Integration Examples

### Discord Music Bot

```python
import discord
from discord.ext import commands
from sonora import SonoraMusicBotSDK

class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.sdk = SonoraMusicBotSDK([
            {"host": "127.0.0.1", "port": 2333, "password": "pass"}
        ])

    async def setup_hook(self):
        await self.sdk.start()

    async def close(self):
        await self.sdk.shutdown()
        await super().close()

bot = MusicBot()

@bot.command()
async def play(ctx, *, query):
    result = await bot.sdk.execute_command(ctx.guild.id, "play", query)
    await ctx.send(result)

@bot.command()
async def queue(ctx):
    result = await bot.sdk.execute_command(ctx.guild.id, "queue")
    await ctx.send(result)

bot.run('YOUR_BOT_TOKEN')
```

### Voice Streaming Application

```python
import asyncio
from sonora import SonoraVoiceSDK

class VoiceStreamer:
    def __init__(self):
        self.voice_sdk = SonoraVoiceSDK([
            {"host": "127.0.0.1", "port": 2333, "password": "pass"}
        ], mode="streaming")

    async def run(self):
        await self.voice_sdk.start()

        # Connect to voice channel
        await self.voice_sdk.connect_voice(
            guild_id=123456789,
            channel_id=987654321,
            session_id="session_id",
            token="voice_token"
        )

        # Stream audio file
        await self.stream_audio_file("music.wav")

        # Monitor connection
        await self.monitor_connection(123456789)

    async def stream_audio_file(self, filename):
        """Stream audio file to voice channel"""
        # Implementation here
        pass

    async def monitor_connection(self, guild_id):
        """Monitor voice connection"""
        while True:
            stats = await self.voice_sdk.get_voice_stats(guild_id)
            print(f"Voice stats: {stats}")
            await asyncio.sleep(60)

# Run the streamer
streamer = VoiceStreamer()
asyncio.run(streamer.run())
```

## SDK Configuration

### Customizing SDK Behavior

```python
from sonora import SonoraMusicBotSDK

# Custom SDK configuration
sdk = SonoraMusicBotSDK(
    lavalink_nodes=[
        {
            "host": "127.0.0.1",
            "port": 2333,
            "password": "pass",
            "timeout": 30,
            "reconnect_delay": 5
        }
    ],
    # SDK-specific options
    default_volume=50,
    max_queue_size=1000,
    enable_autoplay=True,
    autoplay_strategy="similar_artist"
)

# Configure autoplay
autoplay = sdk.get_autoplay_engine(guild_id)
autoplay.configure({
    "enabled": True,
    "strategy": "similar_genre",
    "max_history": 50
})
```

### Error Handling

```python
# SDK includes built-in error handling
try:
    result = await sdk.execute_command(guild_id, "play", "invalid query")
    await ctx.send(result)
except Exception as e:
    # SDK handles most errors internally
    # Only critical errors bubble up
    await ctx.send(f"Critical error: {e}")
```

## Best Practices

### SDK Selection

- **Use SonoraMusicBotSDK** for full-featured music bots
- **Use SonoraVoiceSDK** for voice-only applications
- **Use core API directly** for maximum customization

### Performance Optimization

```python
# Configure SDK for performance
sdk = SonoraMusicBotSDK(
    lavalink_nodes=nodes,
    # Performance settings
    connection_pooling=True,
    compression=True,
    max_concurrent_requests=100
)

# Use efficient commands
@bot.command()
async def bulk_play(ctx, *queries):
    """Play multiple tracks efficiently"""
    results = []
    for query in queries[:5]:  # Limit to 5
        result = await sdk.execute_command(ctx.guild.id, "play", query)
        results.append(result)

    await ctx.send("\n".join(results))
```

### Error Recovery

```python
@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice connection issues"""
    if member == bot.user and after.channel is None:
        # Bot was disconnected from voice
        try:
            # Attempt reconnection using SDK
            await sdk.reconnect_voice(member.guild.id)
        except Exception as e:
            print(f"Reconnection failed: {e}")
```

The Sonora SDKs provide a perfect balance of ease-of-use and powerful features, allowing you to build sophisticated music applications quickly while maintaining access to all advanced capabilities.