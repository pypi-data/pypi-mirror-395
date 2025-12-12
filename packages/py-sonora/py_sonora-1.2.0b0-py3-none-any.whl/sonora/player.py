"""Player and Queue management for Sonora."""

from typing import Any

from .autoplay import AutoplayEngine
from .events import EventType, event_manager
from .exceptions import PlayerException
from .filters import FilterManager
from .queue import SmartQueue
from .track import Track
from .typing import GuildID


class Player:
    """Represents a per-guild player with advanced features."""

    def __init__(self, guild_id: GuildID, node: Any, client: Any = None) -> None:
        self.guild_id = guild_id
        self.node = node
        self.client = client
        self.queue = SmartQueue(guild_id)
        self.autoplay = AutoplayEngine(guild_id, client)
        self.filters = FilterManager()
        self.volume = 100
        self.paused = False
        self.position = 0
        self.connected = False
        self.session_id: str | None = None

    async def connect(self, channel_id: int, session_id: str, token: str) -> None:
        """Connect to voice channel."""
        self.session_id = session_id
        await self.node.send(
            "voiceUpdate",
            guildId=self.guild_id,
            sessionId=session_id,
            event={"token": token, "endpoint": self.node.host},
        )
        self.connected = True
        await event_manager.emit_event(
            EventType.VOICE_UPDATE, {"guild_id": self.guild_id, "connected": True}
        )

    async def disconnect(self) -> None:
        """Disconnect from voice channel."""
        await self.node.send(
            "voiceUpdate", guildId=self.guild_id, sessionId=None, event=None
        )
        self.connected = False
        await event_manager.emit_event(
            EventType.VOICE_DISCONNECTED, {"guild_id": self.guild_id}
        )

    async def play(self, track: Track) -> Track:
        """Play a track."""
        if not self.connected or not self.session_id:
            raise PlayerException(
                "Missing voice state: player is not connected to a voice channel"
            )

        self.queue._current = track
        payload = {"guildId": self.guild_id, "track": track.track, "noReplace": False}
        if self.filters.filters:
            payload["filters"] = self.filters.to_payload()

        await self.node.send("play", **payload)
        await event_manager.emit_event(
            EventType.TRACK_START, {"guild_id": self.guild_id, "track": track}
        )
        return track

    async def pause(self) -> None:
        """Pause the player."""
        await self.node.send("pause", guildId=self.guild_id, pause=True)
        self.paused = True
        await event_manager.emit_event(
            EventType.PLAYER_UPDATE, {"guild_id": self.guild_id, "paused": True}
        )

    async def resume(self) -> None:
        """Resume the player."""
        await self.node.send("pause", guildId=self.guild_id, pause=False)
        self.paused = False
        await event_manager.emit_event(
            EventType.PLAYER_UPDATE, {"guild_id": self.guild_id, "paused": False}
        )

    async def stop(self) -> None:
        """Stop the player."""
        await self.node.send("stop", guildId=self.guild_id)
        self.queue._current = None
        await event_manager.emit_event(
            EventType.TRACK_END, {"guild_id": self.guild_id, "reason": "stopped"}
        )

    async def seek(self, position: int) -> None:
        """Seek to a position in the track."""
        await self.node.send("seek", guildId=self.guild_id, position=position)
        self.position = position
        await event_manager.emit_event(
            EventType.SEEK_UPDATE, {"guild_id": self.guild_id, "position": position}
        )

    async def set_volume(self, volume: int) -> None:
        """Set the player volume."""
        await self.node.send("volume", guildId=self.guild_id, volume=volume)
        self.volume = volume
        await event_manager.emit_event(
            EventType.VOLUME_UPDATE, {"guild_id": self.guild_id, "volume": volume}
        )

    async def set_filters(self) -> None:
        """Apply current filters."""
        if self.filters.filters:
            await self.node.send(
                "filters", guildId=self.guild_id, **self.filters.to_payload()
            )
            await event_manager.emit_event(
                EventType.FILTER_UPDATE,
                {"guild_id": self.guild_id, "filters": self.filters.to_payload()},
            )

    async def skip(self) -> Track | None:
        """Skip to the next track."""
        next_track = await self.queue.advance()
        if next_track:
            await self.play(next_track)
        else:
            # Try autoplay if enabled
            if self.queue.loop_mode == "autoplay" and self.autoplay.enabled:
                context = {
                    "history": self.queue.history[-self.autoplay.max_history:],
                    "current": self.queue.current,
                    "guild_id": self.guild_id
                }
                autoplay_track = await self.autoplay.fetch_next_track(context)
                if autoplay_track:
                    await self.queue.add(autoplay_track)
                    next_track = await self.queue.advance()
                    if next_track:
                        await self.play(next_track)
                        return next_track

            await self.stop()
            await event_manager.emit_event(
                EventType.QUEUE_EMPTY, {"guild_id": self.guild_id}
            )
        return next_track

    async def skip_to(self, position: int) -> Track | None:
        """Skip to a specific position in the queue."""
        try:
            track = await self.queue.skip_to(position)
            await self.play(track)
            return track
        except IndexError:
            return None

    async def destroy(self) -> None:
        """Destroy the player."""
        await self.autoplay.stop()  # Stop autoplay engine
        await self.node.send("destroy", guildId=self.guild_id)
        if self.client:
            self.client.players.pop(self.guild_id, None)
        await event_manager.emit_event(
            EventType.PLAYER_DESTROY, {"guild_id": self.guild_id}
        )
