"""Sonora - A full-featured Python Lavalink client for Discord music bots."""

__version__ = "1.2.0-beta"
__author__ = "code-xon"
__maintainer__ = "Ramkrishna"
__email__ = "ramkrishna@code-xon.fun"
__license__ = "MIT"

from .autoplay import AutoplayEngine
from .client import SonoraClient
from .events import EventManager, EventType, event_manager
from .exceptions import LavalinkException, NodeException, SonoraError
from .filters import Equalizer, FilterManager, Karaoke, Timescale
from .node import Node
from .player import Player
from .queue import SmartQueue
from .track import Playlist, Track

__all__ = [
    "SonoraClient",
    "Player",
    "Track",
    "Playlist",
    "Node",
    "SmartQueue",
    "AutoplayEngine",
    "FilterManager",
    "Equalizer",
    "Karaoke",
    "Timescale",
    "EventManager",
    "EventType",
    "event_manager",
    "SonoraError",
    "LavalinkException",
    "NodeException",
]
