"""Track and Playlist models for Sonora."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class Track(BaseModel):
    """Represents a Lavalink track."""

    track: str
    info: Dict[str, Any]

    @property
    def identifier(self) -> str:
        """The track identifier."""
        return self.info["identifier"]

    @property
    def is_seekable(self) -> bool:
        """Whether the track is seekable."""
        return self.info["isSeekable"]

    @property
    def author(self) -> str:
        """The track author."""
        return self.info["author"]

    @property
    def length(self) -> int:
        """The track length in milliseconds."""
        return self.info["length"]

    @property
    def is_stream(self) -> bool:
        """Whether the track is a stream."""
        return self.info["isStream"]

    @property
    def position(self) -> int:
        """The current position in the track."""
        return self.info["position"]

    @property
    def title(self) -> str:
        """The track title."""
        return self.info["title"]

    @property
    def uri(self) -> Optional[str]:
        """The track URI."""
        return self.info.get("uri")

    @property
    def source_name(self) -> Optional[str]:
        """The source name."""
        return self.info.get("sourceName")


class Playlist(BaseModel):
    """Represents a Lavalink playlist."""

    name: str
    selected_track: Optional[int]
    tracks: List[Track]