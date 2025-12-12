"""
Decision Ledger for Motus Command v0.3.

Extracts and tracks decisions made by AI agents during sessions.
Helps users understand why certain choices were made.

Features:
- Extract decisions from transcript text
- Look for "decided", "chose", "because", "instead of" patterns
- Track files affected by each decision
- CLI: `mc decisions [session-id]`
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .logging import get_logger
from .session_manager import session_manager
from .transcript_parser import TranscriptParser

logger = get_logger(__name__)


# Patterns that indicate a decision was made
DECISION_PATTERNS = [
    # Explicit decision language
    r"(?:I(?:'ve|'ll| will| have)?|(?:we(?:'ve|'ll| will| have)?)) (?:decided to|chose to|chosen to|opted to|going to|will)",
    r"(?:decided|chose|chosen|opted) to (?:use|implement|add|create|remove|change|update|fix|keep|skip|avoid)",
    r"(?:using|implementing|adding|creating|removing|changing|updating|fixing|keeping|skipping|avoiding) .+ instead of",
    r"(?:rather than|instead of|over) .+, (?:I|we)(?:'ll|'ve| will| have)?",
    # Reasoning indicators
    r"because .+ (?:is|are|was|were|will be|would be) (?:better|simpler|cleaner|faster|safer|more)",
    r"(?:this|that) (?:is|would be) (?:better|simpler|cleaner|faster|safer|more)",
    r"(?:the reason|reasoning) (?:is|being) that",
    # Comparison decisions
    r"(?:prefer|preferable|better) (?:to use|to have|than)",
    r"(?:should|shouldn't|will|won't) (?:use|add|include|create|have)",
]

# Compile patterns for efficiency
COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in DECISION_PATTERNS]


@dataclass
class Decision:
    """A decision made during a session."""

    timestamp: str
    decision: str  # The decision text
    reasoning: str = ""  # Why it was made
    files_affected: list[str] = field(default_factory=list)
    reversible: bool = True
    context: str = ""  # Surrounding context

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "files_affected": self.files_affected,
            "reversible": self.reversible,
            "context": self.context,
        }


@dataclass
class DecisionLedger:
    """Collection of decisions from a session."""

    session_id: str
    decisions: list[Decision] = field(default_factory=list)
    timestamp: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "decisions": [d.to_dict() for d in self.decisions],
            "timestamp": self.timestamp,
        }


def extract_decision_from_text(text: str, context: str = "") -> Optional[Decision]:
    """Extract a decision from a text block if one exists.

    Args:
        text: The text to analyze
        context: Surrounding context for the decision

    Returns:
        Decision if found, None otherwise
    """
    # Check if any decision pattern matches
    for pattern in COMPILED_PATTERNS:
        match = pattern.search(text)
        if match:
            # Extract the decision (sentence containing the match)
            start = text.rfind(".", 0, match.start()) + 1
            end = text.find(".", match.end())
            if end == -1:
                end = len(text)

            decision_text = text[start:end].strip()
            if len(decision_text) < 10:  # Too short to be meaningful
                continue

            # Try to extract reasoning (look for "because" or similar)
            reasoning = ""
            because_match = re.search(
                r"because (.+?)(?:\.|$)", text[match.start() :], re.IGNORECASE
            )
            if because_match:
                reasoning = because_match.group(1).strip()

            # Extract file references
            files = extract_file_references(text)

            return Decision(
                timestamp=datetime.now().isoformat(),
                decision=decision_text[:200],  # Limit length
                reasoning=reasoning[:200] if reasoning else "",
                files_affected=files[:5],  # Limit to 5 files
                reversible=True,
                context=context[:100] if context else "",
            )

    return None


def extract_file_references(text: str) -> list[str]:
    """Extract file path references from text.

    Args:
        text: Text to search for file references

    Returns:
        List of file paths found
    """
    files = []

    # Common file patterns
    patterns = [
        r"[\w/.-]+\.(?:py|js|ts|tsx|jsx|json|yaml|yml|md|txt|sh|css|scss|html)",
        r"(?:src|lib|tests?|components?|utils?|config)/[\w/.-]+",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if match not in files and len(match) < 100:
                files.append(match)

    return files


def extract_decisions_from_session(
    session_path: Path,
    source: str = "claude",
) -> list[Decision]:
    """Extract decisions from a session transcript.

    Args:
        session_path: Path to session transcript
        source: Session source (claude, codex, gemini)

    Returns:
        List of decisions found
    """
    decisions = []
    parser = TranscriptParser(extract_file_snapshots=False)

    try:
        data = parser.parse_file(session_path)

        # Analyze assistant messages for decisions
        for event in data.all_events:
            if event.event_type == "assistant":
                content = event.content or ""
                if len(content) > 50:  # Need substantial content
                    decision = extract_decision_from_text(content)
                    if decision:
                        decisions.append(decision)

    except Exception as e:
        logger.debug(f"Error extracting decisions from {session_path}: {e}")

    return decisions


def get_decisions(
    session_id: Optional[str] = None,
    session_path: Optional[Path] = None,
) -> DecisionLedger:
    """Get decisions from a session.

    Args:
        session_id: Session ID to analyze (finds most recent if None)
        session_path: Direct path to session file

    Returns:
        DecisionLedger with extracted decisions
    """
    if session_path:
        decisions = extract_decisions_from_session(session_path)
        return DecisionLedger(
            session_id=session_path.stem,
            decisions=decisions,
            timestamp=datetime.now().isoformat(),
        )

    # Find session by ID
    sessions = session_manager.find_sessions(max_age_hours=24)

    if not sessions:
        return DecisionLedger(
            session_id="none",
            decisions=[],
            timestamp=datetime.now().isoformat(),
        )

    target_session = None
    if session_id:
        for s in sessions:
            if s.session_id.startswith(session_id):
                target_session = s
                break
    else:
        # Use most recent
        target_session = sessions[0]

    if not target_session:
        return DecisionLedger(
            session_id=session_id or "unknown",
            decisions=[],
            timestamp=datetime.now().isoformat(),
        )

    decisions = extract_decisions_from_session(
        target_session.file_path,
        target_session.source,
    )

    return DecisionLedger(
        session_id=target_session.session_id,
        decisions=decisions,
        timestamp=datetime.now().isoformat(),
    )


def format_decision_ledger(ledger: DecisionLedger) -> str:
    """Format decision ledger as a readable string.

    Args:
        ledger: DecisionLedger to format

    Returns:
        Formatted string report
    """
    lines = []

    if not ledger.decisions:
        lines.append("No decisions found in session.")
        lines.append("")
        lines.append(f"Session: {ledger.session_id[:8]}...")
        return "\n".join(lines)

    lines.append(f"Decisions from session {ledger.session_id[:8]}...")
    lines.append("")

    for i, decision in enumerate(ledger.decisions, 1):
        lines.append(f"{i}. {decision.decision}")
        if decision.reasoning:
            lines.append(f"   Reasoning: {decision.reasoning}")
        if decision.files_affected:
            lines.append(f"   Files: {', '.join(decision.files_affected)}")
        lines.append("")

    lines.append(f"Total: {len(ledger.decisions)} decision(s)")
    return "\n".join(lines)


def format_decisions_for_export(ledger: DecisionLedger) -> str:
    """Format decisions for CLAUDE.md or PR description.

    Args:
        ledger: DecisionLedger to format

    Returns:
        Markdown formatted string
    """
    lines = []

    lines.append("## Decisions Made")
    lines.append("")

    if not ledger.decisions:
        lines.append("_No significant decisions recorded._")
        return "\n".join(lines)

    for decision in ledger.decisions:
        lines.append(f"- **{decision.decision}**")
        if decision.reasoning:
            lines.append(f"  - Reasoning: {decision.reasoning}")
        if decision.files_affected:
            files_str = ", ".join(f"`{f}`" for f in decision.files_affected)
            lines.append(f"  - Files affected: {files_str}")

    return "\n".join(lines)
