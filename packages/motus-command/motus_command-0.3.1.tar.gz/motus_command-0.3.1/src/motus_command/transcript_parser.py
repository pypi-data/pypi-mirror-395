"""
Enhanced Transcript Parser - Extracts hidden data from Claude Code transcripts.

The Claude Code transcript JSONL files contain far more data than is typically displayed:
- Token usage (input, output, cache_read, cache_create)
- Model used (claude-opus, claude-sonnet)
- File history snapshots (git-like file backups)
- Error and retry information
- Todos (Claude's task tracking)
- User prompts (the actual intent)

This module extracts all this hidden data to power the Intent Tracker,
Time Machine, and Knowledge Graph features.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .exceptions import TranscriptError
from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class TokenUsage:
    """Token usage for a single message."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_create_tokens: int = 0
    model: str = ""

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def cache_hit_rate(self) -> float:
        """Percentage of input tokens that came from cache."""
        if self.input_tokens == 0:
            return 0.0
        return (self.cache_read_tokens / self.input_tokens) * 100


@dataclass
class FileSnapshot:
    """A snapshot of a file at a point in time."""

    file_path: str
    content: str
    timestamp: datetime
    session_id: str
    hash: str = ""  # Content hash for deduplication

    def __post_init__(self):
        if not self.hash:
            # Simple hash based on content
            self.hash = str(hash(self.content))[:12]


@dataclass
class UserIntent:
    """A user's intent/request extracted from a prompt."""

    prompt: str
    timestamp: datetime
    session_id: str
    completed: bool = False
    completion_notes: str = ""


@dataclass
class ErrorEvent:
    """An error that occurred during execution."""

    message: str
    timestamp: datetime
    session_id: str
    retry_attempt: int = 0
    retry_delay_ms: int = 0
    recovered: bool = False


@dataclass
class TodoItem:
    """A todo item from Claude's task tracking."""

    content: str
    status: str  # 'pending', 'in_progress', 'completed'
    timestamp: datetime
    session_id: str


@dataclass
class TranscriptData:
    """All extracted data from a transcript."""

    session_id: str
    project_path: str
    file_path: Path

    # Token/cost tracking
    token_usage: list[TokenUsage] = field(default_factory=list)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cache_read: int = 0
    models_used: set[str] = field(default_factory=set)

    # File snapshots (Time Machine data)
    file_snapshots: list[FileSnapshot] = field(default_factory=list)
    files_snapshot_count: int = 0

    # User intents (Intent Tracker data)
    user_intents: list[UserIntent] = field(default_factory=list)

    # Errors and retries
    errors: list[ErrorEvent] = field(default_factory=list)

    # Todos
    todos: list[TodoItem] = field(default_factory=list)

    # Files read/modified (Knowledge Graph data)
    files_read: set[str] = field(default_factory=set)
    files_modified: set[str] = field(default_factory=set)

    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens

    @property
    def overall_cache_hit_rate(self) -> float:
        if self.total_input_tokens == 0:
            return 0.0
        return (self.total_cache_read / self.total_input_tokens) * 100


