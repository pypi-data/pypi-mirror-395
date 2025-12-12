"""
Codex CLI Transcript Parser.

Parses OpenAI Codex CLI session transcripts from ~/.codex/sessions/.
Maps Codex events to MC's unified event format.
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .commands.utils import assess_risk

logger = logging.getLogger(__name__)

# Maximum file size to parse (50MB) - prevents OOM on large files
MAX_FILE_SIZE = 50 * 1024 * 1024


@dataclass
class CodexSession:
    """Represents a Codex CLI session."""

    session_id: str
    transcript_path: Path
    project_path: str  # cwd from session_meta
    start_time: Optional[datetime] = None
    source: str = "codex"

    @property
    def display_name(self) -> str:
        """Short display name for UI."""
        return self.project_path.split("/")[-1] if self.project_path else "unknown"


# Map Codex tool names to MC unified names
CODEX_TOOL_MAP = {
    "shell_command": "Bash",
    "update_plan": "TodoWrite",
    "list_mcp_resources": "MCP",
    "mcp__": "MCP",  # prefix for all MCP tools
    "read_file": "Read",
    "write_file": "Write",
    "edit_file": "Edit",
    "create_file": "Write",
}


def map_codex_tool(tool_name: str) -> str:
    """Map Codex tool name to MC unified tool name."""
    if tool_name in CODEX_TOOL_MAP:
        return CODEX_TOOL_MAP[tool_name]
    # Check for MCP prefix
    if tool_name.startswith("mcp__"):
        return "MCP"
    # Return original if no mapping
    return tool_name


class CodexTranscriptParser:
    """Parser for Codex CLI transcript files."""

    def __init__(self):
        self.codex_dir = Path.home() / ".codex"
        self.sessions_dir = self.codex_dir / "sessions"

    def find_sessions(self, max_age_hours: int = 24) -> List[CodexSession]:
        """Find all Codex sessions within max_age_hours."""
        sessions: List[CodexSession] = []

        if not self.sessions_dir.exists():
            return sessions

        cutoff = datetime.now().timestamp() - (max_age_hours * 3600)

        # Walk through year/month/day directories
        for jsonl_file in self.sessions_dir.rglob("*.jsonl"):
            try:
                # Check file age
                if jsonl_file.stat().st_mtime < cutoff:
                    continue

                # Parse session metadata from first line
                with open(jsonl_file, "r") as f:
                    first_line = f.readline()
                    if not first_line:
                        continue

                    data = json.loads(first_line)
                    if data.get("type") != "session_meta":
                        continue

                    payload = data.get("payload", {})
                    session_id = payload.get("id", jsonl_file.stem)
                    cwd = payload.get("cwd", "")
                    timestamp_str = payload.get("timestamp", "")

                    start_time = None
                    if timestamp_str:
                        try:
                            start_time = datetime.fromisoformat(
                                timestamp_str.replace("Z", "+00:00")
                            )
                        except (ValueError, TypeError):
                            pass

                    sessions.append(
                        CodexSession(
                            session_id=session_id,
                            transcript_path=jsonl_file,
                            project_path=cwd,
                            start_time=start_time,
                            source="codex",
                        )
                    )
            except Exception:
                continue

        # Sort by modification time, newest first
        sessions.sort(key=lambda s: s.transcript_path.stat().st_mtime, reverse=True)
        return sessions

    def parse_events(self, transcript_path: Path) -> Iterator[Dict[str, Any]]:
        """
        Parse a Codex transcript file and yield unified MC events.

        Yields events in MC format:
        {
            "event_type": str,  # "tool_call", "thinking", "user_message", etc.
            "tool_name": str,   # Unified tool name
            "content": str,     # Event content/description
            "timestamp": str,   # ISO timestamp
            "risk_level": str,  # "safe", "medium", "high"
            "file_path": str,   # If applicable
            "raw": dict,        # Original Codex event
        }
        """
        if not transcript_path.exists():
            return

        # Size guard to prevent OOM on large files
        try:
            file_size = transcript_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                logger.warning(f"Skipping large Codex file: {transcript_path} ({file_size} bytes)")
                return
        except OSError:
            return

        with open(transcript_path, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    event = self._parse_event(data)
                    if event:
                        yield event
                except json.JSONDecodeError:
                    continue

    def _parse_event(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a single Codex event into MC format."""
        event_type = data.get("type")
        timestamp = data.get("timestamp", "")
        payload = data.get("payload", {})

        if event_type == "session_meta":
            # Skip session metadata
            return None

        if event_type == "response_item":
            return self._parse_response_item(payload, timestamp)

        if event_type == "event_msg":
            return self._parse_event_msg(payload, timestamp)

        if event_type == "turn_context":
            return self._parse_turn_context(payload, timestamp)

        return None

    def _parse_response_item(
        self, payload: Dict[str, Any], timestamp: str
    ) -> Optional[Dict[str, Any]]:
        """Parse a response_item event (tool calls, text output)."""
        item_type = payload.get("type")

        if item_type == "function_call":
            tool_name = payload.get("name", "unknown")
            arguments = payload.get("arguments", {})

            # Parse arguments if string
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except (json.JSONDecodeError, TypeError):
                    arguments = {"raw": arguments}

            # Map tool name
            unified_tool = map_codex_tool(tool_name)

            # Extract file path if present
            file_path = None
            if "workdir" in arguments:
                file_path = arguments.get("workdir")
            if "path" in arguments:
                file_path = arguments.get("path")

            # Determine risk level using centralized assessment
            risk_level = assess_risk(unified_tool, arguments)

            # Build content description
            content = self._build_tool_content(tool_name, arguments)

            return {
                "event_type": "tool_call",
                "tool_name": unified_tool,
                "content": content,
                "timestamp": timestamp,
                "risk_level": risk_level,
                "file_path": file_path,
                "raw": payload,
            }

        if item_type == "message":
            # Model text output
            content = payload.get("content", [])
            text = ""
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text += item.get("text", "")
            elif isinstance(content, str):
                text = content

            return {
                "event_type": "assistant_message",
                "tool_name": None,
                "content": text[:500] if text else "",
                "timestamp": timestamp,
                "risk_level": "safe",
                "file_path": None,
                "raw": payload,
            }

        return None

    def _parse_event_msg(self, payload: Dict[str, Any], timestamp: str) -> Optional[Dict[str, Any]]:
        """Parse an event_msg (user input, system events)."""
        msg_type = payload.get("type")

        if msg_type == "user_message" or payload.get("role") == "user":
            content = payload.get("content", "")
            if isinstance(content, list):
                content = " ".join(str(c.get("text", c)) for c in content if isinstance(c, dict))

            return {
                "event_type": "user_message",
                "tool_name": None,
                "content": str(content)[:500],
                "timestamp": timestamp,
                "risk_level": "safe",
                "file_path": None,
                "raw": payload,
            }

        return None

    def _parse_turn_context(
        self, payload: Dict[str, Any], timestamp: str
    ) -> Optional[Dict[str, Any]]:
        """Parse a turn_context event (turn boundaries)."""
        # Turn context marks conversation turns, useful for Intent Tracker
        return {
            "event_type": "turn_boundary",
            "tool_name": None,
            "content": "Turn boundary",
            "timestamp": timestamp,
            "risk_level": "safe",
            "file_path": None,
            "raw": payload,
        }

    def _build_tool_content(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Build a human-readable content string for a tool call."""
        if tool_name == "shell_command":
            cmd = arguments.get("command", "")
            workdir = arguments.get("workdir", ".")
            return f"{cmd} (in {workdir})"

        if tool_name == "update_plan":
            plan = arguments.get("plan", arguments.get("explanation", ""))
            if isinstance(plan, list):
                return f"Updated plan ({len(plan)} steps)"
            return str(plan)[:100]

        if "path" in arguments:
            return arguments["path"]

        # Default: return first string value or tool name
        for v in arguments.values():
            if isinstance(v, str) and len(v) < 200:
                return v

        return tool_name


def get_codex_parser() -> CodexTranscriptParser:
    """Get a Codex transcript parser instance."""
    return CodexTranscriptParser()


# Singleton parser for line-level parsing
_parser_instance: Optional[CodexTranscriptParser] = None


def parse_codex_line(line: str) -> Optional[Dict[str, Any]]:
    """
    Parse a single JSONL line from a Codex transcript.

    This is useful for incremental/streaming parsing where you read
    the file line by line instead of all at once.

    Returns:
        Dict with event data, or None if the line is not a displayable event.
    """
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = CodexTranscriptParser()

    try:
        data = json.loads(line)
        return _parser_instance._parse_event(data)
    except json.JSONDecodeError:
        return None


if __name__ == "__main__":
    # Test the parser
    parser = CodexTranscriptParser()
    sessions = parser.find_sessions(max_age_hours=720)  # Last 30 days
    print(f"Found {len(sessions)} Codex sessions")

    if sessions:
        latest = sessions[0]
        print(f"\nLatest session: {latest.session_id[:12]}")
        print(f"Project: {latest.project_path}")

        events = list(parser.parse_events(latest.transcript_path))
        print(f"Events: {len(events)}")

        # Count by type
        from collections import Counter

        types = Counter(e["event_type"] for e in events)
        print(f"Event types: {dict(types)}")
