---
title: Examples & Use Cases
description: Real-world examples and use cases for Sonora v1.2.7
---

# 💡 Examples & Use Cases

This page showcases real-world examples and use cases for Sonora v1.2.7, demonstrating how to build powerful music applications.

## Basic Music Bot

### Simple Discord Music Bot

```python
import discord
from discord.ext import commands
from sonora import SonoraClient

class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!')
        self.sonora = SonoraClient([{
            "host": "127.0.0.1",
            "port": 2333,
            "password": "youshallnotpass"
        }])

    async def setup_hook(self):
        await self.sonora.start()

    async def close(self):
        await self.sonora.close()
        await super().close()

bot = MusicBot()

@bot.command()
async def play(ctx, *, query):
    """Play music from YouTube or other sources"""
    player = await bot.sonora.get_player(ctx.guild.id)

    # Join voice channel if not connected
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("You need to be in a voice channel!")

    # Load and play track
    track = await bot.sonora.load_track(f"ytsearch:{query}")
    if track:
        await player.play(track)
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{track.title}**\nby {track.author}",
            color=0x8b5cf6
        )
        embed.set_thumbnail(url=getattr(track, 'thumbnail', None))
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ No results found!")

@bot.command()
async def skip(ctx):
    """Skip current track"""
    player = await bot.sonora.get_player(ctx.guild.id)
    await player.skip()
    await ctx.send("⏭️ Skipped!")

@bot.command()
async def stop(ctx):
    """Stop playback and clear queue"""
    player = await bot.sonora.get_player(ctx.guild.id)
    await player.stop()
    player.queue.clear()
    await ctx.send("⏹️ Stopped and cleared queue!")

bot.run('YOUR_BOT_TOKEN')
```

## Advanced Music Bot with SDK

### Enterprise Music Bot

