"""
MC Safety Features: Checkpoint, Rollback, Dry Run, Test Detection, Memory.

These features make AI agents safer and more effective.
"""

import glob
import json
import os
import shlex
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# MC state directory
MC_DIR = Path.home() / ".mc"
MC_DIR.mkdir(exist_ok=True)


# =============================================================================
# CHECKPOINT / ROLLBACK
# =============================================================================


@dataclass
class Checkpoint:
    """A saved state checkpoint."""

    id: str
    message: str
    timestamp: str
    stash_ref: Optional[str] = None
    files_snapshot: list[str] = field(default_factory=list)


def get_checkpoints_file(project_dir: Optional[Path] = None) -> Path:
    """Get the checkpoints file for a project."""
    if project_dir is None:
        project_dir = Path.cwd()

    mc_project_dir = project_dir / ".mc"
    mc_project_dir.mkdir(exist_ok=True)
    return mc_project_dir / "checkpoints.json"


def load_checkpoints(project_dir: Optional[Path] = None) -> list[Checkpoint]:
    """Load checkpoints for a project."""
    cp_file = get_checkpoints_file(project_dir)
    if not cp_file.exists():
        return []

    try:
        data = json.loads(cp_file.read_text())
        return [Checkpoint(**cp) for cp in data]
    except (json.JSONDecodeError, TypeError):
        return []


def save_checkpoints(checkpoints: list[Checkpoint], project_dir: Optional[Path] = None):
    """Save checkpoints for a project."""
    cp_file = get_checkpoints_file(project_dir)
    data = [asdict(cp) for cp in checkpoints]
    cp_file.write_text(json.dumps(data, indent=2))


