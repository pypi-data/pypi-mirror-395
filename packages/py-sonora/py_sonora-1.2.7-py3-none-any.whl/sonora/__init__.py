"""Sonora - A full-featured Python Lavalink client for Discord music bots."""

__version__ = "1.2.7"
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
from .diagnostics import (
    PlaybackTimelineDebugger,
    PerformanceProfiler,
    PlayerIntrospector,
    ReproduciblePlaybackEngine,
    StructuredLogger,
    WiretapDebugger,
    performance_profiler,
    playback_engine,
    player_introspector,
    structured_logger,
    timeline_debugger,
    wiretap_debugger,
)
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
from .sdk import SonoraMusicBotSDK, SonoraVoiceSDK
from .security import (
    AutoplaySecurityManager,
    CredentialManager,
    PluginSecurityManager,
    SecureDeserializationLayer,
    autoplay_security,
    credential_manager,
    plugin_security,
)
from .simulator import (
    MockFactory,
    ProtocolSimulator,
    SimulatedNode,
    mock_factory,
    protocol_simulator,
)
from .snapshot import SessionSnapshot, SnapshotManager, snapshot_manager
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
    # Performance
    "PerformanceMonitor",
    "AsyncProfiler",
    "BackpressureController",
    "performance_monitor",
    "async_profiler",
    "backpressure_controller",
    # Security
    "CredentialManager",
    "AutoplaySecurityManager",
    "PluginSecurityManager",
    "SecureDeserializationLayer",
    "credential_manager",
    "autoplay_security",
    "plugin_security",
    # SDK
    "SonoraMusicBotSDK",
    "SonoraVoiceSDK",
    # Simulator
    "ProtocolSimulator",
    "SimulatedNode",
    "MockFactory",
    "protocol_simulator",
    "mock_factory",
    # Snapshot
    "SessionSnapshot",
    "SnapshotManager",
    "snapshot_manager",
    # Diagnostics
    "PerformanceProfiler",
    "StructuredLogger",
    "WiretapDebugger",
    "PlayerIntrospector",
    "PlaybackTimelineDebugger",
    "ReproduciblePlaybackEngine",
    "performance_profiler",
    "structured_logger",
    "wiretap_debugger",
    "player_introspector",
    "timeline_debugger",
    "playback_engine",
]
