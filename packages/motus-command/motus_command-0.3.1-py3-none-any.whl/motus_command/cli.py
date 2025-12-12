#!/usr/bin/env python3
"""
Motus Command: See what your AI is thinking.

Usage:
    mc watch     - Watch active Claude Code session in real-time
    mc list      - List recent sessions
    mc dashboard - Multi-session dashboard view
    mc context   - Generate context summary for AI agents
"""

import argparse
import json
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Generator, Optional

if TYPE_CHECKING:
    from . import protocols

# Import logger - with fallback for direct module imports in tests
try:
    from .logging import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)  # type: ignore[assignment]

try:
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Missing dependency: rich")
    print("Run: pip install rich")
    sys.exit(1)

# Initialize Rich console
console = Console()

# Claude projects directory
CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"

# Import Codex parser for multi-source support
try:
    from .codex_parser import CodexTranscriptParser, get_codex_parser, parse_codex_line
except ImportError:
    CodexTranscriptParser = None  # type: ignore[assignment,misc]
    get_codex_parser = None  # type: ignore[assignment]
    parse_codex_line = None  # type: ignore[assignment]

# Import Gemini parser for multi-source support
try:
    from .gemini_parser import GeminiTranscriptParser, parse_gemini_file
except ImportError:
    GeminiTranscriptParser = None  # type: ignore[assignment,misc]
    parse_gemini_file = None  # type: ignore[assignment]

# Import shared utilities (single source of truth in commands.utils)
try:
    from .commands.utils import assess_risk, redact_secrets
except ImportError:
    from commands.utils import assess_risk, redact_secrets

# Import from centralized config
try:
    from .config import ARCHIVE_DIR, MC_STATE_DIR
except ImportError:
    from config import ARCHIVE_DIR, MC_STATE_DIR

# Lazy import of orchestrator to avoid circular import issues with TUI
_orchestrator_module = None
_protocols_module = None


def _get_orchestrator():
    """Lazy import of orchestrator to get the singleton instance."""
    global _orchestrator_module
    if _orchestrator_module is None:
        try:
            from . import orchestrator as _orch

            _orchestrator_module = _orch
        except ImportError:
            # In TUI standalone context, orchestrator is not available
            return None
    return _orchestrator_module.get_orchestrator()


def _get_protocol_types():
    """Lazy import of protocol types for type comparisons."""
    global _protocols_module
    if _protocols_module is None:
        try:
            from . import protocols as _proto

            _protocols_module = _proto
        except ImportError:
            return None
    return _protocols_module


# For backward compatibility, import these if possible (but don't fail)
try:
    from .orchestrator import get_orchestrator
    from .protocols import EventType, UnifiedEvent, UnifiedSession
except ImportError:
    # Set to None - functions that need these should use _get_orchestrator() and _get_protocol_types()
    get_orchestrator = None  # type: ignore[assignment,misc]
    EventType = None  # type: ignore[assignment,misc]
    UnifiedEvent = None  # type: ignore[assignment,misc]
    UnifiedSession = None  # type: ignore[assignment,misc]

# Ensure directories exist
MC_STATE_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)


@dataclass
class ThinkingEvent:
    content: str
    timestamp: datetime


@dataclass
class ToolEvent:
    name: str
    input: dict
    timestamp: datetime
    status: str = "running"
    output: Optional[str] = None
    risk_level: str = "safe"


@dataclass
class TaskEvent:
    """Rich Task/subagent event with full details."""

    description: str
    prompt: str
    subagent_type: str
    model: Optional[str]
    timestamp: datetime


@dataclass
class ErrorEvent:
    """Represents an error during session execution."""

    message: str
    timestamp: datetime
    error_type: str = "unknown"  # "tool_error", "api_error", "safety", "parse_error"
    tool_name: Optional[str] = None  # Tool that caused error, if applicable
    recoverable: bool = True


@dataclass
class FileChange:
    """Track file modifications for checkpoint awareness."""

    path: str
    operation: str
    timestamp: datetime


@dataclass
class SessionStats:
    """Track session statistics."""

    thinking_count: int = 0
    tool_count: int = 0
    agent_count: int = 0
    files_modified: set = field(default_factory=set)
    high_risk_ops: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    errors: list = field(default_factory=list)


@dataclass
class SessionInfo:
    session_id: str
    file_path: Path
    last_modified: datetime
    size: int
    is_active: bool = False
    project_path: str = ""  # Actual project path
    status: str = "idle"  # active, idle, crashed
    last_action: str = ""  # Last tool/action for crash recovery
    source: str = "claude"  # "claude", "codex", "gemini", "sdk"


def unified_session_to_session_info(unified: "protocols.UnifiedSession") -> SessionInfo:
    """
    Convert a UnifiedSession (from orchestrator) to SessionInfo (CLI format).

    This maintains backward compatibility with existing CLI code that uses SessionInfo.
    """
    from .protocols import SessionStatus

    # Map UnifiedSession.status (SessionStatus enum) to SessionInfo.status (str)
    status_map = {
        SessionStatus.ACTIVE: "active",
        SessionStatus.OPEN: "open",
        SessionStatus.CRASHED: "crashed",
        SessionStatus.IDLE: "idle",
        SessionStatus.ORPHANED: "orphaned",
    }

    status_str = status_map.get(unified.status, "idle")
    is_active = unified.status == SessionStatus.ACTIVE

    # Get file size
    try:
        size = unified.file_path.stat().st_size
    except OSError:
        size = 0

    # Get last action (will be populated by builders)
    last_action = ""

    return SessionInfo(
        session_id=unified.session_id,
        file_path=unified.file_path,
        last_modified=unified.last_modified,
        size=size,
        is_active=is_active,
        project_path=unified.project_path,
        status=status_str,
        last_action=last_action,
        source=unified.source.value,
    )


def unified_event_to_legacy(
    event: UnifiedEvent,
) -> ThinkingEvent | ToolEvent | TaskEvent | ErrorEvent | None:
    """
    Convert a UnifiedEvent (from orchestrator) to legacy event types.

    This maintains backward compatibility with existing CLI display code.

    Args:
        event: UnifiedEvent from orchestrator.get_events()

    Returns:
        One of ThinkingEvent, ToolEvent, TaskEvent, ErrorEvent, or None if unmappable.
    """
    if event.event_type == EventType.THINKING:
        return ThinkingEvent(
            content=event.content,
            timestamp=event.timestamp,
        )

    elif event.event_type == EventType.TOOL:
        return ToolEvent(
            name=event.tool_name or "unknown",
            input=event.tool_input or {},
            timestamp=event.timestamp,
            risk_level=event.risk_level.value if event.risk_level else "safe",
            status=event.tool_status.value if event.tool_status else "running",
            output=event.tool_output,
        )

    elif event.event_type == EventType.AGENT_SPAWN:
        return TaskEvent(
            description=event.agent_description or event.content,
            prompt=event.agent_prompt or "",
            subagent_type=event.agent_type or "unknown",
            model=event.agent_model or event.model,
            timestamp=event.timestamp,
        )

    elif event.event_type == EventType.ERROR:
        return ErrorEvent(
            message=event.content,
            timestamp=event.timestamp,
            error_type=event.raw_data.get("error_type", "unknown") if event.raw_data else "unknown",
            tool_name=event.tool_name,
        )

    # For other event types (DECISION, FILE_READ, etc.), we could convert them
    # but the legacy CLI doesn't have direct display formats for them yet.
    # Return None for now - they won't be displayed but won't break the flow.
    return None


def is_claude_process_running(project_path: str = "") -> bool:
    """Check if a Claude Code process is actively running.

    Uses SessionOrchestrator's ProcessDetector for cached, fail-silent detection.
    If project_path is provided, checks if that specific project has a running agent.
    """
    from .orchestrator import get_orchestrator

    orchestrator = get_orchestrator()
    if not project_path:
        # Check if any claude process is running
        return len(orchestrator.get_running_projects()) > 0
    else:
        # Check if specific project has running agent
        return orchestrator.is_project_active(project_path)


def archive_session(session_file: Path) -> bool:
    """Archive a session file to MC state directory archive."""
    try:
        # Create timestamped archive filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{session_file.stem}_{timestamp}.jsonl"
        archive_path = ARCHIVE_DIR / archive_name

        shutil.move(str(session_file), str(archive_path))
        logger.info(f"Archived session to {archive_path}")
        return True
    except OSError as e:
        logger.warning(f"Failed to archive session {session_file}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error archiving session {session_file}: {e}")
        return False


