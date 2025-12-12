---
title: Frequently Asked Questions
description: Answers to common questions about Sonora v1.2.7
---

# ❓ Frequently Asked Questions

Find answers to the most common questions about Sonora v1.2.7.

## Getting Started

### What is Sonora?

Sonora is a modern, enterprise-grade Python Lavalink client for building Discord music bots. It provides a high-performance, secure, and feature-rich foundation for music applications with advanced autoplay, intelligent queuing, and comprehensive monitoring capabilities.

### What's new in v1.2.7?

v1.2.7 is the "Advanced Feature Backport Release" that includes:

- **Enterprise Security**: AES-encrypted credentials, plugin sandboxing
- **High-Level SDKs**: SonoraMusicBotSDK and SonoraVoiceSDK
- **Session Management**: Complete state snapshots with crash recovery
- **Offline Simulation**: Full Lavalink protocol simulator for testing
- **Advanced Diagnostics**: Performance profiling, wiretap debugging
- **92% Test Coverage**: Comprehensive testing with fault injection

### How do I install Sonora?

```bash
pip install py-sonora
```

For development with all features:
```bash
pip install py-sonora[dev]
```

### What are the system requirements?

- **Python**: 3.11 or higher
- **Memory**: 256MB minimum, 1GB recommended
- **Disk**: 50MB for installation
- **Network**: Stable internet connection for Lavalink

## Lavalink Setup

### What is Lavalink?

Lavalink is a standalone audio sending node based on Lavaplayer. Sonora communicates with Lavalink to handle audio processing and streaming to Discord voice channels.

### How do I set up Lavalink?

1. **Download Lavalink**:
   ```bash
   wget https://github.com/freyacodes/Lavalink/releases/download/4.0.1/Lavalink.jar
   ```

2. **Create application.yml**:
   ```yaml
   server:
     port: 2333
     address: 0.0.0.0
   lavalink:
     server:
       password: "youshallnotpass"
       sources:
         youtube: true
         soundcloud: true
   ```

3. **Run Lavalink**:
   ```bash
   java -jar Lavalink.jar
   ```

### Can I use Docker?

Yes! The easiest way:

```bash
# Create application.yml as above
docker run --name lavalink \
  -p 2333:2333 \
  -v $(pwd)/application.yml:/opt/Lavalink/application.yml \
  fredboat/lavalink:4.0.1
```

### Why do I get "Connection refused"?

Common causes:
- Lavalink is not running
- Wrong host/port in your code
- Firewall blocking the connection
- Lavalink password mismatch

Check with:
```bash
sonoractl health-check --host 127.0.0.1 --port 2333
```

## Basic Usage

### How do I create a simple music bot?

```python
import discord
from discord.ext import commands
from sonora import SonoraClient

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    global sonora
    sonora = SonoraClient([{
        "host": "127.0.0.1",
        "port": 2333,
        "password": "youshallnotpass"
    }])
    await sonora.start()

@bot.command()
async def play(ctx, *, query):
    player = await sonora.get_player(ctx.guild.id)
    track = await sonora.load_track(f"ytsearch:{query}")
    if track:
        await player.play(track)
        await ctx.send(f"Now playing: {track.title}")

bot.run('YOUR_TOKEN')
```

### Why doesn't my bot play audio?

Check these:
1. Bot has `Connect` and `Speak` permissions
2. Bot is in a voice channel
3. Lavalink is running and accessible
4. Audio source is supported by Lavalink

### How do I add autoplay?

```python
from sonora import AutoplayEngine

# In your bot setup
autoplay = AutoplayEngine(guild_id)
autoplay.configure({
    "enabled": True,
    "strategy": "similar_artist"
})

# When queue empties
if len(player.queue.upcoming) == 0:
    track = await autoplay.fetch_next_track({
        "history": player.queue.history[-10:]
    })
    if track:
        await player.queue.add(track)
```

## Advanced Features

### How do I use the High-Level SDK?

