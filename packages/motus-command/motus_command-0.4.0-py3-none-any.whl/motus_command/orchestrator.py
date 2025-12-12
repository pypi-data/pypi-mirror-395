"""
Session Orchestrator - Unified session management across all sources.

This is the single entry point for all session discovery, parsing, and management.
All surfaces (CLI, TUI, Web) should use this orchestrator instead of source-specific code.
"""

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from .builders import BaseBuilder, ClaudeBuilder, CodexBuilder, GeminiBuilder
from .logging import get_logger
from .process_detector import ProcessDetector
from .protocols import (
    EventType,
    SessionHealth,
    SessionStatus,
    Source,
    TeleportBundle,
    UnifiedEvent,
    UnifiedSession,
    compute_health,
)

logger = get_logger(__name__)


class SessionOrchestrator:
    """
    Centralized orchestrator for all AI agent session management.

    Provides:
    - Unified session discovery across Claude, Codex, Gemini
    - Consistent event parsing through builders
    - Session health computation
    - Context aggregation
    - Teleport bundle export
    """

    def __init__(self):
        """Initialize orchestrator with all source builders."""
        self._builders: Dict[Source, BaseBuilder] = {
            Source.CLAUDE: ClaudeBuilder(),
            Source.CODEX: CodexBuilder(),
            Source.GEMINI: GeminiBuilder(),
        }
        self._session_cache: Dict[str, UnifiedSession] = {}
        self._event_cache: Dict[str, List[UnifiedEvent]] = {}
        self._process_detector = ProcessDetector()
        self._logger = get_logger(__name__)

    def discover_all(
        self, max_age_hours: int = 24, sources: Optional[List[Source]] = None
    ) -> List[UnifiedSession]:
        """
        Discover all sessions from specified sources.

        Args:
            max_age_hours: Maximum age of sessions to include.
            sources: List of sources to search. Defaults to all.

        Returns:
            List of UnifiedSession objects, sorted by status then recency.
        """
        if sources is None:
            sources = list(self._builders.keys())

        sessions: List[UnifiedSession] = []
        now = datetime.now()

        # Get running projects from ProcessDetector once for all sessions
        running_projects = self._process_detector.get_running_projects()

        for source in sources:
            builder = self._builders.get(source)
            if not builder:
                continue

            try:
                raw_sessions = builder.discover(max_age_hours)
                for raw in raw_sessions:
                    # Compute status using builder's uniform logic with process detection
                    last_action = builder.get_last_action(raw.file_path)
                    has_completion = builder.has_completion_marker(raw.file_path)
                    status, status_reason = builder.compute_status(
                        raw.last_modified,
                        now,
                        last_action,
                        has_completion,
                        raw.project_path,
                        running_projects,
                    )

                    session = UnifiedSession(
                        session_id=raw.session_id,
                        source=source,
                        file_path=raw.file_path,
                        project_path=raw.project_path,
                        status=status,
                        status_reason=status_reason,
                        created_at=raw.created_at or raw.last_modified,
                        last_modified=raw.last_modified,
                    )

                    sessions.append(session)
                    self._session_cache[raw.session_id] = session

            except Exception as e:
                self._logger.error(f"Error discovering {source.value} sessions: {e}")
                continue

        # Sort: active first, then open, then crashed, then by recency
        def sort_key(s: UnifiedSession):
            status_order = {
                SessionStatus.ACTIVE: 0,
                SessionStatus.OPEN: 1,
                SessionStatus.CRASHED: 2,
                SessionStatus.IDLE: 3,
                SessionStatus.ORPHANED: 4,
            }
            return (status_order.get(s.status, 5), -s.last_modified.timestamp())

        sessions.sort(key=sort_key)
        self._logger.debug(f"Discovered {len(sessions)} total sessions")
        return sessions

    def get_session(self, session_id: str) -> Optional[UnifiedSession]:
        """
        Get a session by ID from cache or discover.

        Args:
            session_id: The session ID to look up.

        Returns:
            UnifiedSession if found, None otherwise.
        """
        if session_id in self._session_cache:
            return self._session_cache[session_id]

        # Try to find it by discovering recent sessions
        sessions = self.discover_all(max_age_hours=168)  # Last week
        for session in sessions:
            if session.session_id == session_id:
                return session

        return None

    def get_events(self, session: UnifiedSession, refresh: bool = False) -> List[UnifiedEvent]:
        """
        Get all events for a session.

        Args:
            session: The session to get events for.
            refresh: If True, bypass cache and re-parse.

        Returns:
            List of UnifiedEvent objects in chronological order.
        """
        cache_key = session.session_id

        if not refresh and cache_key in self._event_cache:
            return self._event_cache[cache_key]

        builder = self._builders.get(session.source)
        if not builder:
            return []

        try:
            events = builder.parse_events(session.file_path)
            self._event_cache[cache_key] = events
            return events
        except Exception as e:
            self._logger.error(f"Error parsing events for {session.session_id}: {e}")
            return []

    def get_health(self, session: UnifiedSession) -> SessionHealth:
        """
        Compute health metrics for a session.

        Args:
            session: The session to analyze.

        Returns:
            SessionHealth object with computed metrics.
        """
        events = self.get_events(session)
        return compute_health(session, events)

    def get_context(self, session: UnifiedSession) -> Dict:
        """
        Get aggregated context for a session.

        Returns:
            Dict containing:
            - files_read: List of files read
            - files_modified: List of files modified
            - decisions: List of decisions made
            - tool_counts: Counter of tool usage
            - thinking_summaries: Recent thinking content
        """
        events = self.get_events(session)

        files_read: Set[str] = set()
        files_modified: Set[str] = set()
        decisions: List[str] = []
        tool_counts: Counter = Counter()
        thinking: List[str] = []

        for event in events:
            if event.event_type == EventType.FILE_READ and event.file_path:
                files_read.add(Path(event.file_path).name)
            elif event.event_type == EventType.FILE_MODIFIED and event.file_path:
                files_modified.add(Path(event.file_path).name)
            elif event.event_type == EventType.DECISION and event.decision_text:
                decisions.append(event.decision_text)
            elif event.event_type == EventType.TOOL and event.tool_name:
                tool_counts[event.tool_name] += 1
            elif event.event_type == EventType.THINKING:
                thinking.append(event.content[:200])

        return {
            "files_read": sorted(files_read),
            "files_modified": sorted(files_modified),
            "decisions": decisions[-10:],  # Last 10 decisions
            "tool_counts": dict(tool_counts.most_common(10)),
            "thinking_summaries": thinking[-5:],  # Last 5 thinking blocks
        }

    def _detect_planning_docs(self, project_path: str) -> Dict[str, str]:
        """
        Detect and load planning documents from project.

        Args:
            project_path: Path to the project directory.

        Returns:
            Dictionary mapping document names to their content.
        """
        planning_docs = {}
        project_dir = Path(project_path)

        if not project_dir.exists():
            return planning_docs

        # Define planning doc patterns to search for
        doc_patterns = [
            "ROADMAP.md",
            "ROADMAP-*.md",
            "ARCHITECTURE.md",
            "DESIGN.md",
            "CONTRIBUTING.md",
        ]

        # Search for matching docs
        for pattern in doc_patterns:
            if "*" in pattern:
                # Glob pattern
                for doc_file in project_dir.glob(pattern):
                    if doc_file.is_file():
                        try:
                            content = doc_file.read_text(encoding="utf-8", errors="ignore")
                            # Get first 500 chars or first section
                            preview = self._extract_doc_summary(content)
                            planning_docs[doc_file.name] = preview
                        except Exception as e:
                            logger.debug(f"Failed to read {doc_file}: {e}")
            else:
                # Exact match
                doc_file = project_dir / pattern
                if doc_file.is_file():
                    try:
                        content = doc_file.read_text(encoding="utf-8", errors="ignore")
                        preview = self._extract_doc_summary(content)
                        planning_docs[doc_file.name] = preview
                    except Exception as e:
                        logger.debug(f"Failed to read {doc_file}: {e}")

        # Check for .claude/commands/*.md (custom slash commands)
        claude_commands_dir = project_dir / ".claude" / "commands"
        if claude_commands_dir.exists():
            command_files = list(claude_commands_dir.glob("*.md"))
            if command_files:
                # Combine all command files into one summary
                command_summary = "**Custom Slash Commands:**\n\n"
                for cmd_file in command_files[:5]:  # Limit to 5 commands
                    try:
                        content = cmd_file.read_text(encoding="utf-8", errors="ignore")
                        # Extract just the first line or first 100 chars
                        first_line = content.split("\n")[0] if "\n" in content else content[:100]
                        command_summary += f"- `/{cmd_file.stem}`: {first_line[:100]}\n"
                    except Exception as e:
                        logger.debug(f"Failed to read {cmd_file}: {e}")
                if len(command_summary) > 50:  # Only add if we got content
                    planning_docs[".claude/commands"] = command_summary

        # Check for .mc/intent.yaml
        intent_file = project_dir / ".mc" / "intent.yaml"
        if intent_file.is_file():
            try:
                content = intent_file.read_text(encoding="utf-8", errors="ignore")
                planning_docs["intent.yaml"] = content[:500]
            except Exception as e:
                logger.debug(f"Failed to read {intent_file}: {e}")

        return planning_docs

    def _extract_doc_summary(self, content: str, max_chars: int = 500) -> str:
        """
        Extract a summary from document content.

        Takes the first 500 chars or up to the first major section break.

        Args:
            content: Full document content.
            max_chars: Maximum characters to include.

        Returns:
            Document summary.
        """
        lines = content.split("\n")
        summary_lines = []
        char_count = 0

        for i, line in enumerate(lines):
            # Stop at second major heading (##) or max chars
            if i > 0 and line.startswith("## "):
                break

            summary_lines.append(line)
            char_count += len(line) + 1  # +1 for newline

            if char_count >= max_chars:
                summary_lines.append("...")
                break

        return "\n".join(summary_lines).strip()

    def export_teleport(
        self, session: UnifiedSession, include_planning_docs: bool = True
    ) -> TeleportBundle:
        """
        Export a TeleportBundle for cross-session context transfer.

        Args:
            session: The session to export.
            include_planning_docs: Whether to include planning documents (default: True).

        Returns:
            TeleportBundle for injection into another session.
        """
        events = self.get_events(session)
        context = self.get_context(session)

        # Find intent from thinking blocks
        intent = ""
        for event in events:
            if event.event_type == EventType.THINKING:
                # Look for intent patterns
                content = event.content.lower()
                if any(marker in content for marker in ["i'll ", "i will ", "goal:", "task:"]):
                    intent = event.content[:300]
                    break

        # Get last action from builder
        builder = self._builders.get(session.source)
        last_action = ""
        if builder:
            last_action = builder.get_last_action(session.file_path)

        # Hot files are recently modified
        hot_files = context["files_modified"][-5:]  # Last 5 modified

        # Detect planning docs if enabled
        planning_docs = {}
        if include_planning_docs:
            planning_docs = self._detect_planning_docs(session.project_path)

        return TeleportBundle(
            source_session=session.session_id,
            source_model=session.source.value,
            intent=intent,
            decisions=context["decisions"],
            files_touched=context["files_read"] + context["files_modified"],
            hot_files=hot_files,
            pending_todos=[],  # Not tracking todos yet
            last_action=last_action,
            timestamp=datetime.now(),
            planning_docs=planning_docs,
        )

    def get_active_sessions(self) -> List[UnifiedSession]:
        """
        Get only active sessions (currently generating).

        Returns:
            List of active sessions.
        """
        sessions = self.discover_all(max_age_hours=1)
        return [s for s in sessions if s.status == SessionStatus.ACTIVE]

    def get_recent_sessions(
        self, max_count: int = 10, sources: Optional[List[Source]] = None
    ) -> List[UnifiedSession]:
        """
        Get most recent sessions.

        Args:
            max_count: Maximum number of sessions to return.
            sources: Optional list of sources to filter by.

        Returns:
            List of recent sessions, sorted by recency.
        """
        sessions = self.discover_all(max_age_hours=168, sources=sources)
        return sessions[:max_count]

    def refresh_cache(self, session_id: Optional[str] = None):
        """
        Clear caches to force fresh data.

        Args:
            session_id: If provided, only clear that session's cache.
                       If None, clear all caches.
        """
        if session_id:
            self._session_cache.pop(session_id, None)
            self._event_cache.pop(session_id, None)
        else:
            self._session_cache.clear()
            self._event_cache.clear()

    def get_builder(self, source: Source) -> Optional[BaseBuilder]:
        """
        Get the builder for a specific source.

        Useful for source-specific operations.
        """
        return self._builders.get(source)

    def get_running_projects(self) -> Set[str]:
        """
        Get set of project directories with running agent processes.

        Delegates to ProcessDetector with caching and fail-silent behavior.

        Returns:
            Set of project directory names with running agent processes.
        """
        return self._process_detector.get_running_projects()

    def is_process_degraded(self) -> bool:
        """
        Check if process detection is running in degraded mode.

        Returns:
            True if process detection has been disabled due to errors.
        """
        return self._process_detector.is_degraded()

    def is_project_active(self, project_path: str) -> bool:
        """
        Check if a specific project has a running agent process.

        Args:
            project_path: The project path to check.

        Returns:
            True if the project has a running agent process.
        """
        return self._process_detector.is_project_active(project_path)


# Global orchestrator instance
_orchestrator: Optional[SessionOrchestrator] = None


def get_orchestrator() -> SessionOrchestrator:
    """
    Get the global SessionOrchestrator instance.

    This is the recommended way to access the orchestrator
    throughout the application.
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = SessionOrchestrator()
    return _orchestrator
