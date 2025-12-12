"""Session snapshot and restore functionality."""

import asyncio
import json
import os
import time
from typing import Any, Dict, List, Optional

from ..exceptions import SonoraError
from ..player import Player
from ..security import SecureDeserializationLayer


class SessionSnapshot:
    """Represents a complete session snapshot."""

    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.timestamp = time.time()
        self.version = "1.2.7"
        self.data: Dict[str, Any] = {}

    def capture_player_state(self, player: Player) -> None:
        """Capture complete player state."""
        self.data["player"] = {
            "volume": player.volume,
            "paused": player.paused,
            "position": player.position,
            "connected": player.connected,
            "session_id": player.session_id,
        }

    def capture_queue_state(self, queue) -> None:
        """Capture queue state."""
        self.data["queue"] = {
            "current": self._serialize_track(queue.current) if queue.current else None,
            "upcoming": [self._serialize_track(track) for track in queue.upcoming],
            "history": [self._serialize_track(track) for track in queue.history[-50:]],  # Last 50
            "loop_mode": queue.loop_mode,
            "shuffle_enabled": queue.shuffle_enabled,
        }

    def capture_filters_state(self, filters) -> None:
        """Capture audio filters state."""
        self.data["filters"] = {
            "active_filters": getattr(filters, 'active_filters', []),
            "filter_config": getattr(filters, 'to_payload', lambda: {})(),
        }

    def capture_autoplay_state(self, autoplay) -> None:
        """Capture autoplay state."""
        self.data["autoplay"] = {
            "enabled": getattr(autoplay, 'enabled', True),
            "strategy": getattr(autoplay, 'strategy', 'similar_artist'),
            "max_history": getattr(autoplay, 'max_history', 50),
            "smart_shuffle": getattr(autoplay, 'smart_shuffle', True),
        }

    def _serialize_track(self, track) -> Dict[str, Any]:
        """Serialize a track to dictionary."""
        if not track:
            return {}

        return {
            "title": getattr(track, 'title', ''),
            "author": getattr(track, 'author', ''),
            "uri": getattr(track, 'uri', ''),
            "identifier": getattr(track, 'identifier', ''),
            "length": getattr(track, 'length', 0),
            "position": getattr(track, 'position', 0),
            "isStream": getattr(track, 'isStream', False),
            "isSeekable": getattr(track, 'isSeekable', True),
            "track": getattr(track, 'track', ''),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary."""
        return {
            "guild_id": self.guild_id,
            "timestamp": self.timestamp,
            "version": self.version,
            "data": self.data,
        }

    def to_json(self) -> str:
        """Convert snapshot to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionSnapshot':
        """Create snapshot from dictionary."""
        snapshot = cls(data["guild_id"])
        snapshot.timestamp = data["timestamp"]
        snapshot.version = data.get("version", "1.2.0")
        snapshot.data = data["data"]
        return snapshot

    @classmethod
    def from_json(cls, json_str: str) -> 'SessionSnapshot':
        """Create snapshot from JSON string."""
        deserializer = SecureDeserializationLayer()
        data = deserializer.safe_json_loads(json_str)
        return cls.from_dict(data)


class SnapshotManager:
    """Manager for session snapshots."""

    def __init__(self, snapshot_dir: str = ".sonora_snapshots"):
        self.snapshot_dir = snapshot_dir
        self.auto_snapshot_interval = 300  # 5 minutes
        self.max_snapshots_per_guild = 10
        self._background_task: Optional[asyncio.Task] = None
        self._running = False

        # Create snapshot directory
        os.makedirs(snapshot_dir, exist_ok=True)

    async def start_auto_snapshot(self) -> None:
        """Start automatic snapshot background task."""
        if self._running:
            return

        self._running = True
        self._background_task = asyncio.create_task(self._auto_snapshot_loop())

    async def stop_auto_snapshot(self) -> None:
        """Stop automatic snapshot background task."""
        self._running = False
        if self._background_task:
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass

    async def _auto_snapshot_loop(self) -> None:
        """Background loop for automatic snapshots."""
        while self._running:
            try:
                # This would snapshot all active players
                # For now, just sleep
                await asyncio.sleep(self.auto_snapshot_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Auto-snapshot error: {e}")

    def create_snapshot(self, player: Player) -> SessionSnapshot:
        """Create a snapshot of current player state."""
        snapshot = SessionSnapshot(player.guild_id)

        # Capture all states
        snapshot.capture_player_state(player)
        snapshot.capture_queue_state(player.queue)
        snapshot.capture_filters_state(player.filters)

        # Try to capture autoplay state if available
        if hasattr(player, 'autoplay'):
            snapshot.capture_autoplay_state(player.autoplay)

        return snapshot

    def save_snapshot(self, snapshot: SessionSnapshot, filename: Optional[str] = None) -> str:
        """Save snapshot to file."""
        if not filename:
            timestamp = int(snapshot.timestamp)
            filename = f"guild_{snapshot.guild_id}_{timestamp}.json"

        filepath = os.path.join(self.snapshot_dir, filename)

        with open(filepath, 'w') as f:
            f.write(snapshot.to_json())

        # Clean up old snapshots
        self._cleanup_old_snapshots(snapshot.guild_id)

        return filepath

    def load_snapshot(self, filepath: str) -> SessionSnapshot:
        """Load snapshot from file."""
        if not os.path.exists(filepath):
            raise SonoraError(f"Snapshot file not found: {filepath}")

        with open(filepath, 'r') as f:
            json_data = f.read()

        return SessionSnapshot.from_json(json_data)

    def list_snapshots(self, guild_id: Optional[int] = None) -> List[str]:
        """List available snapshots."""
        if not os.path.exists(self.snapshot_dir):
            return []

        files = os.listdir(self.snapshot_dir)
        json_files = [f for f in files if f.endswith('.json')]

        if guild_id is not None:
            json_files = [f for f in json_files if f.startswith(f"guild_{guild_id}_")]

        return sorted(json_files, reverse=True)  # Most recent first

    def _cleanup_old_snapshots(self, guild_id: int) -> None:
        """Clean up old snapshots for a guild."""
        snapshots = self.list_snapshots(guild_id)

        if len(snapshots) > self.max_snapshots_per_guild:
            to_remove = snapshots[self.max_snapshots_per_guild:]
            for filename in to_remove:
                filepath = os.path.join(self.snapshot_dir, filename)
                try:
                    os.remove(filepath)
                except Exception:
                    pass  # Ignore cleanup errors

    async def restore_snapshot(self, snapshot: SessionSnapshot, player: Player) -> None:
        """Restore player state from snapshot."""
        try:
            # Restore player state
            player_data = snapshot.data.get("player", {})
            player.volume = player_data.get("volume", 100)
            player.paused = player_data.get("paused", False)
            player.position = player_data.get("position", 0)

            # Restore queue state
            queue_data = snapshot.data.get("queue", {})
            player.queue._upcoming.clear()
            player.queue._history.clear()
            player.queue._current = None

            # Restore upcoming tracks (this would need proper track reconstruction)
            # For now, this is a placeholder
            upcoming_tracks = queue_data.get("upcoming", [])
            for track_data in upcoming_tracks[:50]:  # Limit to prevent abuse
                # This would reconstruct Track objects from data
                pass

            player.queue.loop_mode = queue_data.get("loop_mode", "none")
            player.queue.shuffle_enabled = queue_data.get("shuffle_enabled", False)

            # Restore filters (placeholder)
            # filters_data = snapshot.data.get("filters", {})

            # Restore autoplay (placeholder)
            # autoplay_data = snapshot.data.get("autoplay", {})

        except Exception as e:
            raise SonoraError(f"Failed to restore snapshot: {e}")


# Global snapshot manager instance
snapshot_manager = SnapshotManager()