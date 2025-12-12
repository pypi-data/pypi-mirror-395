"""
Process Detector - Cached, fail-silent process detection.

Detects running Claude/Codex/Gemini processes with:
- 5-second cache to avoid repeated subprocess calls
- 0.5-second timeout to prevent blocking
- Auto-disable on permission errors
- Fail-silent logging (debug level only)
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Set

from .config import config
from .logging import get_logger


class ProcessDetector:
    """Cached, fail-silent process detection.

    Detects running Claude/Codex/Gemini processes with:
    - 5-second cache to avoid repeated subprocess calls
    - 0.5-second timeout to prevent blocking
    - Auto-disable on permission errors
    - Fail-silent logging (debug level only)
    """

    def __init__(self, cache_ttl: float = 5.0, timeout: float = 0.5):
        self._cache: Dict[str, Set[str]] = {}
        self._cache_time: float = 0
        self._enabled: bool = True
        self._cache_ttl = cache_ttl
        self._timeout = timeout
        self._logger = get_logger(__name__)

    def get_running_projects(self) -> Set[str]:
        """Get set of project directories with running agent processes."""
        if not self._enabled:
            return self._cache.get("projects", set())

        now = time.time()
        if now - self._cache_time < self._cache_ttl:
            return self._cache.get("projects", set())

        projects: Set[str] = set()

        # Detect Claude processes
        try:
            # Try pgrep for Claude
            result = subprocess.run(
                ["pgrep", "-fl", "claude"],
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    # Extract project paths from command line
                    if "-p " in line or "--project " in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part in ("-p", "--project") and i + 1 < len(parts):
                                projects.add(parts[i + 1])

            # Also check lsof for processes with open files in .claude/projects
            # This is more reliable for detecting active sessions
            try:
                lsof_result = subprocess.run(
                    ["lsof", "+D", str(config.paths.projects_dir)],
                    capture_output=True,
                    text=True,
                    timeout=self._timeout,
                )
                # Process output regardless of return code (lsof returns 1 if any error)
                if lsof_result.stdout:
                    projects_dir_str = str(config.paths.projects_dir)
                    for line in lsof_result.stdout.split("\n"):
                        if config.paths.projects_dir.name in line:
                            for part in line.split():
                                if projects_dir_str in part:
                                    try:
                                        rel_path = Path(part).relative_to(config.paths.projects_dir)
                                        project_dir = rel_path.parts[0] if rel_path.parts else ""
                                        if project_dir:
                                            projects.add(project_dir)
                                    except ValueError:
                                        continue
            except subprocess.TimeoutExpired:
                self._logger.debug("lsof timed out, using pgrep results only")
            except (OSError, subprocess.SubprocessError):
                # lsof failed, but we still have pgrep results
                pass

        except subprocess.TimeoutExpired:
            self._logger.debug("Claude process detection timed out")
        except PermissionError:
            self._logger.debug("Claude process detection permission denied, disabling")
            self._enabled = False
        except FileNotFoundError:
            self._logger.debug("pgrep not available on this system")
            self._enabled = False
        except (OSError, subprocess.SubprocessError) as e:
            self._logger.debug(f"Claude process detection error: {e}")
            # Don't disable on transient errors, just use cache

        # Detect Gemini processes (independent of Claude detection)
        try:
            result = subprocess.run(
                ["pgrep", "-fl", "gemini"],
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    # Extract project paths from command line
                    if "-p " in line or "--project " in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part in ("-p", "--project") and i + 1 < len(parts):
                                projects.add(parts[i + 1])

                    # Also check for working directory argument patterns
                    if "--cwd " in line or "-C " in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part in ("--cwd", "-C") and i + 1 < len(parts):
                                projects.add(parts[i + 1])

            # Check lsof for Gemini session files
            gemini_tmp = Path.home() / ".gemini" / "tmp"
            if gemini_tmp.exists():
                try:
                    lsof_result = subprocess.run(
                        ["lsof", "+D", str(gemini_tmp)],
                        capture_output=True,
                        text=True,
                        timeout=self._timeout,
                    )
                    if lsof_result.stdout:
                        # Extract project hashes from open files in .gemini/tmp/<hash>/chats/
                        for line in lsof_result.stdout.split("\n"):
                            if "/chats/" in line:
                                for part in line.split():
                                    if str(gemini_tmp) in part and "/chats/" in part:
                                        try:
                                            rel_path = Path(part).relative_to(gemini_tmp)
                                            project_hash = (
                                                rel_path.parts[0] if rel_path.parts else ""
                                            )
                                            if project_hash:
                                                # Store as gemini:<hash> to distinguish from Claude
                                                projects.add(f"gemini:{project_hash}")
                                        except ValueError:
                                            continue
                except subprocess.TimeoutExpired:
                    self._logger.debug("Gemini lsof timed out")
                except (OSError, subprocess.SubprocessError):
                    pass

        except subprocess.TimeoutExpired:
            self._logger.debug("Gemini process detection timed out")
        except FileNotFoundError:
            self._logger.debug("pgrep not available for Gemini detection")
        except (OSError, subprocess.SubprocessError) as e:
            self._logger.debug(f"Gemini process detection error: {e}")

        # Detect Codex processes (independent of Claude/Gemini detection)
        try:
            result = subprocess.run(
                ["pgrep", "-fl", "codex"],
                capture_output=True,
                text=True,
                timeout=self._timeout,
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    # Extract project paths from command line
                    if "-p " in line or "--project " in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part in ("-p", "--project") and i + 1 < len(parts):
                                projects.add(parts[i + 1])

                    # Also check for working directory argument patterns
                    if "--cwd " in line or "-C " in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part in ("--cwd", "-C") and i + 1 < len(parts):
                                projects.add(parts[i + 1])

            # Check lsof for Codex session files
            codex_sessions = Path.home() / ".codex" / "sessions"
            if codex_sessions.exists():
                try:
                    lsof_result = subprocess.run(
                        ["lsof", "+D", str(codex_sessions)],
                        capture_output=True,
                        text=True,
                        timeout=self._timeout,
                    )
                    if lsof_result.stdout:
                        # Extract working directories from open session files
                        for line in lsof_result.stdout.split("\n"):
                            if ".jsonl" in line:
                                for part in line.split():
                                    if str(codex_sessions) in part and part.endswith(".jsonl"):
                                        # Try to read session metadata to get cwd
                                        try:
                                            with open(part, "r") as f:
                                                first_line = f.readline()
                                                if first_line:
                                                    data = json.loads(first_line)
                                                    if data.get("type") == "session_meta":
                                                        cwd = data.get("payload", {}).get("cwd", "")
                                                        if cwd:
                                                            projects.add(cwd)
                                        except (OSError, json.JSONDecodeError):
                                            continue
                except subprocess.TimeoutExpired:
                    self._logger.debug("Codex lsof timed out")
                except (OSError, subprocess.SubprocessError):
                    pass

        except subprocess.TimeoutExpired:
            self._logger.debug("Codex process detection timed out")
        except FileNotFoundError:
            self._logger.debug("pgrep not available for Codex detection")
        except (OSError, subprocess.SubprocessError) as e:
            self._logger.debug(f"Codex process detection error: {e}")

        self._cache["projects"] = projects
        self._cache_time = now
        self._logger.debug(f"Detected {len(projects)} running projects across all CLIs")

        return self._cache.get("projects", set())

    def is_project_active(self, project_path: str) -> bool:
        """Check if a specific project has a running agent."""
        running = self.get_running_projects()
        return project_path in running or any(project_path in p for p in running)

    def is_degraded(self) -> bool:
        """Check if process detection is disabled (degraded mode).

        Returns:
            True if process detection has been disabled due to errors.
        """
        return not self._enabled

    def reset(self):
        """Reset detector state (useful for testing)."""
        self._cache.clear()
        self._cache_time = 0
        self._enabled = True
