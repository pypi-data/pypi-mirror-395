"""
Drift Detector for Motus Command.

Detects when an AI agent's actions drift from the user's stated intent.
Surfaces drift as a health signal, not a blocker.

Detection signals:
- Directory drift: Agent working in unexpected project/folder
- File type drift: Agent editing unexpected file types (.py when user said "content")
- Semantic drift: Agent actions unrelated to user's stated goals
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class UserIntent:
    """Extracted intent from user messages."""

    raw_message: str
    timestamp: datetime

    # Extracted signals
    mentioned_directories: Set[str] = field(default_factory=set)
    mentioned_file_types: Set[str] = field(default_factory=set)
    keywords: Set[str] = field(default_factory=set)

    # Confidence
    confidence: float = 0.5  # 0-1, how confident we are in the extraction


@dataclass
class DriftSignal:
    """A detected drift signal."""

    signal_type: str  # "directory", "file_type", "semantic", "tool_pattern"
    description: str
    severity: float  # 0-1
    expected: str
    actual: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DriftState:
    """Current drift state for a session."""

    session_id: str
    is_drifting: bool = False
    drift_score: float = 0.0  # 0-1, aggregated drift severity
    signals: List[DriftSignal] = field(default_factory=list)
    last_checked: datetime = field(default_factory=datetime.now)

    def add_signal(self, signal: DriftSignal) -> None:
        """Add a drift signal and update score."""
        self.signals.append(signal)
        # Keep last 10 signals
        if len(self.signals) > 10:
            self.signals = self.signals[-10:]
        # Recalculate drift score
        self._update_score()

    def _update_score(self) -> None:
        """Update drift score based on recent signals."""
        if not self.signals:
            self.drift_score = 0.0
            self.is_drifting = False
            return

        # Weight recent signals more heavily
        now = datetime.now()
        weighted_sum = 0.0
        weight_total = 0.0

        for signal in self.signals:
            age = (now - signal.timestamp).total_seconds()
            # Decay weight over 5 minutes
            weight = max(0.1, 1.0 - (age / 300))
            weighted_sum += signal.severity * weight
            weight_total += weight

        self.drift_score = weighted_sum / weight_total if weight_total > 0 else 0.0
        self.is_drifting = self.drift_score > 0.5
        self.last_checked = now


# Keywords that suggest different work types
CONTENT_KEYWORDS = {
    "content",
    "blog",
    "post",
    "essay",
    "article",
    "write",
    "writing",
    "linkedin",
    "twitter",
    "social",
    "calendar",
    "newsletter",
    "copy",
    "headline",
    "draft",
    "edit",
    "publish",
    "voice",
    "tone",
    "audience",
}

CODE_KEYWORDS = {
    "code",
    "function",
    "class",
    "bug",
    "fix",
    "implement",
    "refactor",
    "test",
    "deploy",
    "build",
    "compile",
    "package",
    "install",
    "pip",
    "npm",
    "git",
    "commit",
    "merge",
    "branch",
    "api",
    "endpoint",
    "database",
}

CONTENT_FILE_TYPES = {".md", ".txt", ".doc", ".docx", ".rtf"}
CODE_FILE_TYPES = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".css",
    ".html",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
}


class DriftDetector:
    """
    Detects drift between user intent and agent actions.

    Usage:
        detector = DriftDetector()
        detector.set_intent("Help me write a blog post about AI governance")

        # On each agent action:
        drift = detector.check_action(tool_name="Edit", file_path="/code/app.py")
        if drift.is_drifting:
            # Surface in UI health indicator
    """

    def __init__(self):
        self._intents: Dict[str, UserIntent] = {}  # session_id -> intent
        self._states: Dict[str, DriftState] = {}  # session_id -> drift state
        self._action_history: Dict[str, List[dict]] = {}  # session_id -> recent actions

    def set_intent(self, session_id: str, user_message: str) -> UserIntent:
        """
        Extract and store intent from a user message.

        Called when user sends a message to establish what they want.
        """
        intent = self._extract_intent(user_message)
        self._intents[session_id] = intent

        # Reset drift state when intent changes
        if session_id in self._states:
            self._states[session_id] = DriftState(session_id=session_id)

        logger.debug(
            f"Set intent for {session_id[:8]}: dirs={intent.mentioned_directories}, "
            f"types={intent.mentioned_file_types}, keywords={list(intent.keywords)[:5]}"
        )
        return intent

    def check_action(
        self,
        session_id: str,
        tool_name: str,
        file_path: Optional[str] = None,
        tool_input: Optional[dict] = None,
    ) -> DriftState:
        """
        Check if an agent action drifts from the established intent.

        Returns the current drift state for the session.
        """
        # Ensure we have a state
        if session_id not in self._states:
            self._states[session_id] = DriftState(session_id=session_id)

        state = self._states[session_id]
        intent = self._intents.get(session_id)

        # If no intent established, can't detect drift
        if not intent:
            return state

        # Track action
        action = {
            "tool": tool_name,
            "path": file_path,
            "input": tool_input,
            "timestamp": datetime.now(),
        }
        if session_id not in self._action_history:
            self._action_history[session_id] = []
        self._action_history[session_id].append(action)
        # Keep last 20 actions
        self._action_history[session_id] = self._action_history[session_id][-20:]

        # Check for drift signals
        signals = []

        # 1. Directory drift
        if file_path:
            dir_signal = self._check_directory_drift(intent, file_path)
            if dir_signal:
                signals.append(dir_signal)

        # 2. File type drift
        if file_path:
            type_signal = self._check_file_type_drift(intent, file_path)
            if type_signal:
                signals.append(type_signal)

        # 3. Tool pattern drift
        tool_signal = self._check_tool_pattern_drift(
            intent, tool_name, self._action_history[session_id]
        )
        if tool_signal:
            signals.append(tool_signal)

        # Add signals to state
        for signal in signals:
            state.add_signal(signal)
            logger.info(f"Drift detected [{signal.signal_type}]: {signal.description}")

        return state

    def get_state(self, session_id: str) -> DriftState:
        """Get current drift state for a session."""
        if session_id not in self._states:
            self._states[session_id] = DriftState(session_id=session_id)
        return self._states[session_id]

    def clear_session(self, session_id: str) -> None:
        """Clear drift tracking for a session."""
        self._intents.pop(session_id, None)
        self._states.pop(session_id, None)
        self._action_history.pop(session_id, None)

    def _extract_intent(self, message: str) -> UserIntent:
        """Extract intent signals from a user message."""
        message_lower = message.lower()

        # Extract mentioned directories
        directories = set()
        # Look for path-like strings
        path_pattern = r"[/~][\w\-./]+"
        for match in re.findall(path_pattern, message):
            directories.add(match)

        # Extract file types mentioned
        file_types = set()
        type_pattern = r"\.\w{1,4}\b"
        for match in re.findall(type_pattern, message_lower):
            file_types.add(match)

        # Also infer from context
        if any(kw in message_lower for kw in CONTENT_KEYWORDS):
            file_types.update(CONTENT_FILE_TYPES)
        if any(kw in message_lower for kw in CODE_KEYWORDS):
            file_types.update(CODE_FILE_TYPES)

        # Extract keywords
        keywords = set()
        words = set(re.findall(r"\b\w+\b", message_lower))
        keywords.update(words & CONTENT_KEYWORDS)
        keywords.update(words & CODE_KEYWORDS)

        # Calculate confidence based on signal strength
        confidence = 0.3  # Base confidence
        if directories:
            confidence += 0.2
        if file_types:
            confidence += 0.2
        if keywords:
            confidence += 0.3

        return UserIntent(
            raw_message=message,
            timestamp=datetime.now(),
            mentioned_directories=directories,
            mentioned_file_types=file_types,
            keywords=keywords,
            confidence=min(1.0, confidence),
        )

    def _check_directory_drift(self, intent: UserIntent, file_path: str) -> Optional[DriftSignal]:
        """Check if file path is outside expected directories."""
        if not intent.mentioned_directories:
            return None

        path = Path(file_path)
        path_str = str(path)

        # Check if path is within any mentioned directory
        for expected_dir in intent.mentioned_directories:
            if expected_dir in path_str or path_str.startswith(expected_dir):
                return None  # Within expected directory

        # Drift detected
        return DriftSignal(
            signal_type="directory",
            description=f"Working in {path.parent} but expected {intent.mentioned_directories}",
            severity=0.7,
            expected=str(intent.mentioned_directories),
            actual=str(path.parent),
        )

    def _check_file_type_drift(self, intent: UserIntent, file_path: str) -> Optional[DriftSignal]:
        """Check if file type matches expected types."""
        if not intent.mentioned_file_types:
            return None

        path = Path(file_path)
        ext = path.suffix.lower()

        if not ext:
            return None

        # Check if this file type is expected
        if ext in intent.mentioned_file_types:
            return None

        # Check for content vs code mismatch
        is_content_intent = bool(intent.keywords & CONTENT_KEYWORDS)
        is_code_intent = bool(intent.keywords & CODE_KEYWORDS)

        # Content intent but editing code
        if is_content_intent and not is_code_intent and ext in CODE_FILE_TYPES:
            return DriftSignal(
                signal_type="file_type",
                description=f"Editing {ext} file but intent was content-focused",
                severity=0.8,
                expected="content files (.md, .txt)",
                actual=f"{ext} file",
            )

        # Code intent but editing content (less severe, often legitimate)
        if is_code_intent and not is_content_intent and ext in CONTENT_FILE_TYPES:
            return DriftSignal(
                signal_type="file_type",
                description=f"Editing {ext} file but intent was code-focused",
                severity=0.3,  # Lower severity - README edits are common
                expected="code files",
                actual=f"{ext} file",
            )

        return None

    def _check_tool_pattern_drift(
        self, intent: UserIntent, current_tool: str, recent_actions: List[dict]
    ) -> Optional[DriftSignal]:
        """Check if tool usage pattern matches intent."""
        is_content_intent = bool(intent.keywords & CONTENT_KEYWORDS)
        is_code_intent = bool(intent.keywords & CODE_KEYWORDS)

        # Content work typically: Read, Write, Grep (research)
        # Code work typically: Edit, Bash, Write, Read

        code_tools = {"Edit", "Bash", "Write"}

        # Count code-heavy tool usage in recent actions
        if is_content_intent and not is_code_intent:
            code_tool_count = sum(1 for a in recent_actions[-5:] if a["tool"] in code_tools)
            if code_tool_count >= 3:
                return DriftSignal(
                    signal_type="tool_pattern",
                    description=f"Heavy code tool usage ({code_tool_count}/5) but intent was content-focused",
                    severity=0.6,
                    expected="content-focused tools (Read, Write markdown)",
                    actual=f"{code_tool_count} code tools in last 5 actions",
                )

        return None


# Singleton instance
_detector: Optional[DriftDetector] = None


def get_drift_detector() -> DriftDetector:
    """Get the global drift detector instance."""
    global _detector
    if _detector is None:
        _detector = DriftDetector()
    return _detector