def delete_session(session_file: Path) -> bool:
    """Permanently delete a session file."""
    try:
        session_file.unlink()
        logger.info(f"Deleted session {session_file}")
        return True
    except OSError as e:
        logger.warning(f"Failed to delete session {session_file}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error deleting session {session_file}: {e}")
        return False


def format_age(modified: datetime) -> str:
    """Format age in human-readable form (e.g., '5m', '2h', '1d')."""
    age = datetime.now() - modified
    seconds = int(age.total_seconds())

    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        return f"{seconds // 3600}h"
    else:
        return f"{seconds // 86400}d"


def get_last_action(file_path: Path) -> str:
    """Get the last tool action from a session for crash recovery info."""
    try:
        # Read last few KB to find most recent action
        size = file_path.stat().st_size
        with open(file_path, "r") as f:
            if size > 5000:
                f.seek(size - 5000)
            content = f.read()

        # Find last tool use
        last_action = ""
        for line in content.strip().split("\n"):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if data.get("type") == "assistant":
                    message = data.get("message", {})
                    content_blocks = message.get("content", [])
                    if isinstance(content_blocks, list):
                        for block in content_blocks:
                            if block.get("type") == "tool_use":
                                name = block.get("name", "")
                                inp = block.get("input", {})
                                if name == "Edit":
                                    last_action = f"Edit {inp.get('file_path', '')}"
                                elif name == "Write":
                                    last_action = f"Write {inp.get('file_path', '')}"
                                elif name == "Bash":
                                    cmd = inp.get("command", "")[:50]
                                    last_action = f"Bash: {cmd}"
                                elif name == "Read":
                                    last_action = f"Read {inp.get('file_path', '')}"
                                else:
                                    last_action = name
            except json.JSONDecodeError:
                continue
        return last_action
    except OSError as e:
        logger.debug(f"Error reading session file {file_path}: {e}")
        return ""
    except Exception as e:
        logger.warning(f"Unexpected error getting last action from {file_path}: {e}")
        return ""


def get_running_claude_projects() -> set[str]:
    """Get project paths where Claude processes are currently running.

    Uses SessionOrchestrator's ProcessDetector for cached, fail-silent detection.
    Returns a set of project paths that have active Claude processes.
    """
    from .orchestrator import get_orchestrator

    orchestrator = get_orchestrator()
    return orchestrator.get_running_projects()


def find_sessions(max_age_hours: int = 2) -> list[SessionInfo]:
    """
    Find recent sessions from all sources (Claude, Codex, Gemini, SDK).

    Uses SessionOrchestrator to discover sessions. All sources are treated equally.

    Session states:
    - active: Agent is actively generating (modified < 60s)
    - open: Agent process is running but idle (modified > 60s, process running)
    - orphaned: Agent process has ended (modified > 60s, no process)
    - crashed: Was doing risky action when stopped (modified 1-5 min, risky last action)
    """
    from .orchestrator import get_orchestrator

    orchestrator = get_orchestrator()
    unified_sessions = orchestrator.discover_all(max_age_hours=max_age_hours)

    # Convert UnifiedSession objects to SessionInfo for backward compatibility
    session_infos = []
    for unified in unified_sessions:
        session_info = unified_session_to_session_info(unified)
        # Get last_action from builder if needed
        if unified.status.value in ("crashed", "open"):
            builder = orchestrator.get_builder(unified.source)
            if builder:
                session_info.last_action = builder.get_last_action(unified.file_path)
        session_infos.append(session_info)

    return session_infos


# Backward compatibility alias
find_claude_sessions = find_sessions


def find_active_session() -> Optional[SessionInfo]:
    """Find the most recently active session from any source."""
    from .orchestrator import get_orchestrator

    orchestrator = get_orchestrator()
    unified_sessions = orchestrator.discover_all(max_age_hours=1)

    if unified_sessions:
        # Convert first (most recent/active) session to SessionInfo
        unified = unified_sessions[0]
        session_info = unified_session_to_session_info(unified)
        # Get last_action if needed
        builder = orchestrator.get_builder(unified.source)
        if builder:
            session_info.last_action = builder.get_last_action(unified.file_path)
        return session_info

    return None


def parse_content_block(block: dict) -> Optional[ThinkingEvent | ToolEvent | TaskEvent]:
    """Parse a content block from a transcript line."""
    block_type = block.get("type")

    if block_type == "thinking":
        thinking = block.get("thinking", "")
        if thinking:
            return ThinkingEvent(content=thinking, timestamp=datetime.now())

    elif block_type == "tool_use":
        name = block.get("name", "Unknown")
        input_data = block.get("input", {})

        if name == "Task":
            return TaskEvent(
                description=input_data.get("description", ""),
                prompt=input_data.get("prompt", ""),
                subagent_type=input_data.get("subagent_type", "unknown"),
                model=input_data.get("model"),
                timestamp=datetime.now(),
            )

        risk = assess_risk(name, input_data)
        return ToolEvent(name=name, input=input_data, timestamp=datetime.now(), risk_level=risk)

    return None


def parse_transcript_line(line: str) -> list[ThinkingEvent | ToolEvent | TaskEvent]:
    """
    Parse a JSONL line from Claude transcript.

    DEPRECATED: Use orchestrator.get_events() with unified_event_to_legacy() instead.
    This function is kept for backward compatibility but will be removed in a future version.
    """
    events = []

    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return events

    if data.get("type") != "assistant":
        return events

    message = data.get("message", {})
    content = message.get("content", [])

    if isinstance(content, str):
        return events

    for block in content:
        event = parse_content_block(block)
        if event:
            events.append(event)

    return events


def parse_codex_event(event_dict: dict) -> ThinkingEvent | ToolEvent | None:
    """Convert a Codex parser event dict to internal event type."""
    event_type = event_dict.get("event_type")
    timestamp_str = event_dict.get("timestamp", "")

    # Parse timestamp
    try:
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        else:
            timestamp = datetime.now()
    except (ValueError, TypeError):
        timestamp = datetime.now()

    if event_type == "tool_call":
        tool_name = event_dict.get("tool_name", "unknown")
        content = event_dict.get("content", "")
        risk_level = event_dict.get("risk_level", "safe")
        file_path = event_dict.get("file_path")

        # Build input dict for ToolEvent compatibility
        tool_input = {"content": content}
        if file_path:
            tool_input["file_path"] = file_path

        # Add raw arguments if present
        raw = event_dict.get("raw", {})
        if "arguments" in raw:
            try:
                args = raw["arguments"]
                if isinstance(args, str):
                    args = json.loads(args)
                tool_input.update(args)
            except (json.JSONDecodeError, TypeError):
                pass

        return ToolEvent(
            name=tool_name,
            input=tool_input,
            timestamp=timestamp,
            status="completed",
            risk_level=risk_level,
        )

    if event_type == "assistant_message":
        content = event_dict.get("content", "")
        if content:
            return ThinkingEvent(
                content=content,
                timestamp=timestamp,
            )

    # user_message and turn_boundary are not displayed as events
    return None


def parse_gemini_event(event_dict: dict) -> ThinkingEvent | ToolEvent | ErrorEvent | None:
    """Convert a Gemini parser event dict to internal event type."""
    event_type = event_dict.get("event_type")
    timestamp_str = event_dict.get("timestamp", "")

    # Parse timestamp
    try:
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        else:
            timestamp = datetime.now()
    except (ValueError, TypeError):
        timestamp = datetime.now()

    if event_type == "error":
        error_msg = event_dict.get("error_message", "Unknown error")
        error_type = event_dict.get("error_type", "unknown")
        tool_name = event_dict.get("tool_name")
        return ErrorEvent(
            message=error_msg,
            timestamp=timestamp,
            error_type=error_type,
            tool_name=tool_name,
            recoverable=error_type != "safety",
        )

    if event_type == "tool":
        tool_name = event_dict.get("tool_name", "unknown")
        tool_input = event_dict.get("tool_input", {})
        risk_level = event_dict.get("risk_level", "safe")

        return ToolEvent(
            name=tool_name,
            input=tool_input,
            timestamp=timestamp,
            status="completed",
            risk_level=risk_level,
        )

    if event_type == "thinking":
        content = event_dict.get("content", "")
        if content:
            return ThinkingEvent(
                content=content,
                timestamp=timestamp,
            )

    if event_type == "response":
        # Treat responses as thinking events for display
        content = event_dict.get("content", "")
        finish_reason = event_dict.get("finish_reason", "")
        if content:
            # Include finish_reason if not normal stop
            suffix = ""
            if finish_reason and finish_reason not in ("STOP", ""):
                suffix = f" [finish: {finish_reason}]"
            return ThinkingEvent(
                content=(
                    f"[Response] {content[:500]}...{suffix}"
                    if len(content) > 500
                    else f"[Response] {content}{suffix}"
                ),
                timestamp=timestamp,
            )

    # user_input events are not displayed
    return None


