"""Summary generation command."""

import json
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .list_cmd import find_active_session, find_sessions
from .models import SessionInfo, SessionStats
from .utils import redact_secrets

try:
    from ..config import MC_STATE_DIR
except ImportError:
    from pathlib import Path

    MC_STATE_DIR = Path.home() / ".mc"

console = Console()

# Decision markers - used across all sources
DECISION_MARKERS = [
    "I'll ",
    "I will ",
    "I decided ",
    "I'm going to ",
    "The best approach ",
    "I should ",
    "Let's ",
    "I chose ",
    "Decision:",
    "Approach:",
    "Strategy:",
]


def _extract_decision_from_text(text: str, decisions: list[str]) -> None:
    """Helper to extract decisions from a text block."""
    for marker in DECISION_MARKERS:
        if marker in text:
            sentences = text.replace("\n", " ").split(". ")
            for sentence in sentences:
                if marker in sentence and len(sentence) < 200:
                    decisions.append(sentence.strip())
                    break
            break


def extract_decisions(file_path: Path, source: str = "claude") -> list[str]:
    """Extract decision points from a session transcript.

    Supports all sources: Claude, Codex, and Gemini.

    Args:
        file_path: Path to session transcript file.
        source: Session source ("claude", "codex", or "gemini").

    Returns:
        List of decision strings (max 10).
    """
    decisions = []

    try:
        if source == "gemini":
            # Gemini uses JSON (not JSONL)
            with open(file_path, "r") as f:
                data = json.load(f)

            for msg in data.get("messages", []):
                if msg.get("type") == "gemini":
                    # Check thoughts for decisions
                    for thought in msg.get("thoughts", []):
                        desc = thought.get("description", "")
                        _extract_decision_from_text(desc, decisions)
                    # Check response content
                    content = msg.get("content", "")
                    if content:
                        _extract_decision_from_text(content, decisions)
        else:
            # Claude and Codex use JSONL
            with open(file_path, "r") as f:
                for line in f:
                    try:
                        event = json.loads(line)

                        if source == "codex":
                            # Codex: response_item with message type
                            if event.get("type") == "response_item":
                                payload = event.get("payload", {})
                                if payload.get("type") == "message":
                                    content = payload.get("content", [])
                                    if isinstance(content, list):
                                        for item in content:
                                            if (
                                                isinstance(item, dict)
                                                and item.get("type") == "text"
                                            ):
                                                _extract_decision_from_text(
                                                    item.get("text", ""), decisions
                                                )
                                    elif isinstance(content, str):
                                        _extract_decision_from_text(content, decisions)
                        else:
                            # Claude: assistant message with thinking blocks
                            if event.get("type") == "assistant":
                                for block in event.get("message", {}).get("content", []):
                                    if block.get("type") == "thinking":
                                        text = block.get("thinking", "")
                                        _extract_decision_from_text(text, decisions)

                    except json.JSONDecodeError:
                        continue

    except (OSError, IOError, json.JSONDecodeError):
        pass

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for d in decisions:
        if d not in seen:
            seen.add(d)
            unique.append(d)

    return unique[:10]  # Limit to 10 decisions


def _process_claude_event(event: dict, stats: SessionStats) -> None:
    """Process a Claude transcript event for statistics."""
    if event.get("type") == "assistant":
        for block in event.get("message", {}).get("content", []):
            if block.get("type") == "thinking":
                stats.thinking_count += 1
            elif block.get("type") == "tool_use":
                stats.tool_count += 1
                tool_name = block.get("name", "")
                tool_input = block.get("input", {})

                if tool_name in ("Write", "Edit"):
                    file_path = tool_input.get("file_path", "")
                    if file_path:
                        stats.files_modified.add(file_path)

                if tool_name == "Bash":
                    cmd = str(tool_input.get("command", ""))
                    if any(p in cmd.lower() for p in ["rm ", "sudo", "chmod"]):
                        stats.high_risk_ops += 1

                if tool_name == "Task":
                    stats.agent_count += 1


def _process_codex_event(event: dict, stats: SessionStats) -> None:
    """Process a Codex transcript event for statistics."""
    if event.get("type") == "response_item":
        payload = event.get("payload", {})
        if payload.get("type") == "function_call":
            stats.tool_count += 1
            tool_name = payload.get("name", "")
            arguments = payload.get("arguments", {})

            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except (json.JSONDecodeError, TypeError):
                    arguments = {}

            # Map to unified names
            tool_map = {
                "shell_command": "Bash",
                "write_file": "Write",
                "edit_file": "Edit",
                "create_file": "Write",
            }
            unified_name = tool_map.get(tool_name, tool_name)

            if unified_name in ("Write", "Edit"):
                file_path = arguments.get("path", arguments.get("workdir", ""))
                if file_path:
                    stats.files_modified.add(file_path)

            if unified_name == "Bash":
                cmd = str(arguments.get("command", ""))
                if any(p in cmd.lower() for p in ["rm ", "sudo", "chmod"]):
                    stats.high_risk_ops += 1


