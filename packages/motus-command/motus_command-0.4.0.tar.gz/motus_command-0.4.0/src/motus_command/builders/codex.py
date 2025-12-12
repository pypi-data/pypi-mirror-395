"""
Codex Builder - OpenAI Codex CLI session discovery and parsing.

Handles ~/.codex/sessions/ directory structure and JSONL transcript parsing.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from ..commands.utils import assess_risk
from ..logging import get_logger
from ..protocols import (
    EventType,
    RawSession,
    Source,
    UnifiedEvent,
)
from .base import BaseBuilder

logger = get_logger(__name__)

# Maximum file size to parse (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

# Map Codex tool names to unified names
CODEX_TOOL_MAP = {
    "shell_command": "Bash",
    "update_plan": "TodoWrite",
    "list_mcp_resources": "MCP",
    "read_file": "Read",
    "write_file": "Write",
    "edit_file": "Edit",
    "create_file": "Write",
}


def map_codex_tool(tool_name: str) -> str:
    """Map Codex tool name to unified tool name."""
    if tool_name in CODEX_TOOL_MAP:
        return CODEX_TOOL_MAP[tool_name]
    # Check for MCP prefix
    if tool_name.startswith("mcp__"):
        return "MCP"
    return tool_name


class CodexBuilder(BaseBuilder):
    """
    Builder for OpenAI Codex CLI sessions.

    Discovers and parses sessions from ~/.codex/sessions/<date>/*.jsonl
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._codex_dir = Path.home() / ".codex"
        self._sessions_dir = self._codex_dir / "sessions"

    @property
    def source_name(self) -> Source:
        return Source.CODEX

    def discover(self, max_age_hours: int = 24) -> List[RawSession]:
        """
        Find all Codex sessions within age limit.

        Returns:
            List of RawSession objects for Codex sessions.
        """
        sessions: List[RawSession] = []
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        if not self._sessions_dir.exists():
            return sessions

        # Walk through year/month/day directories
        for jsonl_file in self._sessions_dir.rglob("*.jsonl"):
            try:
                stat = jsonl_file.stat()
                modified = datetime.fromtimestamp(stat.st_mtime)

                if modified < cutoff:
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

                    sessions.append(
                        RawSession(
                            session_id=session_id,
                            source=Source.CODEX,
                            file_path=jsonl_file,
                            project_path=cwd,
                            last_modified=modified,
                            size=stat.st_size,
                        )
                    )
            except (OSError, json.JSONDecodeError) as e:
                self._logger.debug(f"Error reading Codex session {jsonl_file}: {e}")
                continue

        self._logger.debug(f"Discovered {len(sessions)} Codex sessions")
        return sessions

    def parse_events(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Parse Codex JSONL transcript into unified events.

        Handles:
        - response_item with function_call (tool calls)
        - response_item with message (assistant responses)
        - event_msg with user_message
        - turn_context (turn boundaries)
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

        # Size guard
        try:
            file_size = file_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                self._logger.warning(f"Skipping large Codex file: {file_path} ({file_size} bytes)")
                return events
        except OSError:
            return events

        try:
            with open(file_path, "r") as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        parsed = self._parse_line(data, session_id)
                        events.extend(parsed)
                    except json.JSONDecodeError as e:
                        self._logger.debug(f"Invalid JSON at line {line_num} in {file_path}: {e}")
                        continue
        except OSError as e:
            self._logger.error(f"Error reading transcript {file_path}: {e}")

        return events

    def _parse_line(self, data: Dict, session_id: str) -> List[UnifiedEvent]:
        """Parse a single JSONL line into events."""
        events: List[UnifiedEvent] = []
        event_type = data.get("type", "")
        timestamp = self._parse_timestamp(data)
        payload = data.get("payload", {})

        if event_type == "session_meta":
            # Skip session metadata
            return events

        if event_type == "response_item":
            events.extend(self._parse_response_item(payload, session_id, timestamp))

        elif event_type == "event_msg":
            events.extend(self._parse_event_msg(payload, session_id, timestamp))

        return events

    def _parse_timestamp(self, data: Dict) -> datetime:
        """Extract timestamp from event data."""
        ts = data.get("timestamp")
        if ts:
            try:
                return datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
        return datetime.now()

    def _parse_response_item(
        self, payload: Dict[str, Any], session_id: str, timestamp: datetime
    ) -> List[UnifiedEvent]:
        """Parse a response_item event (tool calls, text output)."""
        events: List[UnifiedEvent] = []
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

            # Map tool name to unified name
            unified_tool = map_codex_tool(tool_name)

            # Handle Task tool (subagent spawn) specially
            if unified_tool == "Task":
                agent_type = arguments.get("subagent_type", "general")
                description = arguments.get("description", "")
                prompt = arguments.get("prompt", "")
                context_text = arguments.get("context", "")
                agent_model = arguments.get("model")

                events.append(
                    UnifiedEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        timestamp=timestamp,
                        event_type=EventType.AGENT_SPAWN,
                        content=f"{agent_type}: {description[:100]}",
                        agent_type=agent_type,
                        agent_description=description,
                        agent_prompt=prompt,
                        agent_model=agent_model,
                        raw_data={
                            "full_description": description,
                            "full_prompt": prompt,
                            "context": context_text,
                            "depth": 1,
                        },
                    )
                )
            else:
                # Extract file path if present (try multiple key variants)
                file_path = (
                    arguments.get("file_path") or arguments.get("path") or arguments.get("workdir")
                )

                # Create tool event
                events.append(
                    self._create_tool_event(
                        name=unified_tool,
                        input_data=arguments,
                        session_id=session_id,
                        timestamp=timestamp,
                        risk_level=assess_risk(unified_tool, arguments),
                    )
                )

            # Create synthetic thinking surrogate for tool planning
            # (Codex doesn't expose thinking blocks like Claude)
            thinking_content = f"Planning: {unified_tool}"
            if unified_tool == "Bash":
                cmd = arguments.get("command", "")[:100]
                thinking_content = f"Planning to run: {cmd}"
            elif unified_tool in ("Write", "Edit"):
                thinking_content = f"Planning to modify: {file_path or 'file'}"
            elif unified_tool == "Read":
                thinking_content = f"Planning to read: {file_path or 'file'}"

            events.append(
                UnifiedEvent(
                    event_id=str(uuid.uuid4()),
                    session_id=session_id,
                    timestamp=timestamp,
                    event_type=EventType.THINKING,
                    content=thinking_content,
                    raw_data={"synthetic": True, "source": "codex_surrogate"},
                )
            )

            # Track file operations
            if unified_tool in ("Read", "Glob", "Grep") and file_path:
                events.append(
                    UnifiedEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        timestamp=timestamp,
                        event_type=EventType.FILE_READ,
                        content=f"Read: {Path(file_path).name}",
                        file_path=file_path,
                    )
                )
            elif unified_tool in ("Write", "Edit") and file_path:
                events.append(
                    UnifiedEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        timestamp=timestamp,
                        event_type=EventType.FILE_MODIFIED,
                        content=f"Modified: {Path(file_path).name}",
                        file_path=file_path,
                    )
                )

        elif item_type == "message":
            # Model text output
            content = payload.get("content", [])
            text = ""
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text += item.get("text", "")
            elif isinstance(content, str):
                text = content

            if text:
                events.append(
                    UnifiedEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        timestamp=timestamp,
                        event_type=EventType.RESPONSE,
                        content=text[:500],
                        raw_data={"full_text": text} if len(text) > 500 else {},
                    )
                )

                # Extract decisions from response text
                events.extend(self._extract_decisions_from_text(text, session_id, timestamp))

        return events

    def _parse_event_msg(
        self, payload: Dict[str, Any], session_id: str, timestamp: datetime
    ) -> List[UnifiedEvent]:
        """Parse an event_msg (user input, system events)."""
        msg_type = payload.get("type")

        if msg_type == "user_message" or payload.get("role") == "user":
            content = payload.get("content", "")
            if isinstance(content, list):
                content = " ".join(str(c.get("text", c)) for c in content if isinstance(c, dict))

            if content:
                return [
                    UnifiedEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        timestamp=timestamp,
                        event_type=EventType.USER_MESSAGE,
                        content=str(content)[:500],
                    )
                ]

        return []

    def extract_thinking(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract thinking events from transcript.

        For Codex, we generate synthetic thinking surrogates since
        Codex doesn't expose raw thinking blocks.
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

        try:
            with open(file_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        if data.get("type") == "response_item":
                            payload = data.get("payload", {})
                            if payload.get("type") == "function_call":
                                timestamp = self._parse_timestamp(data)
                                tool_name = payload.get("name", "")
                                arguments = payload.get("arguments", {})

                                if isinstance(arguments, str):
                                    try:
                                        arguments = json.loads(arguments)
                                    except json.JSONDecodeError:
                                        arguments = {}

                                unified_tool = map_codex_tool(tool_name)
                                thinking_content = self._build_thinking_surrogate(
                                    unified_tool, arguments
                                )

                                events.append(
                                    self._create_thinking_event(
                                        content=thinking_content,
                                        session_id=session_id,
                                        timestamp=timestamp,
                                    )
                                )
                    except json.JSONDecodeError:
                        continue
        except OSError as e:
            self._logger.error(f"Error reading transcript {file_path}: {e}")

        return events

    def _build_thinking_surrogate(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Build a synthetic thinking description for a tool call."""
        if tool_name == "Bash":
            cmd = arguments.get("command", "")[:100]
            return f"Executing shell command: {cmd}"
        elif tool_name in ("Write", "Edit"):
            path = arguments.get("path", arguments.get("workdir", "file"))
            return f"Modifying file: {path}"
        elif tool_name == "Read":
            path = arguments.get("path", "file")
            return f"Reading file: {path}"
        elif tool_name == "TodoWrite":
            return "Updating plan/todo list"
        else:
            return f"Using tool: {tool_name}"

    def extract_decisions(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract decision events from transcript.

        For Codex, we extract decisions from response text.
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

        try:
            with open(file_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        if data.get("type") == "response_item":
                            payload = data.get("payload", {})
                            if payload.get("type") == "message":
                                timestamp = self._parse_timestamp(data)
                                content = payload.get("content", [])

                                text = ""
                                if isinstance(content, list):
                                    for item in content:
                                        if isinstance(item, dict) and item.get("type") == "text":
                                            text += item.get("text", "")
                                elif isinstance(content, str):
                                    text = content

                                if text:
                                    events.extend(
                                        self._extract_decisions_from_text(
                                            text, session_id, timestamp
                                        )
                                    )
                    except json.JSONDecodeError:
                        continue
        except OSError as e:
            self._logger.error(f"Error reading transcript {file_path}: {e}")

        return events

    def get_last_action(self, file_path: Path) -> str:
        """
        Get the last action from a session file for crash detection.

        Returns human-readable description of last tool action.
        """
        try:
            file_size = file_path.stat().st_size
            read_size = min(10000, file_size)

            with open(file_path, "rb") as f:
                f.seek(max(0, file_size - read_size))
                content = f.read().decode("utf-8", errors="ignore")

            for line in reversed(content.strip().split("\n")):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if data.get("type") == "response_item":
                        payload = data.get("payload", {})
                        if payload.get("type") == "function_call":
                            tool_name = payload.get("name", "")
                            arguments = payload.get("arguments", {})

                            if isinstance(arguments, str):
                                try:
                                    arguments = json.loads(arguments)
                                except json.JSONDecodeError:
                                    arguments = {}

                            unified_name = map_codex_tool(tool_name)

                            if unified_name == "Bash":
                                cmd = arguments.get("command", "")[:50]
                                return f"Bash: {cmd}"
                            elif unified_name in ("Write", "Edit"):
                                path = arguments.get("path", arguments.get("workdir", ""))
                                return f"{unified_name} {path}"
                            elif unified_name == "Read":
                                path = arguments.get("path", "")
                                return f"Read {path}"
                            else:
                                return unified_name
                except json.JSONDecodeError:
                    continue
            return ""
        except Exception as e:
            self._logger.debug(f"Error getting last action from {file_path}: {e}")
            return ""

    def has_completion_marker(self, file_path: Path) -> bool:
        """
        Check if session has a completion marker after last tool call.

        A completion marker indicates the session finished normally.
        """
        try:
            file_size = file_path.stat().st_size
            read_size = min(10000, file_size)

            with open(file_path, "rb") as f:
                f.seek(max(0, file_size - read_size))
                content = f.read().decode("utf-8", errors="ignore")

            found_tool_call = False
            found_response_after_tool = False

            for line in reversed(content.strip().split("\n")):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if data.get("type") == "response_item":
                        payload = data.get("payload", {})
                        if payload.get("type") == "function_call":
                            found_tool_call = True
                            if found_response_after_tool:
                                return True
                        elif found_tool_call:
                            # Any non-function-call response after tool = completion
                            found_response_after_tool = True
                except json.JSONDecodeError:
                    continue

            return found_response_after_tool
        except Exception as e:
            self._logger.debug(f"Error checking completion marker in {file_path}: {e}")
            return False