```python
from sonora import SonoraMusicBotSDK

sdk = SonoraMusicBotSDK([{
    "host": "127.0.0.1",
    "port": 2333,
    "password": "youshallnotpass"
}])

await sdk.start()

# Use pre-built commands
result = await sdk.execute_command(guild_id, "play", "song name")
result = await sdk.execute_command(guild_id, "queue")
result = await sdk.execute_command(guild_id, "filter", "bassboost")
```

### What is session management?

Session snapshots allow you to save and restore the complete bot state:

```python
from sonora import snapshot_manager

# Save current state
player = await client.get_player(guild_id)
snapshot = snapshot_manager.create_snapshot(player)
snapshot_manager.save_snapshot(snapshot, "backup.json")

# Restore later
snapshot = snapshot_manager.load_snapshot("backup.json")
await snapshot_manager.restore_snapshot(snapshot, player)
```

### How do I enable security features?

```python
from sonora import credential_manager, plugin_security

# Encrypt sensitive data
credential_manager.store_credential("api_key", "secret_key")
encrypted_key = credential_manager.retrieve_credential("api_key")

# Configure plugin security
plugin_security.allowed_modules.add("requests")
plugin_security.blocked_functions.add("subprocess.call")
```

### What is offline testing?

Offline testing allows you to develop without Lavalink:

```python
from sonora import protocol_simulator, SonoraClient

await protocol_simulator.start()

client = SonoraClient([{"host": "127.0.0.1", "port": 2333, "password": "test"}])
await client.start()

# All operations work offline for testing
player = await client.get_player(123)
await player.play(mock_track)
```

## Performance & Scaling

### How many servers can Sonora handle?

Depends on:
- Hardware specifications
- Lavalink node configuration
- Concurrent audio streams
- Cache effectiveness

Typical limits:
- **Small bot**: 50-100 servers
- **Medium bot**: 500-1000 servers
- **Large bot**: 5000+ servers (with proper scaling)

### How do I optimize performance?

1. **Enable compression**:
   ```python
   client = SonoraClient(nodes, compression=True)
   ```

2. **Use connection pooling**:
   ```python
   client = SonoraClient(nodes, connection_pooling=True)
   ```

3. **Configure caching**:
   ```python
   autoplay.configure({"cache": {"enabled": True, "ttl": 3600}})
   ```

4. **Monitor resources**:
   ```bash
   sonoractl profile  # Performance profiling
   sonoractl benchmark  # Load testing
   ```

### What are the memory requirements?

- **Base usage**: ~50MB
- **Per active player**: ~2-5MB
- **Queue storage**: ~1MB per 100 tracks
- **Cache**: Configurable, default 100MB

## Troubleshooting

### Bot crashes with "MemoryError"

**Solutions**:
1. Reduce queue size limits
2. Enable garbage collection
3. Monitor memory usage
4. Restart bot periodically

### Audio quality is poor

**Check**:
1. Lavalink encoding quality settings
2. Network connection stability
3. Audio source quality
4. Filter configurations

### Commands are slow

**Optimize**:
1. Enable caching
2. Use connection pooling
3. Profile with `sonoractl profile`
4. Check Lavalink performance

### Plugin not working

**Debug**:
1. Check plugin logs
2. Verify compatibility
3. Test with `sonoractl plugin info <name>`
4. Enable security validation

## Security

### How secure is Sonora?

Sonora v1.2.7 includes enterprise-grade security:

- AES-256 encryption for credentials
- Plugin execution sandboxing
- Secure deserialization with type validation
- Runtime exploit prevention
- Audit logging and monitoring

### Should I encrypt my Lavalink password?

Yes! Use environment variables or the credential vault:

```bash
export SONORA_LAVALINK_PASSWORD="your_secure_password"
```

Or programmatically:
```python
from sonora import credential_manager
credential_manager.store_credential("lavalink_password", "secure_password")
```

## Plugins & Extensions

### How do I create a plugin?

