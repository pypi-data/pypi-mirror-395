"""Tests for SonoraClient."""

from unittest.mock import AsyncMock

import pytest

from sonora import SonoraClient


class TestSonoraClient:
    """Test cases for SonoraClient."""

    def test_init(self):
        """Test client initialization."""
        nodes = [{"host": "127.0.0.1", "port": 2333, "password": "test"}]
        client = SonoraClient(nodes)
        assert len(client.nodes) == 1
        assert not client._running

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test client as context manager."""
        nodes = [{"host": "127.0.0.1", "port": 2333, "password": "test"}]
        client = SonoraClient(nodes)

        # Mock the node connect/disconnect methods
        for node in client.nodes:
            node.connect = AsyncMock()
            node.disconnect = AsyncMock()

        async with client:
            assert client._running
        assert not client._running