```python
import discord
from discord.ext import commands
from sonora import SonoraMusicBotSDK, snapshot_manager
import asyncio

class EnterpriseMusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=['!', '.'], intents=discord.Intents.all())
        self.sdk = SonoraMusicBotSDK([
            {"host": "127.0.0.1", "port": 2333, "password": "youshallnotpass"},
            {"host": "backup.lavalink.com", "port": 2333, "password": "backup_pass"}
        ])
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Set up event handlers for rich interactions"""
        from sonora import event_manager, EventType

        @event_manager.on(EventType.TRACK_START)
        async def on_track_start(event):
            guild_id = event.data['guild_id']
            track = event.data['track']

            # Find the guild's system channel or create a music channel
            guild = self.get_guild(guild_id)
            if guild:
                channel = discord.utils.get(guild.channels, name="music")
                if not channel:
                    # Try to find a general channel
                    channel = discord.utils.get(guild.channels, name="general")

                if channel:
                    embed = discord.Embed(
                        title="🎵 Now Playing",
                        description=f"**{track.title}**\nby {track.author}",
                        color=0x8b5cf6
                    )
                    embed.add_field(name="Duration", value=format_duration(track.length))
                    embed.set_thumbnail(url=getattr(track, 'thumbnail', None))
                    await channel.send(embed=embed)

        @event_manager.on(EventType.QUEUE_EMPTY)
        async def on_queue_empty(event):
            guild_id = event.data['guild_id']
            guild = self.get_guild(guild_id)
            if guild:
                channel = discord.utils.get(guild.channels, name="music")
                if channel:
                    embed = discord.Embed(
                        title="📭 Queue Empty",
                        description="Add more songs with `!play <query>`",
                        color=0xffa726
                    )
                    await channel.send(embed=embed)

    async def setup_hook(self):
        await self.sdk.start()
        # Start auto snapshots
        await snapshot_manager.start_auto_snapshot()

    async def close(self):
        await snapshot_manager.stop_auto_snapshot()
        await self.sdk.shutdown()
        await super().close()

bot = EnterpriseMusicBot()

@bot.command()
async def play(ctx, *, query):
    """Advanced play command with rich feedback"""
    result = await bot.sdk.execute_command(ctx.guild.id, "play", query)

    if "Added to queue" in result:
        embed = discord.Embed(
            title="📝 Added to Queue",
            description=result,
            color=0x4caf50
        )
    elif "Now playing" in result:
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=result,
            color=0x8b5cf6
        )
    else:
        embed = discord.Embed(
            title="❌ Error",
            description=result,
            color=0xf44336
        )

    await ctx.send(embed=embed)

@bot.command()
async def queue(ctx, page: int = 1):
    """Show paginated queue"""
    result = await bot.sdk.execute_command(ctx.guild.id, "queue")

    embed = discord.Embed(
        title="📋 Music Queue",
        description=result,
        color=0x2196f3
    )

    # Add queue statistics
    player = await bot.sdk.get_player(ctx.guild.id)
    embed.add_field(
        name="Queue Stats",
        value=f"Tracks: {len(player.queue.upcoming)}\nHistory: {len(player.queue.history)}",
        inline=True
    )

    await ctx.send(embed=embed)

@bot.command()
async def filters(ctx):
    """Show available audio filters"""
    embed = discord.Embed(
        title="🎛️ Audio Filters",
        description="Apply audio effects to your music",
        color=0x9c27b0
    )

    filters = {
        "bassboost": "Boost low frequencies",
        "nightcore": "Increase speed and pitch",
        "reverb": "Add echo effect",
        "karaoke": "Remove vocals",
        "tremolo": "Add volume modulation"
    }

    filter_list = "\n".join(f"`{name}` - {desc}" for name, desc in filters.items())
    embed.add_field(name="Available Filters", value=filter_list, inline=False)

    embed.add_field(
        name="Usage",
        value="`!filter bassboost`\n`!filter nightcore`\n`!filter reset`",
        inline=True
    )

    await ctx.send(embed=embed)

@bot.command()
async def filter(ctx, name: str):
    """Apply audio filter"""
    valid_filters = ["bassboost", "nightcore", "reverb", "karaoke", "tremolo", "reset"]

    if name not in valid_filters:
        return await ctx.send(f"❌ Invalid filter. Choose from: {', '.join(valid_filters)}")

    result = await bot.sdk.execute_command(ctx.guild.id, "filter", name)

    embed = discord.Embed(
        title="🎛️ Filter Applied" if name != "reset" else "🔄 Filters Reset",
        description=result,
        color=0x9c27b0 if name != "reset" else 0x607d8b
    )

    await ctx.send(embed=embed)

@bot.command()
async def save(ctx):
    """Save current session"""
    player = await bot.sdk.get_player(ctx.guild.id)
    snapshot = snapshot_manager.create_snapshot(player)
    filepath = snapshot_manager.save_snapshot(snapshot)

    embed = discord.Embed(
        title="💾 Session Saved",
        description=f"Session saved to `{filepath}`",
        color=0x4caf50
    )

    await ctx.send(embed=embed)

@bot.command()
async def load(ctx, filename: str):
    """Load saved session"""
    try:
        snapshot = snapshot_manager.load_snapshot(filename)
        player = await bot.sdk.get_player(ctx.guild.id)
        await snapshot_manager.restore_snapshot(snapshot, player)

        embed = discord.Embed(
            title="🔄 Session Restored",
            description=f"Session loaded from `{filename}`",
            color=0x4caf50
        )

        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Restore Failed",
            description=f"Could not restore session: {str(e)}",
            color=0xf44336
        )
        await ctx.send(embed=embed)

@bot.command()
async def stats(ctx):
    """Show bot statistics"""
    from sonora import performance_monitor

    stats = performance_monitor.get_stats()
    system = performance_monitor.get_system_stats()

    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=0x00bcd4
    )

    embed.add_field(
        name="System",
        value=f"CPU: {system['cpu_percent']:.1f}%\nMemory: {system['memory_mb']:.1f} MB",
        inline=True
    )

    embed.add_field(
        name="Uptime",
        value=f"{stats.get('uptime', 0):.1f}s",
        inline=True
    )

    counters = stats.get('counters', {})
    if counters:
        counter_text = "\n".join(f"{k}: {v}" for k, v in list(counters.items())[:5])
        embed.add_field(
            name="Counters",
            value=counter_text,
            inline=False
        )

    await ctx.send(embed=embed)

def format_duration(ms: int) -> str:
    """Format milliseconds to readable duration"""
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"

bot.run('YOUR_BOT_TOKEN')
```

