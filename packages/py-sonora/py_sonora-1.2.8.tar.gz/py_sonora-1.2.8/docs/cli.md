---
title: CLI Reference
description: Complete reference for Sonora's command-line interface
---

# 🖥️ CLI Reference

Sonora v1.2.7 provides a comprehensive command-line interface for development, debugging, and production management.

## Getting Started

```bash
# Show all available commands
sonoractl --help

# Get help for specific command
sonoractl <command> --help

# Use custom Lavalink connection
sonoractl --host 127.0.0.1 --port 2333 --password yourpass <command>
```

## Environment Commands

### `doctor` - Environment Diagnostics

Check your environment and dependencies for issues.

```bash
sonoractl doctor
```

**Output:**
```
🔍 Sonora Doctor - Environment Check
==================================================
✅ Python: 3.12.1
✅ aiohttp: installed
✅ pydantic: installed
✅ cryptography: installed (optional)
✅ psutil: installed (optional)
🔗 Lavalink: 127.0.0.1:2333
   Use 'sonoractl health-check' to test connection

✅ All checks passed!
```

**Checks Performed:**
- Python version compatibility
- Required package installation
- Optional dependency status
- Lavalink connection configuration

### `health-check` - Lavalink Health Check

Test connection to your Lavalink server.

```bash
sonoractl health-check
sonoractl health-check --host lavalink.example.com --port 2333
```

**Output:**
```
🔗 Testing Lavalink connection...
✅ Connection successful
📊 Lavalink v4.0.0
🎵 Loaded 1200 audio sources
⚡ Uptime: 2h 15m
```

**Tests Performed:**
- Network connectivity
- Authentication
- Lavalink version compatibility
- Audio source availability
- Server statistics

## Development Commands

### `debug` - Interactive Debug Monitor

Start an interactive debugging session.

```bash
sonoractl debug
```

**Features:**
- Real-time player monitoring
- Queue inspection
- Event logging
- Performance metrics
- Interactive commands

### `profile` - Performance Profiling

Profile Sonora's performance and memory usage.

```bash
sonoractl profile
```

**Output:**
```
📊 Sonora Performance Profile
==================================================
Execution time: 2.34s
Memory peak: 45.2 MB
Memory current: 32.1 MB

Top 5 most time-consuming functions:
  1. track_loading (0.456s)
  2. queue_processing (0.234s)
  3. filter_application (0.123s)
  4. network_operations (0.089s)
  5. event_dispatch (0.045s)
```

### `benchmark` - Performance Benchmarking

Run comprehensive performance benchmarks.

```bash
sonoractl benchmark
```

**Tests Performed:**
- Track loading throughput
- Queue operation performance
- Memory usage patterns
- Concurrent operation handling
- Network latency simulation

## Session Management

### `snapshot save` - Save Session State

Create a snapshot of current player state.

```bash
sonoractl snapshot save
```

**Output:**
```
📸 Session snapshot saved: guild_123_1703123456.json
💡 Use 'sonoractl snapshot list' to see all snapshots
```

### `snapshot list` - List Saved Snapshots

Show all available session snapshots.

```bash
sonoractl snapshot list
```

**Output:**
```
📁 Saved snapshots:
  • guild_123_1703123456.json (2 minutes ago)
  • guild_456_1703123400.json (5 minutes ago)
  • guild_789_1703123300.json (10 minutes ago)
```

### `snapshot restore` - Restore Session State

Restore player state from a snapshot.

```bash
sonoractl snapshot restore guild_123_1703123456.json
```

**Output:**
```
🔄 Restoring session from guild_123_1703123456.json...
✅ Session restored successfully
📊 Restored: 1 current track, 5 queued tracks, active filters
```

## Plugin Management

### `plugin list` - List Installed Plugins

Show all installed and available plugins.

```bash
sonoractl plugin list
```

**Output:**
```
🔌 Installed Plugins:
  ✅ YouTube (v2.1.0) - enabled
  ✅ Spotify (v1.8.3) - enabled
  ✅ SoundCloud (v1.5.2) - disabled
  ⚠️  Bandcamp (v0.9.1) - update available

Available Plugins:
  🆕 Tidal (v1.0.0)
  🆕 Deezer (v1.0.0)
```

### `plugin enable` - Enable Plugin

Enable a specific plugin.

```bash
sonoractl plugin enable spotify
```

**Output:**
```
🔌 Enabling plugin: spotify
✅ Plugin 'spotify' enabled successfully
🔄 Restarting plugin system...
```

### `plugin disable` - Disable Plugin

Disable a specific plugin.

```bash
sonoractl plugin disable bandcamp
```

**Output:**
```
🔌 Disabling plugin: bandcamp
✅ Plugin 'bandcamp' disabled successfully
```

### `plugin info` - Plugin Information

Show detailed information about a plugin.

```bash
sonoractl plugin info youtube
```

**Output:**
```
🔌 Plugin Information: YouTube
=====================================
Status: ✅ Enabled
Version: 2.1.0
Author: Sonora Team
Description: Official YouTube search and playback
Permissions: track.read, track.modify
Dependencies: None
Last Updated: 2024-12-01
Homepage: https://github.com/code-xon/sonora-youtube
```

## Autoplay Management

### `autoplay status` - Autoplay Status

Check current autoplay configuration and status.

```bash
sonoractl autoplay status
```

**Output:**
```
🎵 Autoplay Status
==================
Status: ✅ Enabled
Strategy: similar_artist
Fallback Playlist: global_fallback
Max History: 50 tracks
Smart Shuffle: ✅ Enabled
Recent Recommendations: 12
Success Rate: 94.2%
```

### `autoplay strategy` - Set Autoplay Strategy

Change the autoplay recommendation strategy.

