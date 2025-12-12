"""Shared typing definitions for Sonora."""

from typing import Any

# Node configuration
NodeConfig = dict[str, str | int | bool]

# Lavalink op codes
OpCode = str

# Track info
TrackInfo = dict[str, Any]

# Player state
PlayerState = dict[str, Any]

# Event data
EventData = dict[str, Any]

# Guild ID type
GuildID = int

# User ID type
UserID = int
