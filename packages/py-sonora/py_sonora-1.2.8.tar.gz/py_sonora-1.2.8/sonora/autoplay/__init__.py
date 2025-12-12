"""Autoplay module for Sonora v1.2.0-beta."""

from .engine import AutoplayEngine
from .scorer import (
    ArtistSimilarityScorer,
    CompositeSimilarityScorer,
    GenreSimilarityScorer,
)
from .strategies import (
    PopularityBasedStrategy,
    SimilarArtistStrategy,
    SimilarGenreStrategy,
)

__all__ = [
    "AutoplayEngine",
    "ArtistSimilarityScorer",
    "GenreSimilarityScorer",
    "CompositeSimilarityScorer",
    "SimilarArtistStrategy",
    "SimilarGenreStrategy",
    "PopularityBasedStrategy",
]
