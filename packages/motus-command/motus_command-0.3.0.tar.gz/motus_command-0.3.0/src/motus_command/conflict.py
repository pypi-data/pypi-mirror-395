"""
Conflict Radar for Motus Command v0.3.

Detects when multiple AI agent sessions are editing the same files.
Warns users about potential merge conflicts and coordination issues.

Features:
- Track file touches per session with timestamps
- Warn on overlap within configurable window (default: 5 min)
- CLI: `mc conflicts` to list potential conflicts
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

from .logging import get_logger
from .session_manager import SessionInfo, session_manager
from .transcript_parser import TranscriptParser

logger = get_logger(__name__)


@dataclass
class FileTouch:
    """A record of a file being touched by a session."""

    file_path: str
    session_id: str
    session_source: str  # claude, codex, gemini
    project_path: str
    timestamp: datetime
    action: str = "modified"  # read, modified


@dataclass
class Conflict:
    """A potential conflict between sessions touching the same file."""

    file_path: str
    sessions: list[dict] = field(default_factory=list)  # [{session_id, source, timestamp, project}]
    severity: str = "warning"  # info, warning, critical

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "file_path": self.file_path,
            "sessions": self.sessions,
            "severity": self.severity,
        }


@dataclass
class ConflictReport:
    """Summary of all detected conflicts."""

    conflicts: list[Conflict] = field(default_factory=list)
    sessions_analyzed: int = 0
    files_touched: int = 0
    window_minutes: int = 5
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "conflicts": [c.to_dict() for c in self.conflicts],
            "sessions_analyzed": self.sessions_analyzed,
            "files_touched": self.files_touched,
            "window_minutes": self.window_minutes,
            "timestamp": self.timestamp,
        }


def get_file_touches_from_session(
    session_info: SessionInfo,
    extract_timestamps: bool = False,
) -> list[FileTouch]:
    """Extract file touches from a session transcript.

    Args:
        session_info: Session to analyze
        extract_timestamps: If True, try to extract per-file timestamps

    Returns:
        List of FileTouch records
    """
    touches = []
    parser = TranscriptParser(extract_file_snapshots=False)

    try:
        data = parser.parse_file(session_info.file_path)

        # Use session's last_modified as the timestamp for all touches
        # (transcript parsing doesn't easily give per-file timestamps)
        session_ts = session_info.last_modified

        for file_path in data.files_modified:
            touches.append(
                FileTouch(
                    file_path=file_path,
                    session_id=session_info.session_id,
                    session_source=session_info.source,
                    project_path=session_info.project_path,
                    timestamp=session_ts,
                    action="modified",
                )
            )

    except Exception as e:
        logger.debug(f"Error parsing session {session_info.session_id}: {e}")

    return touches


def find_conflicts(
    sessions: Optional[list[SessionInfo]] = None,
    window_minutes: int = 5,
    include_read: bool = False,
) -> ConflictReport:
    """Find file conflicts across active sessions.

    Args:
        sessions: Sessions to analyze (defaults to all recent sessions)
        window_minutes: Time window for considering overlapping touches
        include_read: If True, include read-only touches in conflict detection

    Returns:
        ConflictReport with all detected conflicts
    """
    if sessions is None:
        # Get recent active/open sessions
        all_sessions = session_manager.find_sessions(max_age_hours=24)
        # Focus on active and open sessions (not orphaned)
        sessions = [s for s in all_sessions if s.status in ("active", "open", "crashed")]

    # Build file -> touches map
    file_touches: dict[str, list[FileTouch]] = {}
    total_files = 0

    for session in sessions:
        touches = get_file_touches_from_session(session)
        for touch in touches:
            if touch.file_path not in file_touches:
                file_touches[touch.file_path] = []
            file_touches[touch.file_path].append(touch)
            total_files += 1

    # Find conflicts (files touched by multiple sessions within window)
    conflicts = []
    window = timedelta(minutes=window_minutes)

    for file_path, touches in file_touches.items():
        if len(touches) < 2:
            continue

        # Group by session to avoid self-conflicts
        by_session = {}
        for touch in touches:
            if touch.session_id not in by_session:
                by_session[touch.session_id] = touch

        if len(by_session) < 2:
            continue

        # Check if touches are within the window
        touch_list = list(by_session.values())
        touch_list.sort(key=lambda t: t.timestamp)

        # Check pairwise for overlaps within window
        has_conflict = False
        for i, t1 in enumerate(touch_list):
            for t2 in touch_list[i + 1 :]:
                if abs((t2.timestamp - t1.timestamp).total_seconds()) < window.total_seconds():
                    has_conflict = True
                    break
            if has_conflict:
                break

        if has_conflict:
            # Determine severity
            # Critical: active sessions, Warning: open/crashed, Info: orphaned
            severity = "info"
            for touch in touch_list:
                session = next((s for s in sessions if s.session_id == touch.session_id), None)
                if session:
                    if session.status == "active":
                        severity = "critical"
                        break
                    elif session.status in ("open", "crashed"):
                        severity = "warning"

            conflicts.append(
                Conflict(
                    file_path=file_path,
                    sessions=[
                        {
                            "session_id": t.session_id[:8],  # Short ID
                            "full_session_id": t.session_id,
                            "source": t.session_source,
                            "timestamp": t.timestamp.isoformat(),
                            "project": t.project_path,
                        }
                        for t in touch_list
                    ],
                    severity=severity,
                )
            )

    # Sort by severity (critical first)
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    conflicts.sort(key=lambda c: severity_order.get(c.severity, 3))

    return ConflictReport(
        conflicts=conflicts,
        sessions_analyzed=len(sessions),
        files_touched=total_files,
        window_minutes=window_minutes,
        timestamp=datetime.now().isoformat(),
    )


def check_file_conflicts(
    file_path: str,
    exclude_session: Optional[str] = None,
    window_minutes: int = 5,
) -> Optional[Conflict]:
    """Check if a specific file has conflicts with other sessions.

    Args:
        file_path: File to check
        exclude_session: Session ID to exclude from conflict check
        window_minutes: Time window for considering overlapping touches

    Returns:
        Conflict if found, None otherwise
    """
    report = find_conflicts(window_minutes=window_minutes)

    for conflict in report.conflicts:
        if conflict.file_path == file_path:
            # Filter out excluded session
            if exclude_session:
                sessions = [
                    s
                    for s in conflict.sessions
                    if not s["full_session_id"].startswith(exclude_session)
                ]
                if len(sessions) < 2:
                    continue
                conflict.sessions = sessions
            return conflict

    return None


def format_conflict_report(report: ConflictReport) -> str:
    """Format conflict report as a readable string.

    Args:
        report: ConflictReport to format

    Returns:
        Formatted string report
    """
    lines = []

    if not report.conflicts:
        lines.append("No file conflicts detected.")
        lines.append("")
        lines.append(f"Analyzed {report.sessions_analyzed} sessions")
        lines.append(f"Window: {report.window_minutes} minutes")
        return "\n".join(lines)

    # Header
    critical_count = sum(1 for c in report.conflicts if c.severity == "critical")

    if critical_count > 0:
        lines.append(
            f"CONFLICT ALERT: {len(report.conflicts)} file(s) touched by multiple sessions!"
        )
    else:
        lines.append(f"Potential conflicts: {len(report.conflicts)} file(s)")

    lines.append("")

    # List conflicts
    for conflict in report.conflicts:
        icon = (
            "🔴"
            if conflict.severity == "critical"
            else "🟡" if conflict.severity == "warning" else "🔵"
        )
        lines.append(f"{icon} {conflict.file_path}")

        for session in conflict.sessions:
            source_tag = f"[{session['source']}]"
            time_ago = _format_time_ago(session["timestamp"])
            lines.append(f"    {session['session_id']} {source_tag} {time_ago}")

        lines.append("")

    # Summary
    lines.append(f"Sessions analyzed: {report.sessions_analyzed}")
    lines.append(f"Detection window: {report.window_minutes} minutes")

    return "\n".join(lines)


def _format_time_ago(iso_timestamp: str) -> str:
    """Format ISO timestamp as 'X ago' string."""
    try:
        ts = datetime.fromisoformat(iso_timestamp)
        diff = datetime.now() - ts
        seconds = diff.total_seconds()

        if seconds < 60:
            return f"{int(seconds)}s ago"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h ago"
        else:
            return f"{int(seconds // 86400)}d ago"
    except Exception:
        return "unknown"
