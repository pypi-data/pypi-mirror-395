"""YouTube plugin for Sonora."""

import aiohttp

from ..exceptions import TrackException
from ..track import Track


class YouTubePlugin:
    """YouTube search and loading plugin."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.session: aiohttp.ClientSession | None = None

    async def _ensure_session(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def search(self, query: str, limit: int = 10) -> list[Track]:
        """Search YouTube for tracks."""
        await self._ensure_session()

        if not self.api_key:
            # Fallback to yt-dlp or similar
            return await self._search_fallback(query, limit)

        # Use YouTube Data API
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": str(limit),
            "key": self.api_key,
        }

        if self.session is not None:
            async with self.session.get(url, params=params) as resp:
                if resp.status != 200:
                    raise TrackException(f"YouTube API error: {resp.status}")

                data = await resp.json()
                tracks = []

                for item in data.get("items", []):
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]

                    track = Track(
                        track=f"ytsearch:{query}",  # Placeholder
                        info={
                            "identifier": video_id,
                            "isSeekable": True,
                            "author": snippet["channelTitle"],
                            "length": 0,  # Would need another API call
                            "isStream": False,
                            "position": 0,
                            "title": snippet["title"],
                            "uri": f"https://www.youtube.com/watch?v={video_id}",
                            "sourceName": "youtube",
                        },
                    )
                    tracks.append(track)

                return tracks

        return []

    async def _search_fallback(self, query: str, limit: int) -> list[Track]:
        """Fallback search using yt-dlp or similar."""
        # This would integrate with yt-dlp
        # For now, return empty list
        return []

    async def load_track(self, url: str) -> Track | None:
        """Load a YouTube track by URL."""
        # Implementation would use Lavalink's loadTracks
        # This is a placeholder
        return None

    async def close(self) -> None:
        if self.session:
            await self.session.close()
