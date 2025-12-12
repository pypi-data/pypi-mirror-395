"""
MC TUI - Interactive Command Center using Textual.

Features:
- Session list with keyboard navigation
- Filter mode: / to filter by project, tool, risk level
- History retention: selecting a session highlights, not hides
- Git action detection and display
- Real-time updates
"""

import re

# Import from parent module
import sys
from pathlib import Path
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import logger - with fallback for direct module imports in tests
try:
    from motus_command.logging import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)  # type: ignore[assignment]

# Import drift detector
try:
    from motus_command.drift_detector import DriftDetector, get_drift_detector
except ImportError:
    try:
        from drift_detector import DriftDetector, get_drift_detector
    except ImportError:
        get_drift_detector = None  # type: ignore[assignment,misc]
        DriftDetector = None  # type: ignore[assignment,misc]

# Import Gemini parser for multi-source support
try:
    from motus_command.gemini_parser import parse_gemini_file
except ImportError:
    try:
        from gemini_parser import parse_gemini_file
    except ImportError:
        parse_gemini_file = None  # type: ignore[assignment,misc]

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Label, ListItem, ListView, Static

sys.path.insert(0, str(Path(__file__).parent.parent))
from cli import (
    SessionInfo,
    TaskEvent,
    ThinkingEvent,
    ToolEvent,
    find_sdk_traces,
    parse_gemini_event,
    parse_line_by_source,
)

# Import orchestrator for session management
try:
    from motus_command.orchestrator import get_orchestrator
except ImportError:
    from orchestrator import get_orchestrator


def _unified_to_sessioninfo(unified_session) -> SessionInfo:
    """
    Convert UnifiedSession to SessionInfo for backwards compatibility.

    This adapter allows TUI to work with the new orchestrator while maintaining
    the existing SessionInfo interface throughout the display logic.
    """
    # Map SessionStatus enum to status strings
    status_map = {
        "active": "active",
        "open": "open",
        "crashed": "crashed",
        "idle": "idle",
        "orphaned": "orphaned",
    }

    # Handle both enum and string status
    status_str = unified_session.status
    if hasattr(unified_session.status, "value"):
        status_str = unified_session.status.value

    # Map Source enum to source strings
    source_str = unified_session.source
    if hasattr(unified_session.source, "value"):
        source_str = unified_session.source.value

    return SessionInfo(
        session_id=unified_session.session_id,
        file_path=unified_session.file_path,
        last_modified=unified_session.last_modified,
        size=unified_session.file_path.stat().st_size if unified_session.file_path.exists() else 0,
        is_active=(status_str == "active"),
        project_path=unified_session.project_path,
        status=status_map.get(status_str, status_str),
        last_action=unified_session.status_reason or "",
        source=source_str,
    )


class SessionItem(ListItem):
    """A session item in the sidebar list."""

    def __init__(
        self,
        session: Optional[SessionInfo] = None,
        is_all: bool = False,
        sdk_trace: Optional[dict] = None,
        is_drifting: bool = False,
    ):
        super().__init__()
        self.session = session
        self.is_all = is_all
        self.sdk_trace = sdk_trace
        self.is_drifting = is_drifting

    def compose(self) -> ComposeResult:
        if self.is_all:
            yield Label("[bold cyan]ALL[/bold cyan] Combined feed")
        elif self.sdk_trace:
            trace = self.sdk_trace
            status = "[blue]◆[/blue]" if trace["is_active"] else "[dim]◇[/dim]"
            yield Label(f"{status} [dim]SDK[/dim] {trace['name'][:15]}")
        elif self.session:
            s = self.session
            # Drift indicator takes priority
            if self.is_drifting:
                status = "[magenta]⚠[/magenta]"  # Drifting from intent
            elif s.status == "active":
                status = "[green]●[/green]"  # Actively generating
            elif s.status == "open":
                status = "[yellow]○[/yellow]"  # Process running, idle
            elif s.status == "crashed":
                status = "[red]✗[/red]"  # May have crashed mid-action
            else:  # orphaned
                status = "[dim]◌[/dim]"  # Process ended

            # Add drift badge if drifting
            drift_badge = " [magenta]DRIFT[/magenta]" if self.is_drifting else ""

            # Source badge
            source = getattr(s, "source", "claude") or "claude"
            source_colors = {
                "claude": "magenta",
                "codex": "green",
                "gemini": "blue",
                "sdk": "yellow",
            }
            source_color = source_colors.get(source, "dim")
            source_badge = f"[{source_color}]{source[:3].upper()}[/{source_color}]"

            yield Label(
                f"{status} {source_badge} [{s.session_id[:8]}]{drift_badge} {s.project_path[:10]}"
            )


class SessionsList(ListView):
    """The sessions list sidebar."""

    BINDINGS = [
        Binding("j", "cursor_down", "Down"),
        Binding("k", "cursor_up", "Up"),
    ]


