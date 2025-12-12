---
title: Troubleshooting Guide
description: Common issues and solutions for Sonora v1.2.7
---

# 🔧 Troubleshooting Guide

This guide helps you diagnose and resolve common issues with Sonora v1.2.7.

## Quick Diagnosis

### Run Environment Check

```bash
sonoractl doctor
```

This command checks:
- Python version compatibility
- Required dependencies
- Optional features availability
- Lavalink connection configuration

### Check Lavalink Health

```bash
sonoractl health-check
```

Verifies:
- Network connectivity to Lavalink
- Authentication
- Lavalink version compatibility
- Audio source availability

## Connection Issues

### "Connection refused" Error

**Symptoms:**
```
ConnectionError: [Errno 111] Connection refused
LavalinkException: Failed to connect to Lavalink
```

**Solutions:**

1. **Check if Lavalink is running:**
   ```bash
   # If using Docker
   docker ps | grep lavalink

   # If running directly
   ps aux | grep lavalink
   ```

2. **Verify Lavalink configuration:**
   ```yaml
   # application.yml
   server:
     port: 2333
     address: 0.0.0.0
   lavalink:
     server:
       password: "youshallnotpass"
   ```

3. **Check firewall settings:**
   ```bash
   # Linux
   sudo ufw status
   sudo ufw allow 2333

   # Windows Firewall
   # Allow port 2333 in Windows Defender Firewall
   ```

4. **Test network connectivity:**
   ```bash
   telnet 127.0.0.1 2333
   nc -zv 127.0.0.1 2333
   ```

### Authentication Failed

**Symptoms:**
```
LavalinkException: Authentication failed
HTTP 401 Unauthorized
```

**Solutions:**

1. **Verify password in code:**
   ```python
   client = SonoraClient([{
       "host": "127.0.0.1",
       "port": 2333,
       "password": "youshallnotpass"  # Must match Lavalink config
   }])
   ```

2. **Check Lavalink password:**
   ```yaml
   lavalink:
     server:
       password: "youshallnotpass"
   ```

3. **Use environment variables:**
   ```bash
   export LAVALINK_PASSWORD="youshallnotpass"
   ```
   ```python
   import os
   password = os.getenv("LAVALINK_PASSWORD")
   ```

## Audio Playback Issues

### No Audio Plays

**Symptoms:**
- Bot joins voice channel but no sound
- Tracks appear to load but don't play
- Lavalink logs show successful operations

**Solutions:**

1. **Check voice permissions:**
   - Bot needs `Connect`, `Speak`, and `Use Voice Activity` permissions
   - Verify bot role hierarchy

2. **Verify voice region:**
   ```python
   # Check if bot and users are in same voice region
   voice_channel = ctx.author.voice.channel
   bot_voice_client = ctx.guild.voice_client

   print(f"User region: {voice_channel.rtc_region}")
   print(f"Bot region: {bot_voice_client.channel.rtc_region}")
   ```

3. **Test with different audio sources:**
   ```python
   # Try different URLs
   await player.play("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
   await player.play("https://example.com/audio.mp3")
   ```

4. **Check Lavalink audio sources:**
   ```yaml
   lavalink:
     server:
       sources:
         youtube: true
         soundcloud: true
         local: false
   ```

### Audio Distortion or Quality Issues

**Symptoms:**
- Audio sounds distorted or low quality
- Volume is inconsistent
- Filters cause audio artifacts

**Solutions:**

1. **Check audio encoding:**
   ```python
   # Ensure proper encoding
   player.filters.volume = 1.0  # Reset volume
   await player.set_filters()
   ```

2. **Verify Lavalink audio quality:**
   ```yaml
   lavalink:
     server:
       # Higher quality settings
       bufferDurationMs: 400
       frameBufferDurationMs: 1000
       opusEncodingQuality: 10
   ```

3. **Test without filters:**
   ```python
   # Temporarily disable all filters
   player.filters.reset()
   await player.set_filters()
   ```

## Bot Functionality Issues

### Commands Not Responding

**Symptoms:**
- Bot appears online but doesn't respond to commands
- Some commands work, others don't
- Intermittent responsiveness

**Solutions:**

1. **Check command registration:**
   ```python
   # Ensure commands are properly registered
   @bot.event
   async def on_ready():
       print(f"Logged in as {bot.user}")
       print(f"Commands loaded: {len(bot.commands)}")

   # Verify command names
   print([cmd.name for cmd in bot.commands])
   ```

2. **Check permissions:**
   ```python
   # Verify bot has necessary permissions
   permissions = ctx.guild.me.permissions_in(ctx.channel)
   if not permissions.send_messages:
       await ctx.author.send("I don't have permission to send messages here!")
   ```

3. **Test event handling:**
   ```python
   @bot.event
   async def on_command_error(ctx, error):
       print(f"Command error: {error}")
       await ctx.send(f"An error occurred: {error}")
   ```

### Queue Issues

**Symptoms:**
- Tracks not adding to queue
- Queue shows wrong information
- Skip doesn't work properly

**Solutions:**

1. **Check queue state:**
   ```python
   player = await client.get_player(ctx.guild.id)
   print(f"Queue length: {len(player.queue.upcoming)}")
   print(f"Current track: {player.current_track}")
   ```

2. **Verify track loading:**
   ```python
   track = await client.load_track("ytsearch:test song")
   if track:
       print(f"Track loaded: {track.title}")
       await player.queue.add(track)
   else:
       print("Track loading failed")
   ```

