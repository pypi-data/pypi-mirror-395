# 🚀 Quickstart Guide

Get up and running with Sonora MusicPy in just 5 minutes! This guide will walk you through creating your first Discord music bot.

## 📋 Prerequisites

Before we begin, make sure you have:

- **Python 3.11 or higher** installed
- **A Discord bot token** (create one at [Discord Developer Portal](https://discord.com/developers/applications))
- **Docker** (optional, for easy Lavalink setup)

## 📦 Installation

Install Sonora MusicPy using pip:

<div class="code-example">
```bash
pip install py-sonora
```
</div>

## 🎵 Setting up Lavalink

Sonora requires a Lavalink server to function. The easiest way is to use Docker:

### Option 1: Docker (Recommended)

<div class="code-example">
```bash
# Create a directory for Lavalink config
mkdir lavalink && cd lavalink

# Create application.yml
cat > application.yml << 'EOF'
server:
  port: 2333
  address: 0.0.0.0
lavalink:
  server:
    password: "youshallnotpass"
    sources:
      youtube: true
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      mixer: true
      http: true
      local: false
EOF

# Run Lavalink
docker run -d \
  --name lavalink \
  -p 2333:2333 \
  -v $(pwd)/application.yml:/opt/Lavalink/application.yml \
  fredboat/lavalink:4.0.1
```
</div>

### Option 2: Manual Download

1. Download Lavalink from [GitHub Releases](https://github.com/freyacodes/Lavalink/releases)
2. Create `application.yml` as shown above
3. Run: `java -jar Lavalink.jar`

## 🤖 Your First Bot

Create a file called `bot.py`:

<div class="code-example">
```python
import discord
from discord.ext import commands
from sonora import SonoraClient

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Sonora setup
sonora = SonoraClient(
    lavalink_nodes=[{
        "host": "127.0.0.1",
        "port": 2333,
        "password": "youshallnotpass"
    }]
)

@bot.event
async def on_ready():
    await sonora.start()
    print(f'🎵 {bot.user} is ready to play music!')

@bot.command()
async def join(ctx):
    """Join your voice channel"""
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await sonora.get_player(ctx.guild.id)
        await ctx.send("🎵 Joined voice channel!")
    else:
        await ctx.send("❌ You need to be in a voice channel!")

@bot.command()
async def play(ctx, *, query):
    """Play music from YouTube, SoundCloud, or direct URLs"""
    player = await sonora.get_player(ctx.guild.id)

    # Search and play
    track = await sonora.load_track(f"ytsearch:{query}")
    if track:
        await player.play(track)
        await ctx.send(f"🎵 Now playing: **{track.title}**")
    else:
        await ctx.send("❌ No results found!")

@bot.command()
async def pause(ctx):
    """Pause the current track"""
    player = await sonora.get_player(ctx.guild.id)
    await player.pause()
    await ctx.send("⏸️ Paused!")

@bot.command()
async def resume(ctx):
    """Resume playback"""
    player = await sonora.get_player(ctx.guild.id)
    await player.resume()
    await ctx.send("▶️ Resumed!")

@bot.command()
async def stop(ctx):
    """Stop playback and clear queue"""
    player = await sonora.get_player(ctx.guild.id)
    await player.stop()
    await ctx.send("⏹️ Stopped!")

@bot.command()
async def skip(ctx):
    """Skip to the next track"""
    player = await sonora.get_player(ctx.guild.id)
    next_track = await player.skip()
    if next_track:
        await ctx.send(f"⏭️ Skipped! Now playing: **{next_track.title}**")
    else:
        await ctx.send("📭 No more tracks in queue!")

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')
```
</div>

## ▶️ Running Your Bot

1. **Replace `YOUR_DISCORD_BOT_TOKEN`** with your actual bot token
2. **Start Lavalink** (if using Docker): `docker start lavalink`
3. **Run your bot**: `python bot.py`

## 🧪 Testing Your Bot

1. **Invite your bot** to a Discord server with the following permissions:
   - Send Messages
   - Use Voice Activity
   - Connect
   - Speak

2. **Join a voice channel** and try these commands:
   ```
   !join
   !play never gonna give you up
   !pause
   !resume
   !skip
   !stop
   ```

## 🎛️ Advanced Features

### Audio Filters

<div class="code-example">
```python
@bot.command()
async def bassboost(ctx, level: str = "medium"):
    """Apply bass boost filter"""
    player = await sonora.get_player(ctx.guild.id)
    player.filters.bass_boost(level)
    await player.set_filters()
    await ctx.send(f"🎛️ Applied {level} bass boost!")

@bot.command()
async def nightcore(ctx):
    """Apply nightcore effect"""
    player = await sonora.get_player(ctx.guild.id)
    player.filters.nightcore()
    await player.set_filters()
    await ctx.send("🌙 Nightcore mode activated!")
```
</div>

### Queue Management

<div class="code-example">
```python
@bot.command()
async def queue(ctx):
    """Show current queue"""
    player = await sonora.get_player(ctx.guild.id)

    if player.queue.current:
        embed = discord.Embed(title="🎵 Current Queue", color=0x667eea)

        # Current track
        embed.add_field(
            name="Now Playing",
            value=f"**{player.queue.current.title}**",
            inline=False
        )

        # Upcoming tracks
        upcoming = player.queue.get_view("upcoming", limit=5)
        if upcoming:
            queue_list = "\n".join(f"{i+1}. {track.title}" for i, track in enumerate(upcoming))
            embed.add_field(name="Up Next", value=queue_list, inline=False)

        embed.set_footer(text=f"Total tracks: {player.queue.length}")
        await ctx.send(embed=embed)
    else:
        await ctx.send("📭 Queue is empty!")
```
</div>

## 🔧 Troubleshooting

### Common Issues

**"Connection refused" error:**
- Make sure Lavalink is running on port 2333
- Check that the password matches your `application.yml`

**Bot doesn't respond:**
- Verify your bot token is correct
- Check that the bot has proper permissions in your server

**No audio plays:**
- Ensure the bot is in a voice channel
- Check Lavalink logs for errors

### Getting Help

- **📖 [API Reference](api.md)** - Complete documentation
- **🐛 [GitHub Issues](https://github.com/code-xon/sonora/issues)** - Report bugs
- **💬 [Discord Server](https://discord.gg/sonora)** - Community support
- **📧 Email**: [ramkrishna@code-xon.fun](mailto:ramkrishna@code-xon.fun)

## 🚀 v1.2.7 Enterprise Features

### High-Level SDK (Recommended)

<div class="code-example">
```python
from sonora import SonoraMusicBotSDK

# Replace basic client with enterprise SDK
sdk = SonoraMusicBotSDK([
    {"host": "127.0.0.1", "port": 2333, "password": "youshallnotpass"}
])

await sdk.start()

@bot.command()
async def play(ctx, *, query):
    """Smart play with autoplay"""
    result = await sdk.execute_command(ctx.guild.id, "play", query)
    await ctx.send(result)

@bot.command()
async def queue(ctx):
    """Intelligent queue display"""
    result = await sdk.execute_command(ctx.guild.id, "queue")
    await ctx.send(result)

@bot.command()
async def filter(ctx, name):
    """Apply smart filters"""
    result = await sdk.execute_command(ctx.guild.id, "filter", name)
    await ctx.send(result)
```
</div>

### Session Persistence

<div class="code-example">
```python
from sonora import snapshot_manager

@bot.command()
async def save(ctx):
    """Save current session"""
    player = await sonora.get_player(ctx.guild.id)
    snapshot = snapshot_manager.create_snapshot(player)
    filepath = snapshot_manager.save_snapshot(snapshot)
    await ctx.send(f"💾 Session saved: {filepath}")

@bot.command()
async def restore(ctx, filename):
    """Restore session"""
    player = await sonora.get_player(ctx.guild.id)
    try:
        snapshot = snapshot_manager.load_snapshot(filename)
        await snapshot_manager.restore_snapshot(snapshot, player)
        await ctx.send("🔄 Session restored!")
    except Exception as e:
        await ctx.send(f"❌ Restore failed: {e}")
```
</div>

### Enterprise Security

<div class="code-example">
```python
from sonora import credential_manager, autoplay_security

# Secure credential storage (one-time setup)
credential_manager.store_credential("lavalink_password", "your_secure_password")

# Autoplay security configuration
autoplay_security.add_to_allowlist("youtube.com")
autoplay_security.add_to_allowlist("soundcloud.com")

# All plugins are automatically sandboxed
```
</div>

### Performance Profiling

<div class="code-example">
```python
from sonora import performance_profiler

@bot.command()
async def profile_start(ctx):
    """Start performance profiling"""
    performance_profiler.start_profiling()
    await ctx.send("📊 Profiling started")

@bot.command()
async def profile_stop(ctx):
    """Stop profiling and show results"""
    results = performance_profiler.stop_profiling()

    embed = discord.Embed(title="Performance Profile")
    embed.add_field(name="Execution Time", value=f"{results['execution_time']:.2f}s")
    embed.add_field(name="Memory Peak", value=f"{results['memory_peak_mb']:.1f} MB")

    await ctx.send(embed=embed)
```
</div>

### CLI Power Tools

<div class="code-example">
```bash
# Environment diagnostics
sonoractl doctor

# Performance profiling
sonoractl profile

# Session management
sonoractl snapshot save
sonoractl snapshot list
sonoractl snapshot restore backup.json

# Protocol debugging
sonoractl wiretap start
sonoractl wiretap stop

# Benchmarking
sonoractl benchmark
```
</div>

## 🎯 Next Steps

Now that you have a working bot, explore:

- **[🎚️ Audio Filters](api.md#filters)** - Enhance audio quality
- **[📊 Queue Management](api.md#queue)** - Advanced queue features
- **[🔌 Plugins](api.md#plugins)** - Extend functionality
- **[📈 Monitoring](api.md#events)** - Track bot performance
- **[🌐 Multi-Node Setup](api.md#nodes)** - Scale your bot
- **[🔐 Enterprise Security](api.md#v127-enterprise-features-api)** - Advanced security features
- **[🛠 High-Level SDKs](api.md#high-level-sdks)** - Rapid development tools
- **[💾 Session Persistence](api.md#session-management)** - Crash recovery
- **[🧪 Testing Tools](api.md#testing--simulation)** - Offline simulation

Happy coding with Sonora v1.2.7! 🎵✨