class SessionContext:
    """Tracks accumulated context/memory for a session - what the agent 'knows'."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.files_read: list[str] = []  # Files the agent has seen
        self.files_modified: list[str] = []  # Files changed
        self.decisions: list[str] = []  # Key decisions made
        self.agent_tree: list[dict] = []  # Spawned agents with full prompts
        self.key_findings: list[str] = []  # Important discoveries
        self.tool_count: dict[str, int] = {}  # Tool usage stats

    def add_file_read(self, path: str):
        filename = path.split("/")[-1] if "/" in path else path
        if filename not in self.files_read:
            self.files_read.append(filename)
            # Keep last 15
            self.files_read = self.files_read[-15:]

    def add_file_modified(self, path: str):
        filename = path.split("/")[-1] if "/" in path else path
        if filename not in self.files_modified:
            self.files_modified.append(filename)

    def add_decision(self, decision: str):
        if decision and decision not in self.decisions:
            self.decisions.append(decision[:80])
            self.decisions = self.decisions[-5:]

    def add_agent_spawn(
        self, agent_type: str, description: str, prompt: str, model: Optional[str] = None
    ):
        self.agent_tree.append(
            {
                "type": agent_type,
                "desc": description[:50],
                "prompt": prompt,  # Full prompt for "glass into the matrix"
                "model": model or "default",
            }
        )
        # Keep last 5 spawns with full context
        self.agent_tree = self.agent_tree[-5:]

    def add_tool_use(self, tool_name: str):
        self.tool_count[tool_name] = self.tool_count.get(tool_name, 0) + 1

    def render(self) -> str:
        """Render context panel content."""
        lines = []

        # Files in context
        if self.files_read:
            lines.append("[bold cyan]📖 Files Read[/bold cyan]")
            for f in self.files_read[-8:]:
                lines.append(f"  [dim]•[/dim] {f[:25]}")
            lines.append("")

        # Files modified
        if self.files_modified:
            lines.append("[bold yellow]✏️ Modified[/bold yellow]")
            for f in self.files_modified[-5:]:
                lines.append(f"  [yellow]•[/yellow] {f[:25]}")
            lines.append("")

        # Agent spawns with prompts
        if self.agent_tree:
            lines.append("[bold magenta]🤖 Agent Tree[/bold magenta]")
            for i, agent in enumerate(self.agent_tree[-3:]):
                prefix = "└─" if i == len(self.agent_tree[-3:]) - 1 else "├─"
                lines.append(f"  {prefix} [yellow]{agent['type']}[/yellow]")
                lines.append(f"     [dim]{agent['desc'][:30]}[/dim]")
                # Show prompt preview
                prompt_preview = agent["prompt"][:60].replace("\n", " ")
                lines.append(f'     [italic dim]"{prompt_preview}..."[/italic dim]')
            lines.append("")

        # Decisions
        if self.decisions:
            lines.append("[bold green]💡 Decisions[/bold green]")
            for d in self.decisions[-3:]:
                lines.append(f"  [dim]→[/dim] {d[:35]}...")
            lines.append("")

        # Tool stats
        if self.tool_count:
            lines.append("[bold blue]📊 Tools Used[/bold blue]")
            sorted_tools = sorted(self.tool_count.items(), key=lambda x: -x[1])[:5]
            for tool, count in sorted_tools:
                bar = "█" * min(count, 10)
                lines.append(f"  {tool[:8]:8} [dim]{bar}[/dim] {count}")

        if not lines:
            lines.append("[dim]Collecting context...[/dim]")

        return "\n".join(lines)


class EventRecord:
    """An event with metadata for filtering and hierarchy."""

    __slots__ = (
        "text",
        "session_id",
        "tool_name",
        "risk_level",
        "project_path",
        "timestamp",
        "event_type",
        "depth",
        "content",
        "is_agent_spawn",
    )

    def __init__(
        self,
        text: str,
        session_id: str,
        tool_name: str = "",
        risk_level: str = "safe",
        project_path: str = "",
        timestamp: str = "",
        event_type: str = "action",  # "thinking", "decision", "action", "agent_spawn"
        depth: int = 0,  # Agent hierarchy depth
        content: str = "",  # Raw content for grouping
        is_agent_spawn: bool = False,
    ):
        self.text = text
        self.session_id = session_id
        self.tool_name = tool_name
        self.risk_level = risk_level
        self.project_path = project_path
        self.timestamp = timestamp
        self.event_type = event_type
        self.depth = depth
        self.content = content
        self.is_agent_spawn = is_agent_spawn


class ActivityBlock:
    """Groups related events into visual blocks."""

    def __init__(self, session_id: str, timestamp: str):
        self.session_id = session_id
        self.timestamp = timestamp
        self.thinking_summary: str = ""
        self.decisions: list[str] = []
        self.actions: list[EventRecord] = []
        self.agent_spawns: list[tuple[str, str, int]] = []  # (agent_type, description, depth)

    def add_thinking(self, content: str):
        """Add thinking content - capture more detail for visibility."""
        # More comprehensive intent phrases to capture
        intent_phrases = [
            "i'll ",
            "let me ",
            "i need to ",
            "i should ",
            "going to ",
            "i'm ",
            "i am ",
            "i will ",
            "assigning ",
            "spawning ",
            "launching ",
            "creating ",
            "updating ",
            "checking ",
            "searching ",
        ]

        # Store full sentences for display
        for line in content.split("."):
            line_lower = line.lower().strip()
            for phrase in intent_phrases:
                if phrase in line_lower:
                    # Capture the full intent line (longer for visibility)
                    summary = line.strip()[:100]
                    if summary and summary.lower() not in self.thinking_summary.lower():
                        if self.thinking_summary:
                            self.thinking_summary += "\n  "
                        self.thinking_summary += summary
                        break

    def add_decision(self, decision: str):
        if decision not in self.decisions:
            self.decisions.append(decision[:50])

    def add_action(self, record: EventRecord):
        self.actions.append(record)

    def add_agent_spawn(self, agent_type: str, description: str, depth: int = 0):
        self.agent_spawns.append((agent_type, description, depth))

    def render(self, short_id: str, is_highlighted: bool = True) -> list[str]:
        """Render the activity block as a visual thread of thought → action."""
        lines = []
        dim = "" if is_highlighted else "[dim]"
        end_dim = "" if is_highlighted else "[/dim]"

        # Block header with session badge
        sid_badge = (
            f"[black on cyan] {short_id} [/black on cyan]"
            if is_highlighted
            else f"[dim]{short_id}[/dim]"
        )

        # Thread visualization: │ for continuation, └─ for chain links
        thread_start = "┌─"
        thread_cont = "│ "
        thread_branch = "├─"
        thread_end = "└─"

        has_more = bool(self.agent_spawns or self.actions or self.decisions)

        # === THINKING: Start of thread ===
        if self.thinking_summary:
            thinking_lines = self.thinking_summary.split("\n  ")
            first_line = thinking_lines[0][:120]
            conn = thread_start if has_more else "──"
            lines.append(
                f"{dim}{self.timestamp} {sid_badge} {conn} [magenta]💭 THINK[/magenta] {first_line}{end_dim}"
            )

            # Additional thinking lines
            for i, extra_line in enumerate(thinking_lines[1:4]):  # Up to 4 total
                conn = thread_cont if (i < len(thinking_lines) - 2 or has_more) else thread_end
                lines.append(
                    f"{dim}         {sid_badge} {conn}   [italic magenta]{extra_line[:100]}[/italic magenta]{end_dim}"
                )

        # === DECISIONS: What was decided ===
        for i, decision in enumerate(self.decisions[-2:]):  # Last 2 decisions
            is_last_decision = (
                i == len(self.decisions[-2:]) - 1 and not self.agent_spawns and not self.actions
            )
            conn = thread_end if is_last_decision else thread_branch
            lines.append(
                f"{dim}         {sid_badge} {conn} [yellow]⚡ DECIDE[/yellow] {decision}{end_dim}"
            )

        # === AGENT SPAWNS: Show the delegation chain ===
        if self.agent_spawns:
            for i, (agent_type, desc, depth) in enumerate(self.agent_spawns):
                is_last_spawn = i == len(self.agent_spawns) - 1 and not self.actions
                base_conn = thread_end if is_last_spawn else thread_branch
                indent = "  " * depth
                lines.append(
                    f"{dim}         {sid_badge} {base_conn}{indent} [yellow]🤖 {agent_type}[/yellow] → {desc[:50]}{end_dim}"
                )

        # === ACTIONS: What tools were called ===
        action_groups: dict[str, list[EventRecord]] = {}
        for action in self.actions:
            key = action.tool_name
            if key not in action_groups:
                action_groups[key] = []
            action_groups[key].append(action)

        group_keys = list(action_groups.keys())
        for idx, tool_name in enumerate(group_keys):
            actions = action_groups[tool_name]
            is_last_group = idx == len(group_keys) - 1

            if len(actions) == 1:
                conn = thread_end if is_last_group else thread_branch
                # Single action - show inline with thread
                action_text = actions[0].text
                # Strip out the timestamp and badge from original text, we'll add our own connector
                lines.append(f"{dim}{action_text}{end_dim}")
            else:
                conn = thread_end if is_last_group else thread_branch
                risk_bg = self._get_risk_bg(actions[0].risk_level)
                icon = self._get_tool_icon(tool_name)
                lines.append(
                    f"{dim}         {sid_badge} {conn} [{risk_bg}] {tool_name} [/{risk_bg}] {icon} ×{len(actions)}{end_dim}"
                )
                for j, action in enumerate(actions[-3:]):  # Show last 3
                    target = self._extract_target(action)
                    sub_conn = "    └─" if (j == len(actions[-3:]) - 1) else "    ├─"
                    lines.append(
                        f"{dim}         {sid_badge} {thread_cont}{sub_conn} {target}{end_dim}"
                    )

        return lines

    def _get_risk_bg(self, risk_level: str) -> str:
        return {
            "safe": "black on green",
            "medium": "black on yellow",
            "high": "white on red",
            "critical": "white on red",
        }.get(risk_level, "black on blue")

    def _get_tool_icon(self, tool_name: str) -> str:
        return {
            "Read": "📖",
            "Write": "✏️",
            "Edit": "🔧",
            "Bash": "💻",
            "Glob": "🔍",
            "Grep": "🔎",
            "Task": "🤖",
            "Think": "💭",
        }.get(tool_name, "⚡")

    def _extract_target(self, action: EventRecord) -> str:
        """Extract the target/file from action for compact display."""
        # Try to find filename in text
        import re

        # Look for paths
        match = re.search(r"[\w./]+\.\w+", action.content or action.text)
        if match:
            return match.group()[-30:]
        return action.content[:30] if action.content else "..."


class ContextPanel(ScrollableContainer):
    """Panel showing accumulated session context/memory."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Static(id="context-content")