3. **Check for queue corruption:**
   ```python
   # Reset queue if corrupted
   player.queue._upcoming.clear()
   player.queue._history.clear()
   player.queue._current = None
   ```

## Performance Issues

### High CPU Usage

**Symptoms:**
- Bot consumes excessive CPU
- System becomes slow
- Other applications affected

**Solutions:**

1. **Profile performance:**
   ```bash
   sonoractl profile
   ```

2. **Check for infinite loops:**
   ```python
   # Add timeouts to operations
   try:
       await asyncio.wait_for(some_operation(), timeout=30.0)
   except asyncio.TimeoutError:
       print("Operation timed out")
   ```

3. **Optimize concurrent operations:**
   ```python
   # Use semaphores to limit concurrency
   semaphore = asyncio.Semaphore(10)

   async def limited_operation():
       async with semaphore:
           return await some_operation()
   ```

### High Memory Usage

**Symptoms:**
- Memory usage keeps growing
- Out of memory errors
- System becomes unstable

**Solutions:**

1. **Monitor memory usage:**
   ```python
   import psutil
   import os

   process = psutil.Process(os.getpid())
   memory_mb = process.memory_info().rss / 1024 / 1024
   print(f"Memory usage: {memory_mb:.1f} MB")
   ```

2. **Check for memory leaks:**
   ```python
   import gc
   gc.collect()  # Force garbage collection
   ```

3. **Limit queue sizes:**
   ```python
   # Set reasonable limits
   player.queue.max_history_size = 100
   player.queue.max_upcoming_size = 500
   ```

## Plugin Issues

### Plugin Not Loading

**Symptoms:**
- Plugin commands not available
- Plugin not listed in `sonoractl plugin list`
- Import errors in logs

**Solutions:**

1. **Check plugin installation:**
   ```bash
   sonoractl plugin list
   pip list | grep sonora
   ```

2. **Verify plugin compatibility:**
   ```python
   import sonora
   print(f"Sonora version: {sonora.__version__}")
   ```

3. **Check plugin logs:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)

   # Try loading plugin manually
   try:
       import sonora.plugins.youtube
       print("Plugin imported successfully")
   except Exception as e:
       print(f"Plugin import failed: {e}")
   ```

### Plugin Security Violations

**Symptoms:**
- Plugin blocked by firewall
- Security warnings in logs
- Plugin commands disabled

**Solutions:**

1. **Review plugin code:**
   ```python
   # Check for blocked operations
   blocked_functions = ['exec', 'eval', 'open', 'subprocess']
   # Plugin should not use these
   ```

2. **Adjust security settings:**
   ```python
   from sonora import plugin_security

   # Add allowed modules if needed
   plugin_security.allowed_modules.add('custom_module')
   ```

## Network Issues

### High Latency

**Symptoms:**
- Commands take long to respond
- Audio has noticeable delay
- Lavalink operations slow

**Solutions:**

1. **Check network latency:**
   ```bash
   ping lavalink-server.com
   traceroute lavalink-server.com
   ```

2. **Optimize Lavalink settings:**
   ```yaml
   lavalink:
     server:
       # Reduce buffer sizes for lower latency
       bufferDurationMs: 200
       frameBufferDurationMs: 500
   ```

3. **Use regional Lavalink servers:**
   ```python
   # Choose server closest to users
   nodes = [
       {"host": "us-east.lavalink.com", "region": "us-east"},
       {"host": "eu-west.lavalink.com", "region": "eu-west"},
   ]
   ```

## Debugging Tools

### Enable Debug Logging

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Sonora specific logging
sonora_logger = logging.getLogger('sonora')
sonora_logger.setLevel(logging.DEBUG)
```

### Wiretap Debugging

```bash
# Start wiretap to see Lavalink protocol
sonoractl wiretap start

# Perform operations...

# Stop and view captured packets
sonoractl wiretap stop
```

### Performance Profiling

```bash
# Profile performance
sonoractl profile

# Run benchmarks
sonoractl benchmark
```

## Common Error Messages

### "Track not found"
- Check if URL is valid
- Verify Lavalink has access to the source
- Try different search terms

### "Player not connected"
- Ensure bot is in voice channel
- Check voice permissions
- Verify Lavalink connection

### "Invalid track data"
- Lavalink may be having issues
- Try restarting Lavalink
- Check Lavalink logs

### "Queue is full"
- Implement queue limits
- Clear old tracks automatically
- Use fair queuing policies

## Getting Help

### Community Support

1. **Check existing issues:**
   ```bash
   # Search GitHub issues
   # https://github.com/code-xon/sonora/issues
   ```

2. **Gather diagnostic information:**
   ```bash
   # Run diagnostics
   sonoractl doctor
   sonoractl health-check

   # Get system information
   python -c "import sys; print(sys.version)"
   pip list | grep sonora
   ```

3. **Provide detailed bug reports:**
   - Sonora version
   - Python version
   - Lavalink version
   - Full error traceback
   - Steps to reproduce
   - Expected vs actual behavior

### Professional Support

For enterprise deployments and critical issues:

- **Enterprise Support:** enterprise@code-xon.fun
- **Security Issues:** security@code-xon.fun
- **Priority Response:** priority@code-xon.fun

This troubleshooting guide should help resolve most common issues. For persistent problems, don't hesitate to reach out to the community or file detailed bug reports.