"""List sessions command."""

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table

from .models import SessionInfo
from .utils import format_age

console = Console()

# Claude projects directory
CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"


def find_sessions(max_age_hours: int = 2) -> list[SessionInfo]:
    """
    Find recent sessions from all sources (Claude, Codex, Gemini, SDK).

    Uses SessionManager to discover and return sessions from all supported sources.
    All sources are treated equally - no primary/secondary distinction.
    """
    from motus_command.session_manager import SessionManager

    sm = SessionManager()
    return sm.find_sessions(max_age_hours=max_age_hours)


# Backward compatibility alias
find_claude_sessions = find_sessions


def find_active_session() -> Optional[SessionInfo]:
    """Find the most recently active session from any source."""
    sessions = find_sessions(max_age_hours=1)
    active = [s for s in sessions if s.is_active]
    return active[0] if active else (sessions[0] if sessions else None)


def list_sessions(max_age_hours: int = 24, show_all: bool = False):
    """List recent sessions from all sources (Claude, Codex, SDK)."""
    # Use SessionManager to get sessions from all sources
    from ..session_manager import SessionManager

    sm = SessionManager()
    sessions = sm.find_sessions(max_age_hours=max_age_hours)

    if not sessions:
        console.print("[dim]No recent sessions found.[/dim]")
        console.print(f"[dim]Looking in: {PROJECTS_DIR}[/dim]")
        return

    table = Table(title=f"Recent Sessions (last {max_age_hours}h)")
    table.add_column("Status", style="cyan", width=8)
    table.add_column("Source", width=8)
    table.add_column("Project", style="green")
    table.add_column("Session ID", style="dim")
    table.add_column("Age", justify="right")
    table.add_column("Size", justify="right")
    table.add_column("Last Action", style="yellow")

    # Source badge colors
    source_badges = {
        "claude": "[bold magenta]Claude[/bold magenta]",
        "codex": "[bold green]Codex[/bold green]",
        "gemini": "[bold blue]Gemini[/bold blue]",
        "sdk": "[bold yellow]SDK[/bold yellow]",
    }

    for session in sessions:
        status_icon = "🟢" if session.is_active else "⚪"
        status = f"{status_icon} {session.status}"

        # Get source badge with fallback
        source = getattr(session, "source", "claude") or "claude"
        source_badge = source_badges.get(source, f"[dim]{source}[/dim]")

        project_name = session.project_path.split("/")[-1] if session.project_path else "unknown"

        size_kb = session.size / 1024
        size_str = f"{size_kb:.1f}KB" if size_kb < 1000 else f"{size_kb/1024:.1f}MB"

        table.add_row(
            status,
            source_badge,
            project_name,
            session.session_id[:12],
            format_age(session.last_modified),
            size_str,
            session.last_action or "-",
        )

    console.print(table)

    # Show hint for active sessions
    active = [s for s in sessions if s.is_active]
    if active:
        console.print()
        console.print(
            "[green]💡 Tip:[/green] Run [bold]mc watch[/bold] to monitor the active session"
        )
