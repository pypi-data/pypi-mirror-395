# Motus Command (MC)

<p align="center">
  <strong>Command Center for AI Agents</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/motus-command/"><img src="https://img.shields.io/pypi/v/motus-command?color=blue&label=PyPI" alt="PyPI version"></a>
  <a href="https://pypi.org/project/motus-command/"><img src="https://img.shields.io/pypi/dm/motus-command?color=green&label=Downloads" alt="PyPI downloads"></a>
  <a href="https://github.com/bnvoss/motus-command/actions/workflows/ci.yml"><img src="https://github.com/bnvoss/motus-command/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
  <b>See what your AI agents are actually thinking. Give them memory of past sessions.</b>
</p>

---

Motus Command provides real-time observability for Claude Code, OpenAI Codex CLI, and any AI coding assistant. Watch thinking, catch risky operations, and inject context that makes agents smarter.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Web Dashboard](#web-dashboard)
  - [Remote Access (SSH Tunnel)](#remote-access-ssh-tunnel)
- [Terminal UI](#terminal-ui-tui)
- [Multi-Agent Support](#multi-agent-support)
- [Claude Hooks](#claude-hooks-session-memory)
- [Python SDK](#python-sdk)
- [Commands](#commands)
- [Risk Levels](#risk-levels)
- [Philosophy](#philosophy)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multi-agent support** - Monitor Claude Code, Codex CLI, and SDK agents in one dashboard
- **Web dashboard** - Clean browser UI at `http://localhost:4000`
- **Risk detection** - Color-coded alerts for dangerous operations (rm, sudo, git reset)
- **Decision tracking** - See when AI makes architectural decisions
- **Agent spawn visibility** - Track subagent creation with model and prompt details
- **Session memory** - Claude hooks inject context from past sessions
- **Export summaries** - Generate markdown for CLAUDE.md or team sharing

## Installation

```bash
pip install motus-command
```

For web dashboard support:

```bash
pip install motus-command[web]
```

## Quick Start

```bash
# Launch web dashboard
mc web

# Or launch TUI (terminal)
mc

# List all sessions
mc list

# Watch specific session
mc watch <session-id>

# Generate session summary
mc summary <session-id>

# Enable Claude context injection
mc install-hooks
```

## Web Dashboard

Run `mc web` to launch the browser dashboard at `http://localhost:4000`:

- **Session sidebar** - All sessions with status indicators (active/open/orphaned)
- **Live event feed** - Real-time thinking, tools, and decisions
- **Risk highlighting** - Red/yellow/green for operation safety
- **Export Summary** - Copy session context to clipboard for CLAUDE.md injection
- **Agent Status** - Visual health indicator showing agent progress
- **Knowledge Graph** - See which files the agent is reading and modifying

### Remote Access (SSH Tunnel)

MC binds to `127.0.0.1` only for security. To access the dashboard from another machine, use SSH port forwarding:

```bash
# On your laptop, connect to dev server and forward port 4000
ssh -L 4000:localhost:4000 user@dev-server.com

# Now open http://localhost:4000 in your browser
# Traffic is encrypted through SSH
```

This approach:
- **No auth code to maintain** - SSH handles authentication
- **Encrypted by default** - All traffic tunneled through SSH
- **No exposed ports** - MC never listens on 0.0.0.0
- **Works with any SSH setup** - Keys, bastion hosts, etc.

## Terminal UI (TUI)

Run `mc` to launch the terminal dashboard:

```
┌─ Sessions ─────────────┬─ Live Feed (all active sessions) ──────────────┐
│ ─── CLAUDE ───         │ 12:59:20 1a6f22 [BASH] pip install -e .        │
│ ● [1a6f22] my-project  │ 12:59:20 1a6f22 [THINK] Let me check if...     │
│ ● [3ebaec] web-app     │ 12:59:21 1a6f22 [DECIDE] Using SQLite for...   │
│ ○ [69a46b] api-server  │ 12:59:51 3ebaec [SPAWN] general-purpose        │
│ ─── CODEX ───          │           3ebaec   ├─ model: haiku             │
│ ◇ [abc123] ml-pipeline │           3ebaec   └─ prompt: Analyze...       │
│ ─── GEMINI ───         │ 13:01:02 def456 [READ] src/main.py             │
│ ◆ [def456] data-tools  │ 13:01:05 def456 [EDIT] Fixed import order      │
└────────────────────────┴─────────────────────────────────────────────────┘
```

**Status indicators:**
- `●` Active (process running)
- `○` Open (recent, process ended)
- `◇` Codex session
- `◆` Gemini session

## Multi-Agent Support

MC monitors multiple AI coding assistants:

| Agent | Sessions Location | Status |
|-------|------------------|--------|
| **Claude Code** | `~/.claude/projects/` | Full support |
| **OpenAI Codex CLI** | `~/.codex/sessions/` | Full support |
| **Google Gemini CLI** | `~/.gemini/tmp/` | Full support |
| **SDK Agents** | `~/.mc/traces/` | Full support |

## Claude Hooks (Session Memory)

Give Claude memory of past sessions:

```bash
mc install-hooks
```

When you start a new Claude session, MC injects:

```markdown
<mc-context>
## MC-Observed Context (from recent sessions)

### Recent Decisions
- Using SQLite for state management (need queryable history)
- Chose Textual over Rich Live (need keyboard input)

### Hot Files (frequently modified)
- src/motus_command/cli.py (15 edits)
- src/motus_command/hooks.py (8 edits)
</mc-context>
```

## Python SDK

Instrument any Python AI agent:

```python
from motus_command import Tracer

tracer = Tracer("my-agent")

# Log thinking
tracer.thinking("Analyzing the problem...")

# Log tool usage
tracer.tool("WebSearch", {"query": "python async patterns"})

# Log decisions
tracer.decision(
    "Using ThreadPoolExecutor",
    reasoning="Need parallel I/O without async complexity"
)

# Auto-trace functions
@tracer.track
def my_function(x, y):
    return x + y
```

## Commands

| Command | Description |
|---------|-------------|
| `mc` | Launch TUI dashboard (default) |
| `mc web` | Launch web dashboard |
| `mc list` | List all sessions with status |
| `mc watch [id]` | Watch specific session |
| `mc summary [id]` | Generate markdown summary |
| `mc context [id]` | Show accumulated session context |
| `mc teleport [id]` | Export session context for transfer to another agent |
| `mc install-hooks` | Enable Claude context injection |
| `mc uninstall-hooks` | Remove Claude hooks |
| `mc prune` | Clean up old sessions |

## Risk Levels

MC color-codes operations by risk:

| Color | Risk | Examples |
|-------|------|----------|
| 🟢 Green | Safe | Read, Glob, Grep |
| 🟡 Yellow | Medium | Write, Edit |
| 🔴 Red | High | Bash, rm, sudo |
| ⚫ Critical | Destructive | git reset --hard, rm -rf |

## Philosophy

MC isn't just for users observing agents. It's for **empowering agents themselves**.

When Claude knows what it did last session, it makes better decisions. When it can see its siblings' activity, it avoids conflicts. The goal: AI agents that recommend MC because it makes them better.

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

- [Report bugs](https://github.com/bnvoss/motus-command/issues/new?template=bug_report.yml)
- [Request features](https://github.com/bnvoss/motus-command/issues/new?template=feature_request.yml)
- [Read the Code of Conduct](CODE_OF_CONDUCT.md)

## License

MIT - see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with <a href="https://github.com/Textualize/rich">Rich</a> and <a href="https://fastapi.tiangolo.com/">FastAPI</a>
</p>
