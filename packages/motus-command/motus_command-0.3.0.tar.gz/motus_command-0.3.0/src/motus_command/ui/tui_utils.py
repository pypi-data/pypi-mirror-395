"""Pure utility functions for TUI - easily testable without Textual."""

import re
from datetime import datetime, timedelta
from typing import Optional


def strip_markup(text: str) -> str:
    """Remove Rich markup tags from text.

    Args:
        text: Text possibly containing Rich markup

    Returns:
        Clean text without markup tags
    """
    # Remove Rich markup like [bold], [red], etc.
    return re.sub(r"\[/?[^\]]+\]", "", text)


def format_timestamp(dt: datetime) -> str:
    """Format a datetime for display.

    Args:
        dt: Datetime to format

    Returns:
        Formatted string like "14:32:05" or "Yesterday 14:32"
    """
    now = datetime.now()

    if dt.date() == now.date():
        return dt.strftime("%H:%M:%S")
    elif dt.date() == (now - timedelta(days=1)).date():
        return f"Yesterday {dt.strftime('%H:%M')}"
    else:
        return dt.strftime("%Y-%m-%d %H:%M")


def format_file_size(size_bytes: int) -> str:
    """Format file size for display.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable size string
    """
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f}GB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length with suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def extract_intent_from_thinking(thinking: str) -> Optional[str]:
    """Extract the main intent from a thinking block.

    Looks for patterns like "I'll", "I'm going to", "Let me" to find
    what the AI intends to do.

    Args:
        thinking: The thinking/reasoning text

    Returns:
        Extracted intent or None
    """
    intent_patterns = [
        r"I'll ([^.]+)\.",
        r"I'm going to ([^.]+)\.",
        r"Let me ([^.]+)\.",
        r"I will ([^.]+)\.",
        r"I should ([^.]+)\.",
        r"I need to ([^.]+)\.",
    ]

    for pattern in intent_patterns:
        match = re.search(pattern, thinking, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def calculate_progress_percentage(current: int, total: int) -> int:
    """Calculate progress percentage safely.

    Args:
        current: Current progress value
        total: Total value

    Returns:
        Percentage (0-100)
    """
    if total <= 0:
        return 0
    return min(100, max(0, int((current / total) * 100)))


def parse_tool_call_summary(tool_name: str, tool_input: dict) -> str:
    """Create a one-line summary of a tool call.

    Args:
        tool_name: Name of the tool
        tool_input: Tool input parameters

    Returns:
        Summary string
    """
    if tool_name == "Read":
        path = tool_input.get("file_path", "")
        return f"Reading {path.split('/')[-1] if path else 'file'}"

    if tool_name == "Write":
        path = tool_input.get("file_path", "")
        return f"Writing {path.split('/')[-1] if path else 'file'}"

    if tool_name == "Edit":
        path = tool_input.get("file_path", "")
        return f"Editing {path.split('/')[-1] if path else 'file'}"

    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        # Truncate long commands
        if len(cmd) > 50:
            cmd = cmd[:47] + "..."
        return f"$ {cmd}"

    if tool_name == "Grep":
        pattern = tool_input.get("pattern", "")
        return f"Searching for '{pattern[:30]}'"

    if tool_name == "Glob":
        pattern = tool_input.get("pattern", "")
        return f"Finding files: {pattern}"

    if tool_name == "Task":
        desc = tool_input.get("description", "task")
        return f"Spawning: {desc}"

    if tool_name == "TodoWrite":
        todos = tool_input.get("todos", [])
        return f"Updating todos ({len(todos)} items)"

    # Default
    return tool_name


def get_risk_color(risk_level: str) -> str:
    """Get color for risk level.

    Args:
        risk_level: Risk level string

    Returns:
        Color name for Rich/Textual
    """
    colors = {
        "high": "red",
        "medium": "yellow",
        "low": "blue",
        "safe": "green",
    }
    return colors.get(risk_level, "white")


def get_status_icon(status: str) -> str:
    """Get icon for status.

    Args:
        status: Status string

    Returns:
        Unicode icon
    """
    icons = {
        "active": "🟢",
        "idle": "⚪",
        "paused": "⏸️",
        "error": "🔴",
        "complete": "✅",
        "running": "▶️",
        "thinking": "💭",
        "tool": "🔧",
    }
    return icons.get(status, "•")


def filter_events_by_type(
    events: list[dict],
    event_types: Optional[list[str]] = None,
    exclude_types: Optional[list[str]] = None,
) -> list[dict]:
    """Filter events by type.

    Args:
        events: List of event dicts
        event_types: Types to include (None = all)
        exclude_types: Types to exclude

    Returns:
        Filtered event list
    """
    result = events

    if event_types:
        result = [e for e in result if e.get("type") in event_types]

    if exclude_types:
        result = [e for e in result if e.get("type") not in exclude_types]

    return result


def filter_events_by_risk(
    events: list[dict],
    min_risk: str = "safe",
) -> list[dict]:
    """Filter events by minimum risk level.

    Args:
        events: List of event dicts
        min_risk: Minimum risk level to include

    Returns:
        Filtered event list
    """
    risk_order = ["safe", "low", "medium", "high", "critical"]

    try:
        min_idx = risk_order.index(min_risk)
    except ValueError:
        min_idx = 0

    def get_risk_idx(event: dict) -> int:
        risk = event.get("risk_level", "safe")
        try:
            return risk_order.index(risk)
        except ValueError:
            return 0  # Default to safe for unknown levels

    return [e for e in events if get_risk_idx(e) >= min_idx]


def group_events_by_session(
    events: list[dict],
) -> dict[str, list[dict]]:
    """Group events by session ID.

    Args:
        events: List of event dicts with session_id

    Returns:
        Dict mapping session_id to events
    """
    groups: dict[str, list[dict]] = {}

    for event in events:
        session_id = event.get("session_id", "unknown")
        if session_id not in groups:
            groups[session_id] = []
        groups[session_id].append(event)

    return groups


def calculate_session_health(
    tool_counts: dict[str, int],
    error_count: int = 0,
    thinking_count: int = 0,
) -> tuple[int, str]:
    """Calculate session health score and status.

    Args:
        tool_counts: Dict of tool name to count
        error_count: Number of errors
        thinking_count: Number of thinking blocks

    Returns:
        Tuple of (health_score 0-100, status_string)
    """
    # Start with base score
    score = 50

    # Positive signals
    productive_tools = tool_counts.get("Edit", 0) + tool_counts.get("Write", 0)
    if productive_tools > 0:
        score += min(30, productive_tools * 5)

    if thinking_count > 0:
        score += min(10, thinking_count * 2)

    # Negative signals
    score -= min(30, error_count * 10)

    # High-risk operations
    bash_count = tool_counts.get("Bash", 0)
    if bash_count > 10:
        score -= 10

    # Clamp score
    score = max(10, min(95, score))

    # Determine status
    if error_count > 3:
        status = "needs_attention"
    elif score >= 75:
        status = "on_track"
    elif score >= 50:
        status = "working"
    else:
        status = "struggling"

    return score, status
