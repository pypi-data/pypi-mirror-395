---
title: Session Management
description: Complete session snapshots and restore functionality in Sonora v1.2.7
---

# 💾 Session Management

Sonora v1.2.7 provides comprehensive session management capabilities, allowing you to save and restore complete bot states across restarts and deployments.

## Overview

Session management includes:

- **Complete state snapshots** (player, queue, filters, autoplay)
- **Automatic background snapshots** with configurable intervals
- **Crash recovery** across application restarts
- **Deployment-safe persistence** for zero-downtime updates

## Basic Snapshot Operations

### Creating Snapshots

```python
from sonora import snapshot_manager

# Create snapshot of current player state
player = await client.get_player(guild_id)
snapshot = snapshot_manager.create_snapshot(player)

# Save to file
filepath = snapshot_manager.save_snapshot(snapshot, "guild_123_backup.json")
print(f"Snapshot saved: {filepath}")
```

### Restoring Sessions

```python
# Load snapshot from file
snapshot = snapshot_manager.load_snapshot("guild_123_backup.json")

# Restore to player
player = await client.get_player(guild_id)
await snapshot_manager.restore_snapshot(snapshot, player)
print("Session restored successfully")
```

## Automatic Snapshots

### Background Snapshot Service

```python
# Start automatic snapshots (every 5 minutes by default)
await snapshot_manager.start_auto_snapshot()

# Configure snapshot interval
snapshot_manager.auto_snapshot_interval = 300  # 5 minutes
snapshot_manager.max_snapshots_per_guild = 10  # Keep 10 snapshots per guild

# Stop automatic snapshots
await snapshot_manager.stop_auto_snapshot()
```

### Custom Snapshot Scheduling

```python
import asyncio

class SnapshotScheduler:
    def __init__(self, client, interval_minutes=5):
        self.client = client
        self.interval = interval_minutes * 60
        self.running = False

    async def start(self):
        """Start scheduled snapshots"""
        self.running = True
        while self.running:
            try:
                await self.create_all_snapshots()
            except Exception as e:
                print(f"Snapshot scheduling error: {e}")

            await asyncio.sleep(self.interval)

    async def create_all_snapshots(self):
        """Create snapshots for all active players"""
        for guild_id, player in self.client.players.items():
            try:
                snapshot = snapshot_manager.create_snapshot(player)
                snapshot_manager.save_snapshot(snapshot)
            except Exception as e:
                print(f"Failed to snapshot guild {guild_id}: {e}")

    def stop(self):
        """Stop scheduled snapshots"""
        self.running = False

# Usage
scheduler = SnapshotScheduler(client, interval_minutes=10)
await scheduler.start()
```

## Snapshot Contents

### Player State

```json
{
  "player": {
    "volume": 75,
    "paused": false,
    "position": 45000,
    "connected": true,
    "session_id": "session_123"
  }
}
```

### Queue State

```json
{
  "queue": {
    "current": {
      "title": "Never Gonna Give You Up",
      "author": "Rick Astley",
      "uri": "https://youtube.com/watch?v=dQw4w9WgXcQ",
      "length": 213000,
      "position": 45000
    },
    "upcoming": [
      {
        "title": "Track 2",
        "author": "Artist 2",
        "length": 180000
      }
    ],
    "history": [
      {
        "title": "Previous Track",
        "author": "Previous Artist",
        "length": 240000
      }
    ],
    "loop_mode": "none",
    "shuffle_enabled": false
  }
}
```

### Filter State

```json
{
  "filters": {
    "active_filters": ["bassboost", "nightcore"],
    "filter_config": {
      "equalizer": [
        {"band": 0, "gain": 0.5},
        {"band": 14, "gain": -0.2}
      ],
      "timescale": {
        "speed": 1.2,
        "pitch": 1.1
      }
    }
  }
}
```

### Autoplay State

```json
{
  "autoplay": {
    "enabled": true,
    "strategy": "similar_artist",
    "fallback_playlist": "global_fallback",
    "max_history": 50,
    "smart_shuffle": true
  }
}
```

## Advanced Features

### Selective Restoration

```python
class SelectiveRestorer:
    def __init__(self, snapshot):
        self.snapshot = snapshot

    async def restore_player_only(self, player):
        """Restore only player state"""
        player_data = self.snapshot.data.get("player", {})
        player.volume = player_data.get("volume", 100)
        # Skip queue, filters, autoplay

    async def restore_queue_only(self, player):
        """Restore only queue state"""
        queue_data = self.snapshot.data.get("queue", {})

        # Clear current queue
        player.queue._upcoming.clear()
        player.queue._history.clear()

        # Restore upcoming tracks
        for track_data in queue_data.get("upcoming", []):
            # Convert track_data back to Track objects
            track = self._deserialize_track(track_data)
            await player.queue.add(track)

        player.queue.loop_mode = queue_data.get("loop_mode", "none")

    def _deserialize_track(self, track_data):
        """Convert track data back to Track object"""
        from sonora import Track
        return Track(
            track=f"restored_{track_data['identifier']}",
            info=track_data
        )
```

