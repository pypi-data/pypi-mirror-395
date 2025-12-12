"""
MC CLI Commands Module.

Refactored CLI commands extracted from the monolithic cli.py.
Each command gets its own module for maintainability and testability.
"""

# Models and utilities
# Commands
from .context_cmd import context_command
from .hooks_cmd import (
    get_mc_hook_config,
    install_hooks_command,
    uninstall_hooks_command,
)
from .list_cmd import find_active_session, find_claude_sessions, list_sessions
from .models import (
    DESTRUCTIVE_PATTERNS,
    RISK_LEVELS,
    FileChange,
    SessionInfo,
    SessionStats,
    TaskEvent,
    ThinkingEvent,
    ToolEvent,
)
from .prune_cmd import archive_session, delete_session, prune_command
from .summary_cmd import (
    analyze_session,
    extract_decisions,
    generate_agent_context,
    summary_command,
)
from .utils import (
    assess_risk,
    extract_project_path,
    format_age,
    get_last_action,
    get_risk_style,
    parse_content_block,
    tail_file,
)

__all__ = [
    # Models
    "ThinkingEvent",
    "ToolEvent",
    "TaskEvent",
    "FileChange",
    "SessionStats",
    "SessionInfo",
    "RISK_LEVELS",
    "DESTRUCTIVE_PATTERNS",
    # Utilities
    "assess_risk",
    "extract_project_path",
    "format_age",
    "get_last_action",
    "get_risk_style",
    "parse_content_block",
    "tail_file",
    # Commands
    "list_sessions",
    "find_claude_sessions",
    "find_active_session",
    "summary_command",
    "analyze_session",
    "extract_decisions",
    "generate_agent_context",
    "context_command",
    "prune_command",
    "archive_session",
    "delete_session",
    "install_hooks_command",
    "uninstall_hooks_command",
    "get_mc_hook_config",
]
