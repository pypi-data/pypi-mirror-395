"""
Motus Command: Command Center for AI Agents

Real-time observability and memory for AI coding assistants.

Usage:
    # CLI
    $ mc watch     # Watch active Claude session
    $ mc list      # List sessions
    $ mc summary   # Generate AI memory for CLAUDE.md

    # SDK (for any Python agent)
    from motus_command import Tracer

    tracer = Tracer("my-agent")

    @tracer.track
    def my_agent_step(prompt):
        # Your agent logic
        return response

    # Or explicit logging
    tracer.thinking("Deciding which approach...")
    tracer.tool("WebSearch", {"query": "python tips"})
    tracer.decision("Using async because batch is large")
"""

__version__ = "0.3.0"
__author__ = "Ben Voss"

# Core events
# Configuration
from .config import MCConfig, config

# Drift detection
from .drift_detector import DriftDetector, DriftSignal, DriftState, get_drift_detector
from .events import DecisionEvent, ThinkingEvent, ToolEvent

# Exceptions
from .exceptions import (
    ConfigError,
    MCError,
    SessionError,
    SessionNotFoundError,
    SessionParseError,
    TranscriptError,
    WebError,
)

# Logging
from .logging import get_logger

# Session management
from .session_manager import SessionContext, SessionInfo, SessionManager, find_claude_sessions

# Tracer SDK
from .tracer import Tracer, get_tracer

__all__ = [
    # SDK
    "Tracer",
    "get_tracer",
    # Events
    "ThinkingEvent",
    "ToolEvent",
    "DecisionEvent",
    # Config
    "config",
    "MCConfig",
    # Sessions
    "SessionInfo",
    "SessionContext",
    "SessionManager",
    "find_claude_sessions",
    # Logging
    "get_logger",
    # Exceptions
    "MCError",
    "SessionError",
    "SessionNotFoundError",
    "SessionParseError",
    "ConfigError",
    "WebError",
    "TranscriptError",
    # Drift Detection
    "DriftDetector",
    "DriftSignal",
    "DriftState",
    "get_drift_detector",
    # Meta
    "__version__",
]
