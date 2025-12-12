"""Advanced queue management for Sonora."""

from collections import deque
from typing import Deque, List, Optional
from .track import Track


class Queue:
    """Advanced queue with history and multiple views."""

    def __init__(self):
        self._upcoming: Deque[Track] = deque()
        self._history: Deque[Track] = deque(maxlen=100)  # Keep last 100 tracks
        self._current: Optional[Track] = None
        self.loop_mode = "none"  # none, track, queue, autoplay
        self.shuffle_enabled = False

    @property
    def current(self) -> Optional[Track]:
        """The currently playing track."""
        return self._current

    @property
    def upcoming(self) -> List[Track]:
        """The upcoming tracks."""
        return list(self._upcoming)

    @property
    def history(self) -> List[Track]:
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

    def add(self, track: Track, position: Optional[int] = None) -> None:
        """Add a track to the queue."""
        if position is None:
            self._upcoming.append(track)
        else:
            self._upcoming.insert(position, track)

    def add_multiple(self, tracks: List[Track], position: Optional[int] = None) -> None:
        """Add multiple tracks to the queue."""
        if position is None:
            self._upcoming.extend(tracks)
        else:
            for i, track in enumerate(tracks):
                self._upcoming.insert(position + i, track)

    def remove(self, position: int) -> Track:
        """Remove a track from the queue."""
        return self._upcoming[position]

    def pop(self, position: int = 0) -> Track:
        """Pop a track from the queue."""
        if position == 0:
            return self._upcoming.popleft()
        else:
            track = self._upcoming[position]
            del self._upcoming[position]
            return track

    def clear(self) -> None:
        """Clear the queue."""
        self._upcoming.clear()

    def shuffle(self) -> None:
        """Shuffle the upcoming queue."""
        import random
        upcoming_list = list(self._upcoming)
        random.shuffle(upcoming_list)
        self._upcoming = deque(upcoming_list)

    def move(self, from_pos: int, to_pos: int) -> None:
        """Move a track in the queue."""
        track = self._upcoming[from_pos]
        del self._upcoming[from_pos]
        self._upcoming.insert(to_pos, track)

    def skip_to(self, position: int) -> Track:
        """Skip to a specific position in the queue."""
        if position < 0 or position >= len(self._upcoming):
            raise IndexError("Position out of range")
        return self.pop(position)

    def get_next(self) -> Optional[Track]:
        """Get the next track without removing it."""
        if self._upcoming:
            return self._upcoming[0]
        return None

    def advance(self) -> Optional[Track]:
        """Advance to the next track."""
        if self._current:
            self._history.append(self._current)

        if self._upcoming:
            self._current = self._upcoming.popleft()
            return self._current

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

    def rewind(self) -> Optional[Track]:
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

    def get_view(self, view_type: str = "upcoming", limit: Optional[int] = None) -> List[Track]:
        """Get a view of the queue."""
        if view_type == "upcoming":
            tracks = self.upcoming
        elif view_type == "history":
            tracks = self.history
        elif view_type == "all":
            tracks = self.history + ([self._current] if self._current else []) + self.upcoming
        else:
            raise ValueError("Invalid view type")

        if limit:
            return tracks[:limit]
        return tracks