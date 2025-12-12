"""Tests for AutoplayEngine."""

import pytest

from sonora.autoplay import AutoplayEngine


class TestAutoplayEngine:
    """Test cases for AutoplayEngine."""

    def test_initialization(self):
        """Test AutoplayEngine initializes correctly."""
        engine = AutoplayEngine(123)
        assert engine.guild_id == 123
        assert engine.enabled is True
        assert engine.strategy == "similar_artist"
        assert engine.fallback_playlist == "global_fallback"
        assert engine.max_history == 50
        assert engine.smart_shuffle is True

    def test_configuration(self):
        """Test configuration updates."""
        engine = AutoplayEngine(123)

        config = {
            "enabled": False,
            "strategy": "similar_genre",
            "max_history": 100
        }

        engine.configure(config)

        assert engine.enabled is False
        assert engine.strategy == "similar_genre"
        assert engine.max_history == 100

    @pytest.mark.asyncio
    async def test_fetch_next_track_disabled(self):
        """Test fetch returns None when disabled."""
        engine = AutoplayEngine(123)
        engine.enabled = False

        track = await engine.fetch_next_track({})
        assert track is None

    @pytest.mark.asyncio
    async def test_fetch_next_track_shutdown(self):
        """Test fetch returns None when shutting down."""
        engine = AutoplayEngine(123)
        await engine.stop()

        track = await engine.fetch_next_track({})
        assert track is None

    def test_register_strategy(self):
        """Test strategy registration."""
        engine = AutoplayEngine(123)

        async def strategy(context):
            return []
        engine.register_strategy("test_strategy", strategy)

        assert "test_strategy" in engine._strategies

    def test_register_scorer(self):
        """Test scorer registration."""
        engine = AutoplayEngine(123)

        async def scorer(t1, t2):
            return 0.5
        engine.register_scorer("test_scorer", scorer)

        assert "test_scorer" in engine._scorers

    def test_register_provider(self):
        """Test provider registration."""
        engine = AutoplayEngine(123)

        provider = type('Provider', (), {'get_tracks': lambda limit: []})()
        engine.register_provider("test_provider", provider)

        assert "test_provider" in engine._providers
