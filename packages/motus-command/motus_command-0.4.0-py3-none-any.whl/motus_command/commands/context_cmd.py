"""Context display command."""

from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .list_cmd import find_active_session, find_claude_sessions
from .summary_cmd import generate_agent_context

console = Console()


def context_command(session_id: Optional[str] = None):
    """Display context for a session (for AI agent consumption)."""
    if session_id:
        sessions = find_claude_sessions(max_age_hours=168)
        session = next((s for s in sessions if s.session_id.startswith(session_id)), None)
        if not session:
            console.print(f"[red]Session not found: {session_id}[/red]")
            return
    else:
        session = find_active_session()
        if not session:
            console.print("[yellow]No recent sessions found.[/yellow]")
            return

    context = generate_agent_context(session)

    # Output raw markdown for piping to agents
    console.print(Panel(Markdown(context), title="Session Context", border_style="green"))