def parse_gemini_line(line: str) -> Optional[dict]:
    """Parse a single line from Gemini CLI transcript.

    Gemini uses a different format than Claude. This function normalizes
    Gemini transcript lines to unified event dictionaries that can be
    passed to parse_gemini_event().

    Note: Gemini CLI stores sessions as JSON files (not JSONL), so this
    function handles individual JSON objects that may appear in streaming
    or when reading the messages array line-by-line.

    Args:
        line: A single JSON line from the Gemini transcript

    Returns:
        Event dictionary or None if the line cannot be parsed
    """
    try:
        data = json.loads(line)

        # Tool calls - Gemini uses function_call or tool_calls
        if "tool_calls" in data or "function_call" in data:
            calls = data.get("tool_calls") or [data.get("function_call")]
            if calls and calls[0]:
                call = calls[0]
                tool_name = call.get("name", "unknown")
                arguments = call.get("arguments", {})
                # Parse arguments if they're a string
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {"raw": arguments}

                return {
                    "event_type": "tool",
                    "tool_name": tool_name,
                    "tool_input": arguments,
                    "risk_level": assess_risk(tool_name, arguments),
                    "timestamp": data.get("timestamp", ""),
                }

        # Model responses
        if "model_response" in data:
            return {
                "event_type": "response",
                "content": data.get("model_response", ""),
                "timestamp": data.get("timestamp", ""),
            }

        # Thinking/reasoning content
        if "thinking" in data or "reasoning" in data:
            content = data.get("thinking") or data.get("reasoning", "")
            if content:
                return {
                    "event_type": "thinking",
                    "content": content,
                    "timestamp": data.get("timestamp", ""),
                }

        # User messages
        if "user_message" in data or data.get("role") == "user":
            return {
                "event_type": "user_input",
                "content": data.get("user_message") or data.get("content", ""),
                "timestamp": data.get("timestamp", ""),
            }

        # Assistant messages with content
        if data.get("role") == "assistant" or data.get("role") == "model":
            content = data.get("content", "")
            if isinstance(content, list):
                # Handle structured content blocks
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            content = block.get("text", "")
                            break
                    elif isinstance(block, str):
                        content = block
                        break
            if content:
                return {
                    "event_type": "response",
                    "content": content,
                    "timestamp": data.get("timestamp", ""),
                }

        return None
    except json.JSONDecodeError:
        return None


def parse_session_events(
    file_path: Path, source: str = "claude"
) -> Generator[ThinkingEvent | ToolEvent | TaskEvent | ErrorEvent, None, None]:
    """
    Unified event parser that routes to correct parser based on source.

    DEPRECATED: Use orchestrator.get_events() with unified_event_to_legacy() instead.
    This function is kept for backward compatibility but will be removed in a future version.

    Args:
        file_path: Path to the transcript file
        source: Session source - "claude", "codex", "gemini", or "sdk"

    Yields:
        Internal event objects (ThinkingEvent, ToolEvent, TaskEvent)
    """
    if source == "codex" and get_codex_parser is not None:
        # Use Codex parser
        parser = get_codex_parser()
        for event_dict in parser.parse_events(file_path):
            event = parse_codex_event(event_dict)
            if event:
                yield event
    elif source == "gemini" and parse_gemini_file is not None:
        # Use Gemini parser - parses entire JSON file
        for event_dict in parse_gemini_file(file_path):
            event = parse_gemini_event(event_dict)
            if event:
                yield event
    else:
        # Use Claude parser (default)
        try:
            with open(file_path, "r") as f:
                for line in f:
                    if line.strip():
                        for event in parse_transcript_line(line):
                            yield event
        except OSError:
            return


def parse_line_by_source(
    line: str, source: str = "claude"
) -> list[ThinkingEvent | ToolEvent | TaskEvent | ErrorEvent]:
    """
    Parse a single JSONL line based on source type.

    DEPRECATED: Use orchestrator.get_events() with unified_event_to_legacy() instead.
    This function is kept for backward compatibility but will be removed in a future version.

    This is used for incremental/streaming parsing where you read
    new lines as they appear.

    Args:
        line: A single JSONL line from the transcript
        source: Session source - "claude", "codex", "gemini", or "sdk"

    Returns:
        List of internal event objects
    """
    if source == "codex" and parse_codex_line is not None:
        event_dict = parse_codex_line(line)
        if event_dict:
            event = parse_codex_event(event_dict)
            if event:
                return [event]
        return []
    elif source == "gemini":
        event_dict = parse_gemini_line(line)
        if event_dict:
            event = parse_gemini_event(event_dict)
            if event:
                return [event]
        return []
    else:
        # Claude/SDK format
        return parse_transcript_line(line)


def get_last_error(file_path: Path, source: str = "claude") -> Optional[ErrorEvent]:
    """
    Get the most recent error from a session file.

    Useful for error-first context when resuming sessions.
    Returns None if no errors found.
    """
    errors = []

    try:
        # Use orchestrator to get unified session and events
        orchestrator = get_orchestrator()
        unified_sessions = orchestrator.discover_all(max_age_hours=168)

        # Find matching unified session by file path
        unified_session = None
        for s in unified_sessions:
            if s.file_path == file_path:
                unified_session = s
                break

        if not unified_session:
            return None

        # Get events from orchestrator
        unified_events = orchestrator.get_events(unified_session)

        # Convert to legacy and extract errors
        for unified_event in unified_events:
            legacy_event = unified_event_to_legacy(unified_event)
            if isinstance(legacy_event, ErrorEvent):
                errors.append(legacy_event)

    except Exception:
        pass

    return errors[-1] if errors else None


def get_session_errors(file_path: Path, source: str = "claude") -> list[ErrorEvent]:
    """
    Get all errors from a session file.

    Returns list of ErrorEvent objects, newest last.
    """
    errors = []

    try:
        # Use orchestrator to get unified session and events
        orchestrator = get_orchestrator()
        unified_sessions = orchestrator.discover_all(max_age_hours=168)

        # Find matching unified session by file path
        unified_session = None
        for s in unified_sessions:
            if s.file_path == file_path:
                unified_session = s
                break

        if not unified_session:
            return []

        # Get events from orchestrator
        unified_events = orchestrator.get_events(unified_session)

        # Convert to legacy and extract errors
        for unified_event in unified_events:
            legacy_event = unified_event_to_legacy(unified_event)
            if isinstance(legacy_event, ErrorEvent):
                errors.append(legacy_event)

    except Exception:
        pass

    return errors


def get_risk_style(risk_level: str) -> tuple[str, str]:
    """Get border style and icon for risk level."""
    styles = {
        "safe": ("green", "✓"),
        "low": ("blue", "○"),
        "medium": ("yellow", "◐"),
        "high": ("red", "●"),
        "critical": ("bold red", "⚠"),
    }
    return styles.get(risk_level, ("white", "?"))


def format_thinking(thinking: ThinkingEvent, stats: SessionStats) -> Panel:
    """Format a thinking event for display."""
    content = redact_secrets(thinking.content)
    stats.thinking_count += 1

    max_len = 800 if len(content) < 1000 else 500
    if len(content) > max_len:
        content = content[:max_len] + "..."

    content = content.strip()
    time_str = thinking.timestamp.strftime("%H:%M:%S")

    return Panel(
        Text(content, style="italic"),
        title=f"[bold magenta]💭 THINKING[/bold magenta] [dim]#{stats.thinking_count}[/dim]",
        subtitle=f"[dim]{time_str}[/dim]",
        border_style="magenta",
        padding=(0, 1),
    )


