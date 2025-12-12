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
    from fastapi.responses import FileResponse, HTMLResponse
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


# Embedded dashboard HTML - no external files needed
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MC - Command Center</title>
    <style>
        :root {
            --veritas-mint: #66FFDE;
            --veritas-purple: #AB45C0;
            --veritas-black: #0a0a0a;
            --veritas-dark: #111111;
            --veritas-gray: #1a1a1a;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
            background: var(--veritas-black);
            background-image:
                radial-gradient(ellipse at 20% 20%, rgba(171, 69, 192, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(102, 255, 222, 0.08) 0%, transparent 50%);
            color: #e0e0e0;
            min-height: 100vh;
        }
        .container {
            display: grid;
            grid-template-columns: 240px 1fr 280px;
            height: 100vh;
            gap: 1px;
            background: transparent;
        }
        .panel {
            background: rgba(17, 17, 17, 0.85);
            backdrop-filter: blur(10px);
            padding: 16px;
            overflow-y: auto;
            border-right: 1px solid rgba(102, 255, 222, 0.1);
        }
        .panel:last-child { border-right: none; border-left: 1px solid rgba(171, 69, 192, 0.1); }
        .panel-title {
            font-size: 14px;
            font-weight: 600;
            background: linear-gradient(90deg, var(--veritas-purple), var(--veritas-mint));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        /* Sessions Panel */
        .session-item {
            padding: 10px 12px;
            border-radius: 6px;
            margin-bottom: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid transparent;
            background: rgba(26, 26, 26, 0.6);
        }
        .session-item:hover {
            background: rgba(171, 69, 192, 0.1);
            border-color: rgba(171, 69, 192, 0.3);
        }
        .session-item.active {
            background: linear-gradient(135deg, rgba(171, 69, 192, 0.15) 0%, rgba(102, 255, 222, 0.1) 100%);
            border-color: var(--veritas-mint);
            box-shadow: 0 0 20px rgba(102, 255, 222, 0.1);
        }
        .session-status {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-active { background: var(--veritas-mint); box-shadow: 0 0 8px var(--veritas-mint); }
        .status-open { background: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.5); }
        .status-crashed { background: #ef4444; box-shadow: 0 0 6px rgba(239, 68, 68, 0.5); }
        .status-orphaned { background: #4b5563; opacity: 0.6; }
        .session-id { color: var(--veritas-mint); font-size: 12px; }
        .session-project { color: #9ca3af; font-size: 11px; margin-top: 4px; }
        .session-age { color: #6b7280; font-size: 10px; margin-top: 2px; }
        /* Source badges */
        .source-badge {
            display: inline-block;
            font-size: 9px;
            font-weight: 600;
            padding: 1px 5px;
            border-radius: 3px;
            margin-left: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .source-claude { background: rgba(171, 69, 192, 0.3); color: #d8b4fe; }
        .source-codex { background: rgba(34, 197, 94, 0.3); color: #86efac; }
        .source-gemini { background: rgba(59, 130, 246, 0.3); color: #93c5fd; }
        .source-sdk { background: rgba(249, 115, 22, 0.3); color: #fdba74; }
        /* Feed Panel */
        #feed {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .event {
            padding: 12px;
            border-radius: 8px;
            background: rgba(26, 26, 26, 0.7);
            border-left: 3px solid var(--veritas-purple);
            animation: slideIn 0.3s ease;
            transition: all 0.2s ease;
        }
        .event:hover {
            background: rgba(171, 69, 192, 0.08);
            transform: translateX(2px);
        }
        /* Event type colors */
        .event-think { border-left-color: var(--veritas-purple); }
        .event-tool { border-left-color: var(--veritas-mint); }
        .event-spawn { border-left-color: #f59e0b; }  /* Amber for spawn */
        .event-high { border-left-color: #ef4444; }    /* Red for high-risk */
        .event-read { border-left-color: #3b82f6; }    /* Blue for read */
        .event-write { border-left-color: #22c55e; }   /* Green for write */
        .event-bash { border-left-color: #f97316; }    /* Orange for bash */
        /* Sub-agent indentation */
        .event.depth-1 { margin-left: 24px; border-left-width: 2px; opacity: 0.95; }
        .event.depth-2 { margin-left: 48px; border-left-width: 2px; opacity: 0.9; }
        .event.depth-3 { margin-left: 72px; border-left-width: 2px; opacity: 0.85; }
        /* Thread connector for sub-agents */
        .event-thread {
            position: relative;
        }
        .event-thread::before {
            content: '';
            position: absolute;
            left: -16px;
            top: 0;
            bottom: 50%;
            width: 12px;
            border-left: 2px solid rgba(102, 255, 222, 0.3);
            border-bottom: 2px solid rgba(102, 255, 222, 0.3);
            border-bottom-left-radius: 6px;
        }
        /* Agent type specific event styling */
        .event.agent-explore { border-left-color: #3b82f6; }
        .event.agent-plan { border-left-color: var(--veritas-purple); }
        .event.agent-general { border-left-color: var(--veritas-mint); }
        /* Error event styling */
        .event.event-error {
            background: rgba(239, 68, 68, 0.1);
            border-left-color: #ef4444 !important;
            border-left-width: 4px;
            animation: error-pulse 2s ease-in-out infinite;
        }
        @keyframes error-pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.2); }
            50% { box-shadow: 0 0 8px 2px rgba(239, 68, 68, 0.3); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .event-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        .event-time { color: #6b7280; font-size: 11px; }
        .event-badge {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        .badge-think { background: linear-gradient(135deg, var(--veritas-purple), #8B5CF6); color: white; }
        .badge-tool { background: linear-gradient(135deg, #047857, var(--veritas-mint)); color: #0a0a0a; }
        .badge-spawn { background: linear-gradient(135deg, var(--veritas-purple), var(--veritas-mint)); color: white; }
        .badge-high { background: linear-gradient(135deg, #dc2626, #ef4444); color: white; }
        .event-content {
            color: #d1d5db;
            font-size: 13px;
            line-height: 1.5;
            white-space: pre-wrap;
            word-break: break-word;
        }
        /* Context Panel */
        .context-section {
            margin-bottom: 20px;
        }
        .context-label {
            font-size: 11px;
            color: var(--veritas-mint);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            opacity: 0.8;
        }
        .context-item {
            padding: 6px 10px;
            background: rgba(26, 26, 26, 0.6);
            border-radius: 4px;
            margin-bottom: 4px;
            font-size: 12px;
            transition: all 0.15s ease;
        }
        .context-item:hover { background: rgba(102, 255, 222, 0.05); }
        .file-read { border-left: 2px solid var(--veritas-mint); }
        .file-modified { border-left: 2px solid var(--veritas-purple); }
        .agent-spawn { border-left: 2px solid var(--veritas-purple); }
        .tool-stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .tool-bar {
            height: 6px;
            background: linear-gradient(90deg, var(--veritas-purple), var(--veritas-mint));
            border-radius: 3px;
            margin-left: 10px;
        }
        /* Header */
        .header {
            grid-column: 1 / -1;
            background: linear-gradient(90deg, rgba(171, 69, 192, 0.1) 0%, rgba(102, 255, 222, 0.05) 100%);
            backdrop-filter: blur(10px);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(102, 255, 222, 0.1);
        }
        .logo {
            font-size: 18px;
            font-weight: 700;
            background: linear-gradient(90deg, var(--veritas-purple), var(--veritas-mint));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .connection-status {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--veritas-mint);
            box-shadow: 0 0 8px var(--veritas-mint);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .status-dot.disconnected { background: #ef4444; box-shadow: 0 0 8px #ef4444; animation: none; }
        /* Breadcrumbs */
        .breadcrumbs {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            flex: 1;
            margin-left: 24px;
        }
        .breadcrumb {
            color: #6b7280;
            transition: color 0.2s;
        }
        .breadcrumb:hover { color: var(--veritas-mint); }
        .breadcrumb.active {
            color: var(--veritas-mint);
            font-weight: 500;
        }
        .breadcrumb-sep { color: #4b5563; }
        .breadcrumb-project {
            padding: 4px 10px;
            background: rgba(171, 69, 192, 0.15);
            border-radius: 4px;
            color: var(--veritas-purple);
        }
        .breadcrumb-session {
            padding: 4px 10px;
            background: rgba(102, 255, 222, 0.1);
            border-radius: 4px;
            color: var(--veritas-mint);
        }
        /* Empty state */
        .empty-state {
            text-align: center;
            color: #6b7280;
            padding: 40px;
            background: linear-gradient(135deg, rgba(171, 69, 192, 0.05) 0%, rgba(102, 255, 222, 0.03) 100%);
            border-radius: 8px;
        }
        /* Loading state with subtle pulse */
        .loading-state {
            animation: loadingPulse 1.5s ease-in-out infinite;
        }
        @keyframes loadingPulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        /* Floating Orbs - Over the top ambient animation */
        .orb-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.4;
            animation: float 20s infinite ease-in-out;
        }
        .orb-1 {
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, var(--veritas-purple), transparent 70%);
            top: -100px;
            left: -100px;
            animation-delay: 0s;
            animation-duration: 25s;
        }
        .orb-2 {
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, var(--veritas-mint), transparent 70%);
            bottom: -50px;
            right: -50px;
            animation-delay: -5s;
            animation-duration: 22s;
        }
        .orb-3 {
            width: 250px;
            height: 250px;
            background: radial-gradient(circle, rgba(171, 69, 192, 0.8), transparent 70%);
            top: 40%;
            left: 30%;
            animation-delay: -10s;
            animation-duration: 28s;
        }
        .orb-4 {
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(102, 255, 222, 0.6), transparent 70%);
            top: 20%;
            right: 20%;
            animation-delay: -15s;
            animation-duration: 18s;
        }
        .orb-5 {
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.5), transparent 70%);
            bottom: 20%;
            left: 10%;
            animation-delay: -8s;
            animation-duration: 30s;
        }
        .orb-6 {
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(102, 255, 222, 0.7), transparent 70%);
            top: 60%;
            right: 40%;
            animation-delay: -12s;
            animation-duration: 24s;
        }
        @keyframes float {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            25% {
                transform: translate(50px, -30px) scale(1.1);
            }
            50% {
                transform: translate(-20px, 40px) scale(0.9);
            }
            75% {
                transform: translate(30px, 20px) scale(1.05);
            }
        }
        /* Pulse animation for intensity */
        .orb-1 { animation: float 25s infinite, pulse-orb 8s infinite ease-in-out; }
        .orb-2 { animation: float 22s infinite, pulse-orb 6s infinite ease-in-out 1s; }
        .orb-3 { animation: float 28s infinite, pulse-orb 10s infinite ease-in-out 2s; }
        .orb-4 { animation: float 18s infinite, pulse-orb 7s infinite ease-in-out 3s; }
        .orb-5 { animation: float 30s infinite, pulse-orb 9s infinite ease-in-out 4s; }
        .orb-6 { animation: float 24s infinite, pulse-orb 5s infinite ease-in-out 2.5s; }
        @keyframes pulse-orb {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.6; }
        }
        /* All sessions badge */
        .all-sessions {
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px dashed rgba(102, 255, 222, 0.3);
            background: transparent;
            margin-bottom: 12px;
            text-align: center;
            color: var(--veritas-mint);
            font-size: 12px;
        }
        .all-sessions:hover {
            background: rgba(102, 255, 222, 0.05);
            border-color: var(--veritas-mint);
        }
        .all-sessions.active {
            background: rgba(102, 255, 222, 0.1);
            border-style: solid;
        }
        /* Session filter toggle */
        .session-filter {
            display: flex;
            gap: 6px;
            margin-bottom: 12px;
        }
        .filter-toggle {
            flex: 1;
            padding: 6px 8px;
            border-radius: 4px;
            border: 1px solid rgba(102, 255, 222, 0.2);
            background: transparent;
            color: #9ca3af;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
            position: relative;
        }
        .filter-toggle::before {
            content: '';
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            margin-right: 6px;
            vertical-align: middle;
        }
        /* Active filter: green/yellow gradient (active + open sessions) */
        .filter-toggle[data-filter="active"]::before {
            background: linear-gradient(135deg, var(--veritas-mint) 50%, #f59e0b 50%);
        }
        /* All filter: shows all colors including grey orphaned */
        .filter-toggle[data-filter="all"]::before {
            background: linear-gradient(135deg, var(--veritas-mint) 33%, #f59e0b 33%, #f59e0b 66%, #4b5563 66%);
        }
        .filter-toggle:hover {
            border-color: var(--veritas-mint);
            color: var(--veritas-mint);
        }
        .filter-toggle.active {
            background: rgba(102, 255, 222, 0.15);
            border-color: var(--veritas-mint);
            color: var(--veritas-mint);
        }
        .session-age {
            font-size: 10px;
            color: #6b7280;
            margin-top: 2px;
        }
        .session-actions {
            display: flex;
            gap: 4px;
            margin-top: 6px;
        }
        .session-action-btn {
            padding: 3px 8px;
            border-radius: 3px;
            border: none;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }
        .btn-view {
            background: rgba(102, 255, 222, 0.1);
            color: var(--veritas-mint);
        }
        .btn-view:hover {
            background: rgba(102, 255, 222, 0.2);
        }
        .btn-export {
            background: rgba(171, 69, 192, 0.1);
            color: var(--veritas-purple);
        }
        .btn-export:hover {
            background: rgba(171, 69, 192, 0.2);
        }
        /* Working Memory Panel */
        .working-memory {
            background: linear-gradient(135deg, rgba(171, 69, 192, 0.1) 0%, rgba(102, 255, 222, 0.05) 100%);
            border: 1px solid rgba(171, 69, 192, 0.3);
            border-radius: 8px;
            margin-bottom: 16px;
            overflow: hidden;
        }
        .working-memory-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 14px;
            background: rgba(171, 69, 192, 0.15);
            cursor: pointer;
            transition: all 0.2s;
        }
        .working-memory-header:hover {
            background: rgba(171, 69, 192, 0.2);
        }
        .working-memory-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 600;
            color: var(--veritas-mint);
        }
        .working-memory-toggle {
            font-size: 10px;
            color: #6b7280;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid rgba(102, 255, 222, 0.2);
            background: transparent;
            cursor: pointer;
            transition: all 0.2s;
        }
        .working-memory-toggle:hover {
            border-color: var(--veritas-mint);
            color: var(--veritas-mint);
        }
        .working-memory-content {
            padding: 12px;
        }
        .working-memory.collapsed .working-memory-content {
            display: none;
        }
        .working-memory.disabled {
            opacity: 0.5;
        }
        .working-memory.disabled .working-memory-content {
            display: none;
        }
        .wm-section {
            margin-bottom: 12px;
        }
        .wm-section:last-child {
            margin-bottom: 0;
        }
        .wm-label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--veritas-purple);
            margin-bottom: 4px;
        }
        .wm-goal {
            font-size: 13px;
            color: #e0e0e0;
            padding: 8px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
            border-left: 3px solid var(--veritas-mint);
        }
        .wm-focus {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }
        .wm-focus-item {
            padding: 3px 8px;
            background: rgba(102, 255, 222, 0.1);
            border-radius: 4px;
            font-size: 11px;
            color: var(--veritas-mint);
        }
        .wm-confidence {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .wm-confidence-bar {
            flex: 1;
            height: 6px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 3px;
            overflow: hidden;
        }
        .wm-confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--veritas-purple), var(--veritas-mint));
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        .wm-confidence-label {
            font-size: 11px;
            color: #9ca3af;
        }
        /* Simple status indicator (replaced EKG animation) */
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 0;
        }
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #6b7280;
        }
        .status-dot.active { background: var(--veritas-mint); animation: pulse 2s infinite; }
        .status-dot.thinking { background: #f59e0b; animation: pulse 1s infinite; }
        .status-dot.idle { background: #6b7280; }
        .status-dot.crashed { background: #ef4444; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        /* Health badge */
        .health-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .health-badge.on_track {
            background: rgba(102, 255, 222, 0.2);
            color: var(--veritas-mint);
        }
        .health-badge.exploring {
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
        }
        .health-badge.working_through_it {
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
        }
        .health-badge.needs_attention {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        .health-badge.waiting {
            background: rgba(107, 114, 128, 0.2);
            color: #9ca3af;
        }
        .health-badge.drifting {
            background: rgba(171, 69, 192, 0.3);
            color: var(--veritas-purple);
            animation: drift-pulse 1.5s ease-in-out infinite;
        }
        @keyframes drift-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        .health-status-text {
            font-size: 11px;
            color: #9ca3af;
            margin-top: 4px;
        }
        /* Filter Bar */
        .filter-bar {
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding: 16px;
            background: rgba(26, 26, 26, 0.7);
            border-radius: 8px;
            margin-bottom: 16px;
            border: 1px solid rgba(102, 255, 222, 0.1);
        }
        .filter-row {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
        }
        .filter-label {
            font-size: 11px;
            color: var(--veritas-mint);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            min-width: 60px;
        }
        .filter-search {
            flex: 1;
            min-width: 200px;
            padding: 8px 12px;
            background: rgba(17, 17, 17, 0.9);
            border: 1px solid rgba(102, 255, 222, 0.2);
            border-radius: 6px;
            color: #e0e0e0;
            font-family: inherit;
            font-size: 12px;
            transition: all 0.2s ease;
        }
        .filter-search:focus {
            outline: none;
            border-color: var(--veritas-mint);
            box-shadow: 0 0 0 2px rgba(102, 255, 222, 0.1);
        }
        .filter-search::placeholder {
            color: #6b7280;
        }
        .filter-chips {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            flex: 1;
        }
        .filter-chip {
            padding: 6px 12px;
            background: rgba(26, 26, 26, 0.8);
            border: 1px solid rgba(102, 255, 222, 0.2);
            border-radius: 16px;
            font-size: 11px;
            color: #d1d5db;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }
        .filter-chip:hover {
            background: rgba(102, 255, 222, 0.1);
            border-color: var(--veritas-mint);
            transform: translateY(-1px);
        }
        .filter-chip.active {
            background: linear-gradient(135deg, var(--veritas-purple), var(--veritas-mint));
            border-color: transparent;
            color: var(--veritas-black);
            font-weight: 600;
            box-shadow: 0 0 12px rgba(102, 255, 222, 0.3);
        }
        .filter-chip.risk-all.active {
            background: linear-gradient(135deg, #6b7280, #9ca3af);
        }
        .filter-chip.risk-safe.active {
            background: linear-gradient(135deg, #047857, #10b981);
        }
        .filter-chip.risk-medium.active {
            background: linear-gradient(135deg, #d97706, #f59e0b);
        }
        .filter-chip.risk-high.active {
            background: linear-gradient(135deg, #dc2626, #ef4444);
        }
        .clear-filters-btn {
            padding: 6px 16px;
            background: rgba(171, 69, 192, 0.15);
            border: 1px solid rgba(171, 69, 192, 0.3);
            border-radius: 6px;
            font-size: 11px;
            color: var(--veritas-purple);
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
        }
        .clear-filters-btn:hover {
            background: rgba(171, 69, 192, 0.25);
            border-color: var(--veritas-purple);
            transform: translateY(-1px);
        }
        .clear-filters-btn:active {
            transform: translateY(0);
        }
        .results-count {
            font-size: 11px;
            color: #6b7280;
            padding: 4px 0;
        }
        .results-count .count {
            color: var(--veritas-mint);
            font-weight: 600;
        }
        /* Agent Tree Hierarchy */
        .agent-tree-container {
            margin-top: 16px;
        }
        .agent-tree-header {
            font-size: 11px;
            color: var(--veritas-mint);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            opacity: 0.8;
        }
        .agent-node {
            position: relative;
            padding: 8px 12px;
            margin: 6px 0;
            background: rgba(26, 26, 26, 0.6);
            border-radius: 6px;
            border-left: 3px solid var(--veritas-mint);
            font-size: 12px;
            transition: all 0.2s ease;
        }
        .agent-node:hover {
            background: rgba(102, 255, 222, 0.05);
            transform: translateX(2px);
        }
        .agent-node.active {
            background: rgba(102, 255, 222, 0.1);
            box-shadow: 0 0 12px rgba(102, 255, 222, 0.2);
        }
        .agent-node.completed {
            opacity: 0.6;
            border-left-color: #6b7280;
        }
        .agent-node-type-explore {
            border-left-color: #3b82f6;
        }
        .agent-node-type-plan {
            border-left-color: var(--veritas-purple);
        }
        .agent-node-type-general {
            border-left-color: var(--veritas-mint);
        }
        .agent-node-label {
            font-weight: 600;
            color: var(--veritas-mint);
            margin-bottom: 4px;
        }
        .agent-node-type-explore .agent-node-label {
            color: #3b82f6;
        }
        .agent-node-type-plan .agent-node-label {
            color: var(--veritas-purple);
        }
        .agent-node-desc {
            color: #9ca3af;
            font-size: 11px;
            line-height: 1.4;
        }
        .agent-branch {
            position: absolute;
            left: 8px;
            top: 100%;
            width: 1px;
            height: 10px;
            background: linear-gradient(180deg, rgba(102, 255, 222, 0.3), transparent);
        }
        .agent-status-badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 10px;
            font-weight: 600;
            margin-left: 8px;
        }
        .agent-status-active {
            background: linear-gradient(135deg, var(--veritas-mint), #10b981);
            color: var(--veritas-black);
        }
        .agent-status-completed {
            background: rgba(107, 114, 128, 0.3);
            color: #9ca3af;
        }
        .agent-child {
            margin-left: 20px;
            padding-left: 12px;
            border-left: 1px solid rgba(102, 255, 222, 0.2);
        }
        /* Expandable Events */
        .event-expandable {
            cursor: pointer;
        }
        .event-expandable:hover .expand-icon {
            opacity: 1;
        }
        .expand-icon {
            opacity: 0.4;
            transition: all 0.2s;
            font-size: 10px;
            margin-left: auto;
        }
        .event-detail {
            display: none;
            margin-top: 10px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 6px;
            font-size: 11px;
            border: 1px solid rgba(102, 255, 222, 0.1);
        }
        .event.expanded .event-detail {
            display: block;
            animation: slideDown 0.2s ease;
        }
        .event.expanded .expand-icon {
            transform: rotate(90deg);
        }
        @keyframes slideDown {
            from { opacity: 0; max-height: 0; }
            to { opacity: 1; max-height: 300px; }
        }
        .detail-row {
            display: flex;
            margin-bottom: 6px;
        }
        .detail-label {
            color: var(--veritas-mint);
            min-width: 70px;
            opacity: 0.8;
        }
        .detail-value {
            color: #d1d5db;
            word-break: break-all;
        }
        .file-path {
            font-family: 'SF Mono', monospace;
            font-size: 11px;
            color: var(--veritas-mint);
            opacity: 0.8;
            margin-top: 4px;
        }
        .file-path:hover {
            opacity: 1;
            text-decoration: underline;
        }
        /* Spawn event expandable sections */
        .spawn-expandable {
            margin-top: 8px;
            border: 1px solid rgba(171, 69, 192, 0.2);
            border-radius: 4px;
            overflow: hidden;
        }
        .spawn-expandable-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 10px;
            background: rgba(171, 69, 192, 0.1);
            cursor: pointer;
            font-size: 11px;
            color: var(--veritas-purple);
            font-weight: 600;
            transition: all 0.2s;
        }
        .spawn-expandable-header:hover {
            background: rgba(171, 69, 192, 0.15);
        }
        .spawn-expandable-content {
            display: none;
            padding: 10px;
            background: rgba(0, 0, 0, 0.3);
            color: #d1d5db;
            font-size: 12px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 300px;
            overflow-y: auto;
        }
        .spawn-expandable.expanded .spawn-expandable-content {
            display: block;
        }
        .spawn-expandable.expanded .spawn-expandable-header {
            background: rgba(171, 69, 192, 0.2);
        }
        .spawn-expand-icon {
            transition: transform 0.2s;
        }
        .spawn-expandable.expanded .spawn-expand-icon {
            transform: rotate(90deg);
        }
        .copy-button {
            padding: 2px 8px;
            background: rgba(102, 255, 222, 0.1);
            border: 1px solid rgba(102, 255, 222, 0.3);
            border-radius: 3px;
            color: var(--veritas-mint);
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
            margin-left: 8px;
        }
        .copy-button:hover {
            background: rgba(102, 255, 222, 0.2);
            border-color: rgba(102, 255, 222, 0.5);
        }
        .copy-button:active {
            background: rgba(102, 255, 222, 0.3);
        }
        /* Collapsible Sub-agent Groups */
        .subagent-group {
            margin: 8px 0;
            border: 1px solid rgba(171, 69, 192, 0.2);
            border-radius: 8px;
            overflow: hidden;
        }
        .subagent-header {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            background: rgba(171, 69, 192, 0.1);
            cursor: pointer;
            transition: all 0.2s;
        }
        .subagent-header:hover {
            background: rgba(171, 69, 192, 0.15);
        }
        .subagent-header .collapse-icon {
            transition: transform 0.2s;
        }
        .subagent-group.collapsed .collapse-icon {
            transform: rotate(-90deg);
        }
        .subagent-group.collapsed .subagent-events {
            display: none;
        }
        .subagent-events {
            padding: 8px;
            background: rgba(0, 0, 0, 0.2);
        }
        .subagent-badge {
            padding: 2px 8px;
            background: linear-gradient(135deg, var(--veritas-purple), var(--veritas-mint));
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            color: var(--veritas-black);
        }
        .subagent-desc {
            color: #9ca3af;
            font-size: 12px;
        }
        .subagent-count {
            margin-left: auto;
            font-size: 11px;
            color: #6b7280;
        }
        /* Local Only Security Badge */
        .local-only-badge {
            position: fixed;
            top: 16px;
            right: 16px;
            z-index: 9999;
            padding: 8px 16px;
            background: rgba(26, 26, 26, 0.95);
            border: 1px solid rgba(102, 255, 222, 0.3);
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            color: var(--veritas-mint);
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }
        .local-only-badge::before {
            content: '🔒';
            font-size: 14px;
        }
    </style>
</head>
<body>
    <!-- Local Only Security Badge -->
    <div class="local-only-badge">Local Only (127.0.0.1)</div>

    <!-- Floating Orbs Background -->
    <div class="orb-container">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="orb orb-4"></div>
        <div class="orb orb-5"></div>
        <div class="orb orb-6"></div>
    </div>
    <div class="container" style="position:relative;z-index:1;">
        <header class="header">
            <div class="logo">🔮 MC</div>
            <div class="breadcrumbs" id="breadcrumbs">
                <span class="breadcrumb active">All Sessions</span>
            </div>
            <div class="connection-status">
                <div class="status-dot" id="status-dot"></div>
                <span id="status-text">Connecting...</span>
            </div>
        </header>

        <div class="panel" id="sessions-panel">
            <div class="panel-title">📡 Sessions</div>
            <div class="session-filter">
                <button class="filter-toggle active" data-filter="active" onclick="setSessionFilter('active')">Active</button>
                <button class="filter-toggle" data-filter="all" onclick="setSessionFilter('all')">All</button>
            </div>
            <div id="sessions"></div>
        </div>

        <div class="panel" id="feed-panel">
            <div class="panel-title">⚡ Live Feed</div>

            <!-- Filter Bar -->
            <div class="filter-bar">
                <div class="filter-row">
                    <span class="filter-label">Search</span>
                    <input type="text"
                           class="filter-search"
                           id="search-filter"
                           placeholder="Filter events by content..."
                           oninput="applyFilters()">
                </div>

                <div class="filter-row">
                    <span class="filter-label">Tools</span>
                    <div class="filter-chips">
                        <div class="filter-chip" data-tool="Read" onclick="toggleToolFilter('Read')">Read</div>
                        <div class="filter-chip" data-tool="Write" onclick="toggleToolFilter('Write')">Write</div>
                        <div class="filter-chip" data-tool="Edit" onclick="toggleToolFilter('Edit')">Edit</div>
                        <div class="filter-chip" data-tool="Bash" onclick="toggleToolFilter('Bash')">Bash</div>
                        <div class="filter-chip" data-tool="Glob" onclick="toggleToolFilter('Glob')">Glob</div>
                        <div class="filter-chip" data-tool="Grep" onclick="toggleToolFilter('Grep')">Grep</div>
                        <div class="filter-chip" data-tool="THINK" onclick="toggleToolFilter('THINK')">Think</div>
                        <div class="filter-chip" data-tool="SPAWN" onclick="toggleToolFilter('SPAWN')">Spawn</div>
                    </div>
                </div>

                <div class="filter-row">
                    <span class="filter-label">Risk</span>
                    <div class="filter-chips">
                        <div class="filter-chip risk-all active" data-risk="all" onclick="setRiskFilter('all')">All</div>
                        <div class="filter-chip risk-safe" data-risk="safe" onclick="setRiskFilter('safe')">Safe</div>
                        <div class="filter-chip risk-medium" data-risk="medium" onclick="setRiskFilter('medium')">Medium</div>
                        <div class="filter-chip risk-high" data-risk="high" onclick="setRiskFilter('high')">High</div>
                    </div>
                    <button class="clear-filters-btn" onclick="clearAllFilters()">Clear Filters</button>
                </div>

                <div class="results-count" id="results-count"></div>
            </div>

            <div id="feed">
                <div class="empty-state">Waiting for events...</div>
            </div>
        </div>

        <div class="panel" id="context-panel">
            <div class="panel-title">🧠 Context</div>

            <!-- Health Monitor Panel (toggleable) -->
            <div class="working-memory" id="working-memory">
                <div class="working-memory-header" onclick="toggleWorkingMemory()">
                    <span class="working-memory-title">
                        <span>💓</span> Agent Health
                    </span>
                    <button class="working-memory-toggle" onclick="event.stopPropagation(); disableWorkingMemory()">Disable</button>
                </div>
                <div class="working-memory-content health-waiting" id="wm-content">
                    <!-- Simple Status Indicator -->
                    <div class="wm-section">
                        <div class="status-indicator">
                            <div class="status-dot idle" id="status-dot"></div>
                            <span class="health-status-text" id="health-status-text">Waiting...</span>
                        </div>
                    </div>
                    <!-- Current Goal -->
                    <div class="wm-section">
                        <div class="wm-label">Current Focus</div>
                        <div class="wm-goal" id="wm-goal">Waiting for task...</div>
                    </div>
                    <!-- Active Files -->
                    <div class="wm-section">
                        <div class="wm-label">Active</div>
                        <div class="wm-focus" id="wm-focus">
                            <span class="wm-focus-item">—</span>
                        </div>
                    </div>
                </div>
            </div>

            <div id="context">
                <div class="empty-state">Select a session</div>
            </div>
        </div>
    </div>

    <script>
        let ws;
        let selectedSession = null;
        let events = [];
        let contexts = {};
        let agentStacks = {};  // Track active agents per session
        const maxEvents = 50;

        // Session filter: 'active' or 'all'
        let sessionFilter = 'active';

        // Filter state
        let filters = {
            searchText: '',
            tools: new Set(),
            riskLevel: 'all'
        };

        // Session filter toggle
        function setSessionFilter(filter) {
            sessionFilter = filter;
            document.querySelectorAll('.filter-toggle').forEach(btn => {
                btn.classList.toggle('active', btn.dataset.filter === filter);
            });
            renderSessions(lastSessions);
        }

        // Working Memory state (persisted to localStorage)
        let workingMemoryEnabled = localStorage.getItem('mc_wm_enabled') !== 'false';
        let workingMemoryCollapsed = localStorage.getItem('mc_wm_collapsed') === 'true';

        // Initialize Working Memory UI state
        function initWorkingMemory() {
            const wm = document.getElementById('working-memory');
            if (!workingMemoryEnabled) {
                wm.classList.add('disabled');
                wm.querySelector('.working-memory-toggle').textContent = 'Enable';
            }
            if (workingMemoryCollapsed) {
                wm.classList.add('collapsed');
            }
        }

        function toggleWorkingMemory() {
            const wm = document.getElementById('working-memory');
            if (wm.classList.contains('disabled')) return;
            workingMemoryCollapsed = !workingMemoryCollapsed;
            wm.classList.toggle('collapsed');
            localStorage.setItem('mc_wm_collapsed', workingMemoryCollapsed);
        }

        function disableWorkingMemory() {
            const wm = document.getElementById('working-memory');
            const btn = wm.querySelector('.working-memory-toggle');
            workingMemoryEnabled = !workingMemoryEnabled;
            wm.classList.toggle('disabled');
            btn.textContent = workingMemoryEnabled ? 'Disable' : 'Enable';
            localStorage.setItem('mc_wm_enabled', workingMemoryEnabled);
        }

        function updateWorkingMemory(ctx) {
            if (!workingMemoryEnabled || !ctx) return;

            // Calculate health from context
            const health = calculateHealth(ctx);
            // Update simple status indicator
            const statusDot = document.getElementById('status-dot');
            const healthText = document.getElementById('health-status-text');
            const wmContent = document.getElementById('wm-content');

            // Map health status to simple dot class
            const statusMap = {
                'on_track': { dot: 'active', text: 'Active' },
                'exploring': { dot: 'thinking', text: 'Thinking' },
                'working_through_it': { dot: 'thinking', text: 'Working' },
                'needs_attention': { dot: 'crashed', text: 'Needs Attention' },
                'drifting': { dot: 'crashed', text: 'Drifting from Intent' },
                'waiting': { dot: 'idle', text: 'Idle' }
            };
            const config = statusMap[health.status] || statusMap.waiting;
            statusDot.className = `status-dot ${config.dot}`;
            healthText.textContent = config.text;
            wmContent.className = `working-memory-content health-${health.status}`;

            // Update goal from first decision
            const goalEl = document.getElementById('wm-goal');
            if (ctx.decisions && ctx.decisions.length > 0) {
                goalEl.textContent = ctx.decisions[ctx.decisions.length - 1];
            } else {
                goalEl.textContent = 'Waiting for task...';
            }

            // Update focus from modified files + agents
            const focusEl = document.getElementById('wm-focus');
            let focusItems = [];
            if (ctx.files_modified && ctx.files_modified.length > 0) {
                focusItems = ctx.files_modified.slice(-3).map(f => `📝 ${f}`);
            }
            if (ctx.agent_tree && ctx.agent_tree.length > 0) {
                const latestAgent = ctx.agent_tree[ctx.agent_tree.length - 1];
                focusItems.push(`🤖 ${latestAgent.type}`);
            }
            if (focusItems.length === 0 && ctx.files_read && ctx.files_read.length > 0) {
                focusItems = ctx.files_read.slice(-2).map(f => `📖 ${f}`);
            }
            if (focusItems.length === 0) {
                focusEl.innerHTML = '<span class="wm-focus-item">—</span>';
            } else {
                focusEl.innerHTML = focusItems.map(f =>
                    `<span class="wm-focus-item">${escapeHtml(f)}</span>`
                ).join('');
            }
        }

        // Pure JavaScript health calculation (mirrors Python backend)
        function calculateHealth(ctx) {
            if (!ctx) return { health: 50, status: 'waiting', metrics: {} };

            // Friction score (gentler - friction is normal)
            const frictionCount = ctx.friction_count || 0;
            const frictionScore = Math.max(0, 100 - (frictionCount * 15));

            // Activity score
            const tools = ctx.tool_count || {};
            const totalTools = Object.values(tools).reduce((a, b) => a + b, 0);
            const productive = (tools['Edit'] || 0) + (tools['Write'] || 0);
            const readHeavy = (tools['Read'] || 0) + (tools['Glob'] || 0) + (tools['Grep'] || 0);

            let activityScore = 50;
            if (totalTools === 0) {
                activityScore = 50;
            } else if (productive > 0) {
                activityScore = Math.min(100, 60 + (productive * 8));
            } else if (readHeavy > 5) {
                activityScore = 70;
            }

            // Progress score
            const filesModified = (ctx.files_modified || []).length;
            const progressScore = Math.min(100, 40 + (filesModified * 15));

            // Decision score
            const decisions = ctx.decisions || [];
            const decisionScore = Math.min(100, 50 + (decisions.length * 10));

            // Weighted health (friction matters less - it's normal)
            let health = Math.round(
                frictionScore * 0.20 +
                activityScore * 0.30 +
                progressScore * 0.30 +
                decisionScore * 0.20
            );
            health = Math.max(10, Math.min(95, health));

            // Status - use gentler language
            let status = 'waiting';
            if (frictionCount > 3) {
                status = 'working_through_it';
            } else if (health >= 75) {
                status = 'on_track';
            } else if (health >= 50) {
                status = 'exploring';
            } else {
                status = 'needs_attention';
            }

            return { health, status, metrics: { frictionScore, activityScore, progressScore, decisionScore } };
        }

        // Filter functions
        function toggleToolFilter(tool) {
            if (filters.tools.has(tool)) {
                filters.tools.delete(tool);
                document.querySelector(`[data-tool="${tool}"]`).classList.remove('active');
            } else {
                filters.tools.add(tool);
                document.querySelector(`[data-tool="${tool}"]`).classList.add('active');
            }
            applyFilters();
        }

        function setRiskFilter(level) {
            filters.riskLevel = level;
            // Update UI
            document.querySelectorAll('[data-risk]').forEach(chip => {
                chip.classList.remove('active');
            });
            document.querySelector(`[data-risk="${level}"]`).classList.add('active');
            applyFilters();
        }

        function clearAllFilters() {
            filters.searchText = '';
            filters.tools.clear();
            filters.riskLevel = 'all';
            // Update UI
            document.getElementById('search-filter').value = '';
            document.querySelectorAll('[data-tool]').forEach(chip => {
                chip.classList.remove('active');
            });
            document.querySelectorAll('[data-risk]').forEach(chip => {
                chip.classList.remove('active');
            });
            document.querySelector('[data-risk="all"]').classList.add('active');
            applyFilters();
        }

        function applyFilters() {
            // Update search text from input
            filters.searchText = document.getElementById('search-filter').value.toLowerCase();
            renderFeed();
        }

        function eventPassesFilters(e) {
            // Session filter - when a session is selected, only show its events
            if (selectedSession && e.session_id !== selectedSession) {
                return false;
            }

            // Text search filter
            if (filters.searchText) {
                const content = (e.content || '').toLowerCase();
                const toolName = (e.tool_name || '').toLowerCase();
                const searchMatch = content.includes(filters.searchText) ||
                                  toolName.includes(filters.searchText);
                if (!searchMatch) return false;
            }

            // Tool filter
            if (filters.tools.size > 0) {
                let eventTool = e.tool_name || '';
                if (e.event_type === 'thinking') eventTool = 'THINK';
                if (e.event_type === 'spawn') eventTool = 'SPAWN';

                if (!filters.tools.has(eventTool)) return false;
            }

            // Risk level filter
            if (filters.riskLevel !== 'all') {
                const riskLevel = e.risk_level || 'safe';
                if (filters.riskLevel === 'safe' && riskLevel !== 'safe') return false;
                if (filters.riskLevel === 'medium' && riskLevel !== 'medium') return false;
                if (filters.riskLevel === 'high' && !['high', 'critical'].includes(riskLevel)) return false;
            }

            return true;
        }

        let reconnectAttempts = 0;
        const maxReconnectDelay = 30000;

        function connect() {
            const port = window.location.port || '8765';
            ws = new WebSocket(`ws://localhost:${port}/ws`);

            ws.onopen = () => {
                document.getElementById('status-dot').classList.remove('disconnected');
                document.getElementById('status-text').textContent = 'Connected';
                reconnectAttempts = 0;
                // Clear events on reconnect to avoid duplicates, then request fresh backfill
                events = [];
                sessionContexts = {};
                ws.send(JSON.stringify({ type: 'request_backfill', limit: 30 }));
            };

            ws.onclose = () => {
                document.getElementById('status-dot').classList.add('disconnected');
                reconnectAttempts++;
                const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), maxReconnectDelay);
                if (reconnectAttempts > 5) {
                    document.getElementById('status-text').textContent = 'Server offline. Run: mc web';
                } else {
                    document.getElementById('status-text').textContent = `Reconnecting in ${Math.round(delay/1000)}s...`;
                }
                setTimeout(connect, delay);
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                if (reconnectAttempts > 3) {
                    document.getElementById('status-text').textContent = 'Server offline. Run: mc web';
                } else {
                    document.getElementById('status-text').textContent = 'Connection error';
                }
            };

            ws.onmessage = (e) => {
                const data = JSON.parse(e.data);
                handleMessage(data);
            };
        }

        let parsingErrors = {};

        function handleMessage(data) {
            if (data.type === 'sessions') {
                lastSessions = data.sessions;  // Store sessions for persistence
                renderSessions(data.sessions);
                // Update status with degraded mode if applicable
                if (data.degraded) {
                    document.getElementById('status-text').textContent = 'Connected ⚠ Limited status detection';
                }
                // Track parsing errors
                if (data.errors) {
                    parsingErrors = data.errors;
                    // Show errors in console for now
                    Object.entries(data.errors).forEach(([sessionId, error]) => {
                        console.warn(`Session ${sessionId.substring(0, 6)}: ${error}`);
                    });
                }
            } else if (data.type === 'backfill') {
                // Load historical events on connect/refresh
                if (data.events && data.events.length > 0) {
                    events = data.events.concat(events);
                    events = events.slice(0, maxEvents); // Keep within limit
                    renderFeed();
                    document.getElementById('status-text').textContent = 'Connected (backfilled)';
                }
            } else if (data.type === 'session_history') {
                // FULL session history loaded when session is selected
                loadingSession = null;  // Clear loading state
                if (data.events && data.events.length > 0) {
                    events = data.events;  // Replace events with full history
                    renderFeed();
                    const totalText = data.total_events > data.events.length
                        ? `Loaded ${data.events.length} of ${data.total_events} events`
                        : `Loaded ${data.events.length} events`;
                    document.getElementById('status-text').textContent = totalText;
                } else {
                    // No events - show empty state instead of loading
                    const container = document.getElementById('feed');
                    container.innerHTML = '<div class="empty-state">No events in this session yet</div>';
                    document.getElementById('results-count').innerHTML = '';
                    document.getElementById('status-text').textContent = 'Session loaded (empty)';
                }
            } else if (data.type === 'event') {
                addEvent(data.event);
            } else if (data.type === 'context') {
                contexts[data.session_id] = data.context;
                if (selectedSession === data.session_id || !selectedSession) {
                    renderContext(data.context);
                    updateWorkingMemory(data.context);
                }
            }
        }

        function renderSessions(sessions) {
            const container = document.getElementById('sessions');

            // Filter sessions based on toggle
            // "active" filter shows active + open + crashed (excludes orphaned)
            let filteredSessions = sessions;
            if (sessionFilter === 'active') {
                filteredSessions = sessions.filter(s =>
                    s.status === 'active' || s.status === 'open' || s.status === 'crashed'
                );
            }

            // Add "All Sessions" option at top
            let html = `
                <div class="all-sessions ${!selectedSession ? 'active' : ''}"
                     onclick="selectAllSessions()">
                    📡 All Sessions (${filteredSessions.length})
                </div>
            `;

            // Session list with status indicator
            html += filteredSessions.map(s => {
                // Map status to CSS class
                const statusClass = 'status-' + (s.status || 'orphaned');
                // Source badge
                const source = s.source || 'claude';
                const sourceBadge = `<span class="source-badge source-${source}">${source}</span>`;
                // Status label with last_action for crashed
                let statusLabel = '';
                if (s.status === 'open') statusLabel = '<div class="session-age">open</div>';
                else if (s.status === 'crashed') {
                    const lastAction = s.last_action ? escapeHtml(s.last_action.slice(0, 30)) : 'crashed';
                    statusLabel = `<div class="session-age" style="color:#ef4444" title="${escapeHtml(s.last_action || '')}">${lastAction}</div>`;
                }
                else if (s.status === 'orphaned') statusLabel = '<div class="session-age">ended</div>';

                return `
                    <div class="session-item ${selectedSession === s.session_id ? 'active' : ''}"
                         onclick="selectSession('${escapeHtml(s.session_id)}', '${escapeHtml(s.project_path)}')">
                        <span class="session-status ${statusClass}"></span>
                        <span class="session-id">${escapeHtml(s.session_id.slice(0, 8))}</span>
                        ${sourceBadge}
                        <div class="session-project">${escapeHtml(s.project_path.split('/').pop())}</div>
                        ${statusLabel}
                    </div>
                `;
            }).join('');

            container.innerHTML = html;
        }

        let loadingSession = null;  // Track which session is loading

        function selectSession(id, projectPath) {
            selectedSession = id;
            selectedProject = projectPath;
            loadingSession = id;  // Mark as loading
            renderSessions(lastSessions);
            updateBreadcrumbs();
            // Show loading state instead of rendering stale/empty feed
            showLoadingState();
            if (contexts[id]) renderContext(contexts[id]);
            // Request context for this session
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'select_session', session_id: id }));
            }
        }

        function showLoadingState() {
            const container = document.getElementById('feed');
            const resultsCounter = document.getElementById('results-count');
            container.innerHTML = '<div class="empty-state loading-state">Loading session history...</div>';
            resultsCounter.innerHTML = '';
        }

        function selectAllSessions() {
            selectedSession = null;
            selectedProject = null;
            renderSessions(lastSessions);
            updateBreadcrumbs();
            renderFeed();  // Re-render feed to show all sessions
            renderContext(null);
        }

        function updateBreadcrumbs() {
            const container = document.getElementById('breadcrumbs');
            if (!selectedSession) {
                container.innerHTML = '<span class="breadcrumb active">All Sessions</span>';
            } else {
                const projectName = selectedProject ? selectedProject.split('/').pop() : 'Unknown';
                container.innerHTML = `
                    <span class="breadcrumb" onclick="selectAllSessions()" style="cursor:pointer">All Sessions</span>
                    <span class="breadcrumb-sep">›</span>
                    <span class="breadcrumb-project">${escapeHtml(projectName)}</span>
                    <span class="breadcrumb-sep">›</span>
                    <span class="breadcrumb-session">${escapeHtml(selectedSession.slice(0, 8))}</span>
                    <button class="session-action-btn btn-export" onclick="exportSummary('${escapeHtml(selectedSession)}')" style="margin-left:auto">
                        Export Summary
                    </button>
                `;
            }
        }

        async function exportSummary(sessionId) {
            try {
                const response = await fetch('/api/summary/' + sessionId);
                const data = await response.json();
                if (data.error) {
                    alert('Error: ' + data.error);
                    return;
                }
                // Download as markdown file
                const blob = new Blob([data.summary], {type: 'text/markdown'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'mc-session-' + sessionId.slice(0, 8) + '.md';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch (err) {
                console.error('Export failed:', err);
                alert('Export failed: ' + err.message);
            }
        }

        let lastSessions = [];
        let selectedProject = null;

        function addEvent(event) {
            events.unshift(event);
            if (events.length > maxEvents) events.pop();
            renderFeed();
        }

        function renderFeed() {
            const container = document.getElementById('feed');
            const resultsCounter = document.getElementById('results-count');

            if (events.length === 0) {
                if (lastSessions.length === 0) {
                    container.innerHTML = '<div class="empty-state">No sessions found - start Claude/Codex/Gemini to see activity</div>';
                } else {
                    container.innerHTML = '<div class="empty-state">Waiting for events...</div>';
                }
                resultsCounter.innerHTML = '';
                return;
            }

            // Apply filters
            const filteredEvents = events.filter(eventPassesFilters);

            // Update results count
            const activeFiltersCount = filters.tools.size + (filters.searchText ? 1 : 0) + (filters.riskLevel !== 'all' ? 1 : 0);
            if (activeFiltersCount > 0) {
                resultsCounter.innerHTML = `<span class="count">${filteredEvents.length}</span> of ${events.length} events`;
            } else {
                resultsCounter.innerHTML = `<span class="count">${filteredEvents.length}</span> events`;
            }

            if (filteredEvents.length === 0) {
                container.innerHTML = '<div class="empty-state">No events match the current filters</div>';
                return;
            }

            container.innerHTML = filteredEvents.map((e, idx) => {
                let badgeClass = 'badge-tool';
                let badge = e.tool_name || 'EVENT';
                let eventTypeClass = 'event-tool';
                let depthClass = '';
                let threadClass = '';
                let agentTypeClass = '';

                // Determine event type and color
                if (e.event_type === 'thinking') {
                    badgeClass = 'badge-think';
                    badge = 'THINK';
                    eventTypeClass = 'event-think';
                } else if (e.event_type === 'spawn') {
                    badgeClass = 'badge-spawn';
                    badge = 'SPAWN';
                    eventTypeClass = 'event-spawn';
                } else if (e.risk_level === 'high' || e.risk_level === 'critical') {
                    badgeClass = 'badge-high';
                    eventTypeClass = 'event-high';
                } else if (e.tool_name === 'Read' || e.tool_name === 'Glob' || e.tool_name === 'Grep') {
                    eventTypeClass = 'event-read';
                } else if (e.tool_name === 'Write' || e.tool_name === 'Edit') {
                    eventTypeClass = 'event-write';
                } else if (e.tool_name === 'Bash') {
                    eventTypeClass = 'event-bash';
                }

                // Apply depth for sub-agents ONLY (depth > 0)
                const depth = e.agent_depth || 0;
                if (depth > 0) {
                    depthClass = 'depth-' + Math.min(depth, 3);
                    threadClass = 'event-thread';
                }

                // Agent type specific styling
                if (e.agent_type) {
                    const lowerType = e.agent_type.toLowerCase();
                    if (lowerType.includes('explore')) {
                        agentTypeClass = 'agent-explore';
                    } else if (lowerType.includes('plan')) {
                        agentTypeClass = 'agent-plan';
                    } else {
                        agentTypeClass = 'agent-general';
                    }
                }

                // Agent badge with icon (only for sub-agents)
                let agentBadge = '';
                if (depth > 0 && e.agent_type) {
                    const lowerType = e.agent_type.toLowerCase();
                    let icon = '⚡';
                    if (lowerType.includes('explore')) icon = '🔍';
                    else if (lowerType.includes('plan')) icon = '📋';
                    agentBadge = `<span class="event-badge badge-spawn" style="font-size:10px;padding:1px 6px;">${icon} ${escapeHtml(e.agent_type)}</span>`;
                }

                // Error highlighting
                let errorClass = '';
                let errorBadge = '';
                if (e.has_error) {
                    errorClass = 'event-error';
                    errorBadge = '<span class="event-badge badge-high" style="font-size:10px;padding:1px 6px;">⚠ ERROR</span>';
                }

                // Build expandable detail section for all event types
                let detailRows = [];
                if (e.file_path) detailRows.push(`<div class="detail-row"><span class="detail-label">Path:</span><span class="detail-value">${escapeHtml(e.file_path)}</span></div>`);
                if (e.tool_name && e.event_type !== 'spawn') detailRows.push(`<div class="detail-row"><span class="detail-label">Tool:</span><span class="detail-value">${escapeHtml(e.tool_name)}</span></div>`);
                if (e.risk_level && e.risk_level !== 'safe') detailRows.push(`<div class="detail-row"><span class="detail-label">Risk:</span><span class="detail-value">${escapeHtml(e.risk_level)}</span></div>`);
                if (e.agent_type && e.event_type !== 'spawn') detailRows.push(`<div class="detail-row"><span class="detail-label">Agent:</span><span class="detail-value">${escapeHtml(e.agent_type)} (depth ${depth})</span></div>`);
                if (e.event_type === 'spawn' && e.model) detailRows.push(`<div class="detail-row"><span class="detail-label">Model:</span><span class="detail-value">${escapeHtml(e.model)}</span></div>`);
                detailRows.push(`<div class="detail-row"><span class="detail-label">Session:</span><span class="detail-value">${escapeHtml(e.session_id || 'unknown')}</span></div>`);

                let detailSection = detailRows.length > 1 ? `<div class="event-detail">${detailRows.join('')}</div>` : '';

                // Add spawn-specific expandable sections for prompt and context
                let spawnSections = '';
                if (e.event_type === 'spawn') {
                    if (e.description) {
                        spawnSections += `
                            <div class="spawn-expandable">
                                <div class="spawn-expandable-header" onclick="toggleSpawnExpand(event, this.parentElement)">
                                    <span>📋 Full Description</span>
                                    <span class="spawn-expand-icon">▶</span>
                                </div>
                                <div class="spawn-expandable-content">${escapeHtml(e.description)}</div>
                            </div>
                        `;
                    }
                    if (e.prompt) {
                        const eventId = 'spawn-' + idx;
                        spawnSections += `
                            <div class="spawn-expandable">
                                <div class="spawn-expandable-header" onclick="toggleSpawnExpand(event, this.parentElement)">
                                    <span>🎯 Prompt</span>
                                    <div>
                                        <button class="copy-button" onclick="copySpawnText(event, '${eventId}-prompt')">Copy</button>
                                        <span class="spawn-expand-icon">▶</span>
                                    </div>
                                </div>
                                <div class="spawn-expandable-content" id="${eventId}-prompt">${escapeHtml(e.prompt)}</div>
                            </div>
                        `;
                    }
                    if (e.context) {
                        const eventId = 'spawn-' + idx;
                        spawnSections += `
                            <div class="spawn-expandable">
                                <div class="spawn-expandable-header" onclick="toggleSpawnExpand(event, this.parentElement)">
                                    <span>📦 Context</span>
                                    <div>
                                        <button class="copy-button" onclick="copySpawnText(event, '${eventId}-context')">Copy</button>
                                        <span class="spawn-expand-icon">▶</span>
                                    </div>
                                </div>
                                <div class="spawn-expandable-content" id="${eventId}-context">${escapeHtml(e.context)}</div>
                            </div>
                        `;
                    }
                }

                let hasDetails = detailSection !== '' || spawnSections !== '';

                return `
                    <div class="event ${hasDetails ? 'event-expandable' : ''} ${eventTypeClass} ${depthClass} ${threadClass} ${agentTypeClass} ${errorClass}" ${hasDetails && !spawnSections ? 'onclick="toggleEventExpand(this)"' : ''} data-idx="${idx}">
                        <div class="event-header">
                            <span class="event-time">${escapeHtml(e.timestamp || '')}</span>
                            ${agentBadge}
                            ${errorBadge}
                            <span class="event-badge ${badgeClass}">${escapeHtml(badge)}</span>
                            <span class="session-id">${escapeHtml((e.session_id || '').slice(0, 6))}</span>
                            ${hasDetails && !spawnSections ? '<span class="expand-icon">▶</span>' : ''}
                        </div>
                        <div class="event-content">${escapeHtml(e.content || '')}</div>
                        ${detailSection}
                        ${spawnSections}
                    </div>
                `;
            }).join('');
        }

        function renderContext(ctx) {
            const container = document.getElementById('context');
            if (!ctx) {
                container.innerHTML = '<div class="empty-state">No context yet</div>';
                return;
            }
            let html = '';

            // 1. FRICTION (alert at top)
            if (ctx.friction_count && ctx.friction_count > 0) {
                html += `<div class="context-section">
                    <div class="context-label" style="color:#f59e0b;">🔧 Friction (${ctx.friction_count})</div>
                    <div class="context-item" style="border-left: 3px solid #f59e0b; background: rgba(245,158,11,0.1);">
                        Working through ${ctx.friction_count} challenge${ctx.friction_count > 1 ? 's' : ''}
                    </div>
                </div>`;
            }

            // 2. FILES READ (context gathering - what agent looked at)
            if (ctx.files_read && ctx.files_read.length) {
                html += `<div class="context-section">
                    <div class="context-label">📖 Files Read (${ctx.files_read.length})</div>
                    ${ctx.files_read.slice(0, 8).map(f => `<div class="context-item file-read">${escapeHtml(f)}</div>`).join('')}
                    ${ctx.files_read.length > 8 ? `<div class="context-item" style="opacity:0.6">+${ctx.files_read.length - 8} more</div>` : ''}
                </div>`;
            }

            // 3. FILES MODIFIED (what changed)
            if (ctx.files_modified && ctx.files_modified.length) {
                html += `<div class="context-section">
                    <div class="context-label">✏️ Modified (${ctx.files_modified.length})</div>
                    ${ctx.files_modified.map(f => `<div class="context-item file-modified">${escapeHtml(f)}</div>`).join('')}
                </div>`;
            }

            // 4. AGENT TREE (spawned agents with prompt preview)
            if (ctx.agent_tree && ctx.agent_tree.length) {
                html += `<div class="context-section">
                    <div class="context-label">🤖 Agent Tree (${ctx.agent_tree.length})</div>
                    <div class="agent-tree-container">
                        ${renderAgentTree(ctx.agent_tree)}
                    </div>
                </div>`;
            }

            // 5. DECISIONS (AI reasoning trail)
            if (ctx.decisions && ctx.decisions.length) {
                html += `<div class="context-section">
                    <div class="context-label">💡 Decisions</div>
                    ${ctx.decisions.map(d => `<div class="context-item" style="border-left: 2px solid #f59e0b;">→ ${escapeHtml(d)}</div>`).join('')}
                </div>`;
            }

            // 6. TOOLS (activity summary)
            if (ctx.tool_count && Object.keys(ctx.tool_count).length) {
                const maxCount = Math.max(...Object.values(ctx.tool_count));
                const totalTools = Object.values(ctx.tool_count).reduce((a, b) => a + b, 0);
                html += `<div class="context-section">
                    <div class="context-label">📊 Tools (${totalTools} calls)</div>
                    ${Object.entries(ctx.tool_count).sort((a,b) => b[1] - a[1]).slice(0, 8).map(([tool, count]) => `
                        <div class="context-item tool-stat">
                            <span>${escapeHtml(tool)}</span>
                            <div style="display:flex;align-items:center">
                                <div class="tool-bar" style="width:${(count/maxCount)*60}px"></div>
                                <span style="margin-left:8px;color:#6b7280">${count}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>`;
            }

            container.innerHTML = html || '<div class="empty-state">Collecting context...</div>';
        }

        function renderAgentTree(agentTree) {
            if (!agentTree || agentTree.length === 0) return '';

            // Determine agent type class and icon
            function getAgentStyle(type) {
                const lowerType = (type || '').toLowerCase();
                if (lowerType.includes('explore')) {
                    return { class: 'agent-node-type-explore', icon: '🔍', color: 'Explore' };
                } else if (lowerType.includes('plan')) {
                    return { class: 'agent-node-type-plan', icon: '📋', color: 'Plan' };
                } else {
                    return { class: 'agent-node-type-general', icon: '⚡', color: 'Agent' };
                }
            }

            return agentTree.map((agent, idx) => {
                const style = getAgentStyle(agent.type);
                const isActive = idx === agentTree.length - 1;
                const statusClass = isActive ? 'active' : 'completed';
                const statusBadge = isActive ?
                    '<span class="agent-status-badge agent-status-active">Active</span>' :
                    '<span class="agent-status-badge agent-status-completed">Completed</span>';

                return `
                    <div class="agent-node ${style.class} ${statusClass}">
                        <div class="agent-node-label">
                            ${style.icon} ${escapeHtml(agent.type)}
                            ${statusBadge}
                        </div>
                        <div class="agent-node-desc">${escapeHtml(agent.desc)}</div>
                        ${agent.prompt ? `<div class="agent-node-desc" style="margin-top:4px;opacity:0.7">${escapeHtml(agent.prompt.slice(0, 80))}...</div>` : ''}
                    </div>
                `;
            }).join('');
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Toggle event expand/collapse
        function toggleEventExpand(element) {
            element.classList.toggle('expanded');
        }

        // Toggle spawn expandable section
        function toggleSpawnExpand(event, element) {
            event.stopPropagation();
            element.classList.toggle('expanded');
        }

        // Copy spawn text to clipboard
        async function copySpawnText(event, elementId) {
            event.stopPropagation();
            const element = document.getElementById(elementId);
            if (element) {
                const text = element.textContent;
                try {
                    await navigator.clipboard.writeText(text);
                    // Visual feedback
                    const button = event.target;
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    button.style.background = 'rgba(102, 255, 222, 0.3)';
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.style.background = '';
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy:', err);
                    alert('Failed to copy to clipboard');
                }
            }
        }

        // Initialize and start
        initWorkingMemory();
        connect();

        // Heartbeat to keep connection alive
        setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'heartbeat' }));
            }
        }, 30000);
    </script>
</body>
</html>
"""


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
            # Serve from template file if it exists, otherwise fall back to embedded HTML
            template_file = TEMPLATES_DIR / "dashboard.html"
            if template_file.exists():
                return FileResponse(template_file, media_type="text/html")
            # Fallback to embedded HTML for backwards compatibility
            return DASHBOARD_HTML

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
                    event, session_id, target_session.project_path
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
                            event, session.session_id, session.project_path
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
                                    event, session.session_id, session.project_path
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
        self, event, session_id: str, project_path: str, agent_depth: int = 0
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
