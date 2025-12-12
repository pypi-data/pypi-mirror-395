"""
MC Web UI - Lightweight browser-based Command Center.

Optional module: pip install motus-command[web]
Fallback: CLI mode if dependencies not available.
"""

import asyncio
import socket
import sys
import webbrowser
from pathlib import Path
from typing import Optional

# Check for optional dependencies
try:
    import uvicorn
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    from fastapi.staticfiles import StaticFiles

    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

# Static files and template paths
UI_DIR = Path(__file__).parent
STATIC_DIR = UI_DIR / "static"
TEMPLATES_DIR = UI_DIR / "templates"

# Import from parent - try package imports first, fall back for direct module imports
try:
    from motus_command.cli import (
        TaskEvent,
        ThinkingEvent,
        ToolEvent,
        analyze_session,
        extract_decisions,
        parse_line_by_source,
        parse_session_events,
    )
except ImportError:
    # Fallback for direct module imports in tests or standalone runs
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from cli import (  # noqa: E402, I001
        TaskEvent,
        ThinkingEvent,
        ToolEvent,
        analyze_session,
        extract_decisions,
        parse_line_by_source,
        parse_session_events,
    )

# Import transcript parser for advanced data extraction
try:
    from motus_command.transcript_parser import TranscriptParser
except ImportError:
    from transcript_parser import TranscriptParser

# Import logger - with fallback for direct module imports in tests
try:
    from motus_command.logging import get_logger

    logger = get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

# Import drift detector for intent tracking
try:
    from motus_command.drift_detector import DriftDetector, get_drift_detector
except ImportError:
    try:
        from drift_detector import DriftDetector, get_drift_detector
    except ImportError:
        get_drift_detector = None
        DriftDetector = None

# Import secret redaction utility
try:
    from motus_command.commands.utils import redact_secrets
except ImportError:
    try:
        from commands.utils import redact_secrets
    except ImportError:
        # Fallback: no-op if import fails
        def redact_secrets(text: str) -> str:
            return text


# Import orchestrator for unified session management
try:
    from motus_command.orchestrator import get_orchestrator
    from motus_command.protocols import EventType, UnifiedEvent
except ImportError:
    try:
        from orchestrator import get_orchestrator
        from protocols import EventType, UnifiedEvent
    except ImportError:
        get_orchestrator = None
        EventType = None
        UnifiedEvent = None


# Note: Dashboard HTML served from templates/dashboard.html
# Static assets: static/dashboard.js, static/dashboard.css
# Embedded HTML/CSS/JS removed in v0.3.2 (-2,005 lines)


def calculate_health(ctx: dict, drift_state: Optional[dict] = None) -> dict:
    """
    Pure Python health calculation. Zero dependencies.

    Returns health score (0-100) and status based on:
    - Error rate (errors hurt health)
    - Activity productivity (edits/writes vs reads)
    - Decision consistency
    - Tool efficiency
    - Drift detection (overrides status if drifting)
    """
    if not ctx:
        return {"health": 50, "status": "waiting", "metrics": {}, "drift": None}

    # Friction score: starts at 100, drops 15 per friction point (gentler)
    # Friction is normal - it's Claude working through challenges
    friction_count = ctx.get("friction_count", 0)
    friction_score = max(0, 100 - (friction_count * 15))

    # Activity score: productive tools (Edit, Write) vs total
    tools = ctx.get("tool_count", {})
    total_tools = sum(tools.values()) if tools else 0
    productive = tools.get("Edit", 0) + tools.get("Write", 0)
    read_heavy = tools.get("Read", 0) + tools.get("Glob", 0) + tools.get("Grep", 0)

    if total_tools == 0:
        activity_score = 50  # No activity yet
    elif productive > 0:
        activity_score = min(100, 60 + (productive * 8))  # Productive work
    elif read_heavy > 5:
        activity_score = 70  # Research phase, acceptable
    else:
        activity_score = 50

    # Progress score: files modified = progress
    files_modified = len(ctx.get("files_modified", []))
    progress_score = min(100, 40 + (files_modified * 15))

    # Decision score: having decisions = clarity
    decisions = ctx.get("decisions", [])
    decision_score = min(100, 50 + (len(decisions) * 10))

    # Weighted health calculation (friction matters less than before)
    health = int(
        friction_score * 0.20  # Friction is normal, lower weight
        + activity_score * 0.30  # Productivity matters more
        + progress_score * 0.30  # Actual progress matters more
        + decision_score * 0.20  # Clarity of intent
    )
    health = max(10, min(95, health))  # Clamp to 10-95

    # Status determination - use gentler language
    if friction_count > 3:
        status = "working_through_it"
    elif health >= 75:
        status = "on_track"
    elif health >= 50:
        status = "exploring"
    else:
        status = "needs_attention"

    # Drift detection overrides status if drifting
    drift_info = None
    if drift_state and drift_state.get("is_drifting"):
        status = "drifting"
        drift_info = {
            "score": drift_state.get("drift_score", 0),
            "signals": [
                {"type": s.get("signal_type"), "description": s.get("description")}
                for s in drift_state.get("signals", [])[-3:]  # Last 3 signals
            ],
        }

    return {
        "health": health,
        "status": status,
        "drift": drift_info,
        "metrics": {
            "friction": friction_score,
            "activity": activity_score,
            "progress": progress_score,
            "decisions": decision_score,
        },
    }