class FeedPanel(ScrollableContainer):
    """The main feed panel showing events."""

    mode = reactive("all")  # "all" or session_id
    filter_text = reactive("")  # Filter string

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events: list[str] = []  # Formatted event strings for display
        self.activity_blocks: list[ActivityBlock] = []  # Grouped for display
        self.insights: list[str] = []
        self.session_positions: dict[str, int] = {}
        self.git_actions: list[str] = []
        self.session_projects: dict[str, str] = {}  # session_id -> project_path
        self.agent_depth: dict[str, int] = {}  # session_id -> current agent depth
        self.session_contexts: dict[str, SessionContext] = {}  # session_id -> context
        self.drift_detector = get_drift_detector() if get_drift_detector else None
        self.session_drift_states: dict[str, dict] = {}  # session_id -> drift state
        self.gemini_event_counts: dict[str, int] = {}  # session_id -> number of events shown
        self.parsing_errors: dict[str, str] = {}  # session_id -> error message

    def compose(self) -> ComposeResult:
        yield Static(id="feed-content")

    def clear_events(self):
        self.events = []
        self.activity_blocks = []
        self.insights = []
        self.git_actions = []

    def _get_or_create_block(self, session_id: str, timestamp: str) -> ActivityBlock:
        """Get current activity block or create new one."""
        # Create new block if none exists or if it's been >30 seconds
        if not self.activity_blocks or self.activity_blocks[-1].session_id != session_id:
            block = ActivityBlock(session_id, timestamp)
            self.activity_blocks.append(block)
            return block
        return self.activity_blocks[-1]

    def matches_filter(
        self, record: EventRecord, selected_session: Optional[str]
    ) -> tuple[bool, bool]:
        """
        Check if event matches current filter.
        Returns (matches, is_highlighted).
        - matches: event passes filter (should be shown)
        - is_highlighted: event is for selected session (should be bright)
        """
        # Text filter
        if self.filter_text:
            filter_lower = self.filter_text.lower()
            text_match = any(
                [
                    filter_lower in record.text.lower(),
                    filter_lower in record.tool_name.lower(),
                    filter_lower in record.project_path.lower(),
                    filter_lower in record.risk_level.lower(),
                ]
            )
            if not text_match:
                return False, False

        # Session selection (for highlighting, not filtering)
        is_highlighted = selected_session is None or record.session_id == selected_session
        return True, is_highlighted

    def render_all_mode(
        self, sessions: list[SessionInfo], selected_session: Optional[str] = None
    ) -> str:
        """Render with visual hierarchy using ActivityBlocks."""

        # Clean up gemini_event_counts for sessions that no longer exist
        active_session_ids = {s.session_id for s in sessions}
        stale_gemini_sessions = set(self.gemini_event_counts.keys()) - active_session_ids
        for stale_id in stale_gemini_sessions:
            del self.gemini_event_counts[stale_id]

        # Collect events from ALL sessions (including orphaned - for history viewing)
        for session in sessions:
            session_id = session.session_id
            project_path = session.project_path
            self.session_projects[session_id] = project_path

            last_pos = self.session_positions.get(session_id, 0)

            try:
                current_size = session.file_path.stat().st_size
                if current_size > last_pos:
                    # Get session source for multi-source parsing
                    source = getattr(session, "source", "claude") or "claude"

                    # Gemini uses single JSON blob format, not JSONL
                    if source == "gemini" and parse_gemini_file is not None:
                        # Parse entire file to get all events
                        event_dicts = parse_gemini_file(session.file_path)

                        # Track how many events we've already shown
                        last_event_count = self.gemini_event_counts.get(session_id, 0)

                        # Only process new events
                        for event_dict in event_dicts[last_event_count:]:
                            event = parse_gemini_event(event_dict)
                            if event:
                                self._process_event_to_block(event, session_id, project_path)

                        # Update the count of displayed events
                        self.gemini_event_counts[session_id] = len(event_dicts)

                        # Mark file as fully read
                        self.session_positions[session_id] = current_size
                    else:
                        # Claude/Codex use JSONL format (one JSON object per line)
                        with open(session.file_path, "r") as f:
                            f.seek(last_pos)
                            new_content = f.read()
                            self.session_positions[session_id] = f.tell()

                        for line in new_content.strip().split("\n"):
                            if line.strip():
                                # Check for user intent before parsing
                                self._check_for_user_intent(line, session_id, project_path)
                                events = parse_line_by_source(line, source)
                                for event in events:
                                    self._process_event_to_block(event, session_id, project_path)
            except OSError as e:
                logger.debug(f"Error reading session file {session.file_path}: {e}")
                self.parsing_errors[session_id] = f"File read error: {str(e)[:50]}"
            except Exception as e:
                logger.warning(f"Unexpected error processing session {session_id}: {e}")
                self.parsing_errors[session_id] = f"Parsing error: {str(e)[:50]}"

        # Trim to last 15 activity blocks
        self.activity_blocks = self.activity_blocks[-15:]

        if not self.activity_blocks:
            if not sessions:
                return (
                    "[yellow]No sessions found[/yellow] - start Claude/Codex/Gemini to see activity"
                )
            return "[dim]Waiting for activity...[/dim]"

        # Build output with visual hierarchy
        output_lines = []

        # Filter/Focus status
        if self.filter_text:
            output_lines.append(
                f"[black on yellow] FILTER: {self.filter_text} [/black on yellow] [dim]ESC to clear[/dim]"
            )
            output_lines.append("")

        if selected_session:
            proj = self.session_projects.get(selected_session, "")[:25]
            output_lines.append(
                f"[black on cyan] FOCUS [/black on cyan] {proj} [dim]'a' for all[/dim]"
            )
            output_lines.append("")

        # Render activity blocks with visual separation
        last_session = None
        for block in self.activity_blocks[-10:]:  # Show last 10 blocks
            short_id = block.session_id[:6]

            # Session changed - add separator
            if last_session and last_session != block.session_id:
                output_lines.append("[dim]────────────────────────────────────────[/dim]")

            is_highlighted = selected_session is None or block.session_id == selected_session

            # Filter check - skip blocks that don't match
            if self.filter_text:
                filter_lower = self.filter_text.lower()
                proj_path = self.session_projects.get(block.session_id, "")
                block_text = f"{block.thinking_summary} {' '.join(a.tool_name for a in block.actions)} {proj_path}"
                if filter_lower not in block_text.lower():
                    continue

            block_lines = block.render(short_id, is_highlighted)
            output_lines.extend(block_lines)
            output_lines.append("")  # Space between blocks

            last_session = block.session_id

        if not output_lines or all(
            line in ("", "[dim]────────────────────────────────────────[/dim]")
            for line in output_lines
        ):
            output_lines.append("[dim]No events match filter...[/dim]")

        # Parsing errors section
        if self.parsing_errors:
            output_lines.append("[dim]────────────────────────────────────────[/dim]")
            output_lines.append("[bold red]⚠ ERRORS[/bold red]")
            for session_id, error in list(self.parsing_errors.items())[-3:]:
                short_id = session_id[:6]
                output_lines.append(f"  [red]{short_id}:[/red] {error}")

        # Insights section - show important events
        if self.insights:
            output_lines.append("[dim]────────────────────────────────────────[/dim]")
            output_lines.append("[bold yellow]💡 INSIGHTS[/bold yellow]")
            # Keep last 5 insights, display last 3
            self.insights = self.insights[-5:]
            for insight in self.insights[-3:]:
                output_lines.append(f"  {insight}")

        # Git actions at bottom
        if self.git_actions:
            output_lines.append("[dim]────────────────────────────────────────[/dim]")
            output_lines.append("[bold blue]📌 GIT[/bold blue]")
            for action in self.git_actions[-3:]:
                output_lines.append(f"  {action}")

        return "\n".join(output_lines)

    def _get_or_create_context(self, session_id: str) -> SessionContext:
        """Get or create SessionContext for tracking what agent knows."""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = SessionContext(session_id)
        return self.session_contexts[session_id]

    def get_context_for_session(self, session_id: str) -> Optional[SessionContext]:
        """Get context for a specific session."""
        return self.session_contexts.get(session_id)

    def get_active_context(self) -> Optional[SessionContext]:
        """Get context for most recent active session."""
        if self.activity_blocks:
            last_session = self.activity_blocks[-1].session_id
            return self.session_contexts.get(last_session)
        return None

    def get_drift_state(self, session_id: str) -> Optional[dict]:
        """Get drift state for a session."""
        return self.session_drift_states.get(session_id)

    def _check_for_user_intent(self, line: str, session_id: str, project_path: str):
        """Check if line contains a user message and set intent for drift detection."""
        if not self.drift_detector:
            return

        try:
            import json

            data = json.loads(line)

            # Claude transcript format: {"type": "user", "message": {"content": [...]}}
            if data.get("type") == "user":
                message = data.get("message", {})
                content = message.get("content", [])
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        prompt = block.get("text", "").strip()
                        if prompt and len(prompt) > 5:
                            intent_text = f"{prompt} (working in {project_path})"
                            self.drift_detector.set_intent(session_id, intent_text)
                            logger.debug(f"TUI: Set intent for {session_id[:8]}: {prompt[:50]}...")
                            return

            # Codex format: {"role": "user", "content": "..."}
            if data.get("role") == "user" and data.get("content"):
                prompt = data.get("content", "").strip()
                if prompt and len(prompt) > 5:
                    intent_text = f"{prompt} (working in {project_path})"
                    self.drift_detector.set_intent(session_id, intent_text)
                    logger.debug(f"TUI: Set intent for {session_id[:8]}: {prompt[:50]}...")

        except (json.JSONDecodeError, TypeError, AttributeError):
            pass

    def _check_drift_on_tool(self, session_id: str, tool_name: str, tool_input: dict) -> None:
        """Check if a tool action causes drift from intent."""
        if not self.drift_detector:
            return

        # Extract file path if present
        file_path = tool_input.get("file_path") or tool_input.get("path")

        # Check for drift
        drift_result = self.drift_detector.check_action(
            session_id=session_id, tool_name=tool_name, file_path=file_path, tool_input=tool_input
        )

        # Store drift state
        if drift_result.is_drifting or drift_result.drift_score > 0.3:
            self.session_drift_states[session_id] = {
                "is_drifting": drift_result.is_drifting,
                "drift_score": drift_result.drift_score,
                "signals": [
                    {"type": s.signal_type, "description": s.description, "severity": s.severity}
                    for s in drift_result.signals[-3:]
                ],
            }
            if drift_result.is_drifting:
                short_id = session_id[:6]
                self.insights.append(
                    f"[magenta]⚠ {short_id}: DRIFT[/magenta] {drift_result.signals[-1].description[:40] if drift_result.signals else ''}"
                )

    def _process_event_to_block(self, event, session_id: str, project_path: str):
        """Process an event into an ActivityBlock with visual hierarchy."""
        time_str = event.timestamp.strftime("%H:%M:%S")
        short_id = session_id[:6]
        block = self._get_or_create_block(session_id, time_str)
        ctx = self._get_or_create_context(session_id)

        if isinstance(event, ThinkingEvent):
            # Add to thinking summary
            block.add_thinking(event.content)

            # Extract decisions from thinking
            decision_markers = ["i'll ", "i decided", "let me ", "i should", "going to"]
            for marker in decision_markers:
                if marker in event.content.lower():
                    # Extract the decision sentence
                    for sentence in event.content.split("."):
                        if marker in sentence.lower():
                            ctx.add_decision(sentence.strip())
                            break
                    break

            # Check for git
            if "git " in event.content.lower():
                self._extract_git_action(event.content, short_id)

        elif isinstance(event, TaskEvent):
            # Agent spawn - show in tree with FULL context
            depth = self.agent_depth.get(session_id, 0)
            block.add_agent_spawn(event.subagent_type, event.description, depth)
            # Track full agent spawn with prompt for context panel
            ctx.add_agent_spawn(
                event.subagent_type,
                event.description,
                event.prompt,  # Full prompt - "glass into the matrix"
                event.model,
            )
            # Increase depth for nested agents
            self.agent_depth[session_id] = depth + 1

        elif isinstance(event, ToolEvent):
            sid_badge = f"[black on cyan] {short_id} [/black on cyan]"
            risk_bg = self._get_risk_bg(event.risk_level)
            icon = self._get_tool_icon(event.name)

            # Track tool usage
            ctx.add_tool_use(event.name)

            # Check for drift from user intent
            self._check_drift_on_tool(session_id, event.name, event.input)

            # Format based on tool type
            if event.name == "Read":
                path = event.input.get("file_path", "")
                ctx.add_file_read(path)  # Track file read
                path_short = path.split("/")[-1][:25]
                text = f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] {event.name:5} [/{risk_bg}] {icon} {path_short}"
            elif event.name in ("Edit", "Write"):
                path = event.input.get("file_path", "")
                ctx.add_file_modified(path)  # Track file modified
                path_short = path.split("/")[-1][:25]
                text = f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] {event.name:5} [/{risk_bg}] {icon} {path_short}"
            elif event.name == "Bash":
                cmd = event.input.get("command", "")[:35]
                text = (
                    f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] BASH  [/{risk_bg}] {icon} {cmd}"
                )
                if cmd.strip().startswith("git "):
                    self._extract_git_action(cmd, short_id)
            elif event.name in ("Glob", "Grep"):
                pattern = event.input.get("pattern", "")[:25]
                text = f"[dim]{time_str}[/dim] {sid_badge} [black on green] {event.name:5} [/black on green] {icon} {pattern}"
            elif event.name == "Task":
                desc = event.input.get("description", "")[:30]
                text = f"[dim]{time_str}[/dim] {sid_badge} [black on yellow] AGENT [/black on yellow] 🤖 {desc}"
            else:
                text = f"[dim]{time_str}[/dim] {sid_badge} [black on blue] {event.name[:5]:5} [/black on blue] {icon}"

            record = EventRecord(
                text=text,
                session_id=session_id,
                tool_name=event.name,
                risk_level=event.risk_level,
                project_path=project_path,
                timestamp=time_str,
                content=str(event.input),
            )
            block.add_action(record)

    def _get_risk_bg(self, risk_level: str) -> str:
        return {
            "safe": "black on green",
            "medium": "black on yellow",
            "high": "white on red",
            "critical": "white on red",
        }.get(risk_level, "black on blue")

    def _get_tool_icon(self, tool_name: str) -> str:
        return {
            "Read": "📖",
            "Write": "✏️",
            "Edit": "🔧",
            "Bash": "💻",
            "Glob": "🔍",
            "Grep": "🔎",
            "Task": "🤖",
        }.get(tool_name, "⚡")

    def _strip_markup(self, text: str) -> str:
        """Strip rich markup for dimmed display."""
        import re

        return re.sub(r"\[/?[^\]]+\]", "", text)

    def render_selected_mode(self, session: SessionInfo) -> str:
        """Render rich watch format for selected session."""
        lines = []
        short_id = session.session_id[:8]

        # Session header
        lines.append(f"[bold cyan]Session:[/bold cyan] {session.session_id[:16]}...")
        lines.append(f"[bold cyan]Project:[/bold cyan] {session.project_path}")
        lines.append(f"[bold cyan]Size:[/bold cyan] {session.size // 1024}KB")
        lines.append("")
        lines.append("[bold green]─── Events ───[/bold green]")
        lines.append("")

        # Read and render events with rich formatting - use full history
        last_pos = self.session_positions.get(session.session_id, 0)

        try:
            current_size = session.file_path.stat().st_size
            if current_size > last_pos:
                # Get session source for multi-source parsing
                source = getattr(session, "source", "claude") or "claude"

                # Gemini uses single JSON blob format, not JSONL
                if source == "gemini" and parse_gemini_file is not None:
                    # Parse entire file to get all events
                    event_dicts = parse_gemini_file(session.file_path)

                    # Track how many events we've already shown
                    last_event_count = self.gemini_event_counts.get(session.session_id, 0)

                    # Only process new events
                    for event_dict in event_dicts[last_event_count:]:
                        event = parse_gemini_event(event_dict)
                        if event:
                            formatted = self._format_rich_event(event, short_id)
                            if formatted:
                                self.events.extend(formatted)

                    # Update the count of displayed events
                    self.gemini_event_counts[session.session_id] = len(event_dicts)

                    # Mark file as fully read
                    self.session_positions[session.session_id] = current_size
                else:
                    # Claude/Codex use JSONL format (one JSON object per line)
                    with open(session.file_path, "r") as f:
                        f.seek(last_pos)
                        new_content = f.read()
                        self.session_positions[session.session_id] = f.tell()

                    for line in new_content.strip().split("\n"):
                        if line.strip():
                            events = parse_line_by_source(line, source)
                            for event in events:
                                formatted = self._format_rich_event(event, short_id)
                                if formatted:
                                    self.events.extend(formatted)
        except OSError as e:
            logger.debug(f"Error reading session file {session.file_path}: {e}")
        except Exception as e:
            logger.warning(f"Unexpected error rendering selected session: {e}")

        # Trim to last 20 events
        self.events = self.events[-20:]

        if self.events:
            lines.extend(self.events)
        else:
            lines.append("[dim]No recent activity...[/dim]")

        # Add git actions for this session
        if self.git_actions:
            lines.append("")
            lines.append("[bold blue]─── GIT ACTIONS ───[/bold blue]")
            for action in self.git_actions[-5:]:
                lines.append(action)

        return "\n".join(lines)

    def _format_compact_event(
        self, event, short_id: str, session_id: str, project_path: str
    ) -> list[EventRecord]:
        """Format event in compact mode with colored boxes, returning EventRecords."""
        records = []
        time_str = event.timestamp.strftime("%H:%M:%S")
        sid_badge = f"[black on cyan] {short_id} [/black on cyan]"

        if isinstance(event, ThinkingEvent):
            text = event.content[:100] + "..." if len(event.content) > 100 else event.content
            text = text.replace("\n", " ")
            line = f"[dim]{time_str}[/dim] {sid_badge} [white on magenta] THINK [/white on magenta] {text}"
            records.append(
                EventRecord(
                    text=line,
                    session_id=session_id,
                    tool_name="Think",
                    project_path=project_path,
                    timestamp=time_str,
                )
            )

            # Check for decisions
            if any(
                d in event.content.lower() for d in ["i'll ", "i decided", "let me", "i should"]
            ):
                decision_text = event.content[:80].replace("\n", " ")
                dec_line = f"           {sid_badge} [black on yellow] DECIDE [/black on yellow] {decision_text}..."
                records.append(
                    EventRecord(
                        text=dec_line,
                        session_id=session_id,
                        tool_name="Decision",
                        project_path=project_path,
                        timestamp=time_str,
                    )
                )
                self.insights.append(f"[yellow]💡 {short_id}: decision[/yellow]")

            # Check for git mentions
            if "git " in event.content.lower():
                self._extract_git_action(event.content, short_id)

        elif isinstance(event, TaskEvent):
            agent_info = f"{event.subagent_type}: {event.description[:60]}"
            line = f"[dim]{time_str}[/dim] {sid_badge} [black on yellow] SPAWN [/black on yellow] 🤖 {agent_info}"
            records.append(
                EventRecord(
                    text=line,
                    session_id=session_id,
                    tool_name="Task",
                    project_path=project_path,
                    timestamp=time_str,
                )
            )
            if event.model:
                model_line = (
                    f"           {sid_badge}   ├─ [dim]model:[/dim] [cyan]{event.model}[/cyan]"
                )
                records.append(
                    EventRecord(
                        text=model_line,
                        session_id=session_id,
                        tool_name="Task",
                        project_path=project_path,
                        timestamp=time_str,
                    )
                )
            if event.prompt:
                prompt_preview = event.prompt[:100].replace("\n", " ")
                prompt_line = f"           {sid_badge}   └─ [dim]prompt:[/dim] {prompt_preview}..."
                records.append(
                    EventRecord(
                        text=prompt_line,
                        session_id=session_id,
                        tool_name="Task",
                        project_path=project_path,
                        timestamp=time_str,
                    )
                )
            self.insights.append(f"[yellow]🤖 {short_id}: {event.subagent_type}[/yellow]")

        elif isinstance(event, ToolEvent):
            records.extend(
                self._format_tool_compact(
                    event, time_str, sid_badge, short_id, session_id, project_path
                )
            )

        return records

    def _format_tool_compact(
        self,
        event: ToolEvent,
        time_str: str,
        sid_badge: str,
        short_id: str,
        session_id: str,
        project_path: str,
    ) -> list[EventRecord]:
        """Format a tool event in compact mode, returning EventRecords."""
        records = []
        risk_bg = {
            "safe": "black on green",
            "medium": "black on yellow",
            "high": "white on red",
            "critical": "white on red",
        }.get(event.risk_level, "black on blue")

        line = ""
        if event.name == "Edit":
            path = event.input.get("file_path", "").split("/")[-1][:25]
            line = f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] EDIT [/{risk_bg}] ✏️  {path}"
        elif event.name == "Write":
            path = event.input.get("file_path", "").split("/")[-1][:25]
            line = f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] WRITE [/{risk_bg}] 📝 {path}"
        elif event.name == "Read":
            path = event.input.get("file_path", "").split("/")[-1][:40]
            line = f"[dim]{time_str}[/dim] {sid_badge} [black on green] READ [/black on green] 📖 {path}"
        elif event.name == "Bash":
            cmd = event.input.get("command", "")[:60]
            line = f"[dim]{time_str}[/dim] {sid_badge} [{risk_bg}] BASH [/{risk_bg}] 💻 {cmd}"

            # Extract git actions from bash commands
            if cmd.strip().startswith("git "):
                self._extract_git_action(cmd, short_id)

            if event.risk_level in ("high", "critical"):
                self.insights.append(f"[red]⚠ {short_id}: {cmd[:40]}[/red]")
        elif event.name == "Task":
            desc = event.input.get("description", "")[:50]
            line = f"[dim]{time_str}[/dim] {sid_badge} [black on yellow] AGENT [/black on yellow] 🤖 {desc}"
        elif event.name == "Glob":
            pattern = event.input.get("pattern", "")[:40]
            line = f"[dim]{time_str}[/dim] {sid_badge} [black on green] GLOB [/black on green] 🔍 {pattern}"
        elif event.name == "Grep":
            pattern = event.input.get("pattern", "")[:40]
            line = f"[dim]{time_str}[/dim] {sid_badge} [black on green] GREP [/black on green] 🔎 {pattern}"
        else:
            line = f"[dim]{time_str}[/dim] {sid_badge} [black on blue] {event.name[:6]:6} [/black on blue] ⚡"

        if line:
            records.append(
                EventRecord(
                    text=line,
                    session_id=session_id,
                    tool_name=event.name,
                    risk_level=event.risk_level,
                    project_path=project_path,
                    timestamp=time_str,
                )
            )

        return records

    def _format_rich_event(self, event, short_id: str) -> list[str]:
        """Format event in rich watch mode with full details."""
        lines = []
        time_str = event.timestamp.strftime("%H:%M:%S")

        if isinstance(event, ThinkingEvent):
            content = event.content[:400] + "..." if len(event.content) > 400 else event.content
            lines.append(f"[bold magenta]💭 THINKING[/bold magenta] [dim]{time_str}[/dim]")
            lines.append(f"[italic]{content}[/italic]")
            lines.append("")

            # Check for git
            if "git " in event.content.lower():
                self._extract_git_action(event.content, short_id)

        elif isinstance(event, TaskEvent):
            lines.append(f"[bold yellow]🤖 SPAWNING AGENT[/bold yellow] [dim]{time_str}[/dim]")
            lines.append(f"  [cyan]{event.description}[/cyan]")
            lines.append(f"  [dim]Type:[/dim] {event.subagent_type}")
            if event.model:
                lines.append(f"  [dim]Model:[/dim] {event.model}")
            if event.prompt:
                prompt = event.prompt[:200] + "..." if len(event.prompt) > 200 else event.prompt
                lines.append(f"  [dim]Prompt:[/dim] {prompt}")
            lines.append("")

        elif isinstance(event, ToolEvent):
            lines.extend(self._format_tool_rich(event, time_str, short_id))

        return lines

    def _format_tool_rich(self, event: ToolEvent, time_str: str, short_id: str) -> list[str]:
        """Format a tool event in rich watch mode."""
        lines = []

        icon = {
            "Read": "📖",
            "Write": "✏️",
            "Edit": "🔧",
            "Bash": "💻",
            "Glob": "🔍",
            "Grep": "🔎",
            "Task": "🤖",
            "WebFetch": "🌐",
            "WebSearch": "🔍",
            "TodoWrite": "📝",
        }.get(event.name, "⚡")

        risk_color = {
            "safe": "green",
            "medium": "yellow",
            "high": "red",
            "critical": "bold red",
        }.get(event.risk_level, "blue")

        risk_indicator = ""
        if event.risk_level == "critical":
            risk_indicator = " [bold red]⚠ DESTRUCTIVE[/bold red]"
        elif event.risk_level == "high":
            risk_indicator = " [red]● HIGH RISK[/red]"

        lines.append(
            f"[bold {risk_color}]{icon} {event.name}[/bold {risk_color}]{risk_indicator} [dim]{time_str}[/dim]"
        )

        # Tool-specific details
        if event.name == "Read":
            lines.append(f"  {event.input.get('file_path', '')}")
        elif event.name == "Write":
            fp = event.input.get("file_path", "")
            lines.append(f"  [bold]{fp}[/bold]")
            lines.append("  [dim]Creating new file[/dim]")
        elif event.name == "Edit":
            fp = event.input.get("file_path", "")
            old_str = event.input.get("old_string", "")[:60]
            lines.append(f"  [bold]{fp}[/bold]")
            lines.append(f"  [dim]replacing:[/dim] {old_str}...")
        elif event.name == "Bash":
            cmd = event.input.get("command", "")
            desc = event.input.get("description", "")
            if desc:
                lines.append(f"  [dim]{desc}[/dim]")
            lines.append(f"  {cmd[:100]}")

            # Extract git action
            if cmd.strip().startswith("git "):
                self._extract_git_action(cmd, short_id)
        elif event.name == "Glob":
            pattern = event.input.get("pattern", "")
            path = event.input.get("path", "")
            lines.append(f"  {pattern}" + (f" in {path}" if path else ""))
        elif event.name == "Grep":
            pattern = event.input.get("pattern", "")
            path = event.input.get("path", "")
            lines.append(f"  /{pattern}/" + (f" in {path}" if path else ""))

        lines.append("")
        return lines

    def _extract_git_action(self, text: str, short_id: str):
        """Extract and format git actions from text."""
        # Pattern for git commands
        git_patterns = [
            (r"git\s+commit.*?-m\s+[\"']([^\"']+)[\"']", "commit"),
            (r"git\s+push", "push"),
            (r"git\s+pull", "pull"),
            (r"git\s+checkout\s+(\S+)", "checkout"),
            (r"git\s+branch\s+(\S+)", "branch"),
            (r"git\s+merge\s+(\S+)", "merge"),
            (r"git\s+rebase", "rebase"),
            (r"git\s+stash", "stash"),
            (r"git\s+reset", "reset"),
            (r"git\s+add\s+(\S+)", "add"),
        ]

        for pattern, action_type in git_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if action_type == "commit":
                    msg = match.group(1)[:40]
                    self.git_actions.append(f'[green]📌 {short_id}:[/green] commit "{msg}"')
                elif action_type in ("checkout", "branch", "merge"):
                    ref = match.group(1) if match.lastindex else ""
                    self.git_actions.append(f"[blue]🔀 {short_id}:[/blue] {action_type} {ref}")
                elif action_type == "push":
                    self.git_actions.append(f"[cyan]⬆ {short_id}:[/cyan] push")
                elif action_type == "pull":
                    self.git_actions.append(f"[cyan]⬇ {short_id}:[/cyan] pull")
                elif action_type == "reset":
                    self.git_actions.append(f"[red]⚠ {short_id}:[/red] reset")
                elif action_type == "add":
                    path = match.group(1) if match.lastindex else ""
                    self.git_actions.append(f"[dim]+ {short_id}:[/dim] add {path[:20]}")
                break

        # Trim git actions
        self.git_actions = self.git_actions[-10:]


