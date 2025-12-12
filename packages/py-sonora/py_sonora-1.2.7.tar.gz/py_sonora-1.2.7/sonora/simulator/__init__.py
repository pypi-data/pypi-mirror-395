"""Offline Lavalink protocol simulator for testing and development."""

import asyncio
import json
import random
import time
from typing import Any, Dict, List, Optional, Union

from ..events import EventType, event_manager
from ..exceptions import SonoraError
from ..track import Track


class SimulatedNode:
    """Simulated Lavalink node for offline testing."""

    def __init__(self, host: str = "127.0.0.1", port: int = 2333, password: str = "youshallnotpass"):
        self.host = host
        self.port = port
        self.password = password
        self.connected = False
        self.players: Dict[int, 'SimulatedPlayer'] = {}
        self.latency = 50  # ms
        self.jitter = 10   # ms
        self.packet_loss = 0.001  # 0.1%
        self._running = False
        self._background_task: Optional[asyncio.Task] = None

    async def connect(self) -> None:
        """Simulate connection to Lavalink node."""
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Connection delay
        self.connected = True
        await event_manager.emit_event(EventType.NODE_READY, {"node": self})

    async def disconnect(self) -> None:
        """Simulate disconnection."""
        self.connected = False
        for player in self.players.values():
            await player.destroy()
        self.players.clear()
        await event_manager.emit_event(EventType.NODE_DISCONNECTED, {"node": self})

    async def send(self, op: str, **data) -> None:
        """Simulate sending data to Lavalink."""
        if random.random() < self.packet_loss:
            return  # Simulate packet loss

        # Add simulated latency
        delay = (self.latency + random.uniform(-self.jitter, self.jitter)) / 1000
        await asyncio.sleep(delay)

        # Simulate response based on operation
        if op == "play":
            guild_id = data.get("guildId")
            if guild_id in self.players:
                player = self.players[guild_id]
                await player._simulate_track_start(data)
        elif op == "pause":
            guild_id = data.get("guildId")
            if guild_id in self.players:
                player = self.players[guild_id]
                player.paused = data.get("pause", False)
        elif op == "stop":
            guild_id = data.get("guildId")
            if guild_id in self.players:
                player = self.players[guild_id]
                await player._simulate_track_end("stopped")
        elif op == "seek":
            guild_id = data.get("guildId")
            position = data.get("position", 0)
            if guild_id in self.players:
                player = self.players[guild_id]
                player.position = position
        elif op == "volume":
            guild_id = data.get("guildId")
            volume = data.get("volume", 100)
            if guild_id in self.players:
                player = self.players[guild_id]
                player.volume = volume
        elif op == "destroy":
            guild_id = data.get("guildId")
            if guild_id in self.players:
                await self.players[guild_id].destroy()
                del self.players[guild_id]

    def get_player(self, guild_id: int) -> 'SimulatedPlayer':
        """Get or create a simulated player."""
        if guild_id not in self.players:
            self.players[guild_id] = SimulatedPlayer(guild_id, self)
        return self.players[guild_id]


class SimulatedPlayer:
    """Simulated player for offline testing."""

    def __init__(self, guild_id: int, node: SimulatedNode):
        self.guild_id = guild_id
        self.node = node
        self.connected = False
        self.session_id: Optional[str] = None
        self.current_track: Optional[Track] = None
        self.volume = 100
        self.paused = False
        self.position = 0
        self._start_time = 0
        self._track_task: Optional[asyncio.Task] = None

    async def connect(self, channel_id: int, session_id: str, token: str) -> None:
        """Simulate voice connection."""
        self.session_id = session_id
        self.connected = True
        await event_manager.emit_event(EventType.VOICE_UPDATE, {
            "guild_id": self.guild_id,
            "connected": True
        })

    async def disconnect(self) -> None:
        """Simulate voice disconnection."""
        self.connected = False
        if self._track_task:
            self._track_task.cancel()
        await event_manager.emit_event(EventType.VOICE_DISCONNECTED, {
            "guild_id": self.guild_id
        })

    async def destroy(self) -> None:
        """Destroy the simulated player."""
        await self.disconnect()
        await event_manager.emit_event(EventType.PLAYER_DESTROY, {
            "guild_id": self.guild_id
        })

    async def _simulate_track_start(self, data: Dict[str, Any]) -> None:
        """Simulate track start."""
        track_data = data.get("track", "")
        # Simulate track info (this would normally come from Lavalink)
        track_info = {
            "title": f"Simulated Track {random.randint(1000, 9999)}",
            "author": f"Simulated Artist {random.randint(100, 999)}",
            "length": random.randint(120000, 300000),  # 2-5 minutes
            "identifier": f"sim_{random.randint(10000, 99999)}",
            "uri": f"sim://track/{random.randint(1000, 9999)}",
            "isStream": False,
            "isSeekable": True,
            "position": 0
        }

        self.current_track = Track(track=track_data, info=track_info)
        self.position = 0
        self._start_time = time.time()
        self.paused = False

        await event_manager.emit_event(EventType.TRACK_START, {
            "guild_id": self.guild_id,
            "track": self.current_track
        })

        # Start track progression simulation
        if self._track_task:
            self._track_task.cancel()
        self._track_task = asyncio.create_task(self._simulate_track_progress())

    async def _simulate_track_progress(self) -> None:
        """Simulate track progress and end."""
        try:
            while self.current_track and not self.paused:
                await asyncio.sleep(1)  # Update every second
                if not self.paused:
                    self.position += 1000  # 1 second in ms

                # Check if track should end
                if self.position >= self.current_track.length:
                    await self._simulate_track_end("finished")
                    break

        except asyncio.CancelledError:
            pass

    async def _simulate_track_end(self, reason: str) -> None:
        """Simulate track end."""
        if self.current_track:
            await event_manager.emit_event(EventType.TRACK_END, {
                "guild_id": self.guild_id,
                "track": self.current_track,
                "reason": reason
            })
            self.current_track = None
            self.position = 0