## Voice Streaming Application

### Custom Audio Streamer

```python
import asyncio
import numpy as np
from sonora import SonoraVoiceSDK

class AudioStreamerApp:
    def __init__(self):
        self.voice_sdk = SonoraVoiceSDK([
            {"host": "127.0.0.1", "port": 2333, "password": "pass"}
        ], mode="streaming")

        self.is_streaming = False
        self.stream_task = None

    async def start(self):
        """Start the streaming application"""
        await self.voice_sdk.start()
        print("🎵 Audio streaming application started")

    async def connect_to_channel(self, guild_id: int, channel_id: int,
                                session_id: str, token: str):
        """Connect to a voice channel"""
        await self.voice_sdk.connect_voice(guild_id, channel_id, session_id, token)
        print(f"🔗 Connected to voice channel in guild {guild_id}")

    async def stream_sine_wave(self, guild_id: int, frequency: float = 440.0,
                              duration: float = 10.0):
        """Stream a sine wave"""
        if self.is_streaming:
            await self.stop_streaming()

        self.is_streaming = True
        print(f"🎵 Streaming {frequency}Hz sine wave for {duration}s")

        # Audio parameters
        sample_rate = 48000
        chunk_size = 960  # 20ms at 48kHz
        amplitude = 0.3

        start_time = asyncio.get_event_loop().time()

        try:
            while self.is_streaming:
                current_time = asyncio.get_event_loop().time()
                elapsed = current_time - start_time

                if elapsed >= duration:
                    break

                # Generate sine wave samples
                t = np.linspace(elapsed, elapsed + chunk_size/sample_rate, chunk_size)
                samples = amplitude * np.sin(2 * np.pi * frequency * t)

                # Convert to 16-bit PCM
                pcm_data = (samples * 32767).astype(np.int16).tobytes()

                # Send to voice
                await self.voice_sdk.stream_audio(guild_id, pcm_data)

                # Small delay to maintain timing
                await asyncio.sleep(chunk_size / sample_rate)

        finally:
            self.is_streaming = False
            print("🏁 Sine wave streaming completed")

    async def stream_file(self, guild_id: int, file_path: str):
        """Stream audio from file"""
        import wave

        if self.is_streaming:
            await self.stop_streaming()

        self.is_streaming = True
        print(f"🎵 Streaming file: {file_path}")

        try:
            with wave.open(file_path, 'rb') as wav_file:
                # Check format
                if wav_file.getsampwidth() != 2 or wav_file.getframerate() != 48000:
                    print("⚠️  Converting audio format...")
                    # Would need audio conversion here
                    pass

                chunk_size = 960  # 20ms chunks

                data = wav_file.readframes(chunk_size)
                while data and self.is_streaming:
                    await self.voice_sdk.stream_audio(guild_id, data)
                    data = wav_file.readframes(chunk_size)
                    await asyncio.sleep(0.02)  # 20ms delay

        except Exception as e:
            print(f"❌ Streaming error: {e}")
        finally:
            self.is_streaming = False
            print("🏁 File streaming completed")

    async def stop_streaming(self):
        """Stop current streaming"""
        self.is_streaming = False
        if self.stream_task and not self.stream_task.done():
            self.stream_task.cancel()
            try:
                await self.stream_task
            except asyncio.CancelledError:
                pass

    async def get_stats(self, guild_id: int):
        """Get streaming statistics"""
        return await self.voice_sdk.get_voice_stats(guild_id)

    async def disconnect(self, guild_id: int):
        """Disconnect from voice"""
        await self.voice_sdk.disconnect_voice(guild_id)

    async def shutdown(self):
        """Shutdown the application"""
        await self.stop_streaming()
        await self.voice_sdk.shutdown()

# Usage example
async def main():
    app = AudioStreamerApp()
    await app.start()

    # Connect to voice channel (would get these from Discord)
    guild_id = 123456789
    channel_id = 987654321
    session_id = "session_id_from_discord"
    token = "voice_token_from_discord"

    await app.connect_to_channel(guild_id, channel_id, session_id, token)

    # Stream a 440Hz sine wave for 5 seconds
    await app.stream_sine_wave(guild_id, frequency=440.0, duration=5.0)

    # Stream an audio file
    await app.stream_file(guild_id, "music.wav")

    await app.disconnect(guild_id)
    await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

## Testing & Development

### Offline Testing Setup

```python
import asyncio
from sonora import protocol_simulator, SonoraClient