```bash
sonoractl autoplay strategy similar_genre
```

**Available Strategies:**
- `similar_artist` - Recommend tracks by same artist
- `similar_genre` - Recommend tracks in similar genres
- `popularity` - Recommend popular tracks
- `random` - Random track selection

**Output:**
```
🎵 Changed autoplay strategy to: similar_genre
✅ Strategy updated successfully
```

## Queue Management

### `queue inspect` - Queue Inspection

Inspect the current queue state for a guild.

```bash
sonoractl queue inspect --guild-id 123456789
```

**Output:**
```
📋 Queue Inspection - Guild 123456789
======================================
Current Track:
  🎵 "Never Gonna Give You Up" by Rick Astley
  📊 Position: 1:23 / 3:32 (38%)
  🔊 Volume: 75%

Upcoming (5 tracks):
  1. "Take On Me" by a-ha
  2. "Billie Jean" by Michael Jackson
  3. "Sweet Child O' Mine" by Guns N' Roses
  4. "Livin' on a Prayer" by Bon Jovi
  5. "Wonderwall" by Oasis

History (3 tracks):
  • "Bohemian Rhapsody" by Queen
  • "Stairway to Heaven" by Led Zeppelin
  • "Hotel California" by Eagles

Queue Stats:
  📊 Total tracks: 8
  🔄 Loop mode: none
  🔀 Shuffle: disabled
  📈 Skip fatigue threshold: 3
  🎯 Smart features: enabled
```

## Wiretap Debugging

### `wiretap start` - Start Protocol Wiretap

Begin capturing Lavalink protocol packets for debugging.

```bash
sonoractl wiretap start
```

**Output:**
```
🎯 Starting Lavalink protocol wiretap...
📡 Capturing packets on all connections
💡 Use 'sonoractl wiretap stop' to stop and view captured packets
🔍 Real-time monitoring enabled
```

### `wiretap stop` - Stop Wiretap and Show Results

Stop packet capture and display captured packets.

```bash
sonoractl wiretap stop
```

**Output:**
```
🛑 Wiretap stopped
📦 Captured 47 packets (showing last 10):

  1. [OUT] play - {"track": "QAAA...", "guildId": "123"}
  2. [IN]  playerUpdate - {"guildId": "123", "state": {"position": 15000}}
  3. [OUT] volume - {"guildId": "123", "volume": 75}
  4. [IN]  playerUpdate - {"guildId": "123", "state": {"volume": 75}}
  5. [OUT] seek - {"guildId": "123", "position": 30000}
  6. [IN]  playerUpdate - {"guildId": "123", "state": {"position": 30000}}
  7. [OUT] filters - {"guildId": "123", "volume": 1.0, "equalizer": [...]}
  8. [IN]  playerUpdate - {"guildId": "123", "state": {"filters": {...}}}
  9. [OUT] pause - {"guildId": "123", "pause": true}
 10. [IN]  playerUpdate - {"guildId": "123", "state": {"paused": true}}
```

## Advanced Options

### Global Options

```bash
# Set custom Lavalink connection
sonoractl --host lavalink.example.com --port 2333 --password mypass command

# Set log level
sonoractl --log-level DEBUG command

# Use JSON output for scripting
sonoractl --json command
```

### Configuration Files

Create a configuration file for repeated use:

```bash
# Create .sonoractl config file
cat > .sonoractl << EOF
host=lavalink.example.com
port=2333
password=mypass
log_level=INFO
EOF

# CLI will automatically use these settings
sonoractl doctor
```

### Batch Operations

```bash
# Process multiple guilds
for guild_id in 123 456 789; do
  echo "Processing guild $guild_id..."
  sonoractl queue inspect --guild-id $guild_id
done

# Bulk plugin management
sonoractl plugin list | grep disabled | while read plugin; do
  sonoractl plugin enable "$plugin"
done
```

## Error Handling

### Common Error Messages

**Connection Failed:**
```
❌ Failed to connect to Lavalink
   Check that Lavalink is running and accessible
   Verify host, port, and password settings
```

**Plugin Not Found:**
```
❌ Plugin 'unknown' not found
   Use 'sonoractl plugin list' to see available plugins
```

**Snapshot Restore Failed:**
```
❌ Failed to restore snapshot
   Snapshot may be corrupted or from incompatible version
   Check snapshot file integrity
```

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
export SONORA_LOG_LEVEL=DEBUG
sonoractl --log-level DEBUG command
```

## Integration Examples

### Shell Scripts

```bash
#!/bin/bash
# Daily maintenance script

echo "🔍 Running daily Sonora maintenance..."

# Health check
if ! sonoractl health-check > /dev/null 2>&1; then
    echo "❌ Lavalink health check failed!"
    exit 1
fi

# Clean old snapshots (older than 7 days)
sonoractl snapshot list | grep "week" | while read snapshot; do
    rm ".sonora_snapshots/$snapshot"
done

# Update plugins
sonoractl plugin list | grep "update available" | while read plugin; do
    echo "Updating $plugin..."
    # Plugin update logic here
done

echo "✅ Maintenance completed successfully"
```

### Monitoring Integration

```bash
#!/bin/bash
# Nagios/Icinga compatible check

OUTPUT=$(sonoractl health-check 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "OK - $OUTPUT"
    exit 0
else
    echo "CRITICAL - $OUTPUT"
    exit 2
fi
```

### CI/CD Integration

```yaml
# .github/workflows/deploy.yml
- name: Health Check
  run: sonoractl health-check

- name: Performance Test
  run: sonoractl benchmark

- name: Create Deployment Snapshot
  run: sonoractl snapshot save
```

The Sonora CLI provides powerful tools for development, debugging, and production management of your music bot infrastructure.