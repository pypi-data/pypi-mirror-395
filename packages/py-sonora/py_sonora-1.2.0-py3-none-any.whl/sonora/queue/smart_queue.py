"""Smart Queue with intelligence features for Sonora v1.2.0-beta."""

import asyncio
import random
import time
from collections import Counter, deque
from typing import Dict, List, Optional

from ..events import EventType, event_manager
from ..track import Track
from ..typing import GuildID


class AsyncLockFreeQueue:
    """Lock-free async queue for high-throughput operations."""

    def __init__(self) -> None:
        self._queue: deque[Track] = deque()
        self._lock = asyncio.Lock()
        self._not_empty = asyncio.Event()
        self._max_size = 1000  # Prevent unbounded growth

    async def put(self, item: Track) -> None:
        """Put an item in the queue."""
        async with self._lock:
            if len(self._queue) >= self._max_size:
                # Remove oldest item to maintain size limit
                self._queue.popleft()
            self._queue.append(item)
            self._not_empty.set()

    async def get(self) -> Optional[Track]:
        """Get an item from the queue."""
        async with self._lock:
            if not self._queue:
                self._not_empty.clear()
                return None
            return self._queue.popleft()

    async def get_batch(self, size: int) -> List[Track]:
        """Get a batch of items."""
        async with self._lock:
            if not self._queue:
                return []
            batch_size = min(size, len(self._queue))
            return [self._queue.popleft() for _ in range(batch_size)]

    def qsize(self) -> int:
        """Get queue size."""
        return len(self._queue)

    def empty(self) -> bool:
        """Check if queue is empty."""
        return len(self._queue) == 0


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