def format_error(error: ErrorEvent, stats: SessionStats) -> Panel:
    """Format an error event for display."""
    stats.error_count = getattr(stats, "error_count", 0) + 1

    lines = []
    lines.append(f"[bold red]{redact_secrets(error.message)}[/bold red]")

    if error.error_type:
        lines.append(f"[dim]Type:[/dim] {error.error_type}")
    if error.tool_name:
        lines.append(f"[dim]Tool:[/dim] {error.tool_name}")
    if not error.recoverable:
        lines.append("[yellow]⚠ Non-recoverable[/yellow]")

    content = "\n".join(lines)
    time_str = error.timestamp.strftime("%H:%M:%S")

    return Panel(
        Text.from_markup(content),
        title=f"[bold red]❌ ERROR[/bold red] [dim]#{stats.error_count}[/dim]",
        subtitle=f"[dim]{time_str}[/dim]",
        border_style="red",
        padding=(0, 1),
    )


def format_task(task: TaskEvent, stats: SessionStats) -> Panel:
    """Format a Task/subagent event with rich details."""
    stats.agent_count += 1
    lines = []

    lines.append(f"[bold cyan]{task.description}[/bold cyan]")
    lines.append("")

    agent_info = f"[dim]Agent:[/dim] {task.subagent_type}"
    if task.model:
        agent_info += f"  [dim]Model:[/dim] {task.model}"
    lines.append(agent_info)

    if task.prompt:
        # Show full prompt (no truncation)
        full_prompt = redact_secrets(task.prompt)
        lines.append("")
        lines.append("[dim]Prompt:[/dim]")
        lines.append(f"[white]{full_prompt}[/white]")

    content = "\n".join(lines)
    time_str = task.timestamp.strftime("%H:%M:%S")

    return Panel(
        Text.from_markup(content),
        title=f"[bold yellow]🤖 SPAWNING AGENT[/bold yellow] [dim]#{stats.agent_count}[/dim]",
        subtitle=f"[dim]{time_str}[/dim]",
        border_style="yellow",
        padding=(0, 1),
    )


def format_tool(tool: ToolEvent, stats: SessionStats) -> Panel:
    """Format a tool event for display."""
    stats.tool_count += 1
    input_summary = ""

    if tool.name in ("Write", "Edit"):
        file_path = tool.input.get("file_path", "")
        if file_path:
            stats.files_modified.add(file_path)

    if tool.risk_level in ("high", "critical"):
        stats.high_risk_ops += 1

    if tool.name == "Read":
        input_summary = tool.input.get("file_path", "")
    elif tool.name == "Write":
        fp = tool.input.get("file_path", "")
        input_summary = f"[bold]{fp}[/bold]\n[dim]Creating new file[/dim]"
    elif tool.name == "Edit":
        file_path = tool.input.get("file_path", "")
        old_str = redact_secrets(tool.input.get("old_string", "")[:40])
        input_summary = f"[bold]{file_path}[/bold]\n[dim]replacing:[/dim] {old_str}..."
    elif tool.name == "Bash":
        cmd = redact_secrets(tool.input.get("command", ""))
        desc = tool.input.get("description", "")
        if desc:
            input_summary = f"[dim]{desc}[/dim]\n{cmd[:100]}"
        else:
            input_summary = cmd[:120] + ("..." if len(cmd) > 120 else "")
    elif tool.name == "Glob":
        pattern = tool.input.get("pattern", "")
        path = tool.input.get("path", "")
        input_summary = f"{pattern}" + (f" in {path}" if path else "")
    elif tool.name == "Grep":
        pattern = tool.input.get("pattern", "")
        path = tool.input.get("path", "")
        input_summary = f"/{pattern}/" + (f" in {path}" if path else "")
    elif tool.name == "WebFetch":
        url = tool.input.get("url", "")
        prompt = tool.input.get("prompt", "")[:50]
        input_summary = f"{url}\n[dim]{prompt}...[/dim]"
    elif tool.name == "WebSearch":
        input_summary = f'🔍 "{tool.input.get("query", "")}"'
    elif tool.name == "TodoWrite":
        todos = tool.input.get("todos", [])
        if todos:
            items = [t.get("content", "")[:40] for t in todos[:3]]
            input_summary = "\n".join(f"• {item}" for item in items)
            if len(todos) > 3:
                input_summary += f"\n[dim]...and {len(todos) - 3} more[/dim]"
    else:
        for k, v in tool.input.items():
            if isinstance(v, str) and v:
                input_summary = f"[dim]{k}:[/dim] {v[:60]}" + ("..." if len(v) > 60 else "")
                break

    icon = {
        "Read": "📖",
        "Write": "✏️",
        "Edit": "🔧",
        "Bash": "💻",
        "Glob": "🔍",
        "Grep": "🔎",
        "Task": "🤖",
        "WebFetch": "🌐",
        "WebSearch": "🔍",
        "TodoWrite": "📝",
        "AskUserQuestion": "❓",
        "BashOutput": "📤",
        "KillShell": "🛑",
    }.get(tool.name, "⚡")

    border_style, risk_icon = get_risk_style(tool.risk_level)

    risk_indicator = ""
    if tool.risk_level == "critical":
        risk_indicator = " [bold red]⚠ DESTRUCTIVE[/bold red]"
    elif tool.risk_level == "high":
        risk_indicator = " [red]● HIGH RISK[/red]"
    elif tool.risk_level == "medium":
        risk_indicator = " [yellow]◐[/yellow]"

    time_str = tool.timestamp.strftime("%H:%M:%S")
    title = f"[bold {border_style}]{icon} {tool.name}[/bold {border_style}]{risk_indicator}"

    return Panel(
        (
            Text.from_markup(input_summary)
            if "[" in input_summary
            else Text(input_summary, style="cyan")
        ),
        title=title,
        subtitle=f"[dim]{time_str}[/dim]",
        border_style=border_style,
        padding=(0, 1),
    )


def create_header(session: SessionInfo) -> Panel:
    """Create the header panel."""
    return Panel(
        f"[bold]Session:[/bold] {session.session_id[:12]}...\n"
        f"[bold]File:[/bold] {session.file_path.name}\n"
        f"[dim]Press Ctrl+C to exit[/dim]",
        title="[bold green]🎯 MC[/bold green]",
        subtitle="[dim]Command Center for AI Agents[/dim]",
        border_style="green",
    )


def tail_file(file_path: Path, last_position: int = 0) -> Generator[str, None, None]:
    """Tail a file from a given position, yield new lines.

    Note: Generator return values aren't accessible via for-loops.
    If position tracking is needed, callers should use file.tell() directly.
    """
    try:
        with open(file_path, "r") as f:
            f.seek(last_position)
            for line in f:
                if line.strip():
                    yield line
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")


def analyze_session(session: SessionInfo) -> SessionStats:
    """Analyze a session and return stats."""
    stats = SessionStats()

    try:
        # Use orchestrator to get unified session and events
        orchestrator = get_orchestrator()
        unified_sessions = orchestrator.discover_all(max_age_hours=168)

        # Find matching unified session
        unified_session = None
        for s in unified_sessions:
            if s.session_id == session.session_id or s.file_path == session.file_path:
                unified_session = s
                break

        if not unified_session:
            return stats

        # Get events from orchestrator
        unified_events = orchestrator.get_events(unified_session)

        # Convert to legacy and count
        for unified_event in unified_events:
            legacy_event = unified_event_to_legacy(unified_event)
            if isinstance(legacy_event, ThinkingEvent):
                stats.thinking_count += 1
            elif isinstance(legacy_event, TaskEvent):
                stats.agent_count += 1
            elif isinstance(legacy_event, ToolEvent):
                stats.tool_count += 1
                if legacy_event.name in ("Write", "Edit"):
                    fp = legacy_event.input.get("file_path", "")
                    if fp:
                        stats.files_modified.add(fp)
                if legacy_event.risk_level in ("high", "critical"):
                    stats.high_risk_ops += 1

    except Exception as e:
        stats.errors.append(str(e))

    return stats