class ProtocolSimulator:
    """Advanced protocol simulator with fault injection."""

    def __init__(self):
        self.node = SimulatedNode()
        self.fault_injection_enabled = False
        self.faults: Dict[str, Any] = {
            "packet_loss": 0.0,
            "latency_spike": 0.0,
            "connection_drop": 0.0,
            "invalid_response": 0.0,
        }
        self.recorded_packets: List[Dict[str, Any]] = []
        self._replay_mode = False
        self._replay_packets: List[Dict[str, Any]] = []

    async def start(self) -> None:
        """Start the protocol simulator."""
        await self.node.connect()

    async def stop(self) -> None:
        """Stop the protocol simulator."""
        await self.node.disconnect()

    def enable_fault_injection(self, faults: Dict[str, float]) -> None:
        """Enable fault injection for testing."""
        self.fault_injection_enabled = True
        self.faults.update(faults)

    def disable_fault_injection(self) -> None:
        """Disable fault injection."""
        self.fault_injection_enabled = False

    def start_packet_recording(self) -> None:
        """Start recording packets for replay."""
        self.recorded_packets.clear()

    def stop_packet_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return recorded packets."""
        packets = self.recorded_packets.copy()
        self.recorded_packets.clear()
        return packets

    def load_replay_packets(self, packets: List[Dict[str, Any]]) -> None:
        """Load packets for replay."""
        self._replay_packets = packets.copy()
        self._replay_mode = True

    async def replay_packets(self, speed_multiplier: float = 1.0) -> None:
        """Replay recorded packets."""
        if not self._replay_packets:
            return

        start_time = time.time()
        last_timestamp = self._replay_packets[0].get("timestamp", start_time)

        for packet in self._replay_packets:
            current_time = time.time()
            packet_timestamp = packet.get("timestamp", current_time)
            delay = (packet_timestamp - last_timestamp) / speed_multiplier

            if delay > 0:
                await asyncio.sleep(delay)

            # Simulate the packet (this would need more implementation)
            last_timestamp = packet_timestamp

        self._replay_mode = False

    async def inject_faults(self) -> None:
        """Inject faults for testing."""
        if not self.fault_injection_enabled:
            return

        # Random fault injection
        if random.random() < self.faults["connection_drop"]:
            await self.node.disconnect()
            await asyncio.sleep(random.uniform(1, 5))
            await self.node.connect()

        # Latency spikes
        if random.random() < self.faults["latency_spike"]:
            self.node.latency *= random.uniform(5, 20)  # 5-20x latency
            await asyncio.sleep(random.uniform(1, 3))
            self.node.latency = 50  # Reset


class MockFactory:
    """Factory for creating mock objects."""

    @staticmethod
    def create_mock_track(title: str = None, author: str = None, length: int = None) -> Track:
        """Create a mock track for testing."""
        if title is None:
            title = f"Mock Track {random.randint(1000, 9999)}"
        if author is None:
            author = f"Mock Artist {random.randint(100, 999)}"
        if length is None:
            length = random.randint(120000, 300000)

        return Track(
            track=f"mock_track_{random.randint(10000, 99999)}",
            info={
                "title": title,
                "author": author,
                "length": length,
                "identifier": f"mock_{random.randint(10000, 99999)}",
                "uri": f"mock://track/{random.randint(1000, 9999)}",
                "isStream": False,
                "isSeekable": True,
                "position": 0
            }
        )

    @staticmethod
    def create_mock_playlist(name: str = None, track_count: int = 5) -> List[Track]:
        """Create a mock playlist."""
        if name is None:
            name = f"Mock Playlist {random.randint(100, 999)}"

        return [MockFactory.create_mock_track() for _ in range(track_count)]

    @staticmethod
    def create_mock_search_results(query: str, count: int = 10) -> List[Track]:
        """Create mock search results."""
        results = []
        for i in range(count):
            title = f"{query} Result {i+1}"
            results.append(MockFactory.create_mock_track(title=title))
        return results


# Global simulator instance
protocol_simulator = ProtocolSimulator()
mock_factory = MockFactory()