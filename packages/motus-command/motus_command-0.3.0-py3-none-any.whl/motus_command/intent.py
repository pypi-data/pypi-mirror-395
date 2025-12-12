"""
Intent Spine - Structured task representation for AI agents.

The Intent Spine provides a structured way to capture and persist the agent's
task understanding. This helps agents stay on-task during long sessions and
enables context recovery across sessions.

Key features:
- Parse task from first user message in session
- Extract constraints and out-of-scope items
- Track priority files
- Save/load from .mc/intent.yaml
- Generate YAML output for easy inspection
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from .logging import get_logger
from .transcript_parser import TranscriptParser

logger = get_logger(__name__)


@dataclass
class Intent:
    """
    Structured representation of an agent's task.

    Attributes:
        task: Main task description (extracted from first user message)
        constraints: List of constraints/requirements (e.g., "Don't modify tests")
        out_of_scope: List of things explicitly out of scope
        priority_files: List of file paths that are central to the task
    """

    task: str
    constraints: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    priority_files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert Intent to dictionary for serialization."""
        return {
            "task": self.task,
            "constraints": self.constraints,
            "out_of_scope": self.out_of_scope,
            "priority_files": self.priority_files,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Intent":
        """Create Intent from dictionary."""
        return cls(
            task=data.get("task", ""),
            constraints=data.get("constraints", []),
            out_of_scope=data.get("out_of_scope", []),
            priority_files=data.get("priority_files", []),
        )


def parse_intent(session_path: Path) -> Intent:
    """
    Extract intent from a session transcript.

    Analyzes the first user message to understand the task, constraints,
    and scope. Also tracks files that are frequently accessed as priority files.

    Args:
        session_path: Path to the session transcript file (.jsonl or .json)

    Returns:
        Intent object with extracted task information

    Example:
        >>> intent = parse_intent(Path("~/.claude/projects/abc/session.jsonl"))
        >>> print(intent.task)
        "Add source badges to session display"
    """
    parser = TranscriptParser(extract_file_snapshots=False)
    data = parser.parse_file(session_path)

    # Extract task from first user intent
    task = "No task specified"
    if data.user_intents:
        first_intent = data.user_intents[0]
        task = _extract_task_from_prompt(first_intent.prompt)

    # Extract constraints from prompt
    constraints = _extract_constraints(data.user_intents[0].prompt if data.user_intents else "")

    # Infer out-of-scope items from constraints
    out_of_scope = _infer_out_of_scope(constraints)

    # Identify priority files based on modification frequency
    priority_files = _identify_priority_files(data)

    return Intent(
        task=task, constraints=constraints, out_of_scope=out_of_scope, priority_files=priority_files
    )


def _extract_task_from_prompt(prompt: str) -> str:
    """
    Extract the main task from a user prompt.

    Simplifies the prompt to a concise task statement.
    Handles common patterns like "I want to...", "Can you...", etc.

    Args:
        prompt: User's prompt text

    Returns:
        Simplified task description
    """
    # Remove common prefixes
    prompt = prompt.strip()

    # Handle common patterns
    replacements = [
        ("I want to ", ""),
        ("I need to ", ""),
        ("Can you ", ""),
        ("Could you ", ""),
        ("Please ", ""),
        ("Help me ", ""),
        ("I'd like to ", ""),
        ("Let's ", ""),
    ]

    task = prompt
    for old, new in replacements:
        if task.startswith(old):
            task = new + task[len(old) :]
            break

    # Capitalize first letter
    if task:
        task = task[0].upper() + task[1:]

    # Truncate to reasonable length
    if len(task) > 150:
        task = task[:147] + "..."

    return task


def _extract_constraints(prompt: str) -> list[str]:
    """
    Extract constraints from a user prompt.

    Looks for patterns indicating requirements or restrictions:
    - "Don't..."
    - "Make sure..."
    - "Ensure..."
    - "Keep..."
    - "Avoid..."

    Args:
        prompt: User's prompt text

    Returns:
        List of constraint strings
    """
    constraints = []

    # Split into sentences
    sentences = prompt.replace("\n", ". ").split(". ")

    constraint_patterns = [
        "don't ",
        "do not ",
        "make sure ",
        "ensure ",
        "keep ",
        "avoid ",
        "without ",
        "must not ",
        "shouldn't ",
        "maintain ",
    ]

    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        for pattern in constraint_patterns:
            if pattern in sentence_lower:
                # Clean up and add
                constraint = sentence.strip()
                if constraint and len(constraint) > 10:
                    constraints.append(constraint[:100])  # Limit length
                break

    return constraints


def _infer_out_of_scope(constraints: list[str]) -> list[str]:
    """
    Infer out-of-scope items from constraints.

    For example, "Don't modify tests" implies "Modifying test files" is out of scope.

    Args:
        constraints: List of constraint strings

    Returns:
        List of out-of-scope items
    """
    out_of_scope = []

    patterns = [
        ("don't modify", "Modifying"),
        ("don't add", "Adding"),
        ("don't change", "Changing"),
        ("don't refactor", "Refactoring"),
        ("avoid", ""),
        ("without", ""),
        ("keep.*minimal", "Large-scale changes"),
    ]

    for constraint in constraints:
        constraint_lower = constraint.lower()
        for pattern, replacement in patterns:
            if pattern in constraint_lower:
                # Extract what shouldn't be done
                if replacement:
                    # Find what comes after the pattern
                    parts = constraint_lower.split(pattern)
                    if len(parts) > 1:
                        what = parts[1].strip().split()[0:3]  # Take next few words
                        scope_item = replacement + " " + " ".join(what)
                        out_of_scope.append(scope_item.strip())
                        break

    return out_of_scope


def _identify_priority_files(data) -> list[str]:
    """
    Identify priority files based on modification activity.

    Files that are modified are considered priority files for the task.

    Args:
        data: TranscriptData object from parser

    Returns:
        List of file paths sorted by relevance
    """
    # Files that were modified are definitely priorities
    priority = list(data.files_modified)

    # Limit to top 10 most relevant
    return priority[:10]


def generate_intent_yaml(intent: Intent) -> str:
    """
    Generate YAML representation of an Intent.

    Creates a clean, readable YAML structure that can be saved to
    .mc/intent.yaml for use by agents.

    Args:
        intent: Intent object to serialize

    Returns:
        YAML string

    Example:
        >>> yaml_str = generate_intent_yaml(intent)
        >>> print(yaml_str)
        task: Add source badges to session display
        constraints:
          - Keep changes minimal
        ...
    """
    # Use custom YAML formatting for cleaner output
    data = intent.to_dict()

    # Use yaml.safe_dump with clean formatting
    yaml_str = yaml.safe_dump(
        data, default_flow_style=False, sort_keys=False, allow_unicode=True, width=80
    )

    return yaml_str


def load_intent(mc_dir: Path) -> Optional[Intent]:
    """
    Load intent from .mc/intent.yaml.

    Args:
        mc_dir: Path to .mc directory (typically in project root)

    Returns:
        Intent object if file exists, None otherwise

    Example:
        >>> intent = load_intent(Path(".mc"))
        >>> if intent:
        ...     print(intent.task)
    """
    intent_file = mc_dir / "intent.yaml"

    if not intent_file.exists():
        logger.debug(f"Intent file not found: {intent_file}")
        return None

    try:
        with open(intent_file, "r") as f:
            data = yaml.safe_load(f)

        if not data:
            logger.warning(f"Empty intent file: {intent_file}")
            return None

        return Intent.from_dict(data)

    except yaml.YAMLError as e:
        logger.error(f"Failed to parse intent YAML: {e}")
        return None
    except OSError as e:
        logger.error(f"Failed to read intent file: {e}")
        return None


def save_intent(mc_dir: Path, intent: Intent) -> bool:
    """
    Save intent to .mc/intent.yaml.

    Creates the .mc directory if it doesn't exist.

    Args:
        mc_dir: Path to .mc directory (typically in project root)
        intent: Intent object to save

    Returns:
        True if successful, False otherwise

    Example:
        >>> intent = Intent(task="Add feature X")
        >>> save_intent(Path(".mc"), intent)
        True
    """
    # Ensure .mc directory exists
    try:
        mc_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create .mc directory: {e}")
        return False

    intent_file = mc_dir / "intent.yaml"

    try:
        yaml_str = generate_intent_yaml(intent)
        with open(intent_file, "w") as f:
            f.write(yaml_str)

        logger.info(f"Saved intent to {intent_file}")
        return True

    except OSError as e:
        logger.error(f"Failed to write intent file: {e}")
        return False
