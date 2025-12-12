"""
State Checkpoints Module for Motus Command v0.3.

Git-based checkpoints that allow safe experimentation and rollback.
Uses git stash for state storage with a manifest of modified files.
"""

import json
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Checkpoint:
    """A saved state checkpoint using git stash.

    Attributes:
        id: Unique checkpoint identifier (timestamp-based)
        label: User-provided description of the checkpoint
        timestamp: ISO format timestamp when checkpoint was created
        git_stash_ref: Git stash reference (e.g., "stash@{0}")
        file_manifest: List of modified files at checkpoint time
    """

    id: str
    label: str
    timestamp: str
    git_stash_ref: Optional[str] = None
    file_manifest: list[str] = field(default_factory=list)


def _get_checkpoints_file(repo_path: Path) -> Path:
    """Get the checkpoints metadata file for a repository.

    Args:
        repo_path: Path to git repository root

    Returns:
        Path to checkpoints.json file
    """
    mc_dir = repo_path / ".mc"
    mc_dir.mkdir(exist_ok=True)
    return mc_dir / "checkpoints.json"


def _is_git_repo(repo_path: Path) -> bool:
    """Check if directory is a git repository.

    Args:
        repo_path: Path to check

    Returns:
        True if path is inside a git repository
    """
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _get_git_root(repo_path: Path) -> Optional[Path]:
    """Get the git repository root directory.

    Args:
        repo_path: Path within a git repository

    Returns:
        Path to git root, or None if not in a git repo
    """
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return None


def _get_modified_files(repo_path: Path) -> list[str]:
    """Get list of modified files in the working directory.

    Args:
        repo_path: Path to git repository

    Returns:
        List of file paths relative to repo root (excludes .mc/ directory)
    """
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    files = []
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            # Format is "XY filename" where XY is status code
            # Strip first 3 characters to get filename
            filename = line[3:]
            # Exclude .mc/ directory (checkpoint metadata)
            if not filename.startswith(".mc/"):
                files.append(filename)

    return files