def _process_gemini_message(msg: dict, stats: SessionStats) -> None:
    """Process a Gemini message for statistics."""
    if msg.get("type") == "gemini":
        # Count thoughts as thinking
        thoughts = msg.get("thoughts", [])
        stats.thinking_count += len(thoughts)

        # Process tool calls
        for tool_call in msg.get("toolCalls", []):
            stats.tool_count += 1
            func_name = tool_call.get("name", "")
            func_args = tool_call.get("args", {})

            # Map to unified names
            tool_map = {
                "shell": "Bash",
                "run_shell_command": "Bash",
                "write_file": "Write",
                "edit_file": "Edit",
            }
            unified_name = tool_map.get(func_name, func_name)

            if unified_name in ("Write", "Edit"):
                file_path = func_args.get("path", "")
                if file_path:
                    stats.files_modified.add(file_path)

            if unified_name == "Bash":
                cmd = str(func_args.get("command", ""))
                if any(p in cmd.lower() for p in ["rm ", "sudo", "chmod"]):
                    stats.high_risk_ops += 1


def analyze_session(session: SessionInfo) -> SessionStats:
    """Analyze a session and return statistics.

    Supports all sources: Claude, Codex, and Gemini.

    Args:
        session: SessionInfo object with file_path and source.

    Returns:
        SessionStats with counts and file lists.
    """
    stats = SessionStats()
    source = getattr(session, "source", "claude") or "claude"

    try:
        if source == "gemini":
            # Gemini uses JSON (not JSONL)
            with open(session.file_path, "r") as f:
                data = json.load(f)

            for msg in data.get("messages", []):
                _process_gemini_message(msg, stats)
        else:
            # Claude and Codex use JSONL
            with open(session.file_path, "r") as f:
                for line in f:
                    try:
                        event = json.loads(line)

                        if source == "codex":
                            _process_codex_event(event, stats)
                        else:
                            _process_claude_event(event, stats)

                    except json.JSONDecodeError:
                        continue

    except (OSError, IOError, json.JSONDecodeError):
        pass

    return stats


def generate_agent_context(session: SessionInfo) -> str:
    """Generate context summary for AI agents."""
    source = getattr(session, "source", "claude") or "claude"
    stats = analyze_session(session)
    decisions = extract_decisions(session.file_path, source=source)

    context_parts = [
        "## Session Context",
        "",
        f"**Project**: {session.project_path}",
        f"**Session ID**: {session.session_id[:12]}",
        f"**Status**: {'🟢 Active' if session.is_active else '⚪ Idle'}",
        "",
        "### Activity Summary",
        f"- Thinking blocks: {stats.thinking_count}",
        f"- Tool calls: {stats.tool_count}",
        f"- Files modified: {len(stats.files_modified)}",
        f"- Agent spawns: {stats.agent_count}",
        f"- High-risk ops: {stats.high_risk_ops}",
        "",
    ]

    if stats.files_modified:
        context_parts.append("### Files Modified")
        for f in list(stats.files_modified)[:10]:
            short = f.split("/")[-1]
            context_parts.append(f"- {short}")
        context_parts.append("")

    if decisions:
        context_parts.append("### Key Decisions")
        for d in decisions[:5]:
            # Redact any secrets that might be in decision text
            context_parts.append(f"- {redact_secrets(d)}")
        context_parts.append("")

    return "\n".join(context_parts)


def summary_command(session_id: Optional[str] = None):
    """Generate and display session summary for any source (Claude, Codex, Gemini)."""
    if session_id:
        # Find specific session from any source
        sessions = find_sessions(max_age_hours=168)  # Last week
        session = next((s for s in sessions if s.session_id.startswith(session_id)), None)
        if not session:
            console.print(f"[red]Session not found: {session_id}[/red]")
            return
    else:
        # Use most recent/active session from any source
        session = find_active_session()
        if not session:
            console.print("[yellow]No recent sessions found.[/yellow]")
            return

    # Generate context
    context = generate_agent_context(session)

    # Display
    console.print(
        Panel(
            Markdown(context),
            title=f"Session Summary: {session.session_id[:12]}",
            border_style="blue",
        )
    )

    # Save to file for agent consumption
    summary_file = MC_STATE_DIR / "latest_summary.md"
    MC_STATE_DIR.mkdir(exist_ok=True)
    summary_file.write_text(context)
    console.print(f"\n[dim]Summary saved to: {summary_file}[/dim]")