class MCWebServer:
    """Lightweight WebSocket server for MC Web UI."""

    def __init__(self, port: int = 0):
        self.port = port or self._find_free_port()
        self.app = None
        self.clients: set[WebSocket] = set()
        self.session_positions: dict[str, int] = {}
        self.session_contexts: dict[str, dict] = {}
        self.agent_stacks: dict[str, list[str]] = {}  # session_id -> [agent_types]
        self.running = False
        self.poll_counter: dict[WebSocket, int] = {}  # Track poll counts per client
        self.known_sessions: dict[WebSocket, set] = {}  # Track known session IDs per client
        # Drift detector for intent tracking
        self.drift_detector = get_drift_detector() if get_drift_detector else None
        # Track parsing errors
        self.parsing_errors: dict[str, str] = {}  # session_id -> error message

    def _find_free_port(self) -> int:
        """Find an available port.

        In sandboxed CI environments, socket binding may be restricted.
        Falls back to a non-privileged default port if dynamic allocation fails.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 0))
                return s.getsockname()[1]
        except OSError:
            # Sandboxed environment - return default port without referencing self
            return 4000

    def create_app(self) -> FastAPI:
        """Create the FastAPI application."""
        app = FastAPI(title="MC Web UI")

        # Mount static files directory
        if STATIC_DIR.exists():
            app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

        @app.get("/", response_class=HTMLResponse)
        async def dashboard():
            # Serve from template file (required - no embedded fallback)
            template_file = TEMPLATES_DIR / "dashboard.html"
            if not template_file.exists():
                raise FileNotFoundError(
                    f"Dashboard template not found: {template_file}. "
                    "Ensure motus-command is properly installed with template files."
                )
            from motus_command import __version__

            content = template_file.read_text()
            content = content.replace("{{ version }}", __version__)
            return HTMLResponse(content=content)

        @app.get("/api/summary/{session_id}")
        async def get_summary(session_id: str):
            """Generate session summary markdown (same as CLI mc summary)."""
            sessions = get_orchestrator().discover_all(max_age_hours=168)  # 7 days
            target_session = None
            for s in sessions:
                if s.session_id.startswith(session_id):
                    target_session = s
                    break

            if not target_session:
                return {"error": f"Session not found: {session_id}"}

            try:
                stats = analyze_session(target_session)
                decisions = extract_decisions(target_session.file_path)

                # Generate rich markdown for CLAUDE.md
                summary = f"""## MC Session Memory

> Auto-generated by Motus Command. Inject this into CLAUDE.md for agent continuity.

