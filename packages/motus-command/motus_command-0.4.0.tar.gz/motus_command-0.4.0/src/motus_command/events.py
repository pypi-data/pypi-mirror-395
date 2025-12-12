"""
MC Event Types

These represent the core events that MC tracks across any AI agent.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class BaseEvent:
    """Base class for all MC events."""

    timestamp: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None

    def to_dict(self) -> dict:
        # Convert CamelCase class name to snake_case type
        class_name = self.__class__.__name__
        type_name = class_name.replace("Event", "").lower()
        return {
            "type": type_name,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class ThinkingEvent(BaseEvent):
    """Represents an AI's internal reasoning/thinking."""

    content: str = ""

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["content"] = self.content
        return d


@dataclass
class ToolEvent(BaseEvent):
    """Represents a tool call by the AI."""

    name: str = ""
    input: dict = field(default_factory=dict)
    output: Optional[Any] = None
    status: str = "running"  # running, success, error
    risk_level: str = "safe"  # safe, low, medium, high, critical
    duration_ms: Optional[int] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "name": self.name,
                "input": self.input,
                "output": str(self.output) if self.output else None,
                "status": self.status,
                "risk_level": self.risk_level,
                "duration_ms": self.duration_ms,
            }
        )
        return d


@dataclass
class DecisionEvent(BaseEvent):
    """Represents a decision point captured from AI reasoning."""

    decision: str = ""
    reasoning: Optional[str] = None
    alternatives: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "decision": self.decision,
                "reasoning": self.reasoning,
                "alternatives": self.alternatives,
            }
        )
        return d


@dataclass
class AgentSpawnEvent(BaseEvent):
    """Represents spawning a subagent."""

    agent_type: str = ""
    description: str = ""
    prompt: str = ""
    model: Optional[str] = None

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "agent_type": self.agent_type,
                "description": self.description,
                "prompt": self.prompt,  # Full prompt - no truncation
                "model": self.model,
            }
        )
        return d


@dataclass
class FileChangeEvent(BaseEvent):
    """Represents a file modification."""

    path: str = ""
    operation: str = ""  # read, write, edit, delete
    lines_added: int = 0
    lines_removed: int = 0
    diff: Optional[str] = None  # Unified diff for edit operations

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "path": self.path,
                "operation": self.operation,
                "lines_added": self.lines_added,
                "lines_removed": self.lines_removed,
                "diff": self.diff,
            }
        )
        return d


@dataclass
class ErrorEvent(BaseEvent):
    """Represents an error during execution."""

    message: str = ""
    error_type: str = ""  # "tool_error", "api_error", "parse_error", "safety"
    tool_name: Optional[str] = None  # Tool that caused error, if applicable
    recoverable: bool = True
    retry_count: int = 0

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "message": self.message,
                "error_type": self.error_type,
                "tool_name": self.tool_name,
                "recoverable": self.recoverable,
                "retry_count": self.retry_count,
            }
        )
        return d


@dataclass
class SessionEndEvent(BaseEvent):
    """Represents session completion with finish reason."""

    finish_reason: str = ""  # "stop", "max_tokens", "safety", "error", "user_cancel"
    final_status: str = ""  # "success", "partial", "failed"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "finish_reason": self.finish_reason,
                "final_status": self.final_status,
            }
        )
        return d
