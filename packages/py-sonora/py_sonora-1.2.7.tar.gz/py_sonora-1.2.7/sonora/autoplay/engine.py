"""Smart Autoplay Engine for Sonora v1.2.0-beta."""

import asyncio
import logging
from typing import Any, Protocol

from ..events import EventType, event_manager
from ..track import Track
from ..typing import GuildID

logger = logging.getLogger(__name__)


class SimilarityScorer(Protocol):
    """Protocol for similarity scoring between tracks."""

    async def score(self, track1: Track, track2: Track) -> float:
        """Score similarity between two tracks (0.0 to 1.0)."""
        ...


class RecommendationStrategy(Protocol):
    """Protocol for recommendation strategies."""

    async def recommend(self, context: dict[str, Any]) -> list[Track]:
        """Recommend tracks based on context."""
        ...


class AutoplayEngine:
    """Smart autoplay engine with context-aware recommendations."""

    def __init__(self, guild_id: GuildID, client: Any = None):
        self.guild_id = guild_id
        self.client = client
        self.enabled = True
        self.strategy = "similar_artist"
        self.fallback_playlist = "global_fallback"
        self.max_history = 50
        self.smart_shuffle = True
        self._strategies: dict[str, RecommendationStrategy] = {}
        self._scorers: dict[str, SimilarityScorer] = {}
        self._providers: dict[str, Any] = {}
        self._task: asyncio.Task | None = None
        self._shutdown = False

        # Register default strategies
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default strategies and scorers."""
        # This would be implemented with actual strategy classes
        pass

    async def start(self) -> None:
        """Start the autoplay engine."""
        self._shutdown = False
        logger.info(f"Autoplay engine started for guild {self.guild_id}")

    async def stop(self) -> None:
        """Stop the autoplay engine."""
        self._shutdown = True
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info(f"Autoplay engine stopped for guild {self.guild_id}")

    async def fetch_next_track(self, context: dict[str, Any]) -> Track | None:
        """Fetch the next track for autoplay."""
        if not self.enabled or self._shutdown:
            return None

        await event_manager.emit_event(
            EventType.AUTOPLAY_FETCH, {"guild_id": self.guild_id, "context": context}
        )

        try:
            strategy = self._strategies.get(self.strategy)
            if not strategy:
                logger.warning(f"Strategy {self.strategy} not found, using fallback")
                return await self._fetch_fallback_track(context)

            recommendations = await strategy.recommend(context)
            if recommendations:
                track = recommendations[0]
                await event_manager.emit_event(
                    EventType.AUTOPLAY_START,
                    {"guild_id": self.guild_id, "track": track, "strategy": self.strategy}
                )
                return track
            else:
                return await self._fetch_fallback_track(context)

        except Exception as e:
            logger.error(f"Autoplay fetch failed: {e}")
            await event_manager.emit_event(
                EventType.AUTOPLAY_FAIL,
                {"guild_id": self.guild_id, "error": str(e), "strategy": self.strategy}
            )
            return await self._fetch_fallback_track(context)

    async def _fetch_fallback_track(self, context: dict[str, Any]) -> Track | None:
        """Fetch a fallback track when primary strategy fails."""
        provider = self._providers.get(self.fallback_playlist)
        if provider:
            try:
                tracks = await provider.get_tracks(limit=1)
                if tracks:
                    return tracks[0]  # type: ignore
            except Exception as e:
                logger.error(f"Fallback provider failed: {e}")

        # Ultimate fallback: return None
        return None

    def register_strategy(self, name: str, strategy: RecommendationStrategy) -> None:
        """Register a recommendation strategy."""
        self._strategies[name] = strategy

    def register_scorer(self, name: str, scorer: SimilarityScorer) -> None:
        """Register a similarity scorer."""
        self._scorers[name] = scorer

    def register_provider(self, name: str, provider: Any) -> None:
        """Register a track provider."""
        self._providers[name] = provider

    def configure(self, config: dict[str, Any]) -> None:
        """Configure the autoplay engine."""
        self.enabled = config.get("enabled", self.enabled)
        self.strategy = config.get("strategy", self.strategy)
        self.fallback_playlist = config.get("fallback_playlist", self.fallback_playlist)
        self.max_history = config.get("max_history", self.max_history)
        self.smart_shuffle = config.get("smart_shuffle", self.smart_shuffle)