### Session Info
- **ID:** `{target_session.session_id[:12]}`
- **Project:** `{target_session.project_path}`
- **Size:** {target_session.size // 1024}KB
- **Last Active:** {target_session.last_modified.strftime("%Y-%m-%d %H:%M")}

### Activity Summary
| Metric | Count |
|--------|-------|
| Thinking blocks | {stats.thinking_count} |
| Tool calls | {stats.tool_count} |
| Agents spawned | {stats.agent_count} |
| Files modified | {len(stats.files_modified)} |
| High-risk ops | {stats.high_risk_ops} |

### Files Modified This Session
"""
                if stats.files_modified:
                    for f in list(stats.files_modified)[:15]:
                        short_path = f
                        if len(f) > 60:
                            parts = f.split("/")
                            short_path = "/".join(parts[-3:]) if len(parts) > 3 else f
                        summary += f"- `{short_path}`\n"
                else:
                    summary += "- None yet\n"

                summary += "\n### Decisions Made (from thinking blocks)\n"
                if decisions:
                    for d in decisions[:8]:
                        summary += f"- {d}\n"
                else:
                    summary += "- No explicit decisions captured\n"

                return {
                    "session_id": target_session.session_id,
                    "summary": summary,
                    "project": target_session.project_path,
                }
            except Exception as e:
                logger.error(f"Error generating summary: {e}")
                return {"error": str(e)}

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.clients.add(websocket)
            try:
                # Send initial sessions and track known sessions
                orchestrator = get_orchestrator()
                sessions = orchestrator.discover_all(max_age_hours=24)
                self.known_sessions[websocket] = {s.session_id for s in sessions[:10]}

                # Build session data with last_action for crashed sessions
                session_data = []
                for s in sessions[:10]:
                    data = {
                        "session_id": s.session_id,
                        "project_path": s.project_path,
                        "status": s.status.value,  # Convert enum to string
                        "source": s.source.value,  # Convert enum to string
                    }
                    # Add last_action for crashed sessions
                    if s.status.value == "crashed":
                        builder = orchestrator.get_builder(s.source)
                        if builder:
                            data["last_action"] = builder.get_last_action(s.file_path)
                    session_data.append(data)

                await websocket.send_json(
                    {
                        "type": "sessions",
                        "sessions": session_data,
                    }
                )

                # Handle messages
                while True:
                    try:
                        data = await asyncio.wait_for(websocket.receive_json(), timeout=1.0)
                        await self._handle_client_message(websocket, data)
                    except asyncio.TimeoutError:
                        # Poll for new events
                        await self._poll_events(websocket)
                    except WebSocketDisconnect:
                        break
            finally:
                self.clients.discard(websocket)
                self.known_sessions.pop(websocket, None)
                self.poll_counter.pop(websocket, None)

        return app

    async def _handle_client_message(self, websocket: WebSocket, data: dict):
        """Handle incoming client messages."""
        msg_type = data.get("type")
        if msg_type == "select_session":
            session_id = data.get("session_id")
            # Send context if available
            if session_id and session_id in self.session_contexts:
                await websocket.send_json(
                    {
                        "type": "context",
                        "session_id": session_id,
                        "context": self.session_contexts[session_id],
                    }
                )
            # Load FULL history and intents for selected session
            if session_id:
                await self._send_session_history(websocket, session_id)
                await self._send_session_intents(websocket, session_id)
        elif msg_type == "request_backfill":
            # Load recent historical events for all active sessions
            await self._send_backfill(websocket, data.get("limit", 30))
        elif msg_type == "request_intents":
            # Get user intents for a session using enhanced parser
            session_id = data.get("session_id")
            if session_id:
                await self._send_session_intents(websocket, session_id)
        elif msg_type == "heartbeat":
            pass  # Keep-alive

    async def _send_session_history(self, websocket: WebSocket, session_id: str):
        """Send FULL history for a specific session."""
        sessions = get_orchestrator().discover_all(max_age_hours=168)  # 7 days
        target_session = None

        for session in sessions:
            if session.session_id == session_id:
                target_session = session
                break

        if not target_session:
            return

        history_events = []
        try:
            # Use source-aware parsing for Claude/Codex/SDK sessions
            source = target_session.source.value
            for event in parse_session_events(target_session.file_path, source=source):
                event_data = self._format_event_for_client(
                    event, session_id, target_session.project_path, source=source
                )
                if event_data:
                    history_events.append(event_data)
        except OSError as e:
            logger.debug(f"Error reading session file: {e}")
            return
        except Exception as e:
            logger.warning(f"Unexpected error loading session history: {e}")
            return

        # Send full history (up to 500 events for performance)
        await websocket.send_json(
            {
                "type": "session_history",
                "session_id": session_id,
                "events": history_events[-500:],
                "total_events": len(history_events),
            }
        )

    async def _send_backfill(self, websocket: WebSocket, limit: int = 30):
        """Send historical events to client on connect/refresh."""
        sessions = get_orchestrator().discover_all(max_age_hours=24)
        backfill_events = []

        for session in sessions[:5]:  # Limit to 5 most recent sessions
            try:
                source = session.source.value

                if source in ("codex", "gemini"):
                    # For Codex/Gemini, use unified parser (different file formats)
                    session_events = []
                    for event in parse_session_events(session.file_path, source=source):
                        event_data = self._format_event_for_client(
                            event, session.session_id, session.project_path, source=source
                        )
                        if event_data:
                            session_events.append(event_data)
                    # Take last 10 events per session for backfill
                    backfill_events.extend(session_events[-10:])
                else:
                    # For Claude/SDK, read last ~10KB for efficiency (JSONL format)
                    file_size = session.file_path.stat().st_size
                    read_start = max(0, file_size - 10000)

                    with open(session.file_path, "r") as f:
                        f.seek(read_start)
                        content = f.read()

                    # Parse events using source-aware parser
                    for line in content.strip().split("\n"):
                        if line.strip():
                            events = parse_line_by_source(line, source)
                            for event in events:
                                event_data = self._format_event_for_client(
                                    event, session.session_id, session.project_path, source=source
                                )
                                if event_data:
                                    backfill_events.append(event_data)
            except OSError as e:
                logger.debug(f"Error reading session file {session.file_path}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Unexpected error processing session {session.session_id}: {e}")
                continue

        # Sort by timestamp and take most recent
        backfill_events = backfill_events[-limit:]

        await websocket.send_json({"type": "backfill", "events": backfill_events})

    async def _send_session_intents(self, websocket: WebSocket, session_id: str):
        """Extract and send user intents for a session using enhanced parser."""
        sessions = get_orchestrator().discover_all(max_age_hours=168)  # 7 days
        target_session = None

        for session in sessions:
            if session.session_id == session_id:
                target_session = session
                break

        if not target_session:
            return

        try:
            # Use enhanced parser to extract intents
            parser = TranscriptParser(extract_file_snapshots=False)
            data = parser.parse_file(
                target_session.file_path,
                session_id=session_id,
                project_path=target_session.project_path,
            )

            # Format intents for client
            intents = []
            for intent in data.user_intents:
                intents.append(
                    {
                        "prompt": intent.prompt,
                        "timestamp": intent.timestamp.strftime("%H:%M:%S"),
                        "completed": intent.completed,
                    }
                )

            # Also include token stats and file activity
            await websocket.send_json(
                {
                    "type": "session_intents",
                    "session_id": session_id,
                    "intents": intents,
                    "stats": {
                        "total_input_tokens": data.total_input_tokens,
                        "total_output_tokens": data.total_output_tokens,
                        "cache_hit_rate": f"{data.overall_cache_hit_rate:.1f}%",
                        "models_used": list(data.models_used),
                        "files_read": len(data.files_read),
                        "files_modified": len(data.files_modified),
                        "errors": len(data.errors),
                    },
                }
            )
        except Exception as e:
            logger.warning(f"Error extracting intents for session {session_id}: {e}")

    def _format_event_for_client(
        self, event, session_id: str, project_path: str, agent_depth: int = 0, source: str = ""
    ) -> dict:
        """Format an event for sending to the client.

        Note: We use type().__name__ instead of isinstance() to handle module
        path differences between different import styles (e.g., 'cli.ToolEvent'
        vs 'motus_command.cli.ToolEvent').
        """
        time_str = event.timestamp.strftime("%H:%M:%S")
        event_type_name = type(event).__name__

        if event_type_name == "ThinkingEvent":
            content = event.content[:200] + "..." if len(event.content) > 200 else event.content
            return {
                "event_type": "thinking",
                "timestamp": time_str,
                "session_id": session_id,
                "content": content.replace("\n", " "),
                "agent_depth": agent_depth,
                "source": source,
            }
        elif event_type_name == "TaskEvent":
            return {
                "event_type": "spawn",
                "timestamp": time_str,
                "session_id": session_id,
                "content": f"{event.subagent_type}: {event.description}",
                "tool_name": "SPAWN",
                "agent_type": event.subagent_type,
                "agent_depth": agent_depth,
                "description": event.description,
                "model": event.model,
                "prompt": getattr(event, "prompt", ""),
                "source": source,
            }
        elif event_type_name == "ToolEvent":
            # Get file path for display
            file_path = ""
            if event.name in ("Read", "Edit", "Write"):
                file_path = event.input.get("file_path", "")
            return {
                "event_type": "tool",
                "timestamp": time_str,
                "session_id": session_id,
                "content": self._format_tool_content(event),
                "tool_name": event.name,
                "risk_level": event.risk_level,
                "agent_depth": agent_depth,
                "file_path": file_path,
                "source": source,
            }
        return None

    def _format_tool_content(self, event: ToolEvent) -> str:
        """Format tool event content with secret redaction."""
        if event.name == "Read":
            path = event.input.get("file_path", "")
            return f"📖 {path.split('/')[-1] if '/' in path else path}"
        elif event.name == "Edit":
            path = event.input.get("file_path", "")
            return f"✏️ {path.split('/')[-1] if '/' in path else path}"
        elif event.name == "Write":
            path = event.input.get("file_path", "")
            return f"📝 {path.split('/')[-1] if '/' in path else path}"
        elif event.name == "Bash":
            cmd = redact_secrets(event.input.get("command", "")[:60])
            return f"💻 {cmd}"
        elif event.name == "Glob":
            pattern = event.input.get("pattern", "")
            return f"🔍 {pattern}"
        elif event.name == "Grep":
            pattern = redact_secrets(event.input.get("pattern", ""))
            return f"🔎 {pattern}"
        else:
            return f"⚡ {event.name}"

    async def _poll_events(self, websocket: WebSocket):
        """Poll for new events from Claude sessions."""
        sessions = get_orchestrator().discover_all(max_age_hours=24)

        # Check for new sessions and send updates
        current_session_ids = {s.session_id for s in sessions[:10]}
        known = self.known_sessions.get(websocket, set())
        new_sessions = current_session_ids - known

        if new_sessions:
            # New session detected - send updated session list
            await websocket.send_json(
                {
                    "type": "sessions",
                    "sessions": [
                        {
                            "session_id": s.session_id,
                            "project_path": s.project_path,
                            "status": s.status.value,  # Convert enum to string
                            "source": s.source.value,  # Convert enum to string
                        }
                        for s in sessions[:10]
                    ],
                    "degraded": get_orchestrator().is_process_degraded(),
                    "errors": self.parsing_errors,
                }
            )
            self.known_sessions[websocket] = current_session_ids

        # Process ALL sessions (including orphaned - for history viewing)
        for session in sessions:
            session_id = session.session_id
            last_pos = self.session_positions.get(session_id, 0)

            # Initialize context if needed
            if session_id not in self.session_contexts:
                self.session_contexts[session_id] = {
                    "files_read": [],
                    "files_modified": [],
                    "agent_tree": [],
                    "decisions": [],
                    "tool_count": {},
                }

            try:
                source = session.source.value
                current_size = session.file_path.stat().st_size

                if source == "gemini":
                    # Gemini is a single JSON file - re-parse when file changes
                    if current_size != last_pos:
                        self.session_positions[session_id] = current_size
                        for event in parse_session_events(session.file_path, source=source):
                            await self._process_and_send_event(
                                websocket, event, session_id, session.project_path
                            )
                elif current_size > last_pos:
                    # Claude/Codex/SDK use JSONL - read new lines incrementally
                    with open(session.file_path, "r") as f:
                        f.seek(last_pos)
                        new_content = f.read()
                        self.session_positions[session_id] = f.tell()

                    for line in new_content.strip().split("\n"):
                        if line.strip():
                            # Check for user messages to set intent for drift detection
                            self._check_for_user_intent(line, session_id, session.project_path)

                            events = parse_line_by_source(line, source=source)
                            for event in events:
                                await self._process_and_send_event(
                                    websocket, event, session_id, session.project_path
                                )
            except OSError as e:
                logger.debug(f"Error reading session file {session.file_path}: {e}")
                self.parsing_errors[session_id] = f"File read error: {str(e)[:50]}"
            except Exception as e:
                logger.warning(f"Unexpected error polling session {session_id}: {e}")
                self.parsing_errors[session_id] = f"Parsing error: {str(e)[:50]}"

    def _check_for_user_intent(self, line: str, session_id: str, project_path: str):
        """Check if line contains a user message and set intent for drift detection."""
        if not self.drift_detector:
            return

        try:
            import json

            data = json.loads(line)

            # Claude transcript format: {"type": "user", "message": {"content": [...]}}
            if data.get("type") == "user":
                message = data.get("message", {})
                content = message.get("content", [])
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        prompt = block.get("text", "").strip()
                        if prompt and len(prompt) > 5:
                            # Set intent with both user message and project context
                            intent_text = f"{prompt} (working in {project_path})"
                            self.drift_detector.set_intent(session_id, intent_text)
                            logger.debug(f"Set intent for {session_id[:8]}: {prompt[:50]}...")
                            return

            # Codex format: {"type": "event_msg", "payload": {"type": "user_message", ...}}
            if data.get("type") == "event_msg":
                payload = data.get("payload", {})
                if payload.get("type") == "user_message" or payload.get("role") == "user":
                    content = payload.get("content", "")
                    if isinstance(content, list):
                        content = " ".join(
                            str(c.get("text", c)) for c in content if isinstance(c, dict)
                        )
                    if content and len(content) > 5:
                        intent_text = f"{content} (working in {project_path})"
                        self.drift_detector.set_intent(session_id, intent_text)
                        logger.debug(f"Set intent for {session_id[:8]}: {content[:50]}...")

        except (json.JSONDecodeError, TypeError, AttributeError):
            pass  # Not a valid JSON line or unexpected format

    async def _process_and_send_event(
        self, websocket: WebSocket, event, session_id: str, project_path: str
    ):
        """Process event and send to client."""
        ctx = self.session_contexts[session_id]
        time_str = event.timestamp.strftime("%H:%M:%S")

        # Check if this is a UnifiedEvent with AGENT_SPAWN type
        is_unified_spawn = (
            UnifiedEvent
            and isinstance(event, UnifiedEvent)
            and EventType
            and event.event_type == EventType.AGENT_SPAWN
        )

        # SPAWN events are sub-agents (depth 1), everything else is main agent (depth 0)
        # We can't reliably track sub-agent boundaries beyond the spawn itself
        agent_depth = 1 if (isinstance(event, TaskEvent) or is_unified_spawn) else 0
        agent_type = None
        if isinstance(event, TaskEvent):
            agent_type = event.subagent_type
        elif is_unified_spawn:
            agent_type = event.agent_type

        if isinstance(event, ThinkingEvent):
            content = event.content[:200] + "..." if len(event.content) > 200 else event.content
            # Redact any secrets in thinking content
            content = redact_secrets(content)

            # Extract decisions from thinking (same logic as TUI)
            decision_markers = ["i'll ", "i decided", "let me", "i should", "i'm going to"]
            content_lower = event.content.lower()
            for marker in decision_markers:
                if marker in content_lower:
                    # Extract the decision sentence
                    idx = content_lower.find(marker)
                    end_idx = min(idx + 80, len(event.content))
                    decision = event.content[idx:end_idx].replace("\n", " ").strip()
                    # Redact secrets in decisions
                    decision = redact_secrets(decision)
                    if decision and decision not in ctx.get("decisions", []):
                        if "decisions" not in ctx:
                            ctx["decisions"] = []
                        ctx["decisions"].append(
                            decision[:60] + "..." if len(decision) > 60 else decision
                        )
                        ctx["decisions"] = ctx["decisions"][-5:]  # Keep last 5
                    break

            # Detect ACTUAL system errors only (not Claude discussing challenges)
            # These are output patterns that indicate real failures, not reasoning
            actual_error_patterns = [
                "traceback (most recent call last)",  # Python stack trace
                "syntaxerror:",  # Python syntax error
                "typeerror:",  # Python type error
                "nameerror:",  # Python name error
                "command not found",  # Bash error
                "permission denied",  # File system error
                "no such file or directory",  # Missing file
            ]
            has_error = any(p in content_lower for p in actual_error_patterns)
            if has_error:
                ctx["friction_count"] = ctx.get("friction_count", 0) + 1

            await websocket.send_json(
                {
                    "type": "event",
                    "event": {
                        "event_type": "thinking",
                        "timestamp": time_str,
                        "session_id": session_id,
                        "content": content.replace("\n", " "),
                        "agent_depth": agent_depth,
                        "agent_type": agent_type,
                        "has_error": has_error,
                    },
                }
            )

        elif isinstance(event, TaskEvent):
            # Legacy TaskEvent handling (from parse_line_by_source)
            # Redact secrets in task description and prompt
            desc = redact_secrets(event.description[:50])
            prompt = redact_secrets(event.prompt[:100]) if event.prompt else ""
            full_prompt = redact_secrets(event.prompt) if event.prompt else ""

            # Track agent spawn in context (for display)
            ctx["agent_tree"].append(
                {
                    "type": event.subagent_type,
                    "desc": desc,
                    "prompt": prompt,
                    "full_prompt": full_prompt,
                }
            )
            ctx["agent_tree"] = ctx["agent_tree"][-5:]

            await websocket.send_json(
                {
                    "type": "event",
                    "event": {
                        "event_type": "spawn",
                        "timestamp": time_str,
                        "session_id": session_id,
                        "content": f"{event.subagent_type}: {desc}",
                        "tool_name": "SPAWN",
                        "agent_depth": agent_depth,
                        "agent_type": event.subagent_type,
                        "description": desc,
                        "model": event.model,
                        "prompt": full_prompt,  # Include full prompt
                        "context": "",  # Legacy events don't have context field
                    },
                }
            )

            # Send updated context
            await websocket.send_json({"type": "context", "session_id": session_id, "context": ctx})

        elif is_unified_spawn:
            # UnifiedEvent with AGENT_SPAWN type (from orchestrator/builders)
            # Extract full data from the event
            desc = redact_secrets(event.agent_description[:50]) if event.agent_description else ""
            full_desc = redact_secrets(event.agent_description) if event.agent_description else ""
            full_prompt = redact_secrets(event.agent_prompt) if event.agent_prompt else ""
            context_text = event.raw_data.get("context", "") if event.raw_data else ""
            full_context = redact_secrets(context_text) if context_text else ""

            # Track agent spawn in context (for display)
            ctx["agent_tree"].append(
                {
                    "type": event.agent_type or "general",
                    "desc": desc,
                    "prompt": full_prompt[:100] if full_prompt else "",
                    "full_prompt": full_prompt,
                    "context": full_context,
                }
            )
            ctx["agent_tree"] = ctx["agent_tree"][-5:]

            await websocket.send_json(
                {
                    "type": "event",
                    "event": {
                        "event_type": "spawn",
                        "timestamp": time_str,
                        "session_id": session_id,
                        "content": f"{event.agent_type}: {desc}",
                        "tool_name": "SPAWN",
                        "agent_depth": agent_depth,
                        "agent_type": event.agent_type,
                        "description": full_desc,  # Full description for expandable
                        "model": event.agent_model or event.model,
                        "prompt": full_prompt,  # Full prompt for expandable
                        "context": full_context,  # Full context for expandable
                    },
                }
            )

            # Send updated context
            await websocket.send_json({"type": "context", "session_id": session_id, "context": ctx})

        elif isinstance(event, ToolEvent):
            # Track tool usage
            ctx["tool_count"][event.name] = ctx["tool_count"].get(event.name, 0) + 1

            # Track file operations and get file path
            file_path = ""
            if event.name == "Read":
                path = event.input.get("file_path", "")
                file_path = path
                filename = path.split("/")[-1] if "/" in path else path
                if filename and filename not in ctx["files_read"]:
                    ctx["files_read"].append(filename)
                    ctx["files_read"] = ctx["files_read"][-10:]

            elif event.name in ("Edit", "Write"):
                path = event.input.get("file_path", "")
                file_path = path
                filename = path.split("/")[-1] if "/" in path else path
                if filename and filename not in ctx["files_modified"]:
                    ctx["files_modified"].append(filename)

            # Drift detection: check if this action drifts from intent
            drift_state = None
            if self.drift_detector:
                drift_result = self.drift_detector.check_action(
                    session_id=session_id,
                    tool_name=event.name,
                    file_path=file_path if file_path else None,
                    tool_input=event.input,
                )
                if drift_result.is_drifting:
                    drift_state = {
                        "is_drifting": drift_result.is_drifting,
                        "drift_score": drift_result.drift_score,
                        "signals": [
                            {"signal_type": s.signal_type, "description": s.description}
                            for s in drift_result.signals[-3:]
                        ],
                    }
                    ctx["drift_state"] = drift_state

            # Format content based on tool with secret redaction
            if event.name == "Bash":
                content = redact_secrets(event.input.get("command", "")[:60])
            elif event.name in ("Read", "Edit", "Write"):
                content = event.input.get("file_path", "").split("/")[-1]
            elif event.name in ("Glob", "Grep"):
                content = redact_secrets(event.input.get("pattern", "")[:40])
            else:
                content = redact_secrets(str(event.input)[:60])

            await websocket.send_json(
                {
                    "type": "event",
                    "event": {
                        "event_type": "tool",
                        "timestamp": time_str,
                        "session_id": session_id,
                        "tool_name": event.name,
                        "content": content,
                        "risk_level": event.risk_level,
                        "agent_depth": agent_depth,
                        "agent_type": agent_type,
                        "file_path": file_path,
                        "is_drifting": drift_state is not None,
                    },
                }
            )

            # Send updated context with drift state
            await websocket.send_json({"type": "context", "session_id": session_id, "context": ctx})

    def run(self, open_browser: bool = True):
        """Run the web server."""
        if not WEB_AVAILABLE:
            print("Web dependencies not installed.")
            print("Install with: pip install motus-command[web]")
            print("\nFalling back to CLI mode...")
            return False

        self.app = self.create_app()

        print(f"🔮 MC Web UI starting on http://localhost:{self.port}")

        if open_browser:
            # Open browser after short delay
            import threading

            def open_delayed():
                import time

                time.sleep(0.5)
                webbrowser.open(f"http://localhost:{self.port}")

            threading.Thread(target=open_delayed, daemon=True).start()

        try:
            uvicorn.run(
                self.app,
                host="127.0.0.1",
                port=self.port,
                log_level="warning",
            )
        except KeyboardInterrupt:
            print("\n👋 MC Web UI stopped")

        return True


def run_web(port: Optional[int] = None, no_browser: bool = False):
    """Entry point for mc web command."""
    server = MCWebServer(port=port or 0)
    success = server.run(open_browser=not no_browser)
    if not success:
        # Fallback to CLI
        from .tui import main as tui_main

        print("Starting TUI instead...")
        tui_main()


if __name__ == "__main__":
    run_web()