def generate_agent_context(session: SessionInfo) -> str:
    """
    Generate a context summary that can be injected into AI agent prompts.
    This is the key feature for AI self-improvement through MC.
    """
    stats = analyze_session(session)

    context = f"""## MC Session Context

**Session ID:** {session.session_id[:12]}
**Duration:** Since {session.last_modified.strftime("%H:%M:%S")}
**Transcript Size:** {session.size // 1024}KB

### Activity Summary
- **Thinking blocks:** {stats.thinking_count}
- **Tool calls:** {stats.tool_count}
- **Agents spawned:** {stats.agent_count}
- **Files modified:** {len(stats.files_modified)}
- **High-risk operations:** {stats.high_risk_ops}

### Files You've Modified
{chr(10).join(f"- {f}" for f in list(stats.files_modified)[:10]) if stats.files_modified else "None yet"}

### Recommendations
"""

    # Add contextual recommendations
    if stats.high_risk_ops > 3:
        context += (
            "- ⚠️ Multiple high-risk operations detected. Consider pausing for human review.\n"
        )

    if stats.tool_count > 50 and stats.thinking_count < 5:
        context += (
            "- 💭 High tool usage with low thinking. Consider more deliberation before acting.\n"
        )

    if len(stats.files_modified) > 10:
        context += "- 📁 Many files modified. Consider committing a checkpoint.\n"

    if stats.agent_count > 5:
        context += "- 🤖 Multiple subagents spawned. Ensure coordination between agents.\n"

    return context


def watch_session(session: SessionInfo):
    """Watch a Claude session in real-time."""
    console.clear()

    stats = SessionStats(start_time=datetime.now())

    console.print(create_header(session))
    console.print()

    last_position = 0

    console.print("[dim]Loading recent activity...[/dim]\n")

    # Use orchestrator to get UnifiedSession and events
    orchestrator = get_orchestrator()
    unified_sessions = orchestrator.discover_all(max_age_hours=168)

    # Find matching UnifiedSession
    unified_session = None
    for s in unified_sessions:
        if s.session_id == session.session_id or s.file_path == session.file_path:
            unified_session = s
            break

    if not unified_session:
        console.print("[red]Error: Session not found in orchestrator[/red]")
        return

    # Get all events using orchestrator
    all_unified_events = orchestrator.get_events(unified_session)

    # Convert to legacy event types for display
    recent_events = []
    for unified_event in all_unified_events:
        legacy_event = unified_event_to_legacy(unified_event)
        if legacy_event:
            recent_events.append(legacy_event)

    history_stats = SessionStats()

    for event in recent_events[-8:]:
        if isinstance(event, ThinkingEvent):
            console.print(format_thinking(event, history_stats))
        elif isinstance(event, TaskEvent):
            console.print(format_task(event, history_stats))
        elif isinstance(event, ToolEvent):
            console.print(format_tool(event, history_stats))
        elif isinstance(event, ErrorEvent):
            console.print(format_error(event, history_stats))
        console.print()

    # Track event count for incremental updates
    last_position = len(all_unified_events)
    last_activity = time.time()

    console.print(Rule("[bold green]Watching for new activity[/bold green]", style="green"))
    console.print()

    poll_count = 0
    is_active = False

    try:
        while True:
            has_new_content = False
            new_events = []

            # Get events using orchestrator (with refresh to bypass cache)
            all_unified_events = orchestrator.get_events(unified_session, refresh=True)

            if len(all_unified_events) > last_position:
                has_new_content = True
                # Convert new events to legacy format
                for unified_event in all_unified_events[last_position:]:
                    legacy_event = unified_event_to_legacy(unified_event)
                    if legacy_event:
                        new_events.append(legacy_event)
                last_position = len(all_unified_events)

            if has_new_content:
                last_activity = time.time()
                is_active = True
                for event in new_events:
                    if isinstance(event, ThinkingEvent):
                        console.print(format_thinking(event, stats))
                    elif isinstance(event, TaskEvent):
                        console.print(format_task(event, stats))
                    elif isinstance(event, ToolEvent):
                        console.print(format_tool(event, stats))
                    elif isinstance(event, ErrorEvent):
                        console.print(format_error(event, stats))
                    console.print()
            else:
                idle_time = time.time() - last_activity
                if idle_time > 3:
                    is_active = False

            poll_count += 1
            if poll_count % 10 == 0:
                idle_secs = int(time.time() - last_activity)
                activity = "● LIVE" if is_active else f"○ idle ({idle_secs}s)"
                status = f"[dim]💭{stats.thinking_count} ⚡{stats.tool_count} 🤖{stats.agent_count} │ {activity}[/dim]"
                console.print(status, end="\r")

            time.sleep(0.3)

    except KeyboardInterrupt:
        console.print("\n")
        console.print(Rule("[dim]Session ended[/dim]"))

        duration = datetime.now() - stats.start_time
        mins = int(duration.total_seconds() // 60)
        secs = int(duration.total_seconds() % 60)

        summary = Table(show_header=False, box=box.SIMPLE)
        summary.add_column("Metric", style="dim")
        summary.add_column("Value", style="cyan")
        summary.add_row("Duration", f"{mins}m {secs}s")
        summary.add_row("Thinking blocks", str(stats.thinking_count))
        summary.add_row("Tool calls", str(stats.tool_count))
        summary.add_row("Agents spawned", str(stats.agent_count))
        summary.add_row("Files modified", str(len(stats.files_modified)))
        if stats.high_risk_ops > 0:
            summary.add_row("High-risk ops", f"[red]{stats.high_risk_ops}[/red]")

        console.print(summary)


def find_sdk_traces() -> list[dict]:
    """Find SDK trace files."""
    traces = []
    traces_dir = MC_STATE_DIR / "traces"

    if not traces_dir.exists():
        return traces

    for trace_file in traces_dir.glob("*.jsonl"):
        stat = trace_file.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)
        age_seconds = (datetime.now() - modified).total_seconds()

        # Read first line to get session info
        try:
            with open(trace_file, "r") as f:
                first_line = f.readline()
                data = json.loads(first_line)
                tracer_name = data.get("tracer_name", trace_file.stem)
        except (OSError, json.JSONDecodeError, KeyError):
            tracer_name = trace_file.stem

        traces.append(
            {
                "name": tracer_name,
                "file": trace_file,
                "modified": modified,
                "size": stat.st_size,
                "is_active": age_seconds < 60,
            }
        )

    traces.sort(key=lambda t: t["modified"], reverse=True)
    return traces[:5]