def checkpoint_command(message: str = "checkpoint"):
    """Create a checkpoint of the current state.

    Uses git stash to save uncommitted changes.
    """
    # Check if we're in a git repo
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print("[red]Error: Not in a git repository[/red]")
        return False

    # Get list of modified files
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    modified_files = [line[3:] for line in result.stdout.strip().split("\n") if line.strip()]

    if not modified_files:
        console.print("[yellow]No changes to checkpoint[/yellow]")
        return False

    # Create timestamp-based ID
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    cp_id = f"mc-{timestamp}"

    # Create git stash with message
    stash_message = f"mc-checkpoint: {message}"
    result = subprocess.run(
        ["git", "stash", "push", "-m", stash_message, "--include-untracked"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        console.print(f"[red]Failed to create checkpoint: {result.stderr}[/red]")
        return False

    # Get the stash reference
    result = subprocess.run(
        ["git", "stash", "list", "--format=%gd %s"],
        capture_output=True,
        text=True,
    )
    stash_ref = None
    for line in result.stdout.strip().split("\n"):
        if stash_message in line:
            stash_ref = line.split()[0]
            break

    # Save checkpoint metadata
    checkpoint = Checkpoint(
        id=cp_id,
        message=message,
        timestamp=datetime.now().isoformat(),
        stash_ref=stash_ref,
        files_snapshot=modified_files,
    )

    checkpoints = load_checkpoints()
    checkpoints.insert(0, checkpoint)  # Most recent first
    save_checkpoints(checkpoints)

    console.print(
        Panel(
            f"[green]Checkpoint created: {cp_id}[/green]\n"
            f"[dim]Message: {message}[/dim]\n"
            f"[dim]Files: {len(modified_files)}[/dim]",
            title="[bold green]✓ Checkpoint[/bold green]",
            border_style="green",
        )
    )

    # Immediately restore working state (stash pop)
    subprocess.run(["git", "stash", "pop", "--quiet"], capture_output=True)

    console.print("[dim]Working state preserved. Use 'mc rollback' to restore.[/dim]")
    return True


def list_checkpoints_command():
    """List available checkpoints."""
    checkpoints = load_checkpoints()

    if not checkpoints:
        console.print("[yellow]No checkpoints found[/yellow]")
        console.print("[dim]Create one with: mc checkpoint 'before refactor'[/dim]")
        return

    table = Table(title="Checkpoints")
    table.add_column("ID", style="cyan")
    table.add_column("Message", style="white")
    table.add_column("Files", justify="right")
    table.add_column("Age", style="dim")

    for cp in checkpoints[:10]:  # Show last 10
        try:
            dt = datetime.fromisoformat(cp.timestamp)
            age = datetime.now() - dt
            if age.total_seconds() < 3600:
                age_str = f"{int(age.total_seconds() / 60)}m"
            else:
                age_str = f"{int(age.total_seconds() / 3600)}h"
        except (ValueError, TypeError):
            age_str = "?"

        table.add_row(
            cp.id,
            cp.message[:40],
            str(len(cp.files_snapshot)),
            age_str,
        )

    console.print(table)
    console.print("\n[dim]Rollback with: mc rollback <id>[/dim]")


def rollback_command(checkpoint_id: Optional[str] = None):
    """Rollback to a checkpoint.

    If no ID provided, shows diff against most recent checkpoint.
    """
    checkpoints = load_checkpoints()

    if not checkpoints:
        console.print("[red]No checkpoints found[/red]")
        return False

    if checkpoint_id is None:
        # Show diff against most recent
        cp = checkpoints[0]
        console.print(f"[yellow]Most recent checkpoint: {cp.id}[/yellow]")
        console.print(f"[dim]Message: {cp.message}[/dim]")
        console.print(f"[dim]Files: {', '.join(cp.files_snapshot[:5])}...[/dim]")
        console.print("\n[dim]To rollback, run: mc rollback {cp.id}[/dim]")
        return True

    # Find the checkpoint
    target = None
    for cp in checkpoints:
        if cp.id == checkpoint_id or checkpoint_id in cp.id:
            target = cp
            break

    if not target:
        console.print(f"[red]Checkpoint not found: {checkpoint_id}[/red]")
        return False

    # Stash current changes first (safety)
    subprocess.run(
        ["git", "stash", "push", "-m", "mc-rollback-safety", "--include-untracked"],
        capture_output=True,
    )

    # Find and apply the checkpoint stash
    if target.stash_ref:
        result = subprocess.run(
            ["git", "stash", "apply", target.stash_ref],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            console.print(f"[red]Failed to apply checkpoint: {result.stderr}[/red]")
            # Restore safety stash
            subprocess.run(["git", "stash", "pop", "--quiet"], capture_output=True)
            return False

    console.print(
        Panel(
            f"[green]Rolled back to: {target.id}[/green]\n"
            f"[dim]Your previous state is saved in git stash[/dim]",
            title="[bold green]✓ Rollback[/bold green]",
            border_style="green",
        )
    )
    return True


# =============================================================================
# DRY RUN
# =============================================================================


@dataclass
class DryRunResult:
    """Result of a dry-run simulation."""

    supported: bool
    command: str
    action: str = ""
    targets: list[str] = field(default_factory=list)
    size_bytes: int = 0
    reversible: bool = True
    message: str = ""
    risk: str = "unknown"


def dry_run_rm(args: list[str]) -> DryRunResult:
    """Simulate rm command."""
    files = []
    recursive = "-r" in args or "-rf" in args or "-fr" in args

    for arg in args:
        if arg.startswith("-"):
            continue

        path = Path(arg)
        if path.exists():
            if path.is_dir() and recursive:
                for f in path.rglob("*"):
                    if f.is_file():
                        files.append(str(f))
            elif path.is_file():
                files.append(str(path))
        else:
            # Try glob expansion
            for match in glob.glob(arg, recursive=recursive):
                p = Path(match)
                if p.is_file():
                    files.append(match)
                elif p.is_dir() and recursive:
                    for f in p.rglob("*"):
                        if f.is_file():
                            files.append(str(f))

    total_size = sum(os.path.getsize(f) for f in files if os.path.exists(f))

    return DryRunResult(
        supported=True,
        command=f"rm {' '.join(args)}",
        action="DELETE",
        targets=files[:20],  # Limit display
        size_bytes=total_size,
        reversible=False,
        message=f"Would delete {len(files)} files ({total_size // 1024}KB)",
        risk="high" if len(files) > 10 or total_size > 10_000_000 else "medium",
    )


def dry_run_git_reset(args: list[str]) -> DryRunResult:
    """Simulate git reset command."""
    hard = "--hard" in args

    # Get list of files that would be affected
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True,
        text=True,
    )
    staged = result.stdout.strip().split("\n") if result.stdout.strip() else []

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
    )
    cached = result.stdout.strip().split("\n") if result.stdout.strip() else []

    affected = list(set(staged + cached))

    return DryRunResult(
        supported=True,
        command=f"git reset {' '.join(args)}",
        action="RESET",
        targets=affected,
        reversible=not hard,
        message=f"Would {'DISCARD' if hard else 'unstage'} changes to {len(affected)} files",
        risk="high" if hard else "medium",
    )


def dry_run_git_clean(args: list[str]) -> DryRunResult:
    """Simulate git clean command."""
    # Use git's built-in dry run
    result = subprocess.run(
        ["git", "clean", "-n"] + [a for a in args if a not in ["-f", "-d", "-fd"]],
        capture_output=True,
        text=True,
    )

    files = []
    for line in result.stdout.strip().split("\n"):
        if line.startswith("Would remove "):
            files.append(line.replace("Would remove ", ""))

    return DryRunResult(
        supported=True,
        command=f"git clean {' '.join(args)}",
        action="DELETE",
        targets=files,
        reversible=False,
        message=f"Would remove {len(files)} untracked files",
        risk="high" if len(files) > 5 else "medium",
    )


def dry_run_mv(args: list[str]) -> DryRunResult:
    """Simulate mv command."""
    # Simple case: mv src dst
    non_flag_args = [a for a in args if not a.startswith("-")]

    if len(non_flag_args) < 2:
        return DryRunResult(
            supported=False,
            command=f"mv {' '.join(args)}",
            message="Cannot parse mv arguments",
        )

    src, dst = non_flag_args[-2], non_flag_args[-1]

    return DryRunResult(
        supported=True,
        command=f"mv {' '.join(args)}",
        action="MOVE",
        targets=[f"{src} → {dst}"],
        reversible=True,
        message=f"Would move {src} to {dst}",
        risk="low",
    )


def dry_run_command(command: str):
    """Simulate a command and show what would happen.

    Supports: rm, git reset, git clean, mv
    """
    try:
        parts = shlex.split(command)
    except ValueError:
        parts = command.split()

    if not parts:
        console.print("[red]Empty command[/red]")
        return

    base_cmd = parts[0]
    args = parts[1:]

    result: DryRunResult

    if base_cmd == "rm":
        result = dry_run_rm(args)
    elif base_cmd == "git" and args and args[0] == "reset":
        result = dry_run_git_reset(args[1:])
    elif base_cmd == "git" and args and args[0] == "clean":
        result = dry_run_git_clean(args[1:])
    elif base_cmd == "mv":
        result = dry_run_mv(args)
    else:
        result = DryRunResult(
            supported=False,
            command=command,
            message=f"Cannot simulate '{base_cmd}'. Proceed with caution.",
            risk="unknown",
        )

    # Display result
    if result.supported:
        risk_color = {
            "low": "green",
            "medium": "yellow",
            "high": "red",
        }.get(result.risk, "white")

        content = f"[bold]{result.action}[/bold]\n"
        content += f"[{risk_color}]Risk: {result.risk.upper()}[/{risk_color}]\n"
        content += f"{result.message}\n\n"

        if result.targets:
            content += "[dim]Targets:[/dim]\n"
            for target in result.targets[:10]:
                content += f"  • {target}\n"
            if len(result.targets) > 10:
                content += f"  [dim]... and {len(result.targets) - 10} more[/dim]\n"

        if not result.reversible:
            content += "\n[red]⚠ NOT REVERSIBLE[/red]"

        console.print(
            Panel(
                content,
                title=f"[bold]Dry Run: {command[:50]}[/bold]",
                border_style=risk_color,
            )
        )
    else:
        console.print(
            Panel(
                f"[yellow]{result.message}[/yellow]\n\n"
                f"[dim]Supported commands: rm, git reset, git clean, mv[/dim]",
                title="[bold yellow]Cannot Simulate[/bold yellow]",
                border_style="yellow",
            )
        )


# =============================================================================
# TEST DETECTION
# =============================================================================


def detect_test_harness() -> dict:
    """Detect test commands from project configuration.

    This is a wrapper around the comprehensive harness.detect_harness()
    that maintains backward compatibility with the dict format.
    """
    from .harness import detect_harness

    cwd = Path.cwd()
    harness_obj = detect_harness(cwd)

    # Convert to legacy dict format for backward compatibility
    detected_from = []
    if harness_obj.test_command:
        # Infer source from command patterns
        if "pytest" in harness_obj.test_command:
            detected_from.append("pyproject.toml")
        elif "npm test" in harness_obj.test_command:
            detected_from.append("package.json")
        elif "cargo test" in harness_obj.test_command:
            detected_from.append("Cargo.toml")
        elif "make test" in harness_obj.test_command:
            detected_from.append("Makefile")

    return {
        "test_command": harness_obj.test_command,
        "lint_command": harness_obj.lint_command,
        "build_command": harness_obj.build_command,
        "detected_from": detected_from,
    }


def find_related_tests(source_file: str) -> list[str]:
    """Find test files related to a source file."""
    source_path = Path(source_file)
    base_name = source_path.stem

    # Common patterns for test file naming
    patterns = [
        f"test_{base_name}.py",
        f"{base_name}_test.py",
        f"tests/test_{base_name}.py",
        f"tests/{base_name}_test.py",
        f"test/test_{base_name}.py",
        f"**/test_{base_name}.py",
        f"**/{base_name}_test.py",
    ]

    related = []
    for pattern in patterns:
        related.extend(glob.glob(pattern, recursive=True))

    return list(set(related))


def test_harness_command():
    """Show detected test harness configuration."""
    harness = detect_test_harness()

    if not harness["detected_from"]:
        console.print("[yellow]No test configuration detected[/yellow]")
        console.print("[dim]Looking for: pyproject.toml, package.json, Makefile[/dim]")
        return

    table = Table(title="Detected Test Harness")
    table.add_column("Type", style="cyan")
    table.add_column("Command", style="green")

    if harness["test_command"]:
        table.add_row("Test", harness["test_command"])
    if harness["lint_command"]:
        table.add_row("Lint", harness["lint_command"])
    if harness["build_command"]:
        table.add_row("Build", harness["build_command"])

    console.print(table)
    console.print(f"\n[dim]Detected from: {', '.join(harness['detected_from'])}[/dim]")


# =============================================================================
# CROSS-SESSION MEMORY
# =============================================================================


@dataclass
class MemoryEntry:
    """A memory entry for cross-session learning."""

    timestamp: str
    file: str
    event: str  # "test_failure", "fix", "error", "lesson"
    details: str
    test_file: Optional[str] = None


def get_memory_file(project_dir: Optional[Path] = None) -> Path:
    """Get the memory file for a project."""
    if project_dir is None:
        project_dir = Path.cwd()

    mc_project_dir = project_dir / ".mc"
    mc_project_dir.mkdir(exist_ok=True)
    return mc_project_dir / "memory.json"


def load_memory(project_dir: Optional[Path] = None) -> list[MemoryEntry]:
    """Load memory entries for a project."""
    mem_file = get_memory_file(project_dir)
    if not mem_file.exists():
        return []

    try:
        data = json.loads(mem_file.read_text())
        return [MemoryEntry(**entry) for entry in data]
    except (json.JSONDecodeError, TypeError):
        return []


def save_memory(entries: list[MemoryEntry], project_dir: Optional[Path] = None):
    """Save memory entries for a project."""
    mem_file = get_memory_file(project_dir)
    data = [asdict(entry) for entry in entries]
    mem_file.write_text(json.dumps(data, indent=2))


def record_memory(
    file: str,
    event: str,
    details: str,
    test_file: Optional[str] = None,
    project_dir: Optional[Path] = None,
):
    """Record a memory entry."""
    entry = MemoryEntry(
        timestamp=datetime.now().isoformat(),
        file=file,
        event=event,
        details=details,
        test_file=test_file,
    )

    entries = load_memory(project_dir)
    entries.insert(0, entry)

    # Keep only last 100 entries
    entries = entries[:100]
    save_memory(entries, project_dir)

    return entry


def get_file_memories(file: str, project_dir: Optional[Path] = None) -> list[MemoryEntry]:
    """Get memories related to a specific file."""
    entries = load_memory(project_dir)
    return [e for e in entries if e.file == file or e.test_file == file]


def memory_command(file: Optional[str] = None):
    """Show memory for the project or a specific file."""
    entries = load_memory()

    if file:
        entries = get_file_memories(file)

    if not entries:
        console.print("[yellow]No memories recorded yet[/yellow]")
        console.print("[dim]Memories are recorded when tests fail or fixes are applied[/dim]")
        return

    table = Table(title=f"Memory{f' for {file}' if file else ''}")
    table.add_column("Age", style="dim", width=8)
    table.add_column("File", style="cyan")
    table.add_column("Event", style="yellow")
    table.add_column("Details", style="white")

    for entry in entries[:15]:
        try:
            dt = datetime.fromisoformat(entry.timestamp)
            age = datetime.now() - dt
            if age.total_seconds() < 3600:
                age_str = f"{int(age.total_seconds() / 60)}m"
            elif age.total_seconds() < 86400:
                age_str = f"{int(age.total_seconds() / 3600)}h"
            else:
                age_str = f"{int(age.total_seconds() / 86400)}d"
        except (ValueError, TypeError):
            age_str = "?"

        table.add_row(
            age_str,
            Path(entry.file).name,
            entry.event,
            entry.details[:50],
        )

    console.print(table)


def remember_command(file: str, event: str, details: str):
    """Manually record a memory."""
    record_memory(file, event, details)
    console.print(f"[green]✓ Remembered:[/green] {event} for {file}")


# =============================================================================
# CONTEXT HINTS (for injection into agent)
# =============================================================================


def get_context_hints(files: list[str]) -> str:
    """Get context hints for files being edited.

    This is what gets injected into the agent's context via hooks.
    """
    hints = []

    for file in files:
        # Get related tests
        related_tests = find_related_tests(file)
        if related_tests:
            hints.append(f"• Related tests for {file}: {', '.join(related_tests)}")

        # Get memories for this file
        memories = get_file_memories(file)
        if memories:
            recent = memories[0]
            hints.append(f"• Memory ({file}): {recent.event} - {recent.details}")

    # Get test harness
    harness = detect_test_harness()
    if harness["test_command"]:
        hints.append(f"• Test command: {harness['test_command']}")

    # Get checkpoints
    checkpoints = load_checkpoints()
    if checkpoints:
        hints.append(f"• Last checkpoint: {checkpoints[0].id} ({checkpoints[0].message})")

    if hints:
        return "[MC Context]\n" + "\n".join(hints)
    return ""
