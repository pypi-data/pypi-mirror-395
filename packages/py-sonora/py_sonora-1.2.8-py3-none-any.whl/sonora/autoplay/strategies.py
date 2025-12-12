"""Recommendation strategies for autoplay."""

from typing import Any

from ..track import Track
from .scorer import CompositeSimilarityScorer


class SimilarArtistStrategy:
    """Recommend tracks by similar artists."""

    def __init__(self, track_provider: Any):
        self.track_provider = track_provider

    async def recommend(self, context: dict[str, Any]) -> list[Track]:
        """Recommend tracks similar to current context."""
        history = context.get("history", [])
        if not history:
            return []

        current_track = history[-1]
        if not current_track.author:
            return []

        # Get tracks by same artist
        try:
            tracks = await self.track_provider.search(f"artist:{current_track.author}", limit=10)
            # Filter out already played tracks
            played_titles = {t.title for t in history}
            recommendations = [t for t in tracks if t.title not in played_titles]
            return recommendations[:5]
        except Exception:
            return []


class SimilarGenreStrategy:
    """Recommend tracks by similar genre."""

    def __init__(self, track_provider: Any):
        self.track_provider = track_provider

    async def recommend(self, context: dict[str, Any]) -> list[Track]:
        """Recommend tracks similar in genre."""
        history = context.get("history", [])
        if not history:
            return []

        current_track = history[-1]

        # Use title keywords as genre proxy
        keywords = current_track.title.lower().split()[:3]  # First 3 words
        query = " ".join(keywords)

        try:
            tracks = await self.track_provider.search(query, limit=10)
            # Filter out already played
            played_titles = {t.title for t in history}
            recommendations = [t for t in tracks if t.title not in played_titles]
            return recommendations[:5]
        except Exception:
            return []


class PopularityBasedStrategy:
    """Recommend popular tracks."""

    def __init__(self, track_provider: Any):
        self.track_provider = track_provider

    async def recommend(self, context: dict[str, Any]) -> list[Track]:
        """Recommend popular tracks."""
        try:
            # Placeholder for popular tracks
            tracks = await self.track_provider.get_popular(limit=5)
            history = context.get("history", [])
            played_titles = {t.title for t in history}
            recommendations = [t for t in tracks if t.title not in played_titles]
            return recommendations
        except Exception:
            return []


class RandomStrategy:
    """Random track recommendation."""

    def __init__(self, track_provider: Any):
        self.track_provider = track_provider

    async def recommend(self, context: dict[str, Any]) -> list[Track]:
        """Recommend random tracks."""
        try:
            tracks = await self.track_provider.get_random(limit=5)
            return tracks  # type: ignore
        except Exception:
            return []


class SmartRecommendationStrategy:
    """Smart strategy using similarity scoring."""

    def __init__(self, track_provider: Any, scorer: CompositeSimilarityScorer):
        self.track_provider = track_provider
        self.scorer = scorer

    async def recommend(self, context: dict[str, Any]) -> list[Track]:
        """Smart recommendations based on similarity."""
        history = context.get("history", [])
        if not history:
            return []

        current_track = history[-1]

        # Get candidate tracks
        try:
            candidates = await self.track_provider.search("", limit=20)  # Broad search
        except Exception:
            return []

        # Score candidates
        scored_candidates = []
        for candidate in candidates:
            if candidate.title in {t.title for t in history}:
                continue  # Skip already played

            score = await self.scorer.score(current_track, candidate)
            scored_candidates.append((candidate, score))

        # Sort by score descending
        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        return [track for track, score in scored_candidates[:5]]
