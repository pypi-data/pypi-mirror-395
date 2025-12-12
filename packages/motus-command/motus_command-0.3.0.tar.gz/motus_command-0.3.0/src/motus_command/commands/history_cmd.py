"""History command for Motus Command v0.3.0."""

from rich.console import Console

console = Console()


def history_command() -> None:
    """Display command history for recent sessions.

    Shows a summary of recent commands executed across sessions.
    """
    console.print("[yellow]History command not yet implemented.[/yellow]")
    console.print("[dim]This will show recent command history across sessions.[/dim]")