### Snapshot Validation

```python
class SnapshotValidator:
    @staticmethod
    def validate_snapshot(snapshot):
        """Validate snapshot integrity"""
        required_fields = ["player", "queue", "filters", "autoplay"]

        for field in required_fields:
            if field not in snapshot.data:
                raise ValueError(f"Missing required field: {field}")

        # Validate player data
        player_data = snapshot.data["player"]
        if not isinstance(player_data.get("volume"), int):
            raise ValueError("Invalid volume in player data")

        # Validate queue data
        queue_data = snapshot.data["queue"]
        if not isinstance(queue_data.get("upcoming", []), list):
            raise ValueError("Invalid upcoming tracks in queue data")

        return True

# Usage
try:
    snapshot = snapshot_manager.load_snapshot("backup.json")
    SnapshotValidator.validate_snapshot(snapshot)
    print("Snapshot is valid")
except ValueError as e:
    print(f"Invalid snapshot: {e}")
```

### Encrypted Snapshots

```python
from sonora import credential_manager

class EncryptedSnapshotManager:
    def __init__(self, snapshot_manager, credential_manager):
        self.snapshot_manager = snapshot_manager
        self.credential_manager = credential_manager

    def save_encrypted_snapshot(self, snapshot, filename, key_name):
        """Save snapshot encrypted"""
        # Convert to JSON
        json_data = snapshot.to_json()

        # Encrypt with credential vault
        encrypted_data = self.credential_manager.encrypt_credential(json_data)

        # Save encrypted data
        with open(filename, 'w') as f:
            f.write(encrypted_data)

    def load_encrypted_snapshot(self, filename, key_name):
        """Load and decrypt snapshot"""
        # Read encrypted data
        with open(filename, 'r') as f:
            encrypted_data = f.read()

        # Decrypt with credential vault
        json_data = self.credential_manager.decrypt_credential(encrypted_data)

        # Parse back to snapshot
        return self.snapshot_manager.from_json(json_data)

# Usage
encrypted_manager = EncryptedSnapshotManager(snapshot_manager, credential_manager)

# Save encrypted
snapshot = snapshot_manager.create_snapshot(player)
encrypted_manager.save_encrypted_snapshot(snapshot, "secure_backup.json", "backup_key")

# Load encrypted
restored_snapshot = encrypted_manager.load_encrypted_snapshot("secure_backup.json", "backup_key")
```

## Deployment Strategies

### Blue-Green Deployment

```python
class BlueGreenDeployment:
    def __init__(self, client):
        self.client = client
        self.snapshots = {}

    async def prepare_deployment(self):
        """Take snapshots before deployment"""
        for guild_id, player in self.client.players.items():
            snapshot = snapshot_manager.create_snapshot(player)
            self.snapshots[guild_id] = snapshot

        print(f"Prepared snapshots for {len(self.snapshots)} guilds")

    async def rollback_deployment(self):
        """Rollback to previous state if deployment fails"""
        for guild_id, snapshot in self.snapshots.items():
            try:
                player = await self.client.get_player(guild_id)
                await snapshot_manager.restore_snapshot(snapshot, player)
                print(f"Rolled back guild {guild_id}")
            except Exception as e:
                print(f"Failed to rollback guild {guild_id}: {e}")

# Usage
deployment = BlueGreenDeployment(client)

# Before deployment
await deployment.prepare_deployment()

# After deployment issues
await deployment.rollback_deployment()
```

### Rolling Deployment

```python
class RollingDeployment:
    def __init__(self, client, batch_size=5):
        self.client = client
        self.batch_size = batch_size

    async def rolling_update(self, new_version_callback):
        """Perform rolling update with snapshots"""
        guild_ids = list(self.client.players.keys())
        snapshots = {}

        # Process in batches
        for i in range(0, len(guild_ids), self.batch_size):
            batch = guild_ids[i:i + self.batch_size]

            # Take snapshots for this batch
            for guild_id in batch:
                player = self.client.players[guild_id]
                snapshots[guild_id] = snapshot_manager.create_snapshot(player)

            # Update this batch
            for guild_id in batch:
                try:
                    await new_version_callback(guild_id)
                    print(f"Updated guild {guild_id}")
                except Exception as e:
                    # Rollback this guild
                    snapshot = snapshots[guild_id]
                    player = await self.client.get_player(guild_id)
                    await snapshot_manager.restore_snapshot(snapshot, player)
                    print(f"Rolled back guild {guild_id}: {e}")

            # Wait between batches
            await asyncio.sleep(10)
```