def mission_control():
    """
    Unified mission control - sessions + live feed + insights in one view.
    The default MC experience.

    Shows ALL active sessions' feeds combined with session IDs.
    """
    console.clear()

    # Track ALL sessions, not just one
    sessions = find_claude_sessions(max_age_hours=24)
    sdk_traces = find_sdk_traces()

    # Track file positions for ALL sessions
    session_positions = (
        {}
    )  # session_id -> last_position (byte offset for JSONL, event count for Gemini)
    for s in sessions:
        if getattr(s, "source", "claude") == "gemini":
            # Gemini uses event count, not byte offset (single JSON, not JSONL)
            session_positions[s.session_id] = 0
        else:
            # JSONL sources (Claude, Codex) - start from near the end to show recent activity
            session_positions[s.session_id] = max(0, s.file_path.stat().st_size - 5000)

    # Event buffer for live feed (combined from all sessions)
    event_buffer = []
    max_events = 20
    insights = []

    def build_layout():
        nonlocal session_positions, event_buffer, insights

        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3),
        )

        layout["main"].split_row(
            Layout(name="sessions", ratio=1),
            Layout(name="feed", ratio=2),
        )

        # Header
        active_count = len([s for s in sessions if s.status in ("active", "open")])
        layout["header"].update(
            Panel(
                f"[bold]Command Center[/bold] — All Sessions Feed ({active_count} live)",
                title="[bold green]🎯 MC[/bold green]",
                border_style="green",
            )
        )

        # Sessions panel
        sessions_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        sessions_table.add_column("Status", width=3)
        sessions_table.add_column("Info")

        # All sessions (Claude, Codex, Gemini)
        for i, s in enumerate(sessions[:5]):
            if s.status == "active":
                status = "[green]●[/green]"
            elif s.status == "open":
                status = "[yellow]◐[/yellow]"  # Open/idle but process running
            elif s.status == "crashed":
                status = "[red]✗[/red]"
            else:
                status = "[dim]○[/dim]"

            # Add source indicator for non-Claude
            source_badge = ""
            if s.source == "codex":
                source_badge = "[cyan]◇[/cyan]"
            elif s.source == "gemini":
                source_badge = "[magenta]◆[/magenta]"

            info = f"  {source_badge}[{s.session_id[:8]}] {s.project_path[:15]}"
            sessions_table.add_row(status, info)

        # SDK traces
        if sdk_traces:
            sessions_table.add_row("", "[dim]─── SDK ───[/dim]")
            for t in sdk_traces[:3]:
                status = "[blue]◆[/blue]" if t["is_active"] else "[dim]◇[/dim]"
                sessions_table.add_row(status, f"  {t['name'][:20]}")

        layout["sessions"].update(
            Panel(
                sessions_table,
                title="[bold]Sessions[/bold]",
                border_style="blue",
            )
        )

        # Live feed panel - read new events from active and open sessions
        # Get orchestrator and unified sessions for event parsing
        orchestrator = get_orchestrator()
        unified_sessions = orchestrator.discover_all(max_age_hours=24)

        # Build session ID map for quick lookup
        unified_session_map = {s.session_id: s for s in unified_sessions}

        for session in sessions:
            # For Claude, only show active/open. For others, also include idle/crashed/orphaned
            # since Codex/Gemini don't have the same process detection granularity
            if session.source == "claude":
                if session.status not in ("active", "open", "crashed", "orphaned"):
                    continue
            else:
                if session.status not in ("active", "open", "idle", "crashed", "orphaned"):
                    continue

            session_id = session.session_id
            short_id = session_id[:6]
            last_pos = session_positions.get(session_id, 0)

            try:
                # Get unified session for orchestrator access
                unified_session = unified_session_map.get(session_id)
                if not unified_session:
                    continue

                # Use orchestrator to get all events
                all_unified_events = orchestrator.get_events(unified_session, refresh=True)

                # Check if there are new events
                events_list = []
                if len(all_unified_events) > last_pos:
                    # Convert new events to legacy format
                    for unified_event in all_unified_events[last_pos:]:
                        legacy_event = unified_event_to_legacy(unified_event)
                        if legacy_event:
                            events_list.append(legacy_event)
                    session_positions[session_id] = len(all_unified_events)

                # Process events from unified orchestrator
                for event in events_list:
                    time_str = event.timestamp.strftime("%H:%M:%S")
                    # Session ID badge
                    sid_badge = f"[black on cyan] {short_id} [/black on cyan]"

                    if isinstance(event, ThinkingEvent):
                        text = (
                            event.content[:55] + "..." if len(event.content) > 55 else event.content
                        )
                        # Purple box for thinking
                        event_buffer.append(
                            f"[dim]{time_str}[/dim] {sid_badge} [white on magenta] THINK [/white on magenta] {text}"
                        )

                        # Check for decisions in thinking
                        if any(
                            d in event.content.lower()
                            for d in [
                                "i'll ",
                                "i decided",
                                "let me",
                                "i should",
                                "the best",
                            ]
                        ):
                            decision_text = event.content[:40]
                            event_buffer.append(
                                f"           {sid_badge} [black on yellow] DECIDE [/black on yellow] {decision_text}..."
                            )
                            insights.append(f"[yellow]💡 {short_id}: decision made[/yellow]")

                        # Generate insights from thinking
                        if "error" in event.content.lower() or "fail" in event.content.lower():
                            insights.append(f"[yellow]⚠ {short_id}: error discussion[/yellow]")

                    elif isinstance(event, TaskEvent):
                        # Yellow box for agent spawn with rich details
                        agent_info = f"{event.subagent_type}: {event.description[:35]}"
                        event_buffer.append(
                            f"[dim]{time_str}[/dim] {sid_badge} [black on yellow] SPAWN [/black on yellow] 🤖 {agent_info}"
                        )
                        if event.model:
                            event_buffer.append(
                                f"           {sid_badge}   ├─ [dim]model:[/dim] [cyan]{event.model}[/cyan]"
                            )
                        if event.prompt:
                            # Show first 100 chars inline, suggest viewing full prompt in web UI
                            prompt_preview = event.prompt[:100].replace("\n", " ")
                            suffix = "..." if len(event.prompt) > 100 else ""
                            event_buffer.append(
                                f"           {sid_badge}   └─ [dim]prompt:[/dim] {prompt_preview}{suffix}"
                            )
                            if len(event.prompt) > 100:
                                event_buffer.append(
                                    f"           {sid_badge}     [dim](View full prompt in web UI or session details)[/dim]"
                                )
                        insights.append(
                            f"[yellow]🤖 {short_id}: spawned {event.subagent_type}[/yellow]"
                        )

                    elif isinstance(event, ToolEvent):
                        risk_colors = {
                            "safe": "green",
                            "low": "blue",
                            "medium": "yellow",
                            "high": "red",
                            "critical": "bold white on red",
                        }
                        risk_colors.get(event.risk_level, "white")
                        risk_bg = {
                            "safe": "black on green",
                            "medium": "black on yellow",
                            "high": "white on red",
                            "critical": "white on red",
                        }.get(event.risk_level, "black on blue")

                        # Tool-specific formatting with colored boxes
                        if event.name == "Edit":
                            path = event.input.get("file_path", "").split("/")[-1][:25]
                            event_buffer.append(
                                f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] EDIT [/{risk_bg}] ✏️  {path}"
                            )
                        elif event.name == "Write":
                            path = event.input.get("file_path", "").split("/")[-1][:25]
                            event_buffer.append(
                                f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] WRITE [/{risk_bg}] 📝 {path}"
                            )
                        elif event.name == "Read":
                            path = event.input.get("file_path", "").split("/")[-1][:25]
                            event_buffer.append(
                                f"[dim]{time_str}[/dim] {sid_badge} [black on green] READ [/black on green] 📖 {path}"
                            )
                        elif event.name == "Bash":
                            cmd = event.input.get("command", "")[:28]
                            event_buffer.append(
                                f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] BASH [/{risk_bg}] 💻 {cmd}"
                            )

                            # Insight for risky commands
                            if event.risk_level in ("high", "critical"):
                                insights.append(f"[red]⚠ {short_id}: {cmd[:25]}[/red]")
                        elif event.name == "Task":
                            desc = event.input.get("description", "")[:30]
                            event_buffer.append(
                                f"[dim]{time_str}[/dim] {sid_badge} [black on yellow] AGENT [/black on yellow] 🤖 {desc}"
                            )
                        else:
                            event_buffer.append(
                                f"[dim]{time_str}[/dim] {sid_badge} [black on blue] {event.name[:6]:6} [/black on blue] ⚡"
                            )

            except json.JSONDecodeError as e:
                logger.debug(f"JSON decode error in session {session.session_id}: {e}")
            except OSError as e:
                logger.debug(f"Error reading session file {session.file_path}: {e}")
            except Exception as e:
                logger.warning(f"Unexpected error processing session {session.session_id}: {e}")

        # Trim buffer
        event_buffer = event_buffer[-max_events:]
        insights = insights[-5:]

        # Build feed content
        feed_lines = []
        for e in event_buffer:
            feed_lines.append(e)

        if not feed_lines:
            feed_lines = ["[dim]Waiting for activity...[/dim]"]

        # Add insights section if any
        if insights:
            feed_lines.append("")
            feed_lines.append("[bold yellow]─── INSIGHTS ───[/bold yellow]")
            for insight in insights[-3:]:
                feed_lines.append(insight)

        layout["feed"].update(
            Panel(
                "\n".join(feed_lines),
                title="[bold]Live Feed[/bold] [dim](all active sessions)[/dim]",
                border_style="green",
            )
        )

        # Footer
        layout["footer"].update(
            Panel(
                "[dim]Ctrl+C[/dim] Exit  │  [dim]In another terminal:[/dim] [cyan]mc watch <id>[/cyan] [cyan]mc summary <id>[/cyan]",
                border_style="dim",
            )
        )

        return layout

    try:
        with Live(build_layout(), refresh_per_second=2, console=console) as live:
            while True:
                # Refresh sessions periodically
                sessions = find_claude_sessions(max_age_hours=24)
                sdk_traces = find_sdk_traces()

                # Track new sessions
                for s in sessions:
                    if s.session_id not in session_positions:
                        if getattr(s, "source", "claude") == "gemini":
                            # Gemini uses event count, not byte offset
                            session_positions[s.session_id] = 0
                        else:
                            # JSONL sources (Claude, Codex) - start from near the end
                            session_positions[s.session_id] = max(
                                0, s.file_path.stat().st_size - 5000
                            )

                live.update(build_layout())
                time.sleep(0.5)

    except KeyboardInterrupt:
        console.print("\n[dim]Mission control closed.[/dim]")