def _find_stash_ref(repo_path: Path, stash_message: str) -> Optional[str]:
    """Find the git stash reference for a given message.

    Args:
        repo_path: Path to git repository
        stash_message: Message to search for in stash list

    Returns:
        Stash reference (e.g., "stash@{0}") or None if not found
    """
    result = subprocess.run(
        ["git", "stash", "list", "--format=%gd %s"],
        cwd=repo_path,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None

    for line in result.stdout.strip().split("\n"):
        if stash_message in line:
            # Extract stash@{N} from the line
            parts = line.split()
            if parts:
                return parts[0]

    return None


def create_checkpoint(label: str, repo_path: Path) -> Checkpoint:
    """Create a new checkpoint of the current repository state.

    This creates a git stash with the current changes and saves metadata
    about the checkpoint. The working directory is restored immediately
    after the stash is created.

    Args:
        label: User-provided description of the checkpoint
        repo_path: Path to git repository (will use git root)

    Returns:
        Created Checkpoint object

    Raises:
        ValueError: If not in a git repository or no changes to checkpoint
        RuntimeError: If git stash command fails
    """
    # Ensure we're in a git repo
    if not _is_git_repo(repo_path):
        raise ValueError("Not in a git repository")

    # Get git root
    git_root = _get_git_root(repo_path)
    if git_root is None:
        raise ValueError("Could not determine git repository root")

    # Get list of modified files
    modified_files = _get_modified_files(git_root)
    if not modified_files:
        raise ValueError("No changes to checkpoint")

    # Create checkpoint ID with microseconds to ensure uniqueness
    timestamp = datetime.now()
    checkpoint_id = f"mc-{timestamp.strftime('%Y%m%d-%H%M%S')}-{timestamp.microsecond // 1000:03d}"

    # Create checkpoint object first (before stashing)
    checkpoint = Checkpoint(
        id=checkpoint_id,
        label=label,
        timestamp=timestamp.isoformat(),
        git_stash_ref=None,  # Will be set after stashing
        file_manifest=modified_files,
    )

    # Save checkpoint metadata BEFORE stashing (so it doesn't get stashed)
    checkpoints = list_checkpoints(git_root)
    checkpoints.insert(0, checkpoint)  # Most recent first
    _save_checkpoints(checkpoints, git_root)

    # Create git stash with labeled message
    # We use pathspec to exclude .mc/ directory from being stashed
    stash_message = f"mc-checkpoint: {label}"
    result = subprocess.run(
        ["git", "stash", "push", "-u", "-m", stash_message, "--", ".", ":(exclude).mc"],
        cwd=git_root,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to create git stash: {result.stderr}")

    # Find the stash reference and update the checkpoint
    stash_ref = _find_stash_ref(git_root, stash_message)
    checkpoint.git_stash_ref = stash_ref

    # Update checkpoint metadata with stash ref
    checkpoints = list_checkpoints(git_root)
    for cp in checkpoints:
        if cp.id == checkpoint_id:
            # Update the stash_ref (need to create new object due to dataclass)
            updated_cp = Checkpoint(
                id=cp.id,
                label=cp.label,
                timestamp=cp.timestamp,
                git_stash_ref=stash_ref,
                file_manifest=cp.file_manifest,
            )
            checkpoints[checkpoints.index(cp)] = updated_cp
            break
    _save_checkpoints(checkpoints, git_root)

    # Restore working directory using the stash reference (keep stash for later rollback/diff)
    # We use 'apply' instead of 'pop' to preserve the stash
    if stash_ref:
        result = subprocess.run(
            ["git", "stash", "apply", "--index", stash_ref],
            cwd=git_root,
            capture_output=True,
            text=True,
        )
        # If apply fails (e.g., conflicts), just continue - user can manually resolve
        # The stash is still saved and can be used for rollback
        if result.returncode != 0:
            # Try without --index (ignores staging info, easier to apply)
            subprocess.run(
                ["git", "stash", "apply", stash_ref],
                cwd=git_root,
                capture_output=True,
            )

    return checkpoint


def list_checkpoints(repo_path: Path) -> list[Checkpoint]:
    """List all available checkpoints for a repository.

    Args:
        repo_path: Path to git repository

    Returns:
        List of Checkpoint objects, ordered by creation time (newest first)
    """
    if not _is_git_repo(repo_path):
        return []

    git_root = _get_git_root(repo_path)
    if git_root is None:
        return []

    checkpoints_file = _get_checkpoints_file(git_root)

    if not checkpoints_file.exists():
        return []

    try:
        data = json.loads(checkpoints_file.read_text())
        return [Checkpoint(**cp) for cp in data]
    except (json.JSONDecodeError, TypeError, KeyError):
        # Corrupted file or invalid format
        return []


def _save_checkpoints(checkpoints: list[Checkpoint], repo_path: Path) -> None:
    """Save checkpoints metadata to disk.

    Args:
        checkpoints: List of checkpoints to save
        repo_path: Path to git repository
    """
    git_root = _get_git_root(repo_path)
    if git_root is None:
        raise ValueError("Not in a git repository")

    checkpoints_file = _get_checkpoints_file(git_root)
    data = [asdict(cp) for cp in checkpoints]
    checkpoints_file.write_text(json.dumps(data, indent=2))


def rollback_checkpoint(checkpoint_id: str, repo_path: Path) -> Checkpoint:
    """Restore repository state to a previous checkpoint.

    This applies the checkpoint's git stash to restore the state.
    The current working directory changes are stashed first for safety.

    Args:
        checkpoint_id: Full or partial checkpoint ID to rollback to
        repo_path: Path to git repository

    Returns:
        The checkpoint that was restored

    Raises:
        ValueError: If checkpoint not found or not in git repo
        RuntimeError: If git stash apply fails
    """
    if not _is_git_repo(repo_path):
        raise ValueError("Not in a git repository")

    git_root = _get_git_root(repo_path)
    if git_root is None:
        raise ValueError("Could not determine git repository root")

    # Find the checkpoint
    checkpoints = list_checkpoints(git_root)
    target = None
    for cp in checkpoints:
        if cp.id == checkpoint_id or cp.id.startswith(checkpoint_id):
            target = cp
            break

    if target is None:
        raise ValueError(f"Checkpoint not found: {checkpoint_id}")

    if target.git_stash_ref is None:
        raise ValueError(f"Checkpoint {checkpoint_id} has no stash reference")

    # Stash current changes first (safety backup) - exclude .mc/
    subprocess.run(
        ["git", "stash", "push", "-u", "-m", "mc-rollback-safety", "--", ".", ":(exclude).mc"],
        cwd=git_root,
        capture_output=True,
    )

    # Reset working directory to clean state (match last commit)
    # This removes all tracked changes
    subprocess.run(
        ["git", "reset", "--hard", "HEAD"],
        cwd=git_root,
        capture_output=True,
    )

    # Clean untracked files (except .mc/)
    # Use -e flag to exclude .mc/ directory
    subprocess.run(
        ["git", "clean", "-ffd", "-e", ".mc/"],
        cwd=git_root,
        capture_output=True,
    )

    # Find the checkpoint stash by its message (the index may have shifted due to safety stash)
    # The stash message format is "mc-checkpoint: {label}"
    stash_message = f"mc-checkpoint: {target.label}"
    checkpoint_stash_ref = _find_stash_ref(git_root, stash_message)

    if not checkpoint_stash_ref:
        # Fallback to stored reference if message search fails
        checkpoint_stash_ref = target.git_stash_ref

    # Now apply the checkpoint stash to restore that state
    # This will restore both tracked and untracked files from the checkpoint
    result = subprocess.run(
        ["git", "stash", "apply", checkpoint_stash_ref],
        cwd=git_root,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        # Failed - restore the safety stash
        subprocess.run(
            ["git", "reset", "--hard", "HEAD"],
            cwd=git_root,
            capture_output=True,
        )
        subprocess.run(
            ["git", "stash", "pop", "--quiet"],
            cwd=git_root,
            capture_output=True,
        )
        raise RuntimeError(f"Failed to apply checkpoint: {result.stderr}")

    return target


def diff_checkpoint(checkpoint_id: str, repo_path: Path) -> str:
    """Show changes between current state and a checkpoint.

    Args:
        checkpoint_id: Full or partial checkpoint ID
        repo_path: Path to git repository

    Returns:
        Diff output showing changes

    Raises:
        ValueError: If checkpoint not found or not in git repo
    """
    if not _is_git_repo(repo_path):
        raise ValueError("Not in a git repository")

    git_root = _get_git_root(repo_path)
    if git_root is None:
        raise ValueError("Could not determine git repository root")

    # Find the checkpoint
    checkpoints = list_checkpoints(git_root)
    target = None
    for cp in checkpoints:
        if cp.id == checkpoint_id or cp.id.startswith(checkpoint_id):
            target = cp
            break

    if target is None:
        raise ValueError(f"Checkpoint not found: {checkpoint_id}")

    if target.git_stash_ref is None:
        raise ValueError(f"Checkpoint {checkpoint_id} has no stash reference")

    # Find the checkpoint stash by its message (the index may have shifted)
    stash_message = f"mc-checkpoint: {target.label}"
    checkpoint_stash_ref = _find_stash_ref(git_root, stash_message)

    if not checkpoint_stash_ref:
        # Fallback to stored reference if message search fails
        checkpoint_stash_ref = target.git_stash_ref

    # Get diff from stash - use --include-untracked to show untracked files
    # First try with -p (patch) which works for tracked files
    result = subprocess.run(
        ["git", "stash", "show", "-p", "--include-untracked", checkpoint_stash_ref],
        cwd=git_root,
        capture_output=True,
        text=True,
    )

    # If that fails, try without --include-untracked (older git versions)
    if result.returncode != 0:
        result = subprocess.run(
            ["git", "stash", "show", "-p", checkpoint_stash_ref],
            cwd=git_root,
            capture_output=True,
            text=True,
        )

    # If still empty but we have untracked files, list them from the stash
    if not result.stdout.strip() and target.file_manifest:
        # Build a simple diff-like output showing the untracked files
        untracked_info = "Checkpoint contains untracked files:\n"
        for f in target.file_manifest:
            untracked_info += f"  + {f}\n"
        return untracked_info

    if result.returncode != 0:
        raise RuntimeError(f"Failed to show diff: {result.stderr}")

    return result.stdout
