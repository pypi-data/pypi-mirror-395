"""Sonora - A full-featured Python Lavalink client for Discord music bots."""

__version__ = "1.2.0"
__author__ = "code-xon"
__maintainer__ = "Ramkrishna"
__email__ = "ramkrishna@code-xon.fun"
__license__ = "MIT"

from .autoplay import AutoplayEngine
from .autoplay import AutoplayEngine
from .client import SonoraClient
from .events import EventManager, EventType, event_manager
from .exceptions import LavalinkException, NodeException, SonoraError
from .filters import Equalizer, FilterManager, Karaoke, Timescale
from .node import Node
from .performance import (
    AsyncProfiler,
    BackpressureController,
    PerformanceMonitor,
    async_profiler,
    backpressure_controller,
    performance_monitor,
)
from .player import Player
from .queue import SmartQueue
from .security import (
    AutoplaySecurityManager,
    CredentialManager,
    PluginSecurityManager,
    autoplay_security,
    credential_manager,
    plugin_security,
)
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
    "PerformanceMonitor",
    "AsyncProfiler",
    "BackpressureController",
    "performance_monitor",
    "async_profiler",
    "backpressure_controller",
    "CredentialManager",
    "AutoplaySecurityManager",
    "PluginSecurityManager",
    "credential_manager",
    "autoplay_security",
    "plugin_security",
]