class TranscriptParser:
    """
    Enhanced parser for Claude Code transcript JSONL files.

    Extracts all available data including hidden fields:
    - Token usage and costs
    - File history snapshots
    - User intents/prompts
    - Errors and retries
    - Todos
    """

    def __init__(self, extract_file_snapshots: bool = True, max_snapshots: int = 1000):
        """
        Initialize parser.

        Args:
            extract_file_snapshots: Whether to extract full file content snapshots.
                                   Can use significant memory for large sessions.
            max_snapshots: Maximum number of file snapshots to keep in memory.
        """
        self.extract_file_snapshots = extract_file_snapshots
        self.max_snapshots = max_snapshots

    def parse_file(
        self, file_path: Path, session_id: str = "", project_path: str = ""
    ) -> TranscriptData:
        """
        Parse a complete transcript file.

        Args:
            file_path: Path to the JSONL transcript file
            session_id: Session ID (extracted from path if not provided)
            project_path: Project path (extracted from path if not provided)

        Returns:
            TranscriptData with all extracted information
        """
        if not session_id:
            session_id = file_path.stem

        if not project_path:
            # Extract from parent directory name
            project_path = str(file_path.parent.name)

        data = TranscriptData(
            session_id=session_id,
            project_path=project_path,
            file_path=file_path,
            models_used=set(),
            files_read=set(),
            files_modified=set(),
        )

        try:
            with open(file_path, "r") as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        event = json.loads(line)
                        self._process_event(event, data)
                    except json.JSONDecodeError as e:
                        logger.debug(f"Invalid JSON at line {line_num}: {e}")
                        continue
        except OSError as e:
            raise TranscriptError(f"Failed to read transcript: {e}")

        return data

    def _process_event(self, event: dict, data: TranscriptData) -> None:
        """Process a single transcript event."""
        event_type = event.get("type", "")
        timestamp = self._parse_timestamp(event.get("timestamp", ""))

        # Handle different event types
        if event_type == "assistant":
            self._process_assistant_event(event, data, timestamp)
        elif event_type == "user":
            self._process_user_event(event, data, timestamp)
        elif event_type == "file-history-snapshot":
            self._process_file_snapshot(event, data, timestamp)
        elif event_type == "tool_use":
            self._process_tool_use(event, data, timestamp)
        elif event_type == "error":
            self._process_error(event, data, timestamp)

    def _process_assistant_event(
        self, event: dict, data: TranscriptData, timestamp: datetime
    ) -> None:
        """Process an assistant message event."""
        message = event.get("message", {})

        # Extract token usage
        usage = message.get("usage", {})
        if usage:
            token_usage = TokenUsage(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                cache_read_tokens=usage.get("cache_read_input_tokens", 0),
                cache_create_tokens=usage.get("cache_creation_input_tokens", 0),
                model=message.get("model", ""),
            )
            data.token_usage.append(token_usage)
            data.total_input_tokens += token_usage.input_tokens
            data.total_output_tokens += token_usage.output_tokens
            data.total_cache_read += token_usage.cache_read_tokens

        # Track model used
        model = message.get("model", "")
        if model:
            data.models_used.add(model)

        # Check for errors in response
        if "error" in event:
            retry_attempt = event.get("retryAttempt", 0)
            retry_delay = event.get("retryInMs", 0)
            data.errors.append(
                ErrorEvent(
                    message=str(event.get("error", "")),
                    timestamp=timestamp,
                    session_id=data.session_id,
                    retry_attempt=retry_attempt,
                    retry_delay_ms=retry_delay,
                    recovered=retry_attempt > 0,
                )
            )

        # Process content blocks
        content = message.get("content", [])
        for block in content:
            if not isinstance(block, dict):
                continue

            block_type = block.get("type", "")

            if block_type == "text":
                text = block.get("text", "")
                self._extract_todos_from_text(text, data, timestamp)

            elif block_type == "tool_use":
                # Tool use is nested inside assistant message content
                self._process_tool_use_block(block, data, timestamp)

    def _process_user_event(self, event: dict, data: TranscriptData, timestamp: datetime) -> None:
        """Process a user message event - extract intent."""
        message = event.get("message", {})
        content = message.get("content", [])

        # Extract user prompt
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                prompt = block.get("text", "").strip()
                if prompt and len(prompt) > 5:  # Ignore very short messages
                    data.user_intents.append(
                        UserIntent(
                            prompt=prompt[:500],  # Truncate very long prompts
                            timestamp=timestamp,
                            session_id=data.session_id,
                        )
                    )
                    break

    def _process_file_snapshot(
        self, event: dict, data: TranscriptData, timestamp: datetime
    ) -> None:
        """Process a file history snapshot event."""
        data.files_snapshot_count += 1

        if not self.extract_file_snapshots:
            return

        if len(data.file_snapshots) >= self.max_snapshots:
            return  # Memory protection

        file_path = event.get("path", "")
        content = event.get("content", "")

        if file_path and content:
            data.file_snapshots.append(
                FileSnapshot(
                    file_path=file_path,
                    content=content,
                    timestamp=timestamp,
                    session_id=data.session_id,
                )
            )

    def _process_tool_use_block(
        self, block: dict, data: TranscriptData, timestamp: datetime
    ) -> None:
        """Process a tool_use block from inside assistant message content."""
        tool_name = block.get("name", "")
        tool_input = block.get("input", {})

        # Track file operations
        file_path = tool_input.get("file_path", "")
        if file_path:
            if tool_name == "Read":
                data.files_read.add(file_path)
            elif tool_name in ("Edit", "Write"):
                data.files_modified.add(file_path)

        # Track Glob/Grep for files explored
        if tool_name in ("Glob", "Grep"):
            pattern = tool_input.get("pattern", "")
            path = tool_input.get("path", "")
            if path:
                data.files_read.add(f"{path}/{pattern}")

    def _process_tool_use(self, event: dict, data: TranscriptData, timestamp: datetime) -> None:
        """Process a top-level tool use event (legacy format)."""
        tool_name = event.get("name", "")
        tool_input = event.get("input", {})

        # Track file operations
        file_path = tool_input.get("file_path", "")
        if file_path:
            if tool_name == "Read":
                data.files_read.add(file_path)
            elif tool_name in ("Edit", "Write"):
                data.files_modified.add(file_path)

    def _process_error(self, event: dict, data: TranscriptData, timestamp: datetime) -> None:
        """Process an error event."""
        data.errors.append(
            ErrorEvent(
                message=event.get("message", str(event)),
                timestamp=timestamp,
                session_id=data.session_id,
            )
        )

    def _extract_todos_from_text(
        self, text: str, data: TranscriptData, timestamp: datetime
    ) -> None:
        """Extract todo items from assistant text."""
        # Look for common todo patterns
        lines = text.split("\n")
        for line in lines:
            line_stripped = line.strip()
            # Common todo patterns
            if line_stripped.startswith(("- [ ]", "- [x]", "* [ ]", "* [x]")):
                is_completed = "[x]" in line_stripped.lower()
                content = line_stripped.replace("- [ ]", "").replace("- [x]", "")
                content = content.replace("* [ ]", "").replace("* [x]", "").strip()
                if content:
                    data.todos.append(
                        TodoItem(
                            content=content[:200],
                            status="completed" if is_completed else "pending",
                            timestamp=timestamp,
                            session_id=data.session_id,
                        )
                    )

    def _parse_timestamp(self, ts_str: str) -> datetime:
        """Parse ISO timestamp string to datetime."""
        if not ts_str:
            return datetime.now()
        try:
            # Handle various ISO formats
            ts_str = ts_str.replace("Z", "+00:00")
            if "." in ts_str:
                # Truncate microseconds if too long
                parts = ts_str.split(".")
                if len(parts) == 2:
                    decimal_part = parts[1]
                    # Handle timezone in decimal part
                    if "+" in decimal_part:
                        micro, tz = decimal_part.split("+")
                        decimal_part = micro[:6] + "+" + tz
                    elif "-" in decimal_part and decimal_part.count("-") == 1:
                        micro, tz = decimal_part.split("-")
                        decimal_part = micro[:6] + "-" + tz
                    else:
                        decimal_part = decimal_part[:6]
                    ts_str = parts[0] + "." + decimal_part
            return datetime.fromisoformat(ts_str)
        except (ValueError, TypeError):
            return datetime.now()


def get_transcript_summary(file_path: Path) -> dict:
    """
    Quick summary of a transcript without full parsing.

    Returns basic stats without extracting full content.
    """
    parser = TranscriptParser(extract_file_snapshots=False)
    data = parser.parse_file(file_path)

    return {
        "session_id": data.session_id,
        "total_tokens": data.total_tokens,
        "total_input_tokens": data.total_input_tokens,
        "total_output_tokens": data.total_output_tokens,
        "cache_hit_rate": f"{data.overall_cache_hit_rate:.1f}%",
        "models_used": list(data.models_used),
        "file_snapshots": data.files_snapshot_count,
        "user_intents": len(data.user_intents),
        "errors": len(data.errors),
        "files_read": len(data.files_read),
        "files_modified": len(data.files_modified),
    }