def dashboard():
    """Multi-session dashboard view."""
    console.clear()

    console.print(
        Panel(
            "[bold]Multi-Session Dashboard[/bold]\n"
            "[dim]Showing all recent Claude Code sessions[/dim]",
            title="[bold green]🎯 MC DASHBOARD[/bold green]",
            border_style="green",
        )
    )
    console.print()

    try:
        while True:
            sessions = find_claude_sessions(max_age_hours=24)

            if not sessions:
                console.print("[yellow]No recent sessions found.[/yellow]")
                time.sleep(2)
                continue

            # Group sessions
            active_sessions = [s for s in sessions if s.is_active]
            recent_sessions = [s for s in sessions if not s.is_active][:5]

            # Clear and redraw
            console.print("\033[H\033[J", end="")  # Clear screen

            console.print(
                Panel(
                    "[bold]Multi-Session Dashboard[/bold]",
                    title="[bold green]🎯 MC DASHBOARD[/bold green]",
                    border_style="green",
                )
            )

            # Active sessions
            if active_sessions:
                console.print("\n[bold green]● ACTIVE SESSIONS[/bold green]\n")

                for session in active_sessions:
                    stats = analyze_session(session)
                    age = datetime.now() - session.last_modified

                    panel_content = (
                        f"[bold cyan]{session.session_id[:12]}...[/bold cyan]\n"
                        f"[dim]Modified:[/dim] {age.seconds}s ago\n"
                        f"[dim]Size:[/dim] {session.size // 1024}KB\n"
                        f"\n"
                        f"💭 {stats.thinking_count}  "
                        f"⚡ {stats.tool_count}  "
                        f"🤖 {stats.agent_count}  "
                        f"📁 {len(stats.files_modified)}"
                    )

                    if stats.high_risk_ops > 0:
                        panel_content += f"  [red]⚠ {stats.high_risk_ops}[/red]"

                    console.print(
                        Panel(
                            panel_content,
                            title="[bold green]● LIVE[/bold green]",
                            border_style="green",
                            width=60,
                        )
                    )

            # Recent sessions
            if recent_sessions:
                console.print("\n[dim]○ RECENT SESSIONS[/dim]\n")

                table = Table(box=box.SIMPLE)
                table.add_column("Session", style="cyan")
                table.add_column("Last Active", style="dim")
                table.add_column("Size", style="blue")
                table.add_column("💭", justify="right")
                table.add_column("⚡", justify="right")
                table.add_column("🤖", justify="right")

                for session in recent_sessions:
                    stats = analyze_session(session)
                    age = datetime.now() - session.last_modified

                    if age.seconds < 60:
                        age_str = f"{age.seconds}s"
                    elif age.seconds < 3600:
                        age_str = f"{age.seconds // 60}m"
                    else:
                        age_str = f"{age.seconds // 3600}h"

                    table.add_row(
                        session.session_id[:12] + "...",
                        age_str,
                        f"{session.size // 1024}KB",
                        str(stats.thinking_count),
                        str(stats.tool_count),
                        str(stats.agent_count),
                    )

                console.print(table)

            console.print(
                f"\n[dim]Last updated: {datetime.now().strftime('%H:%M:%S')} │ Refreshing every 3s │ Ctrl+C to exit[/dim]"
            )

            time.sleep(3)

    except KeyboardInterrupt:
        console.print("\n[dim]Dashboard closed.[/dim]")


def context_command():
    """Generate context summary for AI agents."""
    session = find_active_session()

    if not session:
        console.print("[yellow]No active session found.[/yellow]")
        sys.exit(1)

    context = generate_agent_context(session)

    # Also save to file for easy injection
    context_file = MC_STATE_DIR / "current_context.md"
    try:
        with open(context_file, "w") as f:
            f.write(context)
        save_status = f"[dim]Saved to {context_file}[/dim]"
    except (OSError, IOError) as e:
        logger.error(f"Failed to write context file: {e}")
        save_status = f"[dim red]Failed to save: {e}[/dim red]"

    console.print(
        Panel(
            context,
            title="[bold cyan]📋 Agent Context[/bold cyan]",
            subtitle=save_status,
            border_style="cyan",
        )
    )

    console.print(
        "\n[dim]This context can be injected into AI agent prompts for self-awareness.[/dim]"
    )


def extract_decisions(file_path: Path, source: str = "claude") -> list[str]:
    """
    Extract decision patterns from thinking blocks.

    Works with Claude, Codex, and Gemini transcript formats.
    """
    decisions = []
    decision_patterns = [
        "I'll use",
        "I decided",
        "I'm going to",
        "Let me",
        "I should",
        "The best approach",
        "I chose",
        "Instead of",
        "Rather than",
    ]

    def extract_from_thinking(thinking: str) -> None:
        """Extract decisions from a thinking text block."""
        for pattern in decision_patterns:
            if pattern.lower() in thinking.lower():
                sentences = thinking.replace("\n", " ").split(". ")
                for sentence in sentences:
                    if pattern.lower() in sentence.lower() and len(sentence) > 20:
                        clean = sentence.strip()[:150]
                        if clean and clean not in decisions:
                            decisions.append(clean)
                        break

    try:
        # Gemini uses JSON (not JSONL), so handle separately
        if source == "gemini":
            with open(file_path, "r") as f:
                data = json.load(f)
                for msg in data.get("messages", []):
                    if msg.get("type") == "gemini":
                        # Gemini stores thoughts in a separate array
                        for thought in msg.get("thoughts", []):
                            description = thought.get("description", "")
                            if description:
                                extract_from_thinking(description)
            return decisions[:10]

        # JSONL format for Claude/Codex
        with open(file_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)

                    # Claude format: type="assistant" with thinking blocks
                    if data.get("type") == "assistant":
                        message = data.get("message", {})
                        content = message.get("content", [])
                        if isinstance(content, list):
                            for block in content:
                                if block.get("type") == "thinking":
                                    thinking = block.get("thinking", "")
                                    extract_from_thinking(thinking)

                    # Codex format: type="response_item" with text content
                    elif data.get("type") == "response_item":
                        payload = data.get("payload", {})
                        item_type = payload.get("type")
                        # Codex thinking is in "message" type items
                        if item_type == "message":
                            content = payload.get("content", [])
                            for c in content if isinstance(content, list) else []:
                                if c.get("type") == "output_text":
                                    text = c.get("text", "")
                                    extract_from_thinking(text)

                except json.JSONDecodeError:
                    continue
    except OSError as e:
        logger.debug(f"Error reading session file {file_path}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error extracting decisions from {file_path}: {e}")

    return decisions[:10]  # Limit to 10 most relevant


def summary_command(session_id: Optional[str] = None):
    """Generate a rich summary for CLAUDE.md injection - the AI memory layer."""
    if session_id:
        sessions = find_sessions(max_age_hours=48)
        session = None
        for s in sessions:
            if s.session_id.startswith(session_id):
                session = s
                break
        if not session:
            console.print(f"[red]Session not found: {session_id}[/red]")
            console.print("Use 'mc list' to see available sessions.")
            sys.exit(1)
    else:
        session = find_active_session()
        if not session:
            console.print("[yellow]No active session found.[/yellow]")
            console.print("Use 'mc summary <session_id>' to specify a session.")
            sys.exit(1)

    stats = analyze_session(session)
    decisions = extract_decisions(session.file_path)

    # Generate rich markdown for CLAUDE.md
    summary = f"""## MC Session Memory

> Auto-generated by Motus Command. Inject this into CLAUDE.md for agent continuity.

### Session Info
- **ID:** `{session.session_id[:12]}`
- **Project:** `{session.project_path}`
- **Size:** {session.size // 1024}KB
- **Last Active:** {session.last_modified.strftime("%Y-%m-%d %H:%M")}

### Activity Summary
| Metric | Count |
|--------|-------|
| Thinking blocks | {stats.thinking_count} |
| Tool calls | {stats.tool_count} |
| Agents spawned | {stats.agent_count} |
| Files modified | {len(stats.files_modified)} |
| High-risk ops | {stats.high_risk_ops} |

### Files Modified This Session
"""

    if stats.files_modified:
        for f in list(stats.files_modified)[:15]:
            # Shorten paths for readability
            short_path = f
            if len(f) > 60:
                parts = f.split("/")
                short_path = "/".join(parts[-3:]) if len(parts) > 3 else f
            summary += f"- `{short_path}`\n"
    else:
        summary += "- None yet\n"

    summary += "\n### Decisions Made (from thinking blocks)\n"

    if decisions:
        for d in decisions[:8]:
            summary += f"- {d}\n"
    else:
        summary += "- No explicit decisions captured\n"

    summary += """
### Recommendations for Next Session
"""

    if stats.high_risk_ops > 3:
        summary += "- ⚠️ Multiple high-risk operations were performed. Review changes carefully.\n"

    if len(stats.files_modified) > 10:
        summary += "- 📁 Many files were modified. Consider committing before continuing.\n"

    if stats.agent_count > 3:
        summary += "- 🤖 Multiple subagents were spawned. Check for coordination issues.\n"

    if stats.tool_count > 100:
        summary += "- ⚡ High tool usage. The session was very active.\n"

    summary += f"\n---\n*Generated by [Motus Command](https://github.com/bnvoss/motus-command) at {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

    # Save to file
    summary_file = MC_STATE_DIR / f"summary_{session.session_id[:8]}.md"
    latest_file = MC_STATE_DIR / "latest_summary.md"

    try:
        with open(summary_file, "w") as f:
            f.write(summary)

        # Also save as "latest" for easy access
        with open(latest_file, "w") as f:
            f.write(summary)

        save_success = True
    except (OSError, IOError) as e:
        logger.error(f"Failed to write summary files: {e}")
        console.print(f"[red]Warning: Failed to save files: {e}[/red]")

    console.print(
        Panel(
            summary,
            title="[bold green]📋 MC Summary[/bold green]",
            subtitle=(
                "Copied to clipboard! [dim]and saved to .mc/[/dim]"
                if save_success
                else "[red]Not saved[/red]"
            ),
            border_style="green",
        )
    )


