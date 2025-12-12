"""
Gemini CLI Transcript Parser.

Parses Google Gemini CLI session files from ~/.gemini/tmp/<project_hash>/chats/.
Maps Gemini events to MC's unified event format.

Session format:
- Single JSON file (not JSONL like Claude/Codex)
- Contains sessionId, projectHash, startTime, lastUpdated, messages[]
- Messages have type: "user" | "gemini"
- Gemini messages include: thoughts[], tokens{}, model
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .commands.utils import assess_risk
from .logging import get_logger

logger = get_logger(__name__)

# Maximum file size to parse (50MB) - prevents OOM on large files
MAX_FILE_SIZE = 50 * 1024 * 1024


@dataclass
class GeminiSession:
    """Represents a Gemini CLI session."""

    session_id: str
    transcript_path: Path
    project_hash: str
    start_time: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    source: str = "gemini"

    @property
    def display_name(self) -> str:
        """Short display name for UI."""
        return self.session_id[:8]


# Map Gemini tool names to MC unified names
# Gemini uses function calling, so these are the known function names
GEMINI_TOOL_MAP = {
    "shell": "Bash",
    "run_shell_command": "Bash",
    "read_file": "Read",
    "write_file": "Write",
    "edit_file": "Edit",
    "search_files": "Grep",
    "list_files": "Glob",
    "web_search": "WebSearch",
    "web_fetch": "WebFetch",
}


def map_gemini_tool(tool_name: str) -> str:
    """Map Gemini function name to MC unified tool name."""
    if tool_name in GEMINI_TOOL_MAP:
        return GEMINI_TOOL_MAP[tool_name]
    return tool_name


@dataclass
class GeminiEvent:
    """A parsed event from a Gemini transcript."""

    event_type: str  # "thinking", "tool", "response", "user_input", "error", "session_end"
    timestamp: datetime
    content: str = ""
    tool_name: str = ""
    tool_input: Optional[Dict[str, Any]] = None
    risk_level: str = "safe"
    model: str = ""
    tokens: Optional[Dict[str, int]] = None
    message_id: str = ""
    # New fields for enhanced observability
    finish_reason: str = ""  # "STOP", "MAX_TOKENS", "SAFETY", etc.
    error_type: str = ""  # "tool_error", "api_error", "safety"
    error_message: str = ""
    safety_ratings: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self):
        if self.tool_input is None:
            self.tool_input = {}
        if self.tokens is None:
            self.tokens = {}
        if self.safety_ratings is None:
            self.safety_ratings = []


class GeminiTranscriptParser:
    """Parser for Gemini CLI transcript files."""

    def __init__(self):
        self.gemini_dir = Path.home() / ".gemini"
        self.tmp_dir = self.gemini_dir / "tmp"

    def find_sessions(self, max_age_hours: int = 24) -> List[GeminiSession]:
        """Find all Gemini sessions within max_age_hours."""
        sessions = []

        if not self.tmp_dir.exists():
            return sessions

        cutoff = datetime.now().timestamp() - (max_age_hours * 3600)

        # Walk through project hash directories
        for project_dir in self.tmp_dir.iterdir():
            if not project_dir.is_dir():
                continue

            chats_dir = project_dir / "chats"
            if not chats_dir.exists():
                continue

            for json_file in chats_dir.glob("session-*.json"):
                try:
                    file_stat = json_file.stat()

                    # Check file age
                    if file_stat.st_mtime < cutoff:
                        continue

                    # Skip files that are too large (OOM protection)
                    if file_stat.st_size > MAX_FILE_SIZE:
                        logger.warning(f"Skipping large session file: {json_file}")
                        continue

                    # Parse session metadata
                    with open(json_file, "r") as f:
                        data = json.load(f)

                    session_id = data.get("sessionId", json_file.stem)
                    project_hash = data.get("projectHash", project_dir.name)

                    start_time = None
                    if data.get("startTime"):
                        try:
                            start_time = datetime.fromisoformat(
                                data["startTime"].replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    last_updated = None
                    if data.get("lastUpdated"):
                        try:
                            last_updated = datetime.fromisoformat(
                                data["lastUpdated"].replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    sessions.append(
                        GeminiSession(
                            session_id=session_id,
                            transcript_path=json_file,
                            project_hash=project_hash,
                            start_time=start_time,
                            last_updated=last_updated,
                        )
                    )
                except (json.JSONDecodeError, OSError) as e:
                    logger.debug(f"Error reading Gemini session {json_file}: {e}")
                    continue

        # Sort by last_updated descending
        sessions.sort(key=lambda s: s.last_updated or datetime.min, reverse=True)
        logger.debug(f"Found {len(sessions)} Gemini sessions")
        return sessions

    def parse_file(self, file_path: Path) -> Iterator[GeminiEvent]:
        """
        Parse a Gemini session JSON file.

        Yields events in chronological order.

        Args:
            file_path: Path to session JSON file

        Yields:
            GeminiEvent objects
        """
        # Size guard to prevent OOM on large files
        try:
            if file_path.stat().st_size > MAX_FILE_SIZE:
                logger.warning(f"Skipping large file in parse_file: {file_path}")
                return
        except OSError:
            return

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Error reading Gemini file {file_path}: {e}")
            return

        messages = data.get("messages", [])

        for msg in messages:
            msg_id = msg.get("id", "")
            msg_type = msg.get("type", "")
            content = msg.get("content", "")
            timestamp_str = msg.get("timestamp", "")

            timestamp = datetime.now()
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            if msg_type == "user":
                yield GeminiEvent(
                    event_type="user_input",
                    timestamp=timestamp,
                    content=content,
                    message_id=msg_id,
                )

            elif msg_type == "gemini":
                model = msg.get("model", "")
                tokens = msg.get("tokens", {})
                finish_reason = msg.get("finishReason", "")
                safety_ratings = msg.get("safetyRatings", [])

                # Check for errors in the message
                error = msg.get("error")
                if error:
                    error_msg = (
                        error.get("message", str(error)) if isinstance(error, dict) else str(error)
                    )
                    yield GeminiEvent(
                        event_type="error",
                        timestamp=timestamp,
                        error_type="api_error",
                        error_message=error_msg,
                        model=model,
                        message_id=msg_id,
                    )

                # Check for safety-triggered stop
                if finish_reason == "SAFETY":
                    yield GeminiEvent(
                        event_type="error",
                        timestamp=timestamp,
                        error_type="safety",
                        error_message="Response blocked by safety filter",
                        safety_ratings=safety_ratings,
                        model=model,
                        message_id=msg_id,
                    )

                # Yield thinking events first
                thoughts = msg.get("thoughts", [])
                for thought in thoughts:
                    thought_time = timestamp
                    if thought.get("timestamp"):
                        try:
                            thought_time = datetime.fromisoformat(
                                thought["timestamp"].replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    yield GeminiEvent(
                        event_type="thinking",
                        timestamp=thought_time,
                        content=f"{thought.get('subject', '')}: {thought.get('description', '')}",
                        model=model,
                        message_id=msg_id,
                    )

                # Yield tool calls if present
                tool_calls = msg.get("toolCalls", [])
                for tool_call in tool_calls:
                    func_name = tool_call.get("name", "")
                    func_args = tool_call.get("args", {})
                    mapped_name = map_gemini_tool(func_name)

                    # Check for tool errors
                    tool_error = tool_call.get("error")
                    if tool_error:
                        yield GeminiEvent(
                            event_type="error",
                            timestamp=timestamp,
                            error_type="tool_error",
                            error_message=str(tool_error),
                            tool_name=mapped_name,
                            model=model,
                            message_id=msg_id,
                        )

                    yield GeminiEvent(
                        event_type="tool",
                        timestamp=timestamp,
                        tool_name=mapped_name,
                        tool_input=func_args,
                        risk_level=assess_risk(mapped_name, func_args or {}),
                        model=model,
                        message_id=msg_id,
                    )

                # Yield response with finish_reason
                if content:
                    yield GeminiEvent(
                        event_type="response",
                        timestamp=timestamp,
                        content=content,
                        model=model,
                        tokens=tokens,
                        message_id=msg_id,
                        finish_reason=finish_reason,
                        safety_ratings=safety_ratings,
                    )


def parse_gemini_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Parse a Gemini session file and return normalized event dicts.

    This is the main entry point for parsing Gemini files.

    Returns:
        List of event dictionaries with unified format:
        {
            "event_type": "thinking" | "tool" | "response" | "user_input" | "error",
            "timestamp": "ISO string",
            "content": "...",
            "tool_name": "...",  # for tool events
            "tool_input": {...},  # for tool events
            "risk_level": "...",  # for tool events
            "model": "...",
            "tokens": {...},
            "finish_reason": "...",  # for response events
            "error_type": "...",  # for error events
            "error_message": "...",  # for error events
        }
    """
    # File size guard to prevent OOM on large files
    try:
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"Skipping large file: {file_path} ({file_size} bytes)")
            return []
    except OSError:
        return []

    parser = GeminiTranscriptParser()
    events = []

    for event in parser.parse_file(file_path):
        event_dict: Dict[str, Any] = {
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat() if event.timestamp else "",
            "content": event.content,
            "tool_name": event.tool_name,
            "tool_input": event.tool_input,
            "risk_level": event.risk_level,
            "model": event.model,
            "tokens": event.tokens,
            "message_id": event.message_id,
        }
        # Add optional fields if present
        if event.finish_reason:
            event_dict["finish_reason"] = event.finish_reason
        if event.error_type:
            event_dict["error_type"] = event.error_type
        if event.error_message:
            event_dict["error_message"] = event.error_message
        if event.safety_ratings:
            event_dict["safety_ratings"] = event.safety_ratings

        events.append(event_dict)

    return events
