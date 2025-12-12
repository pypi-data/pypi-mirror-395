"""Track and Playlist models for Sonora."""

from typing import Any

from pydantic import BaseModel


class Track(BaseModel):
    """Represents a Lavalink track."""

    track: str
    info: dict[str, Any]

    @property
    def identifier(self) -> str:
        """The track identifier."""
        return str(self.info["identifier"])

    @property
    def is_seekable(self) -> bool:
        """Whether the track is seekable."""
        return bool(self.info["isSeekable"])

    @property
    def author(self) -> str:
        """The track author."""
        return str(self.info["author"])

    @property
    def length(self) -> int:
        """The track length in milliseconds."""
        return int(self.info["length"])

    @property
    def is_stream(self) -> bool:
        """Whether the track is a stream."""
        return bool(self.info["isStream"])

    @property
    def position(self) -> int:
        """The current position in the track."""
        return int(self.info["position"])

    @property
    def title(self) -> str:
        """The track title."""
        return str(self.info["title"])

    @property
    def uri(self) -> str | None:
        """The track URI."""
        uri = self.info.get("uri")
        return str(uri) if uri is not None else None

    @property
    def source_name(self) -> str | None:
        """The source name."""
        source = self.info.get("sourceName")
        return str(source) if source is not None else None


class Playlist(BaseModel):
    """Represents a Lavalink playlist."""

    name: str
    selected_track: int | None
    tracks: list[Track]
