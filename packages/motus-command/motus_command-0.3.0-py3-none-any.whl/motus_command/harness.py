"""
Test Harness Detection for Motus Command v0.3.0.

Auto-detect test, lint, build, and smoke test commands from repository structure.
Supports multiple build systems: Python, JavaScript/Node, Rust, Make, and CI configs.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# tomllib is only available in Python 3.11+, use tomli as fallback
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        tomllib = None  # type: ignore[assignment]

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class MCTestHarness:
    """Detected test harness commands for a repository.

    Attributes:
        test_command: Full test suite command (e.g., "pytest tests/ -v")
        lint_command: Linting/style check command (e.g., "ruff check src/")
        build_command: Build/compile command (e.g., "npm run build")
        smoke_test: Fast subset of tests for quick validation
    """

    test_command: Optional[str] = None
    lint_command: Optional[str] = None
    build_command: Optional[str] = None
    smoke_test: Optional[str] = None


# Backward compatibility alias (prevents pytest from treating it as a test class)
TestHarness = MCTestHarness


def detect_harness(repo_path: Path) -> MCTestHarness:
    """Auto-detect test harness from repository structure.

    Scans for common configuration files and extracts test commands:
    - pyproject.toml → pytest, ruff, mypy
    - package.json → npm test, npm run lint, npm run build
    - Makefile → make test, make lint, make build
    - pytest.ini or setup.cfg → pytest configuration
    - Cargo.toml → cargo test, cargo clippy
    - .github/workflows/*.yml → extract test commands from CI

    Args:
        repo_path: Path to repository root

    Returns:
        MCTestHarness with detected commands (None for undetected commands)
    """
    if not repo_path.is_dir():
        return MCTestHarness()

    harness = MCTestHarness()

    # Priority order: specific configs > package managers > Makefile > CI
    _detect_from_pyproject(repo_path, harness)
    _detect_from_package_json(repo_path, harness)
    _detect_from_cargo_toml(repo_path, harness)
    _detect_from_pytest_ini(repo_path, harness)
    _detect_from_setup_cfg(repo_path, harness)
    _detect_from_makefile(repo_path, harness)
    _detect_from_github_workflows(repo_path, harness)

    return harness


def _detect_from_pyproject(repo_path: Path, harness: MCTestHarness) -> None:
    """Detect Python test commands from pyproject.toml."""
    pyproject_file = repo_path / "pyproject.toml"
    if not pyproject_file.exists() or tomllib is None:
        return

    try:
        with open(pyproject_file, "rb") as f:
            data = tomllib.load(f)

        # Test command - check for pytest configuration
        if "tool" in data and "pytest" in data["tool"]:
            pytest_opts = data["tool"]["pytest"].get("ini_options", {})
            testpaths = pytest_opts.get("testpaths", ["tests"])
            if isinstance(testpaths, list):
                testpaths_str = " ".join(testpaths)
            else:
                testpaths_str = str(testpaths)

            # Add verbosity if not specified
            addopts = pytest_opts.get("addopts", "")
            verbose_flag = "-v" if "-v" not in addopts else ""

            harness.test_command = f"pytest {testpaths_str} {verbose_flag}".strip()

            # Smoke test - run a subset (first test path only)
            if isinstance(testpaths, list) and testpaths:
                harness.smoke_test = f"pytest {testpaths[0]} {verbose_flag} -x".strip()

        # Lint command - check for ruff configuration
        if "tool" in data and "ruff" in data["tool"]:
            harness.lint_command = "ruff check src/"

        # Also check for mypy
        if "tool" in data and "mypy" in data["tool"]:
            if harness.lint_command:
                harness.lint_command += " && mypy src/"
            else:
                harness.lint_command = "mypy src/"

        # Check for build system
        if "build-system" in data:
            build_backend = data["build-system"].get("build-backend", "")
            if "hatch" in build_backend:
                harness.build_command = "hatch build"
            elif "setuptools" in build_backend:
                harness.build_command = "python -m build"
            elif "poetry" in build_backend:
                harness.build_command = "poetry build"

    except Exception:
        # Silently handle parse errors - just skip this source
        pass


def _detect_from_package_json(repo_path: Path, harness: MCTestHarness) -> None:
    """Detect Node.js/JavaScript test commands from package.json."""
    package_json = repo_path / "package.json"
    if not package_json.exists():
        return

    try:
        with open(package_json, "r") as f:
            data = json.load(f)

        scripts = data.get("scripts", {})

        # Test command
        if "test" in scripts and not harness.test_command:
            harness.test_command = "npm test"

        # Lint command
        if "lint" in scripts and not harness.lint_command:
            harness.lint_command = "npm run lint"

        # Build command
        if "build" in scripts and not harness.build_command:
            harness.build_command = "npm run build"

        # Smoke test - look for test:unit or test:quick
        if "test:unit" in scripts and not harness.smoke_test:
            harness.smoke_test = "npm run test:unit"
        elif "test:quick" in scripts and not harness.smoke_test:
            harness.smoke_test = "npm run test:quick"

    except Exception:
        # Silently handle parse errors
        pass


def _detect_from_cargo_toml(repo_path: Path, harness: MCTestHarness) -> None:
    """Detect Rust test commands from Cargo.toml."""
    cargo_toml = repo_path / "Cargo.toml"
    if not cargo_toml.exists():
        return

    # Don't need to parse TOML for Cargo - just check if file exists
    # Cargo has standard conventions
    if not harness.test_command:
        harness.test_command = "cargo test"

    if not harness.lint_command:
        harness.lint_command = "cargo clippy"

    if not harness.build_command:
        harness.build_command = "cargo build"

    if not harness.smoke_test:
        harness.smoke_test = "cargo test --lib"


def _detect_from_pytest_ini(repo_path: Path, harness: MCTestHarness) -> None:
    """Detect pytest configuration from pytest.ini."""
    pytest_ini = repo_path / "pytest.ini"
    if not pytest_ini.exists() or harness.test_command:
        return

    try:
        # Simple INI parsing for testpaths
        content = pytest_ini.read_text()
        testpaths_match = re.search(r"testpaths\s*=\s*(.+)", content)
        if testpaths_match:
            testpaths = testpaths_match.group(1).strip()
            harness.test_command = f"pytest {testpaths} -v"
        else:
            harness.test_command = "pytest tests/ -v"
    except Exception:
        pass


def _detect_from_setup_cfg(repo_path: Path, harness: MCTestHarness) -> None:
    """Detect pytest configuration from setup.cfg."""
    setup_cfg = repo_path / "setup.cfg"
    if not setup_cfg.exists() or harness.test_command:
        return

    try:
        content = setup_cfg.read_text()
        # Look for [tool:pytest] section
        if "[tool:pytest]" in content or "[pytest]" in content:
            harness.test_command = "pytest tests/ -v"
    except Exception:
        pass


def _detect_from_makefile(repo_path: Path, harness: MCTestHarness) -> None:
    """Detect test commands from Makefile."""
    for makefile_name in ["Makefile", "makefile", "GNUmakefile"]:
        makefile = repo_path / makefile_name
        if not makefile.exists():
            continue

        try:
            content = makefile.read_text()

            # Look for common make targets
            if not harness.test_command and re.search(r"^test:", content, re.MULTILINE):
                harness.test_command = "make test"

            if not harness.lint_command and re.search(r"^lint:", content, re.MULTILINE):
                harness.lint_command = "make lint"

            if not harness.build_command and re.search(r"^build:", content, re.MULTILINE):
                harness.build_command = "make build"

            # Check for smoke/quick test targets
            if not harness.smoke_test:
                if re.search(r"^test-quick:", content, re.MULTILINE):
                    harness.smoke_test = "make test-quick"
                elif re.search(r"^smoke:", content, re.MULTILINE):
                    harness.smoke_test = "make smoke"

            break  # Found a Makefile, stop searching
        except Exception:
            pass


def _detect_from_github_workflows(repo_path: Path, harness: MCTestHarness) -> None:
    """Extract test commands from GitHub Actions workflows."""
    workflows_dir = repo_path / ".github" / "workflows"
    if not workflows_dir.exists() or not YAML_AVAILABLE:
        return

    try:
        for workflow_file in workflows_dir.glob("*.yml"):
            try:
                with open(workflow_file, "r") as f:
                    workflow = yaml.safe_load(f)

                if not isinstance(workflow, dict):
                    continue

                jobs = workflow.get("jobs", {})
                for job_name, job_config in jobs.items():
                    if not isinstance(job_config, dict):
                        continue

                    steps = job_config.get("steps", [])
                    for step in steps:
                        if not isinstance(step, dict):
                            continue

                        run_cmd = step.get("run", "")
                        if not run_cmd:
                            continue

                        # Extract test commands
                        if not harness.test_command and (
                            "pytest" in run_cmd or "npm test" in run_cmd or "cargo test" in run_cmd
                        ):
                            # Clean up multiline commands
                            clean_cmd = " ".join(run_cmd.split())
                            if len(clean_cmd) < 100:  # Reasonable command length
                                harness.test_command = clean_cmd

                        # Extract lint commands
                        if not harness.lint_command and (
                            "ruff" in run_cmd or "npm run lint" in run_cmd or "clippy" in run_cmd
                        ):
                            clean_cmd = " ".join(run_cmd.split())
                            if len(clean_cmd) < 100:
                                harness.lint_command = clean_cmd

                        # Extract build commands
                        if not harness.build_command and (
                            "build" in run_cmd or "compile" in run_cmd
                        ):
                            clean_cmd = " ".join(run_cmd.split())
                            if len(clean_cmd) < 100:
                                harness.build_command = clean_cmd

            except Exception:
                # Skip individual workflow files that fail to parse
                continue

    except Exception:
        # Silently handle errors
        pass


def get_confidence_level(command: Optional[str], source: str) -> str:
    """Get confidence level for a detected command.

    Args:
        command: The detected command string
        source: Where the command was detected from (e.g., "pyproject.toml", "Makefile")

    Returns:
        Confidence level: "high", "medium", or "low"
    """
    if not command:
        return "none"

    # High confidence sources
    high_confidence_sources = ["pyproject.toml", "package.json", "Cargo.toml"]
    if source in high_confidence_sources:
        return "high"

    # Medium confidence sources
    medium_confidence_sources = ["Makefile", "pytest.ini", "setup.cfg"]
    if source in medium_confidence_sources:
        return "medium"

    # Low confidence (inferred from CI)
    return "low"
