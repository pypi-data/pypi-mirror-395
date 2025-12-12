"""History command for Motus Command."""

from rich import box
from rich.console import Console
from rich.table import Table

console = Console()


def history_command(max_sessions: int = 10, max_events: int = 50) -> None:
    """Display command history for recent sessions.

    Shows a summary of recent tool calls and actions across sessions.

    Args:
        max_sessions: Maximum number of sessions to include (default 10).
        max_events: Maximum events to show per session (default 50).
    """
    try:
        from ..orchestrator import get_orchestrator
        from ..protocols import EventType
    except ImportError:
        console.print("[red]Error: Could not import orchestrator.[/red]")
        return

    orchestrator = get_orchestrator()
    sessions = orchestrator.discover_all(max_age_hours=48)

    if not sessions:
        console.print("[yellow]No recent sessions found.[/yellow]")
        console.print("[dim]Sessions from the last 48 hours will appear here.[/dim]")
        return

    # Collect recent events across sessions
    all_events = []

    for session in sessions[:max_sessions]:
        try:
            events = orchestrator.get_events(session)
            for event in events[-max_events:]:
                all_events.append((session, event))
        except Exception:
            continue

    if not all_events:
        console.print("[yellow]No recent history found.[/yellow]")
        console.print(
            "[dim]Tool calls and actions will appear here once sessions have activity.[/dim]"
        )
        return

    # Sort by timestamp (newest first)
    all_events.sort(key=lambda x: x[1].timestamp, reverse=True)

    # Create table
    table = Table(
        title="Recent History",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Time", style="dim", width=8)
    table.add_column("Session", style="blue", width=10)
    table.add_column("Source", style="magenta", width=8)
    table.add_column("Type", style="green", width=12)
    table.add_column("Details", style="white", no_wrap=False)

    # Display up to 30 most recent events
    for session, event in all_events[:30]:
        time_str = event.timestamp.strftime("%H:%M:%S")
        session_short = session.session_id[:8]
        source = session.source.value.upper()

        # Format event type and details
        event_type = (
            event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type)
        )

        details = ""
        if event.event_type == EventType.TOOL:
            tool_name = event.tool_name or "?"
            if event.tool_input:
                # Extract key info from tool input
                if "file_path" in event.tool_input:
                    details = f"{tool_name}: {event.tool_input['file_path']}"
                elif "command" in event.tool_input:
                    cmd = event.tool_input["command"][:60]
                    details = f"{tool_name}: {cmd}..."
                elif "pattern" in event.tool_input:
                    details = f"{tool_name}: {event.tool_input['pattern']}"
                elif "query" in event.tool_input:
                    details = f"{tool_name}: {event.tool_input['query']}"
                else:
                    details = tool_name
            else:
                details = tool_name
        elif event.event_type == EventType.THINKING:
            content = event.content[:80] if event.content else ""
            details = f"{content}..." if len(event.content or "") > 80 else content
        elif event.event_type == EventType.AGENT_SPAWN:
            agent_type = event.agent_type or "unknown"
            model = event.agent_model or event.model or "?"
            details = f"{agent_type} ({model})"
        elif event.event_type == EventType.DECISION:
            details = event.content[:80] if event.content else ""
        elif event.event_type == EventType.ERROR:
            details = f"[red]{event.content[:60]}[/red]" if event.content else "[red]Error[/red]"
        else:
            details = event.content[:60] if event.content else ""

        # Color-code by event type
        type_style = {
            "tool": "green",
            "thinking": "magenta",
            "agent_spawn": "yellow",
            "decision": "cyan",
            "error": "red",
            "response": "blue",
        }.get(event_type.lower(), "white")

        table.add_row(
            time_str,
            session_short,
            source,
            f"[{type_style}]{event_type}[/{type_style}]",
            details,
        )

    console.print(table)

    # Summary
    console.print()
    console.print(
        f"[dim]Showing {min(30, len(all_events))} of {len(all_events)} events from {len(sessions)} sessions[/dim]"
    )
    console.print("[dim]Use 'mc watch <session_id>' to follow a specific session[/dim]")
