"""Node management for Sonora."""

import asyncio
import json
import logging
from typing import Any

import aiohttp

from .exceptions import NodeException
from .typing import NodeConfig
from .utils import BackoffStrategy

logger = logging.getLogger(__name__)


class Node:
    """Represents a Lavalink node."""

    def __init__(self, config: NodeConfig):
        self.host = config["host"]
        self.port = config["port"]
        self.password = config["password"]
        self.secure = config.get("secure", False)
        self.session: aiohttp.ClientSession | None = None
        self.websocket: aiohttp.ClientWebSocketResponse | None = None
        self.connected = False
        self.stats: dict[str, Any] = {}
        self.backoff = BackoffStrategy()
        self._listener_task: asyncio.Task | None = None

    async def connect(self) -> None:
        """Connect to the Lavalink node."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{'wss' if self.secure else 'ws'}://{self.host}:{self.port}"
        headers = {"Authorization": str(self.password), "User-Id": "sonora"}

        try:
            self.websocket = await self.session.ws_connect(url, headers=headers)
            self.connected = True
            self.backoff.reset()
            logger.info(f"Connected to Lavalink node at {self.host}:{self.port}")
            # Start listener task
            self._listener_task = asyncio.create_task(self._listen())
        except Exception as e:
            raise NodeException(f"Failed to connect to node: {e}") from e

    async def disconnect(self) -> None:
        """Disconnect from the Lavalink node."""
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
        if self.websocket:
            await self.websocket.close()
        if self.session:
            await self.session.close()
        self.connected = False
        logger.info(f"Disconnected from Lavalink node at {self.host}:{self.port}")

    async def _listen(self) -> None:
        """Listen for incoming messages and handle reconnects."""
        while self.connected and self.websocket:
            try:
                msg = await self.websocket.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    await self._handle_message(data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {self.websocket.exception()}")
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    logger.warning("WebSocket closed")
                    break
            except ConnectionResetError as e:
                logger.warning(f"Connection reset by peer: {e}")
                break
            except Exception as e:
                logger.error(f"Error in listener: {e}")
                break

        # Reconnect if still supposed to be connected
        if self.connected:
            await self._reconnect()

    async def _reconnect(self) -> None:
        """Reconnect to the node with backoff."""
        self.connected = False
        if self.websocket:
            await self.websocket.close()
        delay = self.backoff.get_delay()
        logger.info(f"Reconnecting to node in {delay} seconds")
        await asyncio.sleep(delay)
        try:
            await self.connect()
        except Exception as e:
            logger.error(f"Reconnect failed: {e}")
            # Schedule another reconnect
            asyncio.create_task(self._reconnect())

    async def _handle_message(self, data: dict[str, Any]) -> None:
        """Handle incoming message from Lavalink."""
        op = data.get("op")
        if op == "stats":
            self.stats = data
        elif op == "playerUpdate":
            # Update player state if needed
            pass
        elif op == "event":
            # Handle track events
            pass
        # Add more handlers as needed

    async def send(self, op: str, **data: Any) -> None:
        """Send a payload to the node."""
        if not self.connected or not self.websocket:
            raise NodeException("Node is not connected")

        payload = {"op": op, **data}
        await self.websocket.send_json(payload)

    async def receive(self) -> Any:
        """Receive a payload from the node."""
        if not self.connected or not self.websocket:
            raise NodeException("Node is not connected")

        msg = await self.websocket.receive()
        if msg.type == aiohttp.WSMsgType.TEXT:
            return json.loads(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            raise NodeException(f"WebSocket error: {self.websocket.exception()}")
        else:
            raise NodeException("Unexpected message type")

    async def ping(self) -> None:
        """Send a ping to detect half-open connections."""
        if self.websocket:
            await self.websocket.ping()

    async def get_stats(self) -> Any:
        """Get node statistics."""
        # Lavalink stats are sent via events, stored in self.stats
        return self.stats
