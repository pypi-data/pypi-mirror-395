"""
Claude Builder - Claude Code session discovery and parsing.

Handles ~/.claude/projects/ directory structure and JSONL transcript parsing.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from ..commands.utils import extract_project_path
from ..config import config
from ..logging import get_logger
from ..protocols import (
    EventType,
    RawSession,
    Source,
    UnifiedEvent,
)
from .base import BaseBuilder

logger = get_logger(__name__)


class ClaudeBuilder(BaseBuilder):
    """
    Builder for Claude Code sessions.

    Discovers and parses sessions from ~/.claude/projects/<encoded-path>/*.jsonl
    """

    @property
    def source_name(self) -> Source:
        return Source.CLAUDE

    def discover(self, max_age_hours: int = 24) -> List[RawSession]:
        """
        Find all Claude sessions within age limit.

        Returns:
            List of RawSession objects for Claude sessions.
        """
        sessions: List[RawSession] = []
        cutoff = datetime.now() - timedelta(hours=max_age_hours)

        if not config.paths.projects_dir.exists():
            self._logger.debug("Claude projects directory does not exist")
            return sessions

        for project_dir in config.paths.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_path = extract_project_path(project_dir.name)

            for jsonl_file in project_dir.glob("*.jsonl"):
                # Skip agent trace files (sub-agents)
                if jsonl_file.name.startswith("agent-"):
                    continue

                try:
                    stat = jsonl_file.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime)

                    if modified > cutoff:
                        sessions.append(
                            RawSession(
                                session_id=jsonl_file.stem,
                                source=Source.CLAUDE,
                                file_path=jsonl_file,
                                project_path=project_path,
                                last_modified=modified,
                                size=stat.st_size,
                            )
                        )
                except OSError as e:
                    self._logger.debug(f"Error reading session file {jsonl_file}: {e}")
                    continue

        self._logger.debug(f"Discovered {len(sessions)} Claude sessions")
        return sessions

    def parse_events(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Parse Claude JSONL transcript into unified events.

        Handles:
        - assistant messages with text and tool_use blocks
        - tool_result blocks
        - user messages
        - thinking blocks (when available)
        """
        events: List[UnifiedEvent] = []
        session_id = file_path.stem

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

        if event_type == "assistant":
            events.extend(self._parse_assistant_message(data, session_id, timestamp))
        elif event_type == "user":
            events.extend(self._parse_user_message(data, session_id, timestamp))
        elif event_type == "result":
            events.extend(self._parse_result(data, session_id, timestamp))

        return events

    def _parse_timestamp(self, data: Dict) -> datetime:
        """Extract timestamp from event data."""
        # Claude format: "timestamp" field or use now
        ts = data.get("timestamp")
        if ts:
            try:
                return datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
        return datetime.now()

    def _parse_assistant_message(
        self, data: Dict, session_id: str, timestamp: datetime
    ) -> List[UnifiedEvent]:
        """Parse assistant message with content blocks."""
        events: List[UnifiedEvent] = []
        message = data.get("message", {})
        content_blocks = message.get("content", [])
        model = message.get("model", data.get("model"))

        for block in content_blocks:
            block_type = block.get("type")

            if block_type == "thinking":
                # Thinking block - extract as thinking event
                thinking_text = block.get("thinking", "")
                if thinking_text:
                    events.append(
                        self._create_thinking_event(
                            content=thinking_text,
                            session_id=session_id,
                            timestamp=timestamp,
                            model=model,
                        )
                    )
                    # Also extract decisions from thinking
                    events.extend(
                        self._extract_decisions_from_text(thinking_text, session_id, timestamp)
                    )

            elif block_type == "text":
                # Text response
                text = block.get("text", "")
                if text:
                    events.append(
                        UnifiedEvent(
                            event_id=str(uuid.uuid4()),
                            session_id=session_id,
                            timestamp=timestamp,
                            event_type=EventType.RESPONSE,
                            content=text[:500],  # Truncate for display
                            model=model,
                            raw_data={"full_text": text} if len(text) > 500 else {},
                        )
                    )
                    # Extract decisions from response text
                    events.extend(self._extract_decisions_from_text(text, session_id, timestamp))

            elif block_type == "tool_use":
                # Tool call
                tool_name = block.get("name", "")
                tool_input = block.get("input", {})

                # Handle Task tool (subagent spawn) specially
                if tool_name == "Task":
                    # Create AGENT_SPAWN event instead of regular tool event
                    agent_type = tool_input.get("subagent_type", "general")
                    description = tool_input.get("description", "")
                    prompt = tool_input.get("prompt", "")
                    context_text = tool_input.get("context", "")
                    agent_model = tool_input.get("model")

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
                                "depth": 1,  # Direct subagents are depth 1
                            },
                        )
                    )
                else:
                    # Regular tool call
                    events.append(
                        self._create_tool_event(
                            name=tool_name,
                            input_data=tool_input,
                            session_id=session_id,
                            timestamp=timestamp,
                            risk_level=self._classify_risk(tool_name, tool_input).value,
                        )
                    )

                    # Track files from tool use
                    if tool_name in ("Read", "Glob", "Grep"):
                        file_path = tool_input.get("file_path") or tool_input.get("path")
                        if file_path:
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
                    elif tool_name in ("Write", "Edit"):
                        file_path = tool_input.get("file_path") or tool_input.get("path")
                        if file_path:
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

        return events

    def _parse_user_message(
        self, data: Dict, session_id: str, timestamp: datetime
    ) -> List[UnifiedEvent]:
        """Parse user message."""
        message = data.get("message", {})
        content = message.get("content", "")

        # Handle content as list or string
        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif isinstance(block, str):
                    text_parts.append(block)
            content = " ".join(text_parts)

        if content:
            return [
                UnifiedEvent(
                    event_id=str(uuid.uuid4()),
                    session_id=session_id,
                    timestamp=timestamp,
                    event_type=EventType.USER_MESSAGE,
                    content=content[:500],
                )
            ]
        return []

    def _parse_result(self, data: Dict, session_id: str, timestamp: datetime) -> List[UnifiedEvent]:
        """Parse tool result."""
        # Results are tool outputs - we track them for context but
        # typically they're associated with the preceding tool_use
        return []

    def extract_thinking(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract only thinking events from transcript.

        This is an optimized path for when only thinking is needed.
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
                        if data.get("type") == "assistant":
                            message = data.get("message", {})
                            timestamp = self._parse_timestamp(data)
                            model = message.get("model", data.get("model"))

                            for block in message.get("content", []):
                                if block.get("type") == "thinking":
                                    thinking_text = block.get("thinking", "")
                                    if thinking_text:
                                        events.append(
                                            self._create_thinking_event(
                                                content=thinking_text,
                                                session_id=session_id,
                                                timestamp=timestamp,
                                                model=model,
                                            )
                                        )
                    except json.JSONDecodeError:
                        continue
        except OSError as e:
            self._logger.error(f"Error reading transcript {file_path}: {e}")

        return events

    def extract_decisions(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract decision events from transcript.

        Looks in both thinking blocks and response text.
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
                        if data.get("type") == "assistant":
                            message = data.get("message", {})
                            timestamp = self._parse_timestamp(data)

                            for block in message.get("content", []):
                                text = ""
                                if block.get("type") == "thinking":
                                    text = block.get("thinking", "")
                                elif block.get("type") == "text":
                                    text = block.get("text", "")

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
                    if data.get("type") == "assistant":
                        for block in data.get("message", {}).get("content", []):
                            if block.get("type") == "tool_use":
                                name = block.get("name", "")
                                inp = block.get("input", {})
                                if name == "Edit":
                                    return f"Edit {inp.get('file_path', '')}"
                                elif name == "Write":
                                    return f"Write {inp.get('file_path', '')}"
                                elif name == "Bash":
                                    cmd = inp.get("command", "")[:50]
                                    return f"Bash: {cmd}"
                                elif name == "Read":
                                    return f"Read {inp.get('file_path', '')}"
                                else:
                                    return name
                except json.JSONDecodeError:
                    continue
            return ""
        except Exception as e:
            self._logger.debug(f"Error getting last action from {file_path}: {e}")
            return ""

    def has_completion_marker(self, file_path: Path) -> bool:
        """
        Check if session has a completion marker after last tool call.

        A completion marker indicates the session finished normally
        (model responded after the last tool call).
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
                    if data.get("type") == "assistant":
                        content_blocks = data.get("message", {}).get("content", [])
                        has_tool_use = any(b.get("type") == "tool_use" for b in content_blocks)
                        has_text = any(b.get("type") == "text" for b in content_blocks)

                        if has_tool_use:
                            found_tool_call = True
                            if found_response_after_tool:
                                return True
                        elif has_text and found_tool_call:
                            found_response_after_tool = True
                except json.JSONDecodeError:
                    continue

            return found_response_after_tool
        except Exception as e:
            self._logger.debug(f"Error checking completion marker in {file_path}: {e}")
            return False
