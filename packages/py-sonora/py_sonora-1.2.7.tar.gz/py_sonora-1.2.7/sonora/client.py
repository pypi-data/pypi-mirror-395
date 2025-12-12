"""High-level Sonora client."""

import asyncio
import logging
from typing import Any

from .node import Node
from .player import Player
from .typing import GuildID, NodeConfig

logger = logging.getLogger(__name__)


class SonoraClient:
    """High-level client for Sonora."""

    def __init__(
        self,
        lavalink_nodes: list[NodeConfig],
        node_pooling: bool = True,
        reconnect_policy: dict[str, Any] | None = None,
    ):
        self.nodes: list[Node] = [Node(config) for config in lavalink_nodes]
        self.players: dict[GuildID, Player] = {}
        self.node_pooling = node_pooling
        self.reconnect_policy = reconnect_policy or {
            "max_retries": 5,
            "backoff": "exponential",
        }
        self._running = False
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        """Start the client and connect to nodes."""
        if self._running:
            return

        self._running = True
        for node in self.nodes:
            await node.connect()

        logger.info("Sonora client started")

    async def close(self) -> None:
        """Close the client and disconnect from nodes."""
        if not self._running:
            return

        self._running = False
        for player in self.players.values():
            await player.destroy()

        for node in self.nodes:
            await node.disconnect()

        logger.info("Sonora client closed")

    async def get_player(self, guild_id: GuildID) -> Player:
        """Get or create a player for a guild."""
        async with self._lock:
            if guild_id not in self.players:
                # Select node (simple round-robin for now)
                node = self.nodes[0]  # TODO: implement proper node selection
                self.players[guild_id] = Player(guild_id, node, self)
            return self.players[guild_id]

    async def load_track(self, query: str) -> Any | None:
        """Load a track from Lavalink."""
        # TODO: implement track loading
        return None

    async def __aenter__(self) -> "SonoraClient":
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
