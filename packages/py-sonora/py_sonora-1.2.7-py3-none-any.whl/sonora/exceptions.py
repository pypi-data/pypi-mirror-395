"""Exceptions for Sonora."""

from enum import Enum


class ErrorCategory(Enum):
    """Categories for Sonora errors."""

    AUTHENTICATION = "authentication"
    CONNECTION = "connection"
    PLAYER = "player"
    TRACK = "track"
    NODE = "node"
    QUEUE = "queue"
    UNKNOWN = "unknown"


class SonoraError(Exception):
    """Base exception for Sonora with detailed categories."""

    def __init__(self, message: str, category: ErrorCategory = ErrorCategory.UNKNOWN):
        super().__init__(message)
        self.category = category


class LavalinkException(SonoraError):
    """Exception raised for Lavalink-related errors."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.CONNECTION)


class NodeException(SonoraError):
    """Exception raised for node-related errors."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.NODE)


class PlayerException(SonoraError):
    """Exception raised for player-related errors."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.PLAYER)


class TrackException(SonoraError):
    """Exception raised for track-related errors."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.TRACK)


class QueueException(SonoraError):
    """Exception raised for queue-related errors."""

    def __init__(self, message: str):
        super().__init__(message, ErrorCategory.QUEUE)