async def test_music_bot_offline():
    """Test music bot functionality offline"""

    # Start simulator
    await protocol_simulator.start()

    # Create client
    client = SonoraClient([{
        "host": "127.0.0.1",
        "port": 2333,
        "password": "test"
    }])

    await client.start()

    # Test basic functionality
    player = await client.get_player(123)

    # Simulate track loading and playing
    from sonora import mock_factory
    track = mock_factory.create_mock_track("Test Song", "Test Artist")

    await player.play(track)
    assert player.current_track.title == "Test Song"

    # Test queue operations
    track2 = mock_factory.create_mock_track("Second Song", "Second Artist")
    await player.queue.add(track2)

    await player.skip()
    assert player.current_track.title == "Second Song"

    # Test filters
    player.filters.bass_boost("high")
    await player.set_filters()

    await client.close()
    await protocol_simulator.stop()

    print("✅ All offline tests passed!")

asyncio.run(test_music_bot_offline())
```

## Production Deployment

### Docker Compose Setup

```yaml
version: '3.8'

services:
  lavalink:
    image: fredboat/lavalink:4.0.1
    container_name: lavalink
    restart: unless-stopped
    ports:
      - "2333:2333"
    volumes:
      - ./lavalink/application.yml:/opt/Lavalink/application.yml
    environment:
      - JAVA_OPTS=-Xmx2G

  sonora-bot:
    build: .
    container_name: sonora-bot
    restart: unless-stopped
    depends_on:
      - lavalink
    environment:
      - SONORA_LAVALINK_HOST=lavalink
      - SONORA_LAVALINK_PORT=2333
      - SONORA_LAVALINK_PASSWORD=youshallnotpass
      - SONORA_ENCRYPTION_KEY=your-production-key
      - SONORA_MAX_CONCURRENT_REQUESTS=200
      - DISCORD_BOT_TOKEN=your-bot-token
    volumes:
      - ./snapshots:/app/snapshots
      - ./vault:/app/vault

networks:
  default:
    name: sonora-network
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sonora-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sonora-bot
  template:
    metadata:
      labels:
        app: sonora-bot
    spec:
      containers:
      - name: sonora
        image: code-xon/sonora:v1.2.7
        env:
        - name: SONORA_LAVALINK_HOST
          value: "lavalink-service"
        - name: SONORA_LAVALINK_PASSWORD
          valueFrom:
            secretKeyRef:
              name: lavalink-secret
              key: password
        - name: SONORA_ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: sonora-secret
              key: encryption-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import sonora; print('OK')"
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: snapshots
          mountPath: /app/snapshots
        - name: vault
          mountPath: /app/vault
      volumes:
      - name: snapshots
        persistentVolumeClaim:
          claimName: sonora-snapshots
      - name: vault
        secret:
          secretName: sonora-vault
```

These examples demonstrate the versatility and power of Sonora v1.2.7 for building everything from simple music bots to complex enterprise audio applications.