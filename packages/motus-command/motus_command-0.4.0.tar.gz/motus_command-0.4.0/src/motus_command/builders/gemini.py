"""
Gemini Builder - Google Gemini CLI session discovery and parsing.

Handles ~/.gemini/tmp/<project_hash>/chats/ directory structure and JSON transcript parsing.
Note: Gemini uses single JSON files, not JSONL like Claude/Codex.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from ..commands.utils import assess_risk
from ..logging import get_logger
from ..protocols import (
    EventType,
    RawSession,
    RiskLevel,
    Source,
    UnifiedEvent,
)
from .base import BaseBuilder

logger = get_logger(__name__)

# Maximum file size to parse (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

# Map Gemini tool names to unified names
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
    """Map Gemini function name to unified tool name."""
    if tool_name in GEMINI_TOOL_MAP:
        return GEMINI_TOOL_MAP[tool_name]
    return tool_name


class GeminiBuilder(BaseBuilder):
    """
    Builder for Google Gemini CLI sessions.

    Discovers and parses sessions from ~/.gemini/tmp/<project_hash>/chats/session-*.json
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gemini_dir = Path.home() / ".gemini"
        self._tmp_dir = self._gemini_dir / "tmp"

    @property
    def source_name(self) -> Source:
        return Source.GEMINI

    def discover(self, max_age_hours: int = 24) -> List[RawSession]:
        """
        Find all Gemini sessions within age limit.

        Returns:
            List of RawSession objects for Gemini sessions.
        """
        sessions: List[RawSession] = []
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        if not self._tmp_dir.exists():
            return sessions

        # Walk through project hash directories
        for project_dir in self._tmp_dir.iterdir():
            if not project_dir.is_dir():
                continue

            chats_dir = project_dir / "chats"
            if not chats_dir.exists():
                continue

            for json_file in chats_dir.glob("session-*.json"):
                try:
                    stat = json_file.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime)

                    if modified < cutoff:
                        continue

                    # Skip files that are too large
                    if stat.st_size > MAX_FILE_SIZE:
                        self._logger.warning(f"Skipping large session file: {json_file}")
                        continue

                    # Parse session metadata
                    with open(json_file, "r") as f:
                        data = json.load(f)

                    session_id = data.get("sessionId", json_file.stem)
                    project_hash = data.get("projectHash", project_dir.name)

                    # Gemini doesn't store project path, use hash
                    project_path = f"gemini:{project_hash[:8]}"

                    sessions.append(
                        RawSession(
                            session_id=session_id,
                            source=Source.GEMINI,
                            file_path=json_file,
                            project_path=project_path,
                            last_modified=modified,
                            size=stat.st_size,
                        )
                    )
                except (OSError, json.JSONDecodeError) as e:
                    self._logger.debug(f"Error reading Gemini session {json_file}: {e}")
                    continue

        self._logger.debug(f"Discovered {len(sessions)} Gemini sessions")
        return sessions

    def parse_events(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Parse Gemini JSON transcript into unified events.

        Handles:
        - User messages
        - Gemini responses with text content
        - Thinking/thoughts (when available)
        - Tool calls (function calling)
        - Errors (API errors, safety blocks)
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

        # Size guard
        try:
            file_size = file_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                self._logger.warning(f"Skipping large Gemini file: {file_path} ({file_size} bytes)")
                return events
        except OSError:
            return events

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            self._logger.error(f"Error reading Gemini file {file_path}: {e}")
            return events

        messages = data.get("messages", [])

        for msg in messages:
            msg_type = msg.get("type", "")
            content = msg.get("content", "")
            timestamp = self._parse_timestamp_from_msg(msg)

            if msg_type == "user":
                events.append(
                    UnifiedEvent(
                        event_id=str(uuid.uuid4()),
                        session_id=session_id,
                        timestamp=timestamp,
                        event_type=EventType.USER_MESSAGE,
                        content=content[:500] if content else "",
                    )
                )

            elif msg_type == "gemini":
                model = msg.get("model", "")
                tokens = msg.get("tokens", {})
                finish_reason = msg.get("finishReason", "")
                safety_ratings = msg.get("safetyRatings", [])

                # Check for errors
                error = msg.get("error")
                if error:
                    error_msg = (
                        error.get("message", str(error)) if isinstance(error, dict) else str(error)
                    )
                    events.append(
                        UnifiedEvent(
                            event_id=str(uuid.uuid4()),
                            session_id=session_id,
                            timestamp=timestamp,
                            event_type=EventType.ERROR,
                            content=f"API Error: {error_msg}",
                            model=model,
                        )
                    )

                # Check for safety-triggered stop
                if finish_reason == "SAFETY":
                    events.append(
                        UnifiedEvent(
                            event_id=str(uuid.uuid4()),
                            session_id=session_id,
                            timestamp=timestamp,
                            event_type=EventType.ERROR,
                            content="Response blocked by safety filter",
                            model=model,
                            raw_data={"safety_ratings": safety_ratings},
                        )
                    )

                # Process thinking/thoughts (Gemini's reasoning)
                thoughts = msg.get("thoughts", [])
                for thought in thoughts:
                    thought_time = self._parse_timestamp_from_thought(thought, timestamp)
                    subject = thought.get("subject", "")
                    description = thought.get("description", "")
                    thinking_content = f"{subject}: {description}" if subject else description

                    if thinking_content:
                        events.append(
                            self._create_thinking_event(
                                content=thinking_content,
                                session_id=session_id,
                                timestamp=thought_time,
                                model=model,
                            )
                        )

                        # Extract decisions from thinking
                        events.extend(
                            self._extract_decisions_from_text(
                                thinking_content, session_id, thought_time
                            )
                        )

                # Process tool calls
                tool_calls = msg.get("toolCalls", [])
                for tool_call in tool_calls:
                    func_name = tool_call.get("name", "")
                    func_args = tool_call.get("args", {})
                    mapped_name = map_gemini_tool(func_name)

                    # Check for tool errors
                    tool_error = tool_call.get("error")
                    if tool_error:
                        events.append(
                            UnifiedEvent(
                                event_id=str(uuid.uuid4()),
                                session_id=session_id,
                                timestamp=timestamp,
                                event_type=EventType.ERROR,
                                content=f"Tool error ({mapped_name}): {tool_error}",
                                tool_name=mapped_name,
                                model=model,
                            )
                        )

                    # Handle Task tool (subagent spawn) specially
                    if mapped_name == "Task":
                        agent_type = (
                            func_args.get("subagent_type", "general") if func_args else "general"
                        )
                        description = func_args.get("description", "") if func_args else ""
                        prompt = func_args.get("prompt", "") if func_args else ""
                        context_text = func_args.get("context", "") if func_args else ""
                        agent_model = func_args.get("model") if func_args else None

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
                                model=model,
                                raw_data={
                                    "full_description": description,
                                    "full_prompt": prompt,
                                    "context": context_text,
                                    "depth": 1,
                                },
                            )
                        )
                    else:
                        # Convert string risk_level to RiskLevel enum
                        risk_level_str = assess_risk(mapped_name, func_args or {})
                        risk_level_enum = RiskLevel.SAFE  # Default to SAFE

                        if risk_level_str == "safe":
                            risk_level_enum = RiskLevel.SAFE
                        elif risk_level_str == "low":  # Map 'low' to SAFE as per protocols
                            risk_level_enum = RiskLevel.SAFE
                        elif risk_level_str == "medium":
                            risk_level_enum = RiskLevel.MEDIUM
                        elif risk_level_str == "high":
                            risk_level_enum = RiskLevel.HIGH
                        elif risk_level_str == "critical":
                            risk_level_enum = RiskLevel.CRITICAL
                        else:
                            self._logger.warning(
                                f"Unrecognized risk level string '{risk_level_str}'. Defaulting to SAFE."
                            )

                        # Create tool event
                        events.append(
                            self._create_tool_event(
                                name=mapped_name,
                                input_data=func_args or {},
                                session_id=session_id,
                                timestamp=timestamp,
                                risk_level=risk_level_enum,  # Pass the enum member
                            )
                        )

                        # Track file operations (try multiple key variants)
                        file_path_arg = (
                            (func_args.get("file_path") or func_args.get("path"))
                            if func_args
                            else None
                        )
                        if mapped_name in ("Read", "Glob", "Grep") and file_path_arg:
                            events.append(
                                UnifiedEvent(
                                    event_id=str(uuid.uuid4()),
                                    session_id=session_id,
                                    timestamp=timestamp,
                                    event_type=EventType.FILE_READ,
                                    content=f"Read: {Path(file_path_arg).name}",
                                    file_path=file_path_arg,
                                )
                            )
                        elif mapped_name in ("Write", "Edit") and file_path_arg:
                            events.append(
                                UnifiedEvent(
                                    event_id=str(uuid.uuid4()),
                                    session_id=session_id,
                                    timestamp=timestamp,
                                    event_type=EventType.FILE_MODIFIED,
                                    content=f"Modified: {Path(file_path_arg).name}",
                                    file_path=file_path_arg,
                                )
                            )

                # Process response content
                if content:
                    events.append(
                        UnifiedEvent(
                            event_id=str(uuid.uuid4()),
                            session_id=session_id,
                            timestamp=timestamp,
                            event_type=EventType.RESPONSE,
                            content=content[:500],
                            model=model,
                            tokens_used=(
                                tokens.get("output", 0) + tokens.get("input", 0) if tokens else None
                            ),
                            raw_data=(
                                {
                                    "full_text": content,
                                    "finish_reason": finish_reason,
                                }
                                if len(content) > 500 or finish_reason
                                else {}
                            ),
                        )
                    )

                    # Extract decisions from response
                    events.extend(self._extract_decisions_from_text(content, session_id, timestamp))

        return events

    def _parse_timestamp_from_msg(self, msg: Dict) -> datetime:
        """Extract timestamp from message data."""
        timestamp_str = msg.get("timestamp", "")
        if timestamp_str:
            try:
                return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                pass
        return datetime.now()

    def _parse_timestamp_from_thought(self, thought: Dict, fallback: datetime) -> datetime:
        """Extract timestamp from thought data."""
        timestamp_str = thought.get("timestamp", "")
        if timestamp_str:
            try:
                return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                pass
        return fallback

    def extract_thinking(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract thinking events from transcript.

        Gemini has actual thinking/thoughts in the transcript.
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            self._logger.error(f"Error reading Gemini file {file_path}: {e}")
            return events

        for msg in data.get("messages", []):
            if msg.get("type") != "gemini":
                continue

            model = msg.get("model", "")
            timestamp = self._parse_timestamp_from_msg(msg)

            for thought in msg.get("thoughts", []):
                thought_time = self._parse_timestamp_from_thought(thought, timestamp)
                subject = thought.get("subject", "")
                description = thought.get("description", "")
                thinking_content = f"{subject}: {description}" if subject else description

                if thinking_content:
                    events.append(
                        self._create_thinking_event(
                            content=thinking_content,
                            session_id=session_id,
                            timestamp=thought_time,
                            model=model,
                        )
                    )

        return events

    def extract_decisions(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract decision events from transcript.

        Looks in thinking blocks and response text.
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            self._logger.error(f"Error reading Gemini file {file_path}: {e}")
            return events

        for msg in data.get("messages", []):
            if msg.get("type") != "gemini":
                continue

            timestamp = self._parse_timestamp_from_msg(msg)

            # Extract from thoughts
            for thought in msg.get("thoughts", []):
                thought_time = self._parse_timestamp_from_thought(thought, timestamp)
                subject = thought.get("subject", "")
                description = thought.get("description", "")
                text = f"{subject}: {description}" if subject else description
                if text:
                    events.extend(self._extract_decisions_from_text(text, session_id, thought_time))

            # Extract from response content
            content = msg.get("content", "")
            if content:
                events.extend(self._extract_decisions_from_text(content, session_id, timestamp))

        return events

    def get_last_action(self, file_path: Path) -> str:
        """
        Get the last action from a session file for crash detection.

        Returns human-readable description of last tool action.
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            messages = data.get("messages", [])

            # Work backwards through messages
            for msg in reversed(messages):
                if msg.get("type") == "gemini":
                    tool_calls = msg.get("toolCalls", [])
                    if tool_calls:
                        # Get last tool call
                        tool_call = tool_calls[-1]
                        func_name = tool_call.get("name", "")
                        func_args = tool_call.get("args", {})

                        unified_name = map_gemini_tool(func_name)

                        if unified_name == "Bash":
                            cmd = func_args.get("command", "")[:50]
                            return f"Bash: {cmd}"
                        elif unified_name in ("Write", "Edit"):
                            path = func_args.get("path", "")
                            return f"{unified_name} {path}"
                        elif unified_name == "Read":
                            path = func_args.get("path", "")
                            return f"Read {path}"
                        else:
                            return unified_name
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
            with open(file_path, "r") as f:
                data = json.load(f)

            messages = data.get("messages", [])
            if not messages:
                return False

            found_tool_call = False
            found_response_after_tool = False

            for msg in reversed(messages):
                if msg.get("type") == "gemini":
                    tool_calls = msg.get("toolCalls", [])
                    text_content = msg.get("content", "")

                    if tool_calls:
                        found_tool_call = True
                        if found_response_after_tool:
                            return True
                    elif text_content and found_tool_call:
                        # Text response after tool call = completion
                        found_response_after_tool = True

            return found_response_after_tool
        except Exception as e:
            self._logger.debug(f"Error checking completion marker in {file_path}: {e}")
            return False
