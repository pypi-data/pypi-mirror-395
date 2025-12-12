#!/usr/bin/env python3
"""
MC Claude Code Hooks

These hooks integrate MC with Claude Code to inject observed context
back into Claude sessions - completing the feedback loop.

Install with: mc install-hooks
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from .config import config
from .logging import get_logger

logger = get_logger(__name__)

# Use config for directories
MC_STATE_DIR = config.paths.state_dir
CLAUDE_DIR = config.paths.claude_dir


def get_project_sessions(cwd: str, max_age_hours: int = 24) -> list:
    """Find recent MC sessions for a project directory."""
    sessions = []
    cutoff = datetime.now() - timedelta(hours=max_age_hours)

    # Check Claude transcript directory
    projects_dir = CLAUDE_DIR / "projects"
    if projects_dir.exists():
        for session_dir in projects_dir.iterdir():
            if not session_dir.is_dir():
                continue
            # Match project path (encoded as -Users-ben-GitHub-project)
            encoded_cwd = cwd.replace("/", "-").lstrip("-")
            if encoded_cwd in session_dir.name:
                for jsonl_file in session_dir.glob("*.jsonl"):
                    mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime)
                    if mtime > cutoff:
                        sessions.append({"path": jsonl_file, "mtime": mtime, "type": "claude"})

    # Check SDK traces directory
    traces_dir = MC_STATE_DIR / "traces"
    if traces_dir.exists():
        for trace_file in traces_dir.glob("*.jsonl"):
            mtime = datetime.fromtimestamp(trace_file.stat().st_mtime)
            if mtime > cutoff:
                sessions.append({"path": trace_file, "mtime": mtime, "type": "sdk"})

    return sorted(sessions, key=lambda x: x["mtime"], reverse=True)


def extract_decisions_from_session(session_path: Path, max_decisions: int = 5) -> list:
    """Extract key decisions from a session transcript."""
    decisions = []

    try:
        with open(session_path) as f:
            for line in f:
                try:
                    event = json.loads(line)

                    # SDK decision events (case-insensitive for tracer compatibility)
                    event_type = event.get("type", "").lower()
                    if event_type == "decision":
                        decisions.append(
                            {
                                "decision": event.get("decision", ""),
                                "reasoning": event.get("reasoning", ""),
                            }
                        )

                    # Claude thinking blocks with decision patterns
                    if event.get("type") == "assistant":
                        content = event.get("message", {}).get("content", [])
                        for block in content:
                            if block.get("type") == "thinking":
                                text = block.get("thinking", "")
                                # Look for decision patterns
                                decision_markers = [
                                    "I'll ",
                                    "I will ",
                                    "I decided ",
                                    "I'm going to ",
                                    "The best approach ",
                                    "I should ",
                                    "Let's ",
                                ]
                                for marker in decision_markers:
                                    if marker in text:
                                        # Extract the sentence containing the decision
                                        sentences = text.split(". ")
                                        for s in sentences:
                                            if marker in s:
                                                decisions.append(
                                                    {"decision": s.strip()[:200], "reasoning": ""}
                                                )
                                                break
                                        break

                except json.JSONDecodeError:
                    continue
    except OSError as e:
        logger.debug(f"Error reading session file {session_path}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error extracting decisions from {session_path}: {e}")

    return decisions[:max_decisions]


def extract_file_patterns(session_path: Path) -> dict:
    """Extract frequently modified files from a session."""
    file_counts: dict[str, int] = {}

    try:
        with open(session_path) as f:
            for line in f:
                try:
                    event = json.loads(line)

                    event_type = event.get("type", "")

                    # Claude: tool_use events
                    if event_type == "tool_use":
                        tool_name = event.get("name", "")
                        tool_input = event.get("input", {})

                        if tool_name in ["Write", "Edit"]:
                            file_path = tool_input.get("file_path", "")
                            if file_path:
                                file_counts[file_path] = file_counts.get(file_path, 0) + 1

                    # Codex: response_item with function_call
                    elif event_type == "response_item":
                        item = event.get("item", {})
                        func_call = item.get("function_call", {})
                        tool_name = func_call.get("name", "")
                        if tool_name in ["write_file", "edit_file", "Write", "Edit"]:
                            args = func_call.get("arguments", "{}")
                            if isinstance(args, str):
                                try:
                                    args = json.loads(args)
                                except json.JSONDecodeError:
                                    args = {}
                            file_path = args.get("file_path", "") or args.get("path", "")
                            if file_path:
                                file_counts[file_path] = file_counts.get(file_path, 0) + 1

                    # SDK: FileChange events (case-insensitive)
                    elif event_type.lower() == "filechange":
                        file_path = event.get("path", "")
                        if file_path:
                            file_counts[file_path] = file_counts.get(file_path, 0) + 1

                except json.JSONDecodeError:
                    continue
    except OSError as e:
        logger.debug(f"Error reading session file {session_path}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error extracting file patterns from {session_path}: {e}")

    return file_counts


def generate_context_injection(cwd: str) -> str:
    """Generate context to inject into Claude session."""
    sessions = get_project_sessions(cwd, max_age_hours=48)

    if not sessions:
        return ""  # No recent sessions, no context to inject

    context_parts = []
    context_parts.append("<mc-context>")
    context_parts.append("## MC-Observed Context (from recent sessions)")
    context_parts.append("")

    # Collect decisions from recent sessions
    all_decisions: list[str] = []
    all_files: dict[str, int] = {}

    for session in sessions[:3]:  # Last 3 sessions
        decisions = extract_decisions_from_session(session["path"])
        all_decisions.extend(decisions)

        files = extract_file_patterns(session["path"])
        for f, count in files.items():
            all_files[f] = all_files.get(f, 0) + count

    # Add decisions section
    if all_decisions:
        context_parts.append("### Recent Decisions")
        for d in all_decisions[:5]:
            decision_text = d["decision"]
            if d.get("reasoning"):
                decision_text += f" ({d['reasoning'][:100]})"
            context_parts.append(f"- {decision_text}")
        context_parts.append("")

    # Add frequently modified files
    if all_files:
        sorted_files = sorted(all_files.items(), key=lambda x: x[1], reverse=True)
        context_parts.append("### Hot Files (frequently modified)")
        for f, count in sorted_files[:5]:
            # Shorten path for display
            short_path = f.replace(cwd, ".") if cwd in f else f
            context_parts.append(f"- {short_path} ({count} edits)")
        context_parts.append("")

    # Check for latest summary
    summary_file = MC_STATE_DIR / "latest_summary.md"
    if summary_file.exists():
        age = datetime.now() - datetime.fromtimestamp(summary_file.stat().st_mtime)
        if age < timedelta(hours=24):
            context_parts.append("### Session Summary Available")
            context_parts.append("Run `mc summary` to see detailed session analysis")
            context_parts.append("")

    context_parts.append("</mc-context>")

    return "\n".join(context_parts)


def session_start_hook():
    """
    Claude Code SessionStart hook.

    Reads session metadata from stdin and outputs context to stdout.
    """
    try:
        # Read hook input
        hook_input = json.load(sys.stdin)
        cwd = hook_input.get("cwd", "")

        # Generate and output context
        context = generate_context_injection(cwd)
        if context:
            print(context)

        sys.exit(0)
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON from hook input: {e}")
        sys.exit(0)  # Don't block Claude
    except Exception as e:
        logger.error(f"Hook error in session_start: {e}", exc_info=True)
        sys.exit(0)  # Don't block Claude


def user_prompt_hook():
    """
    Claude Code UserPromptSubmit hook.

    Can inject context based on what the user is asking.
    """
    try:
        hook_input = json.load(sys.stdin)
        prompt = hook_input.get("prompt", "")
        cwd = hook_input.get("cwd", "")

        # Check for keywords that might benefit from MC context
        context_keywords = [
            "continue",
            "resume",
            "last session",
            "where was I",
            "what did",
            "why did",
            "decision",
            "remember",
        ]

        should_inject = any(kw in prompt.lower() for kw in context_keywords)

        if should_inject:
            context = generate_context_injection(cwd)
            if context:
                print(context)

        sys.exit(0)
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON from hook input: {e}")
        sys.exit(0)  # Don't block Claude
    except Exception as e:
        logger.error(f"Hook error in user_prompt: {e}", exc_info=True)
        sys.exit(0)  # Don't block Claude


def get_hook_config() -> dict:
    """Generate Claude Code hooks configuration for MC."""
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": 'python3 -c "from motus_command.hooks import session_start_hook; session_start_hook()"',
                            "timeout": 5000,
                        }
                    ],
                }
            ],
            "UserPromptSubmit": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": 'python3 -c "from motus_command.hooks import user_prompt_hook; user_prompt_hook()"',
                            "timeout": 3000,
                        }
                    ],
                }
            ],
        }
    }


if __name__ == "__main__":
    # For testing
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "session_start":
            session_start_hook()
        elif sys.argv[1] == "user_prompt":
            user_prompt_hook()
        elif sys.argv[1] == "config":
            print(json.dumps(get_hook_config(), indent=2))
    else:
        # Test context generation
        print(generate_context_injection("."))
