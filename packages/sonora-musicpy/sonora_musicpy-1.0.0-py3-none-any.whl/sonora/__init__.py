"""Sonora - A full-featured Python Lavalink client for Discord music bots."""

__version__ = "1.0.0"
__author__ = "code-xon"
__maintainer__ = "Ramkrishna"
__email__ = "ramkrishna@code-xon.fun"
__license__ = "MIT"

from .client import SonoraClient
from .exceptions import SonoraException, LavalinkException, NodeException
from .player import Player
from .track import Track, Playlist
from .node import Node
from .queue import Queue
from .filters import FilterManager, Equalizer, Karaoke, Timescale
from .events import EventManager, EventType, event_manager

__all__ = [
    "SonoraClient",
    "Player",
    "Track",
    "Playlist",
    "Node",
    "Queue",
    "FilterManager",
    "Equalizer",
    "Karaoke",
    "Timescale",
    "EventManager",
    "EventType",
    "event_manager",
    "SonoraException",
    "LavalinkException",
    "NodeException",
]