class FilterInput(Input):
    """Input widget for filtering events."""

    def __init__(self, **kwargs):
        super().__init__(placeholder="Filter: project, tool, risk...", **kwargs)


def _reset_terminal():
    """Reset terminal state - disable all mouse tracking modes."""
    import sys

    # Disable ALL mouse tracking modes
    sys.stdout.write("\x1b[?1000l")  # Disable basic mouse tracking
    sys.stdout.write("\x1b[?1002l")  # Disable cell motion tracking
    sys.stdout.write("\x1b[?1003l")  # Disable all motion tracking
    sys.stdout.write("\x1b[?1006l")  # Disable SGR extended mouse mode
    sys.stdout.write("\x1b[?1015l")  # Disable urxvt extended mouse mode
    sys.stdout.write("\x1b[?1005l")  # Disable UTF-8 mouse mode
    sys.stdout.flush()


class MCApp(App):
    """MC TUI - Interactive Command Center for AI Agents."""

    TITLE = "Motus Command"
    SUB_TITLE = "Command Center for AI Agents"

    # Disable mouse support entirely to prevent escape sequence leakage
    ENABLE_COMMAND_PALETTE = False

    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 26;
        height: 100%;
        border: solid green;
    }

    #sidebar-title {
        text-align: center;
        background: $primary-darken-2;
        padding: 1;
    }

    #main {
        width: 1fr;
        height: 100%;
        border: solid blue;
    }

    #context-sidebar {
        width: 32;
        height: 100%;
        border: solid magenta;
    }

    #context-sidebar.hidden {
        display: none;
    }

    #context-title {
        text-align: center;
        background: $primary-darken-2;
        padding: 1;
    }

    #feed-title {
        text-align: center;
        background: $primary-darken-2;
        padding: 1;
    }

    #filter-bar {
        height: 3;
        padding: 0 1;
        display: none;
    }

    #filter-bar.visible {
        display: block;
    }

    #filter-input {
        width: 100%;
    }

    FeedPanel {
        height: 100%;
        padding: 1;
    }

    ContextPanel {
        height: 100%;
        padding: 1;
    }

    SessionsList {
        height: 100%;
    }

    SessionItem {
        padding: 0 1;
    }

    SessionItem:hover {
        background: $primary-darken-1;
    }

    SessionItem.-active {
        background: $primary;
    }

    ListView > ListItem.--highlight {
        background: $accent;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("a", "select_all", "All"),
        Binding("j", "cursor_down", "Down"),
        Binding("k", "cursor_up", "Up"),
        Binding("/", "open_filter", "Filter"),
        Binding("c", "toggle_context", "Context"),
        Binding("escape", "close_filter", "Close", show=False),
    ]

    selected_session: reactive[Optional[str]] = reactive(None)
    filter_visible: reactive[bool] = reactive(False)
    context_visible: reactive[bool] = reactive(True)

    def __init__(self):
        super().__init__()
        self.sessions: list[SessionInfo] = []
        self.sdk_traces: list[dict] = []

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("[bold green]🔮 Sessions[/bold green]", id="sidebar-title")
                yield SessionsList(id="sessions-list")

            with Vertical(id="main"):
                yield Static("[bold blue]📡 Live Feed[/bold blue]", id="feed-title")
                with Horizontal(id="filter-bar"):
                    yield FilterInput(id="filter-input")
                yield FeedPanel(id="feed-panel")

            with Vertical(id="context-sidebar"):
                yield Static("[bold magenta]🧠 Context[/bold magenta]", id="context-title")
                yield ContextPanel(id="context-panel")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize on mount."""
        self.refresh_sessions()
        self.set_interval(1.0, self.update_feed)
        self.set_interval(5.0, self.refresh_sessions)

    def refresh_sessions(self) -> None:
        """Refresh the sessions list."""
        # Use orchestrator to discover all sessions
        unified_sessions = get_orchestrator().discover_all(max_age_hours=24)
        # Convert to SessionInfo for backwards compatibility with display logic
        self.sessions = [_unified_to_sessioninfo(s) for s in unified_sessions]
        self.sdk_traces = find_sdk_traces()

        sessions_list = self.query_one("#sessions-list", SessionsList)
        feed_panel = self.query_one("#feed-panel", FeedPanel)
        sessions_list.clear()

        # Add "ALL" option first
        sessions_list.append(SessionItem(is_all=True))

        # Filter to show active/open first, orphaned only if nothing else
        active_open = [s for s in self.sessions if s.status in ("active", "open", "crashed")]
        orphaned = [s for s in self.sessions if s.status == "orphaned"]

        # Show active/open sessions (up to 6) with drift status
        for session in active_open[:6]:
            drift_state = feed_panel.get_drift_state(session.session_id)
            is_drifting = drift_state.get("is_drifting", False) if drift_state else False
            sessions_list.append(SessionItem(session=session, is_drifting=is_drifting))

        # If we have room and there are orphaned sessions, show a couple
        remaining_slots = 8 - len(active_open[:6])
        if remaining_slots > 0 and orphaned:
            for session in orphaned[:remaining_slots]:
                drift_state = feed_panel.get_drift_state(session.session_id)
                is_drifting = drift_state.get("is_drifting", False) if drift_state else False
                sessions_list.append(SessionItem(session=session, is_drifting=is_drifting))

        # Add SDK traces
        if self.sdk_traces:
            for trace in self.sdk_traces[:3]:
                sessions_list.append(SessionItem(sdk_trace=trace))

        # Initialize session positions for feed - BACKFILL RECENT HISTORY on first load
        # Limit to last 50KB to avoid memory issues with huge session files
        max_backfill_bytes = 50000  # 50KB of recent history
        for s in self.sessions:
            if s.session_id not in feed_panel.session_positions:
                file_size = s.file_path.stat().st_size
                start_pos = max(0, file_size - max_backfill_bytes)
                feed_panel.session_positions[s.session_id] = start_pos

    def update_feed(self) -> None:
        """Update the feed panel with new events."""
        feed_panel = self.query_one("#feed-panel", FeedPanel)
        content_widget = feed_panel.query_one("#feed-content", Static)
        title_widget = self.query_one("#feed-title", Static)

        # Check for degraded mode
        degraded_badge = ""
        if get_orchestrator().is_process_degraded():
            degraded_badge = " [yellow]⚠ Limited status detection[/yellow]"

        if self.selected_session is None:
            # ALL mode: show all sessions with session ID badges
            title_widget.update(
                f"[bold blue]📡 Live Feed[/bold blue] [dim](all sessions)[/dim]{degraded_badge}"
            )
            content = feed_panel.render_all_mode(self.sessions, None)
        else:
            # SINGLE SESSION mode: richer detail, no session badges
            session = None
            for s in self.sessions:
                if s.session_id == self.selected_session:
                    session = s
                    break
            if session:
                # Extract just the folder name for cleaner display
                project_name = (
                    session.project_path.split("/")[-1]
                    if "/" in session.project_path
                    else session.project_path
                )
                title_widget.update(
                    f"[bold blue]📡 {project_name}[/bold blue] [dim](single session)[/dim]{degraded_badge}"
                )
                content = feed_panel.render_selected_mode(session)
            else:
                title_widget.update(f"[bold blue]📡 Live Feed[/bold blue]{degraded_badge}")
                content = feed_panel.render_all_mode(self.sessions, None)

        content_widget.update(content)

        # Update the context panel with session memory
        self.update_context_panel()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle session selection - switches between all/single session mode."""
        item = event.item
        if isinstance(item, SessionItem):
            if item.is_all:
                self.selected_session = None
            elif item.session:
                self.selected_session = item.session.session_id
                # Reset position to 0 to load FULL history for selected session
                feed_panel = self.query_one("#feed-panel", FeedPanel)
                feed_panel.session_positions[item.session.session_id] = 0
                # Clear activity blocks to rebuild from full history
                feed_panel.activity_blocks.clear()

            # Immediately update BOTH panels to reflect the selection
            self.update_feed()  # Switches rendering mode
            self.update_context_panel()  # Shows selected session's context

    def action_select_all(self) -> None:
        """Select ALL mode - shows all events without highlight filter."""
        self.selected_session = None
        # Don't clear - keep all history visible

    def action_refresh(self) -> None:
        """Manual refresh."""
        self.refresh_sessions()

    def action_open_filter(self) -> None:
        """Open the filter input bar."""
        filter_bar = self.query_one("#filter-bar")
        filter_bar.add_class("visible")
        filter_input = self.query_one("#filter-input", FilterInput)
        filter_input.focus()

    def action_close_filter(self) -> None:
        """Close filter and clear filter text."""
        filter_bar = self.query_one("#filter-bar")
        filter_bar.remove_class("visible")
        filter_input = self.query_one("#filter-input", FilterInput)
        filter_input.value = ""
        # Clear the filter on the feed panel
        feed_panel = self.query_one("#feed-panel", FeedPanel)
        feed_panel.filter_text = ""

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle filter input changes."""
        if event.input.id == "filter-input":
            feed_panel = self.query_one("#feed-panel", FeedPanel)
            feed_panel.filter_text = event.value

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter in filter - just keep filter active but unfocus."""
        if event.input.id == "filter-input":
            # Keep filter active but return focus to main view
            self.query_one("#sessions-list", SessionsList).focus()

    def action_toggle_context(self) -> None:
        """Toggle the context panel visibility."""
        self.context_visible = not self.context_visible
        context_sidebar = self.query_one("#context-sidebar")
        if self.context_visible:
            context_sidebar.remove_class("hidden")
        else:
            context_sidebar.add_class("hidden")

    def update_context_panel(self) -> None:
        """Update the context panel with current session context."""
        context_panel = self.query_one("#context-panel", ContextPanel)
        content_widget = context_panel.query_one("#context-content", Static)
        feed_panel = self.query_one("#feed-panel", FeedPanel)

        # Get context for selected session or most recent active
        ctx = None
        session_id = None
        if self.selected_session:
            ctx = feed_panel.get_context_for_session(self.selected_session)
            session_id = self.selected_session
        else:
            ctx = feed_panel.get_active_context()
            if feed_panel.activity_blocks:
                session_id = feed_panel.activity_blocks[-1].session_id

        # Build content with drift info at top
        content_lines = []

        # Show drift status if drifting
        if session_id:
            drift_state = feed_panel.get_drift_state(session_id)
            if drift_state and drift_state.get("is_drifting"):
                content_lines.append("[bold magenta]⚠ DRIFT DETECTED[/bold magenta]")
                score = drift_state.get("drift_score", 0)
                content_lines.append(f"[magenta]Score: {score:.0%}[/magenta]")
                for signal in drift_state.get("signals", [])[-2:]:
                    desc = signal.get("description", "")[:40]
                    content_lines.append(f"  [dim]•[/dim] {desc}")
                content_lines.append("")

        if ctx:
            content_lines.append(ctx.render())
            content_widget.update("\n".join(content_lines))
        else:
            content_widget.update(
                "[dim]No context yet...\nSelect a session or wait for activity.[/dim]"
            )


def main():
    """Run the MC TUI."""
    import atexit
    import signal

    # Register cleanup for all exit paths
    atexit.register(_reset_terminal)

    # Handle signals that might leave terminal in bad state
    def signal_handler(signum, frame):
        _reset_terminal()
        sys.exit(128 + signum)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    app = MCApp()
    try:
        app.run()
    finally:
        _reset_terminal()


if __name__ == "__main__":
    main()