```python
from sonora.plugins import BasePlugin

class MyPlugin(BasePlugin):
    async def search(self, query: str) -> List[Track]:
        # Implement search logic
        return []

    async def load_track(self, url: str) -> Track | None:
        # Implement track loading
        return None
```

### Where are plugins stored?

Default locations:
- `~/.sonora/plugins/`
- `./plugins/`
- Custom paths via configuration

### How do I install plugins?

```bash
# Copy plugin to plugins directory
cp my_plugin.py ~/.sonora/plugins/

# Restart bot or reload plugins
sonoractl plugin enable my_plugin
```

## Development

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### How do I run tests?

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sonora --cov-report=html

# Run specific tests
pytest tests/test_player.py

# Run offline tests
SONORA_OFFLINE_MODE=true pytest tests/
```

### How do I debug issues?

1. **Enable logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use CLI tools**:
   ```bash
   sonoractl debug          # Interactive debugger
   sonoractl wiretap start  # Protocol monitoring
   sonoractl profile        # Performance analysis
   ```

3. **Check health**:
   ```bash
   sonoractl doctor         # Environment check
   sonoractl health-check   # Lavalink status
   ```

## Enterprise & Production

### Can I use Sonora in production?

Yes! Sonora v1.2.7 is production-ready with:
- Enterprise security features
- Comprehensive monitoring
- High availability support
- Performance optimizations
- Professional support options

### What support is available?

- **Community**: Discord server and GitHub issues
- **Documentation**: Comprehensive guides and API reference
- **Enterprise**: Priority support and custom deployments

### How do I deploy to production?

Recommended approaches:

1. **Docker deployment**:
   ```yaml
   services:
     lavalink:
       image: fredboat/lavalink:4.0.1
     sonora-bot:
       image: code-xon/sonora:v1.2.7
       environment:
         - SONORA_ENCRYPTION_KEY=${ENCRYPTION_KEY}
   ```

2. **Kubernetes**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: sonora-bot
   spec:
     replicas: 3
     template:
       spec:
         containers:
         - name: sonora
           image: code-xon/sonora:v1.2.7
   ```

3. **Process manager** (PM2, systemd, etc.)

### How do I monitor production bots?

```python
# Enable comprehensive monitoring
from sonora import performance_monitor, structured_logger

performance_monitor.set_gauge("version", "1.2.7")
structured_logger.enable()

# Custom metrics
performance_monitor.increment_counter("guild_joins")
performance_monitor.record_timing("command_execution", execution_time)
```

Use external monitoring:
- **Prometheus**: Export metrics
- **Grafana**: Create dashboards
- **ELK Stack**: Centralized logging
- **Alerting**: Set up notifications

## Licensing & Legal

### What license does Sonora use?

Sonora is licensed under the **MIT License**, which allows:
- Commercial use
- Private use
- Modification
- Distribution

### Can I use Sonora commercially?

Yes! The MIT license allows commercial use without restrictions.

### Do I need to credit Sonora?

While not required by the license, attribution is appreciated. Consider mentioning Sonora in your project documentation or README.

## Getting Help

### Where can I get help?

1. **Documentation**: https://code-xon.github.io/sonora/
2. **GitHub Issues**: Report bugs and request features
3. **Discord Community**: Real-time help and discussions
4. **Stack Overflow**: Tag questions with `sonora` and `python`

### How do I report bugs?

1. **Check existing issues** on GitHub
2. **Gather information**:
   - Sonora version (`import sonora; sonora.__version__`)
   - Python version
   - Lavalink version
   - Full error traceback
   - Steps to reproduce
3. **Create a minimal reproduction case**
4. **Submit detailed bug report**

### How do I request features?

1. **Check existing issues** for similar requests
2. **Describe the problem** you're trying to solve
3. **Explain your use case** and requirements
4. **Suggest implementation** if possible
5. **Create feature request** on GitHub

This FAQ covers the most common questions. For additional help, join our Discord community or check the documentation.