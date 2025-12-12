"""
Base Builder - Shared logic for all source builders.

Contains the uniform status assignment logic and common utilities
that all builders inherit.
"""

import re
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..logging import get_logger
from ..protocols import (
    DEFAULT_THRESHOLDS,
    EventType,
    RawSession,
    RiskLevel,
    SessionStatus,
    Source,
    StatusThresholds,
    UnifiedEvent,
)

logger = get_logger(__name__)


# Decision detection patterns (source-agnostic)
DECISION_PATTERNS = [
    r"I(?:'ll| will) (?:use|implement|create|add|build|write|make|choose|go with)",
    r"I(?:'ve| have) decided to",
    r"I'm going to (?:use|implement|create|add|build|write|make|choose)",
    r"Let me (?:use|implement|create|add|build|write|make|choose)",
    r"I(?:'m| am) choosing",
    r"(?:Going|Opting) (?:to|with|for)",
    r"(?:Using|Implementing|Creating|Adding|Building|Writing|Making|Choosing)",
    r"The (?:best|right|better|optimal) (?:approach|solution|way|choice) (?:is|would be)",
]

# Compile patterns for efficiency
DECISION_REGEX = re.compile("|".join(DECISION_PATTERNS), re.IGNORECASE)


class BaseBuilder(ABC):
    """
    Base class for all source builders.

    Provides:
    - Uniform mtime-based status assignment
    - Common decision extraction patterns
    - Shared utilities for event creation
    """

    def __init__(self, thresholds: StatusThresholds = DEFAULT_THRESHOLDS):
        self.thresholds = thresholds
        self._logger = get_logger(self.__class__.__name__)

    @property
    @abstractmethod
    def source_name(self) -> Source:
        """Return source identifier."""
        ...

    @abstractmethod
    def discover(self, max_age_hours: int = 24) -> List[RawSession]:
        """Find all sessions from this source within age limit."""
        ...

    @abstractmethod
    def parse_events(self, file_path: Path) -> List[UnifiedEvent]:
        """Parse transcript file into unified events."""
        ...

    @abstractmethod
    def get_last_action(self, file_path: Path) -> str:
        """Get the last action from a session file."""
        ...

    @abstractmethod
    def has_completion_marker(self, file_path: Path) -> bool:
        """Check if session has a completion marker."""
        ...

    def compute_status(
        self,
        last_modified: datetime,
        now: datetime,
        last_action: str = "",
        has_completion: bool = True,
        project_path: str = "",
        running_projects: Optional[set] = None,
    ) -> tuple[SessionStatus, str]:
        """
        Compute session status based on modification time and process state.

        This is the UNIFORM status logic used by all sources.

        Args:
            last_modified: When the session was last modified
            now: Current time
            last_action: Last action taken in the session
            has_completion: Whether session has completion marker
            project_path: The project path for this session
            running_projects: Set of currently running project paths (from ProcessDetector)
        """
        age_seconds = (now - last_modified).total_seconds()

        # Check if process is running for this project
        has_running_process = False
        if running_projects is not None and project_path:
            has_running_process = project_path in running_projects or any(
                project_path in p for p in running_projects
            )

        # Check for crash first (1-5 min, risky op, no completion)
        if self.thresholds.crash_min_seconds < age_seconds < self.thresholds.crash_max_seconds:
            if last_action and any(k in last_action for k in ("Edit", "Write", "Bash")):
                if not has_completion:
                    return (SessionStatus.CRASHED, f"Stopped during: {last_action}")

        # Standard status based on age and process state
        if age_seconds < self.thresholds.active_seconds:
            return (SessionStatus.ACTIVE, "Modified within 2 minutes")
        elif age_seconds < self.thresholds.open_seconds:
            if has_running_process:
                return (SessionStatus.OPEN, "Process running, idle")
            else:
                return (SessionStatus.IDLE, "Modified within 30 minutes")
        elif age_seconds < self.thresholds.idle_seconds:
            if has_running_process:
                return (SessionStatus.OPEN, "Process running, idle")
            else:
                return (SessionStatus.IDLE, "Modified within 2 hours")
        else:
            return (SessionStatus.ORPHANED, "No recent activity")

    def extract_thinking(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract thinking/reasoning events.

        Default implementation returns empty list.
        Override in subclasses for source-specific extraction.
        """
        return []

    def extract_decisions(self, file_path: Path) -> List[UnifiedEvent]:
        """
        Extract decision events from transcript.

        Uses common patterns that work across all sources.
        Override in subclasses for source-specific extraction.
        """
        return []

    def _extract_decisions_from_text(
        self,
        text: str,
        session_id: str,
        timestamp: Optional[datetime] = None,
    ) -> List[UnifiedEvent]:
        """
        Extract decisions from arbitrary text.

        This is the common decision extraction logic used by all builders.
        """
        decisions = []
        timestamp = timestamp or datetime.now()

        # Find all sentences containing decision patterns
        sentences = re.split(r"[.!?]\s+", text)

        for sentence in sentences:
            if DECISION_REGEX.search(sentence):
                # Clean up the sentence
                decision_text = sentence.strip()
                if len(decision_text) > 20:  # Filter out short fragments
                    decisions.append(
                        UnifiedEvent(
                            event_id=str(uuid.uuid4()),
                            session_id=session_id,
                            timestamp=timestamp,
                            event_type=EventType.DECISION,
                            content=decision_text[:200],  # Truncate long decisions
                            decision_text=decision_text[:200],
                        )
                    )

        return decisions

    def _create_thinking_event(
        self,
        content: str,
        session_id: str,
        timestamp: Optional[datetime] = None,
        model: Optional[str] = None,
    ) -> UnifiedEvent:
        """Create a thinking event."""
        return UnifiedEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            timestamp=timestamp or datetime.now(),
            event_type=EventType.THINKING,
            content=content,
            model=model,
        )

    def _create_tool_event(
        self,
        name: str,
        input_data: dict,
        session_id: str,
        timestamp: Optional[datetime] = None,
        output: Optional[str] = None,
        status: str = "success",
        risk_level: str = "safe",
        latency_ms: Optional[int] = None,
    ) -> UnifiedEvent:
        """Create a tool event."""
        from ..protocols import RiskLevel, ToolStatus

        # Convert string risk_level to RiskLevel enum, handling 'low' explicitly
        final_risk_level = RiskLevel.SAFE
        if risk_level:
            try:
                final_risk_level = RiskLevel(risk_level)
            except ValueError:
                # Handle specific case for 'low' or other unrecognized strings
                if risk_level == "low":
                    final_risk_level = RiskLevel.SAFE
                else:
                    self._logger.warning(
                        f"Unrecognized risk level string '{risk_level}'. Defaulting to SAFE."
                    )

        return UnifiedEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            timestamp=timestamp or datetime.now(),
            event_type=EventType.TOOL,
            content=f"{name}: {self._summarize_tool_input(name, input_data)}",
            tool_name=name,
            tool_input=input_data,
            tool_output=output,
            tool_status=ToolStatus(status) if status else None,
            risk_level=final_risk_level,
            tool_latency_ms=latency_ms,
        )

    def _summarize_tool_input(self, name: str, input_data: dict) -> str:
        """Create a human-readable summary of tool input."""
        if name in ("Edit", "Write", "Read"):
            path = input_data.get("file_path") or input_data.get("path", "")
            return Path(path).name if path else "file"
        elif name == "Bash":
            cmd = input_data.get("command", "")[:50]
            return cmd
        elif name in ("Glob", "Grep"):
            pattern = input_data.get("pattern", "")[:30]
            return pattern
        elif name == "WebFetch":
            url = input_data.get("url", "")[:50]
            return url
        else:
            # Generic summary
            keys = list(input_data.keys())[:3]
            return ", ".join(keys) if keys else "..."

    def _classify_risk(self, tool_name: str, input_data: dict) -> RiskLevel:
        """Classify risk level for a tool call."""
        # High risk tools
        if tool_name == "Bash":
            cmd = input_data.get("command", "").lower()
            if any(
                danger in cmd
                for danger in [
                    "rm -rf",
                    "sudo",
                    "chmod",
                    "chown",
                    "mkfs",
                    "dd if=",
                    "> /dev/",
                    "curl | sh",
                    "wget | sh",
                ]
            ):
                return RiskLevel.CRITICAL
            if any(
                risk in cmd
                for risk in ["rm ", "mv ", "cp ", "git push", "git reset", "npm publish"]
            ):
                return RiskLevel.HIGH
            return RiskLevel.MEDIUM

        # Medium risk tools
        if tool_name in ("Write", "Edit"):
            return RiskLevel.MEDIUM

        # Safe tools
        return RiskLevel.SAFE