## Monitoring and Analytics

### Snapshot Analytics

```python
class SnapshotAnalytics:
    def __init__(self, snapshot_manager):
        self.snapshot_manager = snapshot_manager

    def analyze_snapshot_usage(self):
        """Analyze snapshot creation and restoration patterns"""
        snapshots = self.snapshot_manager.list_snapshots()

        stats = {
            "total_snapshots": len(snapshots),
            "snapshots_by_guild": {},
            "average_snapshot_size": 0,
            "oldest_snapshot": None,
            "newest_snapshot": None
        }

        for snapshot_file in snapshots:
            # Parse guild ID from filename
            parts = snapshot_file.split('_')
            if len(parts) >= 2:
                guild_id = parts[1]
                if guild_id not in stats["snapshots_by_guild"]:
                    stats["snapshots_by_guild"][guild_id] = 0
                stats["snapshots_by_guild"][guild_id] += 1

        return stats

    def cleanup_old_snapshots(self, max_age_days=7):
        """Clean up snapshots older than specified days"""
        import os
        import time

        max_age_seconds = max_age_days * 24 * 60 * 60
        current_time = time.time()

        snapshots_dir = self.snapshot_manager.snapshot_dir
        cleaned_count = 0

        for filename in os.listdir(snapshots_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(snapshots_dir, filename)
                file_age = current_time - os.path.getmtime(filepath)

                if file_age > max_age_seconds:
                    os.remove(filepath)
                    cleaned_count += 1

        return cleaned_count

# Usage
analytics = SnapshotAnalytics(snapshot_manager)
stats = analytics.analyze_snapshot_usage()
print(f"Total snapshots: {stats['total_snapshots']}")

cleaned = analytics.cleanup_old_snapshots(max_age_days=30)
print(f"Cleaned {cleaned} old snapshots")
```

## Best Practices

### 1. Snapshot Frequency

- **High-traffic guilds**: Snapshot every 5-10 minutes
- **Low-traffic guilds**: Snapshot every 30-60 minutes
- **Critical sessions**: Snapshot before major operations

### 2. Storage Management

- **Retention policy**: Keep 5-10 snapshots per guild
- **Cleanup automation**: Remove snapshots older than 7-30 days
- **Compression**: Consider compressing large snapshot files

### 3. Security Considerations

- **Encryption**: Use encrypted snapshots for sensitive data
- **Access control**: Restrict snapshot file access
- **Validation**: Always validate snapshots before restoration

### 4. Performance Optimization

- **Background processing**: Don't block main operations for snapshots
- **Incremental snapshots**: Only save changed state
- **Compression**: Use compression for large snapshots

### 5. Error Handling

```python
async def safe_snapshot_restore(snapshot_file, player):
    """Safely restore snapshot with error handling"""
    try:
        # Validate file exists
        if not os.path.exists(snapshot_file):
            raise FileNotFoundError(f"Snapshot file not found: {snapshot_file}")

        # Load and validate snapshot
        snapshot = snapshot_manager.load_snapshot(snapshot_file)
        SnapshotValidator.validate_snapshot(snapshot)

        # Create backup of current state
        backup_snapshot = snapshot_manager.create_snapshot(player)
        backup_file = f"backup_{int(time.time())}.json"
        snapshot_manager.save_snapshot(backup_snapshot, backup_file)

        # Restore snapshot
        await snapshot_manager.restore_snapshot(snapshot, player)

        # Verify restoration
        if not await verify_restoration(player, snapshot):
            # Restore from backup if verification fails
            backup_snapshot = snapshot_manager.load_snapshot(backup_file)
            await snapshot_manager.restore_snapshot(backup_snapshot, player)
            raise RuntimeError("Snapshot restoration verification failed")

        # Cleanup backup
        os.remove(backup_file)

        return True

    except Exception as e:
        print(f"Snapshot restoration failed: {e}")
        return False

async def verify_restoration(player, original_snapshot):
    """Verify that restoration was successful"""
    # Check player state
    player_data = original_snapshot.data.get("player", {})
    if player.volume != player_data.get("volume", 100):
        return False

    # Check queue state
    queue_data = original_snapshot.data.get("queue", {})
    if len(player.queue.upcoming) != len(queue_data.get("upcoming", [])):
        return False

    return True
```

Session management in Sonora v1.2.7 provides enterprise-grade reliability and continuity for your music bot deployments.