try:
    from .commands.context_cmd import context_command as context_cmd_func
    from .commands.harness_cmd import harness_command as harness_cmd_func
    from .commands.history_cmd import history_command as history_cmd_func
    from .commands.list_cmd import list_sessions as list_sessions_func
except ImportError:
    # Handle TUI standalone import context - commands are not needed there
    context_cmd_func = None  # type: ignore[assignment,misc]
    harness_cmd_func = None  # type: ignore[assignment,misc]
    history_cmd_func = None  # type: ignore[assignment,misc]
    list_sessions_func = None  # type: ignore[assignment,misc]


def teleport_command(args):
    """Export a session bundle for cross-session context transfer."""
    import json as json_module
    from pathlib import Path

    from .orchestrator import get_orchestrator

    session_id = args.session_id
    include_docs = not getattr(args, "no_docs", False)
    output_path = getattr(args, "output", None)

    # Get orchestrator singleton
    orch = get_orchestrator()
    sessions = orch.discover_all(max_age_hours=168)  # 7 days

    # Find matching session by prefix
    session = next((s for s in sessions if s.session_id.startswith(session_id)), None)

    if not session:
        console.print(f"[red]Session not found: {session_id}[/red]")
        return

    try:
        bundle = orch.export_teleport(session, include_planning_docs=include_docs)

        # Serialize to JSON
        bundle_dict = {
            "source_session": bundle.source_session,
            "source_model": bundle.source_model,
            "intent": bundle.intent,
            "decisions": bundle.decisions,
            "files_touched": bundle.files_touched,
            "hot_files": bundle.hot_files,
            "pending_todos": bundle.pending_todos,
            "last_action": bundle.last_action,
            "timestamp": bundle.timestamp.isoformat(),
            "planning_docs": bundle.planning_docs,
        }

        json_output = json_module.dumps(bundle_dict, indent=2)

        if output_path:
            Path(output_path).write_text(json_output)
            console.print(f"[green]Teleport bundle written to {output_path}[/green]")
        else:
            print(json_output)

    except Exception as e:
        console.print(f"[red]Error exporting teleport bundle: {e}[/red]")


def watch_command(args):
    """Watch command handler."""
    session_id = getattr(args, "session_id", None)
    if session_id:
        # Find and watch specific session
        sessions = find_sessions(max_age_hours=48)
        session = None
        for s in sessions:
            if s.session_id.startswith(session_id):
                session = s
                break
        if not session:
            console.print(f"[red]Session not found: {session_id}[/red]")
            console.print("Use 'mc list' to see available sessions.")
            sys.exit(1)
        watch_session(session)
    else:
        # Watch most active session
        session = find_active_session()
        if not session:
            console.print("[yellow]No active session found.[/yellow]")
            console.print("Use 'mc list' to see available sessions.")
            sys.exit(1)
        watch_session(session)


def list_sessions():
    """List sessions command handler."""
    if list_sessions_func is not None:
        list_sessions_func()
    else:
        console.print("[red]List command not available in this context.[/red]")


def main():
    """Main entry point."""
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="""
Motus Command: Command Center for AI Agents.
Run 'mc' with no arguments for mission control.
Run 'mc --help' for a list of commands.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # `mc watch` - can take optional session_id
    watch_parser = subparsers.add_parser("watch", help="Watch a session in real-time")
    watch_parser.add_argument("session_id", nargs="?", help="Session ID to watch (optional)")

    # `mc list` - no arguments
    subparsers.add_parser("list", help="List recent sessions")

    # `mc dashboard` - no arguments
    subparsers.add_parser("dashboard", help="Multi-session dashboard view")
    subparsers.add_parser("web", help="Launch web dashboard (alias for dashboard)")

    # `mc context` - no arguments
    subparsers.add_parser("context", help="Generate context summary for AI agent prompts")

    # `mc summary` - can take optional session_id
    summary_parser = subparsers.add_parser(
        "summary", help="Generate a rich summary for CLAUDE.md injection"
    )
    summary_parser.add_argument("session_id", nargs="?", help="Session ID to summarize (optional)")

    # `mc intent`
    intent_parser = subparsers.add_parser("intent", help="Extract/show intent from a session")
    intent_parser.add_argument("session_id", help="Session ID to analyze")
    intent_parser.add_argument("--save", action="store_true", help="Save intent to .mc/intent.yaml")

    # `mc harness`
    harness_parser = subparsers.add_parser("harness", help="Detect test harness for a repository")
    harness_parser.add_argument(
        "--save", action="store_true", help="Save detected harness to .mc/harness.yaml"
    )

    # `mc checkpoint`
    checkpoint_parser = subparsers.add_parser("checkpoint", help="Create a state checkpoint")
    checkpoint_parser.add_argument("label", help="A descriptive label for the checkpoint")

    # `mc checkpoints`
    subparsers.add_parser("checkpoints", help="List all available checkpoints")

    # `mc rollback`
    rollback_parser = subparsers.add_parser(
        "rollback", help="Restore state to a previous checkpoint"
    )
    rollback_parser.add_argument("checkpoint_id", help="Checkpoint ID to roll back to")

    # `mc diff`
    diff_parser = subparsers.add_parser(
        "diff", help="Show changes between current state and a checkpoint"
    )
    diff_parser.add_argument("checkpoint_id", help="Checkpoint ID to diff against")

    # Add history command to parser
    subparsers.add_parser("history", help="Show command history")

    # `mc teleport` - export a session bundle for cross-session context transfer
    teleport_parser = subparsers.add_parser(
        "teleport", help="Export a session bundle for cross-session context transfer"
    )
    teleport_parser.add_argument("session_id", help="Session ID to export")
    teleport_parser.add_argument(
        "--no-docs",
        action="store_true",
        help="Exclude planning docs (ROADMAP, ARCHITECTURE, etc.) from bundle",
    )
    teleport_parser.add_argument(
        "-o", "--output", help="Output file path (default: stdout as JSON)"
    )

    args = parser.parse_args()
    command = args.command

    # Command dispatch
    if command == "harness" and harness_cmd_func is not None:
        harness_cmd_func(save=getattr(args, "save", False))
    elif command == "context" and context_cmd_func is not None:
        context_cmd_func(session_id=getattr(args, "session_id", None))
    elif command == "history" and history_cmd_func is not None:
        history_cmd_func()
    elif command == "watch":
        watch_command(args)
    elif command in ("list", "ls"):
        list_sessions()
    elif command in ("dashboard", "web"):
        from .ui.web import run_web

        run_web()
    elif command == "summary":
        summary_command(args.session_id)
    elif command == "teleport":
        teleport_command(args)
    else:
        # Default to mission control
        mission_control()


if __name__ == "__main__":
    main()