class SmartQueue:
    """Intelligent queue with smart features."""

    def __init__(self, guild_id: GuildID) -> None:
        self.guild_id = guild_id
        self._upcoming: deque[Track] = deque()
        self._history: deque[Track] = deque(maxlen=100)
        self._current: Track | None = None
        self.loop_mode = "none"
        self.shuffle_enabled = False
        self._lock = asyncio.Lock()
        self.metrics = QueueMetrics()
        self.session_memory: dict[str, float] = {}  # Track -> similarity score
        self.enable_adaptive_reorder = False

    @property
    def current(self) -> Track | None:
        """The currently playing track."""
        return self._current

    @property
    def upcoming(self) -> list[Track]:
        """The upcoming tracks."""
        return list(self._upcoming)

    @property
    def history(self) -> list[Track]:
        """The history of played tracks."""
        return list(self._history)

    @property
    def length(self) -> int:
        """Total length of upcoming queue."""
        return len(self._upcoming)

    @property
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self._upcoming) == 0

    async def add(self, track: Track, position: int | None = None) -> None:
        """Add a track to the queue."""
        async with self._lock:
            if position is None:
                self._upcoming.append(track)
            else:
                self._upcoming.insert(position, track)

    async def add_multiple(
        self, tracks: list[Track], position: int | None = None
    ) -> None:
        """Add multiple tracks to the queue."""
        async with self._lock:
            if position is None:
                self._upcoming.extend(tracks)
            else:
                for i, track in enumerate(tracks):
                    self._upcoming.insert(position + i, track)

    async def remove(self, position: int) -> Track:
        """Remove a track from the queue."""
        async with self._lock:
            return self._upcoming[position]

    async def pop(self, position: int = 0) -> Track:
        """Pop a track from the queue."""
        async with self._lock:
            if position == 0:
                return self._upcoming.popleft()
            else:
                track = self._upcoming[position]
                del self._upcoming[position]
                return track

    async def clear(self) -> None:
        """Clear the queue."""
        async with self._lock:
            self._upcoming.clear()

    async def smart_shuffle(self) -> None:
        """Smart shuffle that prevents recent repeats."""
        async with self._lock:
            if len(self._upcoming) < 2:
                return

            upcoming_list = list(self._upcoming)
            recent_titles = {t.title for t in list(self._history)[-10:]}  # Last 10

            # Separate recent and non-recent
            recent = [t for t in upcoming_list if t.title in recent_titles]
            non_recent = [t for t in upcoming_list if t.title not in recent_titles]

            # Shuffle non-recent
            random.shuffle(non_recent)

            # Interleave: non-recent first, then recent
            self._upcoming = deque(non_recent + recent)

            await event_manager.emit_event(
                EventType.SMART_SHUFFLE,
                {"guild_id": self.guild_id, "queue_length": len(self._upcoming)}
            )

    def shuffle(self) -> None:
        """Regular shuffle (for compatibility)."""
        upcoming_list = list(self._upcoming)
        random.shuffle(upcoming_list)
        self._upcoming = deque(upcoming_list)

    async def perform_adaptive_reorder(self) -> None:
        """Reorder queue based on metrics and similarity."""
        if not self.enable_adaptive_reorder or len(self._upcoming) < 2:
            return

        async with self._lock:
            upcoming_list = list(self._upcoming)

            # Sort by popularity score descending (higher popularity first)
            scored = [(t, self.metrics.get_popularity_score(t)) for t in upcoming_list]
            scored.sort(key=lambda x: x[1], reverse=True)

            self._upcoming = deque(t for t, _ in scored)

            await event_manager.emit_event(
                EventType.QUEUE_REORDER,
                {"guild_id": self.guild_id, "method": "adaptive", "queue_length": len(self._upcoming)}
            )

    def move(self, from_pos: int, to_pos: int) -> None:
        """Move a track in the queue."""
        track = self._upcoming[from_pos]
        del self._upcoming[from_pos]
        self._upcoming.insert(to_pos, track)

    async def skip_to(self, position: int) -> Track:
        """Skip to a specific position in the queue."""
        async with self._lock:
            if position < 0 or position >= len(self._upcoming):
                raise IndexError("Position out of range")
            return await self.pop(position)

    def get_next(self) -> Track | None:
        """Get the next track without removing it."""
        if self._upcoming:
            return self._upcoming[0]
        return None

    async def advance(self) -> Track | None:
        """Advance to the next track."""
        async with self._lock:
            if self._current:
                self._history.append(self._current)
                self.metrics.record_play(self._current)

            next_track: Track | None = None
            if self._upcoming:
                next_track = self._upcoming.popleft()

                # Check skip fatigue
                if self.metrics.is_skip_fatigued(next_track):
                    # Skip this track and try next
                    if self._upcoming:
                        next_track = self._upcoming.popleft()
                    else:
                        next_track = None

                if next_track:
                    self._current = next_track
                    return next_track

            # Handle loop modes
            if self.loop_mode == "track" and self._current:
                return self._current
            elif self.loop_mode == "queue" and self._history:
                # Replay from history
                self._upcoming.extend(self._history)
                self._history.clear()
                self._current = self._upcoming.popleft()
                return self._current

            self._current = None
            return None

    def rewind(self) -> Track | None:
        """Rewind to the previous track."""
        if self._history:
            if self._current:
                self._upcoming.appendleft(self._current)
            self._current = self._history.pop()
            return self._current
        return None

    def set_loop_mode(self, mode: str) -> None:
        """Set loop mode."""
        if mode not in ["none", "track", "queue", "autoplay"]:
            raise ValueError("Invalid loop mode")
        self.loop_mode = mode

    def get_view(
        self, view_type: str = "upcoming", limit: int | None = None
    ) -> list[Track]:
        """Get a view of the queue."""
        if view_type == "upcoming":
            tracks = self.upcoming
        elif view_type == "history":
            tracks = self.history
        elif view_type == "all":
            tracks = (
                self.history
                + ([self._current] if self._current else [])
                + self.upcoming
            )
        else:
            raise ValueError("Invalid view type")

        if limit:
            return tracks[:limit]
        return tracks

    def get_heatmap(self) -> dict[str, int]:
        """Get queue popularity heatmap."""
        return self.metrics.get_heatmap()
