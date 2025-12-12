"""Queue metrics for intelligence features."""

import time
from collections import Counter

from ..track import Track


class QueueMetrics:
    """Metrics for queue intelligence."""

    def __init__(self) -> None:
        self.track_plays: Counter[str] = Counter()
        self.track_skips: Counter[str] = Counter()
        self.track_lifespan: dict[str, float] = {}
        self.session_start = time.time()
        self.skip_fatigue_threshold = 3  # Max skips per track per session

    def record_play(self, track: Track) -> None:
        """Record a track play."""
        self.track_plays[track.title] += 1

    def record_skip(self, track: Track) -> None:
        """Record a track skip."""
        self.track_skips[track.title] += 1

    def is_skip_fatigued(self, track: Track) -> bool:
        """Check if track is skip fatigued."""
        return self.track_skips[track.title] >= self.skip_fatigue_threshold

    def get_popularity_score(self, track: Track) -> float:
        """Get popularity score for track."""
        plays = self.track_plays[track.title]
        skips = self.track_skips[track.title]
        total = plays + skips
        return plays / total if total > 0 else 0.0

    def get_heatmap(self) -> dict[str, int]:
        """Get popularity heatmap."""
        return dict(self.track_plays.most_common(10))
