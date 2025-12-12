"""Tests for Player."""

from unittest.mock import AsyncMock

import pytest

from sonora import Player
from sonora.exceptions import PlayerException


class TestPlayer:
    """Test cases for Player."""

    @pytest.mark.asyncio
    async def test_play_without_voice_state(self):
        """Test play raises exception without voice connection."""
        node = AsyncMock()
        player = Player(123, node)

        track = AsyncMock()
        track.track = "test"

        with pytest.raises(PlayerException, match="Missing voice state"):
            await player.play(track)

    @pytest.mark.asyncio
    async def test_skip_advances_queue(self):
        """Test skip advances queue correctly."""
        node = AsyncMock()
        player = Player(123, node)
        player.connected = True
        player.session_id = "test"

        # Mock queue advance
        track1 = AsyncMock()
        track1.track = "track1"
        track2 = AsyncMock()
        track2.track = "track2"
        player.queue._upcoming.append(track1)
        player.queue._upcoming.append(track2)

        # Mock play
        player.play = AsyncMock()

        await player.skip()

        player.play.assert_called_once_with(track1)
        assert player.queue._current == track1
