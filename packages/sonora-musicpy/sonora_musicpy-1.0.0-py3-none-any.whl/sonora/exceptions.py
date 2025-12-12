"""Exceptions for Sonora."""


class SonoraException(Exception):
    """Base exception for Sonora."""


class LavalinkException(SonoraException):
    """Exception raised for Lavalink-related errors."""


class NodeException(SonoraException):
    """Exception raised for node-related errors."""


class PlayerException(SonoraException):
    """Exception raised for player-related errors."""


class TrackException(SonoraException):
    """Exception raised for track-related errors."""