"""
MC Session Manager.

Centralized session discovery, tracking, and management.
Used by CLI, TUI, and Web components.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set

from .commands.utils import extract_project_path
from .config import config
from .logging import get_logger
from .process_detector import ProcessDetector

logger = get_logger(__name__)


@dataclass
class SessionInfo:
    """Information about an AI agent session (Claude Code, Codex, etc.)."""

    session_id: str
    file_path: Path  # Alias for transcript_path for backwards compat
    last_modified: datetime
    size: int
    is_active: bool = False
    project_path: str = ""
    status: str = "orphaned"  # active, open, crashed, orphaned
    last_action: str = ""
    source: str = "claude"  # "claude", "codex", "sdk"

    @property
    def transcript_path(self) -> Path:
        """Alias for file_path for clarity."""
        return self.file_path


@dataclass
class SessionContext:
    """
    Accumulated context/memory for a session.
    Tracks what the agent "knows" - files read, decisions made, etc.
    """

    session_id: str
    files_read: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    agent_tree: List[Dict] = field(default_factory=list)
    tool_count: Dict[str, int] = field(default_factory=dict)

    def add_file_read(self, file_path: str) -> None:
        """Track a file read, storing just the filename."""
        filename = Path(file_path).name
        if filename not in self.files_read:
            self.files_read.append(filename)

    def add_file_modified(self, file_path: str) -> None:
        """Track a file modification."""
        filename = Path(file_path).name
        if filename not in self.files_modified:
            self.files_modified.append(filename)

    def add_decision(self, decision: str) -> None:
        """Track a decision made by the agent."""
        # Keep only last 10 decisions
        self.decisions.append(decision)
        if len(self.decisions) > 10:
            self.decisions = self.decisions[-10:]

    def add_agent_spawn(
        self, agent_type: str, description: str, prompt: str, model: Optional[str] = None
    ) -> None:
        """Track a sub-agent spawn."""
        self.agent_tree.append(
            {
                "type": agent_type,
                "description": description,
                "prompt": prompt,
                "model": model,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_tool_use(self, tool_name: str) -> None:
        """Track tool usage."""
        self.tool_count[tool_name] = self.tool_count.get(tool_name, 0) + 1

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "files_read": self.files_read,
            "files_modified": self.files_modified,
            "decisions": self.decisions,
            "agent_tree": self.agent_tree,
            "tool_count": self.tool_count,
        }


class SessionManager:
    """
    Centralized session management.

    Handles session discovery, process detection, and context tracking.
    """

    def __init__(self):
        self._process_detector = ProcessDetector()
        self._contexts: Dict[str, SessionContext] = {}
        # Keep these for backwards compatibility but they're now unused
        self._running_projects: Optional[Set[str]] = None
        self._running_projects_timestamp: Optional[datetime] = None

    def get_running_projects(self, force_refresh: bool = False) -> Set[str]:
        """
        Get project directories where Claude processes are currently running.

        Uses ProcessDetector with caching and fail-silent behavior.

        Args:
            force_refresh: If True, invalidate the cache and refresh.

        Returns:
            Set of project directory names with running Claude processes.
        """
        if force_refresh:
            self._process_detector.reset()
        return self._process_detector.get_running_projects()

    def is_process_detection_degraded(self) -> bool:
        """
        Check if process detection is running in degraded mode.

        Returns:
            True if process detection has been disabled due to permission errors or other issues.
        """
        return self._process_detector.is_degraded()

    def find_sessions(self, max_age_hours: Optional[int] = None) -> List[SessionInfo]:
        """
        Find recent AI agent session files from all sources.

        Gathers sessions from Claude, Codex, and Gemini independently.
        Each source is checked regardless of whether others exist.

        Session states:
        - active: Agent is actively generating (modified < 60s)
        - open: Agent process is running but idle (modified > 60s, process running)
        - orphaned: Agent process has ended (modified > 60s, no process)
        - crashed: Was doing risky action when stopped (modified 1-5 min, risky last action)

        Args:
            max_age_hours: Maximum age of sessions to return. Defaults to config value.

        Returns:
            List of SessionInfo objects, sorted by status then recency.
        """
        if max_age_hours is None:
            max_age_hours = config.sessions.max_age_hours

        sessions: List[SessionInfo] = []

        # Gather all sources independently - don't gate on any single source
        sessions.extend(self._find_claude_sessions(max_age_hours))
        sessions.extend(self._find_codex_sessions(max_age_hours))
        sessions.extend(self._find_gemini_sessions(max_age_hours))

        # Sort: active first, then open, then by recency
        def sort_key(s: SessionInfo):
            status_order = {"active": 0, "open": 1, "crashed": 2, "orphaned": 3}
            return (status_order.get(s.status, 4), -s.last_modified.timestamp())

        sessions.sort(key=sort_key)
        logger.debug(f"Found {len(sessions)} total sessions across all sources")
        return sessions

    def _find_claude_sessions(self, max_age_hours: int) -> List[SessionInfo]:
        """Find Claude Code sessions from ~/.claude/projects/."""
        sessions: List[SessionInfo] = []
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        now = datetime.now()

        if not config.paths.projects_dir.exists():
            logger.debug("Claude projects directory does not exist")
            return sessions

        # Get projects with running Claude processes
        active_project_dirs = self.get_running_projects()

        for project_dir in config.paths.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue

            project_path = extract_project_path(project_dir.name)
            has_running_process = project_dir.name in active_project_dirs

            for jsonl_file in project_dir.glob("*.jsonl"):
                if jsonl_file.name.startswith("agent-"):
                    continue

                try:
                    stat = jsonl_file.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime)

                    if modified > cutoff:
                        age_seconds = (now - modified).total_seconds()

                        # Determine status based on recency AND process state
                        if age_seconds < config.sessions.active_threshold_seconds:
                            status = "active"
                            is_active = True
                        elif has_running_process:
                            status = "open"
                            is_active = False
                        elif age_seconds < config.sessions.idle_threshold_seconds:
                            # Check if it was doing something risky when it stopped
                            last_action = self._get_last_action(jsonl_file)
                            if last_action and any(
                                keyword in last_action for keyword in ("Edit", "Write", "Bash")
                            ):
                                # Only mark as crashed if no completion marker found
                                # (completion marker = response after tool call)
                                if not self._has_completion_marker(jsonl_file, source="claude"):
                                    status = "crashed"
                                else:
                                    status = "orphaned"
                            else:
                                status = "orphaned"
                            is_active = False
                        else:
                            status = "orphaned"
                            is_active = False

                        sessions.append(
                            SessionInfo(
                                session_id=jsonl_file.stem,
                                file_path=jsonl_file,
                                last_modified=modified,
                                size=stat.st_size,
                                is_active=is_active,
                                project_path=project_path,
                                status=status,
                                last_action=(
                                    self._get_last_action(jsonl_file) if status == "crashed" else ""
                                ),
                                source="claude",
                            )
                        )
                except OSError as e:
                    logger.debug(f"Error reading session file {jsonl_file}: {e}")
                    continue

        logger.debug(f"Found {len(sessions)} Claude sessions")
        return sessions

    def get_context(self, session_id: str) -> SessionContext:
        """Get or create context for a session."""
        if session_id not in self._contexts:
            self._contexts[session_id] = SessionContext(session_id=session_id)
        return self._contexts[session_id]

    def _find_gemini_sessions(self, max_age_hours: int) -> List[SessionInfo]:
        """Find Google Gemini CLI sessions from ~/.gemini/tmp/*/chats/."""
        sessions: List[SessionInfo] = []
        gemini_tmp = Path.home() / ".gemini" / "tmp"
        now = datetime.now()

        if not gemini_tmp.exists():
            return sessions

        cutoff = now - timedelta(hours=max_age_hours)

        # Get projects with running Gemini processes
        active_project_dirs = self.get_running_projects()

        try:
            # Walk through project hash directories
            for project_dir in gemini_tmp.iterdir():
                if not project_dir.is_dir():
                    continue

                chats_dir = project_dir / "chats"
                if not chats_dir.exists():
                    continue

                # Check if this project hash has a running process
                project_hash = project_dir.name
                has_running_process = f"gemini:{project_hash}" in active_project_dirs

                for json_file in chats_dir.glob("session-*.json"):
                    try:
                        stat = json_file.stat()
                        modified = datetime.fromtimestamp(stat.st_mtime)

                        if modified < cutoff:
                            continue

                        # Parse session metadata
                        with open(json_file, "r") as f:
                            data = json.load(f)

                        session_id = data.get("sessionId", json_file.stem)
                        project_hash = data.get("projectHash", project_dir.name)

                        # Gemini doesn't store project path, use hash
                        project_path = f"gemini:{project_hash[:8]}"

                        # Determine status based on recency AND process state
                        age_seconds = (now - modified).total_seconds()

                        if age_seconds < config.sessions.active_threshold_seconds:
                            status = "active"
                            is_active = True
                        elif has_running_process:
                            status = "open"
                            is_active = False
                        elif age_seconds < config.sessions.idle_threshold_seconds:
                            # Check if it was doing something risky when stopped
                            last_action = self._get_last_action(json_file, source="gemini")
                            if last_action and any(
                                keyword in last_action for keyword in ("Edit", "Write", "Bash")
                            ):
                                # Only mark as crashed if no completion marker found
                                # (completion marker = response after tool call)
                                if not self._has_completion_marker(json_file, source="gemini"):
                                    status = "crashed"
                                else:
                                    status = "orphaned"
                            else:
                                status = "orphaned"
                            is_active = False
                        else:
                            status = "orphaned"
                            is_active = False

                        sessions.append(
                            SessionInfo(
                                session_id=session_id,
                                file_path=json_file,
                                last_modified=modified,
                                size=stat.st_size,
                                is_active=is_active,
                                project_path=project_path,
                                status=status,
                                last_action=(
                                    self._get_last_action(json_file, source="gemini")
                                    if status == "crashed"
                                    else ""
                                ),
                                source="gemini",
                            )
                        )
                    except (OSError, json.JSONDecodeError) as e:
                        logger.debug(f"Error reading Gemini session {json_file}: {e}")
                        continue
        except Exception as e:
            logger.debug(f"Error scanning Gemini sessions: {e}")

        logger.debug(f"Found {len(sessions)} Gemini sessions")
        return sessions

    def _has_completion_marker(self, file_path: Path, source: str = "claude") -> bool:
        """Check if session has a completion marker after last tool call.

        A completion marker indicates the session finished normally (model responded
        after the last tool call). This helps distinguish crashed vs completed sessions.

        Args:
            file_path: Path to the session transcript file.
            source: Session source ("claude", "codex", or "gemini").

        Returns:
            True if session has evidence of successful completion, False otherwise.
        """
        try:
            if source == "gemini":
                return self._has_completion_marker_gemini(file_path)

            # Claude and Codex use JSONL - read last 10KB
            file_size = file_path.stat().st_size
            read_size = min(10000, file_size)

            with open(file_path, "rb") as f:
                f.seek(max(0, file_size - read_size))
                content = f.read().decode("utf-8", errors="ignore")

            # Track if we've seen a response after the last tool call
            found_tool_call = False
            found_response_after_tool = False

            for line in reversed(content.strip().split("\n")):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)

                    if source == "codex":
                        # For Codex, check for response_item after function_call
                        if data.get("type") == "response_item":
                            payload = data.get("payload", {})
                            if payload.get("type") == "function_call":
                                found_tool_call = True
                                if found_response_after_tool:
                                    return True
                            elif found_tool_call:
                                # Any non-function-call response after tool = completion
                                found_response_after_tool = True
                    else:  # claude
                        # For Claude, check for assistant message after tool_use
                        if data.get("type") == "assistant":
                            content_blocks = data.get("message", {}).get("content", [])
                            has_tool_use = any(b.get("type") == "tool_use" for b in content_blocks)
                            has_text = any(b.get("type") == "text" for b in content_blocks)

                            if has_tool_use:
                                found_tool_call = True
                                if found_response_after_tool:
                                    return True
                            elif has_text and found_tool_call:
                                # Text response after tool_use = completion
                                found_response_after_tool = True

                except json.JSONDecodeError:
                    continue

            # If we found a response after a tool call, it completed successfully
            return found_response_after_tool

        except Exception as e:
            logger.debug(f"Error checking completion marker in {file_path}: {e}")
            return False

    def _has_completion_marker_gemini(self, file_path: Path) -> bool:
        """Check if Gemini session has a completion marker after last tool call."""
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            messages = data.get("messages", [])
            if not messages:
                return False

            # Track if we've seen a response after the last tool call
            found_tool_call = False
            found_response_after_tool = False

            for msg in reversed(messages):
                if msg.get("type") == "gemini":
                    tool_calls = msg.get("toolCalls", [])
                    text_content = msg.get("text", "")

                    if tool_calls:
                        found_tool_call = True
                        if found_response_after_tool:
                            return True
                    elif text_content and found_tool_call:
                        # Text response after tool call = completion
                        found_response_after_tool = True

            return found_response_after_tool

        except Exception as e:
            logger.debug(f"Error checking Gemini completion marker in {file_path}: {e}")
            return False

    def _get_last_action(self, file_path: Path, source: str = "claude") -> str:
        """Get the last action from a session file for crash detection.

        Supports all sources: Claude, Codex, and Gemini.

        Args:
            file_path: Path to the session transcript file.
            source: Session source ("claude", "codex", or "gemini").

        Returns:
            Human-readable description of last tool action, or empty string.
        """
        try:
            if source == "gemini":
                return self._get_last_action_gemini(file_path)

            # Claude and Codex use JSONL - read last 10KB
            file_size = file_path.stat().st_size
            read_size = min(10000, file_size)

            with open(file_path, "rb") as f:
                f.seek(max(0, file_size - read_size))
                content = f.read().decode("utf-8", errors="ignore")

            last_action = ""
            for line in reversed(content.strip().split("\n")):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)

                    if source == "codex":
                        last_action = self._parse_codex_action(data)
                    else:  # claude
                        last_action = self._parse_claude_action(data)

                    if last_action:
                        return last_action
                except json.JSONDecodeError:
                    continue
            return last_action
        except Exception as e:
            logger.debug(f"Error getting last action from {file_path}: {e}")
            return ""

    def _parse_claude_action(self, data: dict) -> str:
        """Parse Claude transcript line for last action."""
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
        return ""

    def _parse_codex_action(self, data: dict) -> str:
        """Parse Codex transcript line for last action."""
        if data.get("type") == "response_item":
            payload = data.get("payload", {})
            if payload.get("type") == "function_call":
                tool_name = payload.get("name", "")
                arguments = payload.get("arguments", {})

                # Parse arguments if string
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except (json.JSONDecodeError, TypeError):
                        arguments = {}

                # Map tool names to unified names
                tool_map = {
                    "shell_command": "Bash",
                    "write_file": "Write",
                    "edit_file": "Edit",
                    "create_file": "Write",
                    "read_file": "Read",
                }
                unified_name = tool_map.get(tool_name, tool_name)

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
        return ""

    def _get_last_action_gemini(self, file_path: Path) -> str:
        """Get last action from Gemini JSON session file."""
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

                        # Map tool names
                        tool_map = {
                            "shell": "Bash",
                            "run_shell_command": "Bash",
                            "write_file": "Write",
                            "edit_file": "Edit",
                            "read_file": "Read",
                        }
                        unified_name = tool_map.get(func_name, func_name)

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
            logger.debug(f"Error getting last action from Gemini file {file_path}: {e}")
            return ""

    def _find_codex_sessions(self, max_age_hours: int) -> List[SessionInfo]:
        """Find OpenAI Codex CLI sessions from ~/.codex/sessions/."""
        sessions: List[SessionInfo] = []
        codex_dir = Path.home() / ".codex" / "sessions"
        now = datetime.now()

        if not codex_dir.exists():
            return sessions

        cutoff = now - timedelta(hours=max_age_hours)

        # Get projects with running Codex processes
        active_project_dirs = self.get_running_projects()

        try:
            for jsonl_file in codex_dir.rglob("*.jsonl"):
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

                        # Check if this session's project has a running process
                        has_running_process = cwd in active_project_dirs or any(
                            cwd in p for p in active_project_dirs
                        )

                        # Determine status based on recency AND process state
                        age_seconds = (now - modified).total_seconds()

                        if age_seconds < config.sessions.active_threshold_seconds:
                            status = "active"
                            is_active = True
                        elif has_running_process:
                            status = "open"
                            is_active = False
                        elif age_seconds < config.sessions.idle_threshold_seconds:
                            # Check if it was doing something risky when stopped
                            last_action = self._get_last_action(jsonl_file, source="codex")
                            if last_action and any(
                                keyword in last_action for keyword in ("Edit", "Write", "Bash")
                            ):
                                # Only mark as crashed if no completion marker found
                                # (completion marker = response after tool call)
                                if not self._has_completion_marker(jsonl_file, source="codex"):
                                    status = "crashed"
                                else:
                                    status = "orphaned"
                            else:
                                status = "orphaned"
                            is_active = False
                        else:
                            status = "orphaned"
                            is_active = False

                        sessions.append(
                            SessionInfo(
                                session_id=session_id,
                                file_path=jsonl_file,
                                last_modified=modified,
                                size=stat.st_size,
                                is_active=is_active,
                                project_path=cwd,
                                status=status,
                                last_action=(
                                    self._get_last_action(jsonl_file, source="codex")
                                    if status == "crashed"
                                    else ""
                                ),
                                source="codex",
                            )
                        )
                except (OSError, json.JSONDecodeError) as e:
                    logger.debug(f"Error reading Codex session {jsonl_file}: {e}")
                    continue
        except Exception as e:
            logger.debug(f"Error scanning Codex sessions: {e}")

        logger.debug(f"Found {len(sessions)} Codex sessions")
        return sessions


# Global session manager instance
session_manager = SessionManager()


# Convenience function for backward compatibility
def find_claude_sessions(max_age_hours: int = 24) -> List[SessionInfo]:
    """Find recent Claude Code session files."""
    return session_manager.find_sessions(max_age_hours)
