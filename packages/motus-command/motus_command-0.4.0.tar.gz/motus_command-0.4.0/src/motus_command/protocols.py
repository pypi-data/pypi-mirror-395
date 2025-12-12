"""
Motus Command Protocols - Core Data Structures

These are the unified data structures that all builders produce and all surfaces consume.
This is the contract between the builder layer and the surface layer.

Design principles:
- Source-agnostic: Claude, Codex, Gemini, SDK all produce the same structures
- Immutable after creation: Use frozen dataclasses where possible
- Optional fields have defaults: Builders only populate what they can extract
- Serializable: All structures can be JSON-serialized for API/storage
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional, Protocol

# =============================================================================
# Enums
# =============================================================================


class SessionStatus(str, Enum):
    """Session lifecycle status."""

    ACTIVE = "active"  # Modified within 2 minutes
    OPEN = "open"  # Modified within 30 minutes
    IDLE = "idle"  # Modified within 2 hours
    ORPHANED = "orphaned"  # No recent activity
    CRASHED = "crashed"  # Stopped during risky operation


class EventType(str, Enum):
    """Types of events that can occur in a session."""

    THINKING = "thinking"
    TOOL = "tool"
    DECISION = "decision"
    FILE_CHANGE = "file_change"
    FILE_READ = "file_read"
    FILE_MODIFIED = "file_modified"
    AGENT_SPAWN = "agent_spawn"
    ERROR = "error"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    USER_MESSAGE = "user_message"
    RESPONSE = "response"


class RiskLevel(str, Enum):
    """Risk level for operations."""

    SAFE = "safe"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolStatus(str, Enum):
    """Status of a tool execution."""

    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    CANCELLED = "cancelled"


class FileOperation(str, Enum):
    """Type of file operation."""

    READ = "read"
    WRITE = "write"
    EDIT = "edit"
    DELETE = "delete"


class Source(str, Enum):
    """Session source (which CLI/SDK created it)."""

    CLAUDE = "claude"
    CODEX = "codex"
    GEMINI = "gemini"
    SDK = "sdk"


# =============================================================================
# Core Data Structures
# =============================================================================


@dataclass
class UnifiedEvent:
    """
    Source-agnostic event representation.

    This is what all builders produce and all surfaces consume.
    Each event has a type and common fields, plus type-specific optional fields.
    """

    # Identity
    event_id: str
    session_id: str
    timestamp: datetime

    # Type
    event_type: EventType

    # Common fields
    content: str  # Human-readable summary
    raw_data: Dict = field(default_factory=dict)  # Original source data

    # Tool-specific (populated when event_type == TOOL)
    tool_name: Optional[str] = None
    tool_input: Optional[Dict] = None
    tool_output: Optional[str] = None
    tool_status: Optional[ToolStatus] = None
    risk_level: Optional[RiskLevel] = None
    tool_latency_ms: Optional[int] = None

    # Decision-specific (populated when event_type == DECISION)
    decision_text: Optional[str] = None
    reasoning: Optional[str] = None
    files_affected: List[str] = field(default_factory=list)

    # File-specific (populated when event_type == FILE_CHANGE)
    file_path: Optional[str] = None
    file_operation: Optional[FileOperation] = None
    lines_added: int = 0
    lines_removed: int = 0

    # Agent spawn-specific (populated when event_type == AGENT_SPAWN)
    agent_type: Optional[str] = None
    agent_description: Optional[str] = None
    agent_prompt: Optional[str] = None
    agent_model: Optional[str] = None

    # v0.3 forward-ported: Extended metadata
    model: Optional[str] = None
    tokens_used: Optional[int] = None
    cache_hit: Optional[bool] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type.value,
            "content": self.content,
            "raw_data": self.raw_data,
            "tool_name": self.tool_name,
            "tool_input": self.tool_input,
            "tool_output": self.tool_output,
            "tool_status": self.tool_status.value if self.tool_status else None,
            "risk_level": self.risk_level.value if self.risk_level else None,
            "tool_latency_ms": self.tool_latency_ms,
            "decision_text": self.decision_text,
            "reasoning": self.reasoning,
            "files_affected": self.files_affected,
            "file_path": self.file_path,
            "file_operation": self.file_operation.value if self.file_operation else None,
            "lines_added": self.lines_added,
            "lines_removed": self.lines_removed,
            "agent_type": self.agent_type,
            "agent_description": self.agent_description,
            "agent_prompt": self.agent_prompt,
            "agent_model": self.agent_model,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "cache_hit": self.cache_hit,
        }


@dataclass
class UnifiedSession:
    """
    Source-agnostic session representation.

    This is what all builders produce and all surfaces consume.
    """

    # Identity
    session_id: str
    source: Source
    file_path: Path
    project_path: str

    # Timing
    created_at: datetime
    last_modified: datetime

    # Status (computed uniformly by BaseBuilder)
    status: SessionStatus
    status_reason: str

    # Metrics (computed from events)
    event_count: int = 0
    tool_count: int = 0
    decision_count: int = 0
    file_change_count: int = 0
    thinking_count: int = 0

    # Context
    last_action: str = ""
    working_on: str = ""  # Extracted intent/goal

    # v0.3 forward-ported: File tracking (enables Conflict Radar, Scope Creep)
    files_read: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)

    @property
    def is_active(self) -> bool:
        """Convenience property for backwards compatibility."""
        return self.status == SessionStatus.ACTIVE

    @property
    def age_seconds(self) -> float:
        """Seconds since last modification."""
        return (datetime.now() - self.last_modified).total_seconds()

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "source": self.source.value,
            "file_path": str(self.file_path),
            "project_path": self.project_path,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "status": self.status.value,
            "status_reason": self.status_reason,
            "event_count": self.event_count,
            "tool_count": self.tool_count,
            "decision_count": self.decision_count,
            "file_change_count": self.file_change_count,
            "thinking_count": self.thinking_count,
            "last_action": self.last_action,
            "working_on": self.working_on,
            "files_read": self.files_read,
            "files_modified": self.files_modified,
            "is_active": self.is_active,
            "age_seconds": self.age_seconds,
        }


@dataclass
class SessionHealth:
    """
    Health metrics for a session.

    Powers CLI health widget and Web dashboard health indicators.
    """

    session_id: str

    # Overall health score (0-100)
    health_score: int
    health_label: Literal["On Track", "Needs Attention", "At Risk", "Stalled"]

    # Activity metrics
    tool_calls: int = 0
    decisions: int = 0
    files_modified: int = 0
    risky_operations: int = 0
    thinking_blocks: int = 0

    # Timing
    duration_seconds: int = 0
    last_activity_seconds: int = 0

    # Intent (extracted from context)
    current_goal: str = ""
    working_memory: List[str] = field(default_factory=list)  # Recent files/decisions

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "health_score": self.health_score,
            "health_label": self.health_label,
            "tool_calls": self.tool_calls,
            "decisions": self.decisions,
            "files_modified": self.files_modified,
            "risky_operations": self.risky_operations,
            "thinking_blocks": self.thinking_blocks,
            "duration_seconds": self.duration_seconds,
            "last_activity_seconds": self.last_activity_seconds,
            "current_goal": self.current_goal,
            "working_memory": self.working_memory,
        }


@dataclass
class TeleportBundle:
    """
    Portable context for cross-session transfer.

    Used by `mc teleport` to transfer context between sessions/models.
    """

    # Identity
    source_session: str
    source_model: str
    timestamp: datetime

    # Context (redacted, no raw file contents)
    intent: str
    decisions: List[str]
    files_touched: List[str]
    hot_files: List[str]  # Most recently touched
    pending_todos: List[str]
    last_action: str

    # Safety
    warnings: List[str] = field(default_factory=list)

    # Planning Context (v0.3)
    planning_docs: Dict[str, str] = field(default_factory=dict)

    def to_markdown(self) -> str:
        """Format as markdown for injection into target session."""
        lines = [
            f"## Context Teleported from Session {self.source_session[:8]}",
            "",
            f"**Original Task:** {self.intent}",
            f"**Model:** {self.source_model}",
            f"**Teleported:** {self.timestamp.strftime('%Y-%m-%d %H:%M')}",
            "",
        ]

        if self.decisions:
            lines.append("### Decisions Made")
            for d in self.decisions:
                lines.append(f"- {d}")
            lines.append("")

        if self.files_touched:
            lines.append("### Files Touched")
            for f in self.files_touched:
                lines.append(f"- {f}")
            lines.append("")

        if self.pending_todos:
            lines.append("### Pending Work")
            for t in self.pending_todos:
                lines.append(f"- [ ] {t}")
            lines.append("")

        if self.last_action:
            lines.append("### Last Action")
            lines.append(self.last_action)
            lines.append("")

        if self.warnings:
            for w in self.warnings:
                lines.append(f"⚠️ {w}")
            lines.append("")

        # Planning Context
        if self.planning_docs:
            lines.append("### Planning Context")
            lines.append("")
            for doc_name, content in sorted(self.planning_docs.items()):
                lines.append(f"#### {doc_name}")
                lines.append("")
                # Show first 500 chars or until first major section break
                preview = content.strip()
                if len(preview) > 500:
                    preview = preview[:500] + "..."
                lines.append(preview)
                lines.append("")

        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "source_session": self.source_session,
            "source_model": self.source_model,
            "timestamp": self.timestamp.isoformat(),
            "intent": self.intent,
            "decisions": self.decisions,
            "files_touched": self.files_touched,
            "hot_files": self.hot_files,
            "pending_todos": self.pending_todos,
            "last_action": self.last_action,
            "warnings": self.warnings,
            "planning_docs": self.planning_docs,
        }


# =============================================================================
# Raw Session (intermediate structure before UnifiedSession)
# =============================================================================


@dataclass
class RawSession:
    """
    Raw session data before status computation.

    Builders return this from discover(), then compute_status() produces UnifiedSession.
    """

    session_id: str
    source: Source
    file_path: Path
    project_path: str
    last_modified: datetime
    size: int = 0
    created_at: Optional[datetime] = None


# =============================================================================
# Builder Protocol
# =============================================================================


class SessionBuilder(Protocol):
    """
    Protocol that all source builders must implement.

    Each builder handles one source (Claude, Codex, Gemini, SDK) and produces
    unified data structures that surfaces can consume without knowing the source.
    """

    @property
    def source_name(self) -> Source:
        """Return source identifier."""
        ...

    def discover(self, max_age_hours: int = 24) -> List[RawSession]:
        """
        Find all sessions from this source within age limit.

        Returns RawSession objects that will be converted to UnifiedSession
        by the orchestrator after status computation.
        """
        ...

    def parse_events(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Parse transcript file into unified events.

        Should handle all event types the source can produce:
        - thinking, tool, decision, file_change, agent_spawn, error
        """
        ...

    def extract_thinking(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract thinking/reasoning events.

        For Claude: actual thinking blocks from transcript
        For Codex: synthetic thinking from tool planning + response patterns
        For Gemini: thoughts/reasoning fields from JSON
        """
        ...

    def extract_decisions(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract decision events from transcript.

        Patterns to match (source-agnostic):
        - "I'll...", "I decided...", "I'm going to..."
        - "Let me...", "Planning to..."
        - Tool selections with reasoning
        """
        ...

    def get_last_action(self, file_path: Path) -> str:
        """
        Get the last action from a session file.

        Returns human-readable description like "Edit src/foo.py" or "Bash: npm test"
        """
        ...

    def has_completion_marker(self, file_path: Path) -> bool:
        """
        Check if session has a completion marker after last tool call.

        A completion marker indicates the session finished normally.
        Used to distinguish crashed vs completed sessions.
        """
        ...


# =============================================================================
# Status Thresholds (configurable)
# =============================================================================


@dataclass
class StatusThresholds:
    """
    Configurable thresholds for status assignment.

    All sources use the same thresholds for uniform behavior.
    """

    active_seconds: int = 120  # 2 minutes
    open_seconds: int = 1800  # 30 minutes
    idle_seconds: int = 7200  # 2 hours
    crash_min_seconds: int = 60  # 1 minute
    crash_max_seconds: int = 300  # 5 minutes


# Default thresholds
DEFAULT_THRESHOLDS = StatusThresholds()


# =============================================================================
# Utility Functions
# =============================================================================


def compute_status(
    last_modified: datetime,
    now: datetime,
    last_action: str = "",
    has_completion: bool = True,
    thresholds: StatusThresholds = DEFAULT_THRESHOLDS,
) -> tuple[SessionStatus, str]:
    """
    Compute session status based on modification time.

    This is the UNIFORM status logic used by all sources.

    Args:
        last_modified: When the session file was last modified
        now: Current time
        last_action: Last action performed (for crash detection)
        has_completion: Whether session has a completion marker
        thresholds: Status thresholds to use

    Returns:
        Tuple of (status, reason)
    """
    age_seconds = (now - last_modified).total_seconds()

    # Check for crash first (1-5 min, risky op, no completion)
    if thresholds.crash_min_seconds < age_seconds < thresholds.crash_max_seconds:
        if last_action and any(k in last_action for k in ("Edit", "Write", "Bash")):
            if not has_completion:
                return (SessionStatus.CRASHED, f"Stopped during: {last_action}")

    # Standard status based on age
    if age_seconds < thresholds.active_seconds:
        return (SessionStatus.ACTIVE, "Modified within 2 minutes")
    elif age_seconds < thresholds.open_seconds:
        return (SessionStatus.OPEN, "Modified within 30 minutes")
    elif age_seconds < thresholds.idle_seconds:
        return (SessionStatus.IDLE, "Modified within 2 hours")
    else:
        return (SessionStatus.ORPHANED, "No recent activity")


def compute_health(
    session: UnifiedSession,
    events: List[UnifiedEvent],
) -> SessionHealth:
    """
    Compute health metrics for a session.

    Args:
        session: The session to compute health for
        events: Events from the session

    Returns:
        SessionHealth with computed metrics
    """
    # Count event types
    tool_calls = sum(1 for e in events if e.event_type == EventType.TOOL)
    decisions = sum(1 for e in events if e.event_type == EventType.DECISION)
    files_modified = len(session.files_modified)
    thinking_blocks = sum(1 for e in events if e.event_type == EventType.THINKING)
    risky_operations = sum(
        1
        for e in events
        if e.event_type == EventType.TOOL and e.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
    )

    # Compute health score (simple heuristic)
    # Start at 100, deduct for issues
    score = 100

    # Deduct for too many risky operations
    if risky_operations > 5:
        score -= min(30, risky_operations * 3)

    # Deduct for stalled sessions
    if session.status == SessionStatus.CRASHED:
        score -= 40
    elif session.status == SessionStatus.ORPHANED:
        score -= 20
    elif session.age_seconds > 600:  # 10 min without activity
        score -= 10

    # Deduct for low productivity (few tool calls)
    if tool_calls < 3 and session.age_seconds > 300:
        score -= 10

    score = max(0, min(100, score))

    # Determine label
    if score >= 80:
        label = "On Track"
    elif score >= 60:
        label = "Needs Attention"
    elif score >= 40:
        label = "At Risk"
    else:
        label = "Stalled"

    # Working memory: recent files and decisions
    working_memory = []
    working_memory.extend(session.files_modified[-5:])
    recent_decisions = [e.decision_text for e in events if e.event_type == EventType.DECISION][-3:]
    working_memory.extend([d for d in recent_decisions if d])

    return SessionHealth(
        session_id=session.session_id,
        health_score=score,
        health_label=label,
        tool_calls=tool_calls,
        decisions=decisions,
        files_modified=files_modified,
        risky_operations=risky_operations,
        thinking_blocks=thinking_blocks,
        duration_seconds=int(session.age_seconds),
        last_activity_seconds=int(session.age_seconds),
        current_goal=session.working_on,
        working_memory=working_memory,
    )
