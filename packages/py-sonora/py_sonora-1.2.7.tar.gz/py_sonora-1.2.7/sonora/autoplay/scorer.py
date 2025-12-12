"""Similarity scorers for autoplay recommendations."""


from ..track import Track


class ArtistSimilarityScorer:
    """Score similarity based on artist matching."""

    async def score(self, track1: Track, track2: Track) -> float:
        """Score similarity between tracks based on artist."""
        if not track1.author or not track2.author:
            return 0.0

        author1 = track1.author.lower()
        author2 = track2.author.lower()

        if author1 == author2:
            return 1.0

        # Partial match
        if author1 in author2 or author2 in author1:
            return 0.7

        return 0.0


class GenreSimilarityScorer:
    """Score similarity based on genre tags."""

    async def score(self, track1: Track, track2: Track) -> float:
        """Score similarity based on genre."""
        # For now, use title keywords as proxy for genre
        # In real implementation, would use metadata or external APIs
        keywords1 = set(track1.title.lower().split())
        keywords2 = set(track2.title.lower().split())

        intersection = keywords1 & keywords2
        union = keywords1 | keywords2

        if not union:
            return 0.0

        return len(intersection) / len(union)


class PopularitySimilarityScorer:
    """Score similarity based on popularity."""

    async def score(self, track1: Track, track2: Track) -> float:
        """Score based on popularity (placeholder)."""
        # Placeholder - would use actual popularity metrics
        return 0.5


class CompositeSimilarityScorer:
    """Combine multiple scorers with weights."""

    def __init__(self, scorers: dict[str, float]):
        self.scorers = scorers

    async def score(self, track1: Track, track2: Track) -> float:
        """Combined score."""
        total_score = 0.0
        total_weight = 0.0

        for scorer, weight in self.scorers.items():
            if scorer == "artist":
                score = await ArtistSimilarityScorer().score(track1, track2)
            elif scorer == "genre":
                score = await GenreSimilarityScorer().score(track1, track2)
            elif scorer == "popularity":
                score = await PopularitySimilarityScorer().score(track1, track2)
            else:
                continue

            total_score += score * weight
            total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0
