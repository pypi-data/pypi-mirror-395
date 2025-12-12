"""
MC Exception Classes.

Proper exception hierarchy for error handling throughout MC.
"""

from typing import Optional


class MCError(Exception):
    """Base exception for all MC errors."""

    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class SessionError(MCError):
    """Error related to session operations."""

    def __init__(
        self, message: str, session_id: Optional[str] = None, details: Optional[str] = None
    ):
        self.session_id = session_id
        super().__init__(message, details)


class SessionNotFoundError(SessionError):
    """Session file or directory not found."""

    pass


class SessionParseError(SessionError):
    """Error parsing session transcript."""

    pass


class ConfigError(MCError):
    """Configuration-related error."""

    pass


class WebError(MCError):
    """Web UI related error."""

    pass


class WebSocketError(WebError):
    """WebSocket connection error."""

    pass


class ProcessDetectionError(MCError):
    """Error detecting running Claude processes."""

    pass


class TranscriptError(MCError):
    """Error reading or parsing transcript files."""

    pass


class TracerError(MCError):
    """Error in the MC tracer/SDK."""

    pass


class HookError(MCError):
    """Error in MC hooks."""

    pass
