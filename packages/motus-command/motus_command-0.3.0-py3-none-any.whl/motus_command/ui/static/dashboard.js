/**
 * Motus Command Dashboard - Command Center for AI Agents
 */

// State management
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

// Persisted to localStorage
let lastSessions = [];
let selectedProject = null;

// Working Memory state (persisted to localStorage)
let workingMemoryEnabled = localStorage.getItem('motus_wm_enabled') !== 'false';
let workingMemoryCollapsed = localStorage.getItem('motus_wm_collapsed') === 'true';

// Reconnection handling
let reconnectAttempts = 0;
const maxReconnectDelay = 30000;

// ============================================================================
// Session Filter
// ============================================================================

function setSessionFilter(filter) {
    sessionFilter = filter;
    document.querySelectorAll('.filter-toggle').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    renderSessions(lastSessions);
}

// ============================================================================
// Working Memory (Agent Health Panel)
// ============================================================================

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
    localStorage.setItem('motus_wm_collapsed', workingMemoryCollapsed);
}

function disableWorkingMemory() {
    const wm = document.getElementById('working-memory');
    const btn = wm.querySelector('.working-memory-toggle');
    workingMemoryEnabled = !workingMemoryEnabled;
    wm.classList.toggle('disabled');
    btn.textContent = workingMemoryEnabled ? 'Disable' : 'Enable';
    localStorage.setItem('motus_wm_enabled', workingMemoryEnabled);
}

// ============================================================================
// Intent Tracker
// ============================================================================

let intentTrackerCollapsed = localStorage.getItem('motus_intent_collapsed') === 'true';

function initIntentTracker() {
    const tracker = document.getElementById('intent-tracker');
    if (tracker && intentTrackerCollapsed) {
        tracker.classList.add('collapsed');
    }
}

function toggleIntentTracker() {
    const tracker = document.getElementById('intent-tracker');
    if (!tracker) return;
    intentTrackerCollapsed = !intentTrackerCollapsed;
    tracker.classList.toggle('collapsed');
    localStorage.setItem('motus_intent_collapsed', intentTrackerCollapsed);
}

function updateIntentTracker(intents, stats) {
    // Update count badge
    const countEl = document.getElementById('intent-count');
    if (countEl) {
        countEl.textContent = intents.length;
    }

    // Update stats
    if (stats) {
        const tokensEl = document.getElementById('stat-tokens');
        const cacheEl = document.getElementById('stat-cache');
        const filesEl = document.getElementById('stat-files');

        if (tokensEl) {
            const totalTokens = stats.total_input_tokens + stats.total_output_tokens;
            tokensEl.textContent = formatNumber(totalTokens);
        }
        if (cacheEl) {
            cacheEl.textContent = stats.cache_hit_rate || '—';
        }
        if (filesEl) {
            filesEl.textContent = `${stats.files_read}/${stats.files_modified}`;
        }
    }

    // Render intent list
    const listEl = document.getElementById('intent-list');
    if (!listEl) return;

    if (!intents || intents.length === 0) {
        listEl.innerHTML = '<div class="empty-state">No intents found</div>';
        return;
    }

    // Show most recent intents first (reverse order)
    const recentIntents = intents.slice(-10).reverse();

    listEl.innerHTML = recentIntents.map(intent => {
        const statusClass = intent.completed ? 'completed' : '';
        const statusText = intent.completed ? 'Done' : 'Active';
        const promptText = escapeHtml(intent.prompt).substring(0, 150);
        const hasMore = intent.prompt.length > 150;

        return `
            <div class="intent-item ${statusClass}">
                <div class="intent-prompt">${promptText}${hasMore ? '...' : ''}</div>
                <div class="intent-meta">
                    <span class="intent-time">${intent.timestamp}</span>
                    <span class="intent-status">${statusText}</span>
                </div>
            </div>
        `;
    }).join('');
}

function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function clearIntentTracker() {
    const countEl = document.getElementById('intent-count');
    const listEl = document.getElementById('intent-list');
    const tokensEl = document.getElementById('stat-tokens');
    const cacheEl = document.getElementById('stat-cache');
    const filesEl = document.getElementById('stat-files');

    if (countEl) countEl.textContent = '0';
    if (tokensEl) tokensEl.textContent = '—';
    if (cacheEl) cacheEl.textContent = '—';
    if (filesEl) filesEl.textContent = '—';
    if (listEl) listEl.innerHTML = '<div class="empty-state">Select a session to see intents</div>';
}

// ============================================================================
// Time Machine
// ============================================================================

let timeMachineCollapsed = localStorage.getItem('motus_tm_collapsed') === 'true';
let timeMachineFiles = [];  // Cached file list
let currentViewFile = null;  // Currently viewed file

function initTimeMachine() {
    const tm = document.getElementById('time-machine');
    if (tm && timeMachineCollapsed) {
        tm.classList.add('collapsed');
    }
}

function toggleTimeMachine() {
    const tm = document.getElementById('time-machine');
    if (!tm) return;
    timeMachineCollapsed = !timeMachineCollapsed;
    tm.classList.toggle('collapsed');
    localStorage.setItem('motus_tm_collapsed', timeMachineCollapsed);
}

function updateTimeMachine(files, totalSnapshots) {
    timeMachineFiles = files;

    // Update count badge
    const countEl = document.getElementById('snapshot-count');
    if (countEl) {
        countEl.textContent = totalSnapshots;
    }

    // Render file list
    const filesEl = document.getElementById('time-machine-files');
    if (!filesEl) return;

    if (!files || files.length === 0) {
        filesEl.innerHTML = '<div class="empty-state">No file snapshots found</div>';
        return;
    }

    filesEl.innerHTML = files.slice(0, 20).map((file, idx) => `
        <div class="tm-file-item" onclick="viewFileSnapshots('${escapeHtml(file.path)}', ${idx})">
            <span class="tm-file-name" title="${escapeHtml(file.path)}">${escapeHtml(file.filename)}</span>
            <span class="tm-file-versions">${file.versions} ver</span>
        </div>
    `).join('');

    if (files.length > 20) {
        filesEl.innerHTML += `<div class="empty-state" style="font-size:10px;margin-top:8px;">+${files.length - 20} more files</div>`;
    }
}

function viewFileSnapshots(filePath, fileIdx) {
    const file = timeMachineFiles.find(f => f.path === filePath);
    if (!file) return;

    currentViewFile = file;

    // Show viewer
    const viewer = document.getElementById('time-machine-viewer');
    const filename = document.getElementById('viewer-filename');
    const versions = document.getElementById('viewer-versions');
    const content = document.getElementById('viewer-content');

    if (viewer) viewer.style.display = 'block';
    if (filename) filename.textContent = file.filename;

    // Render version buttons
    if (versions) {
        versions.innerHTML = file.snapshots.map((snap, idx) => `
            <button class="version-btn ${idx === 0 ? 'active' : ''}"
                    onclick="loadSnapshotContent('${escapeHtml(file.path)}', ${idx})"
                    title="${snap.timestamp}">
                v${idx + 1} (${snap.timestamp})
            </button>
        `).join('');
    }

    // Load first version
    loadSnapshotContent(filePath, 0);
}

function loadSnapshotContent(filePath, snapshotIdx) {
    // Update active button
    document.querySelectorAll('.version-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', idx === snapshotIdx);
    });

    // Request content from server
    if (ws && ws.readyState === WebSocket.OPEN && selectedSession) {
        ws.send(JSON.stringify({
            type: 'get_snapshot',
            session_id: selectedSession,
            file_path: filePath,
            snapshot_idx: snapshotIdx
        }));
    }
}

function displaySnapshotContent(content, truncated) {
    const contentEl = document.getElementById('viewer-content');
    if (contentEl) {
        contentEl.textContent = content;
        if (truncated) {
            contentEl.textContent += '\n\n... (content truncated)';
        }
    }
}

function closeSnapshotViewer() {
    const viewer = document.getElementById('time-machine-viewer');
    if (viewer) viewer.style.display = 'none';
    currentViewFile = null;
}

function clearTimeMachine() {
    const countEl = document.getElementById('snapshot-count');
    const filesEl = document.getElementById('time-machine-files');
    const viewer = document.getElementById('time-machine-viewer');

    if (countEl) countEl.textContent = '0';
    if (filesEl) filesEl.innerHTML = '<div class="empty-state">Select a session to see file history</div>';
    if (viewer) viewer.style.display = 'none';

    timeMachineFiles = [];
    currentViewFile = null;
}

// ============================================================================
// Knowledge Graph
// ============================================================================

let knowledgeGraphCollapsed = localStorage.getItem('motus_kg_collapsed') === 'true';

function initKnowledgeGraph() {
    const kg = document.getElementById('knowledge-graph');
    if (kg && knowledgeGraphCollapsed) {
        kg.classList.add('collapsed');
    }
}

function toggleKnowledgeGraph() {
    const kg = document.getElementById('knowledge-graph');
    if (!kg) return;
    knowledgeGraphCollapsed = !knowledgeGraphCollapsed;
    kg.classList.toggle('collapsed');
    localStorage.setItem('motus_kg_collapsed', knowledgeGraphCollapsed);
}

function updateKnowledgeGraph(filesRead, filesModified, directories) {
    // Update count badge
    const countEl = document.getElementById('kg-count');
    if (countEl) {
        countEl.textContent = filesRead + filesModified;
    }

    // Update stats
    const readEl = document.getElementById('kg-read');
    const modifiedEl = document.getElementById('kg-modified');
    if (readEl) readEl.textContent = filesRead;
    if (modifiedEl) modifiedEl.textContent = filesModified;

    // Render directory list
    const dirsEl = document.getElementById('kg-dirs');
    if (!dirsEl) return;

    if (!directories || directories.length === 0) {
        dirsEl.innerHTML = '<div class="empty-state">No file activity found</div>';
        return;
    }

    dirsEl.innerHTML = directories.map(dir => {
        const modifiedClass = dir.modified > 0 ? 'has-modified' : '';
        return `
            <div class="kg-dir-item ${modifiedClass}">
                <span class="kg-dir-name" title="${escapeHtml(dir.path)}">${escapeHtml(dir.name)}</span>
                <div class="kg-dir-stats">
                    <span class="kg-dir-read">${dir.read}r</span>
                    <span class="kg-dir-modified">${dir.modified}w</span>
                </div>
            </div>
        `;
    }).join('');
}

function clearKnowledgeGraph() {
    const countEl = document.getElementById('kg-count');
    const readEl = document.getElementById('kg-read');
    const modifiedEl = document.getElementById('kg-modified');
    const dirsEl = document.getElementById('kg-dirs');

    if (countEl) countEl.textContent = '0';
    if (readEl) readEl.textContent = '—';
    if (modifiedEl) modifiedEl.textContent = '—';
    if (dirsEl) dirsEl.innerHTML = '<div class="empty-state">Select a session to see file graph</div>';
}

function updateWorkingMemory(ctx) {
    if (!workingMemoryEnabled || !ctx) return;

    // Calculate health from context
    const health = calculateHealth(ctx);

    // Update status bar
    const statusBar = document.getElementById('status-bar');
    const wmContent = document.getElementById('wm-content');

    if (statusBar) {
        statusBar.style.width = health.health + '%';
    }

    // Update health class for colors
    wmContent.className = `working-memory-content health-${health.status}`;

    // Update health badge
    const healthBadge = document.getElementById('health-badge');
    const healthPercent = document.getElementById('health-percent');
    const healthIcon = document.getElementById('health-status-icon');
    const healthText = document.getElementById('health-status-text');

    healthBadge.className = `health-badge ${health.status}`;
    healthPercent.textContent = health.health + '%';

    // Status icon and text
    const statusConfig = {
        'on_track': { icon: '🟢', text: 'On Track' },
        'exploring': { icon: '🟡', text: 'Exploring' },
        'working_through_it': { icon: '🔧', text: 'Working Through It' },
        'needs_attention': { icon: '🔴', text: 'Needs Attention' },
        'waiting': { icon: '⏳', text: 'Waiting...' }
    };
    const config = statusConfig[health.status] || statusConfig.waiting;
    healthIcon.textContent = config.icon;
    healthText.textContent = config.text;

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

// ============================================================================
// Event Filters
// ============================================================================

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

// ============================================================================
// WebSocket Connection
// ============================================================================

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
            document.getElementById('status-text').textContent = 'Server offline. Run: motus web';
        } else {
            document.getElementById('status-text').textContent = `Reconnecting in ${Math.round(delay/1000)}s...`;
        }
        setTimeout(connect, delay);
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (reconnectAttempts > 3) {
            document.getElementById('status-text').textContent = 'Server offline. Run: motus web';
        } else {
            document.getElementById('status-text').textContent = 'Connection error';
        }
    };

    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        handleMessage(data);
    };
}

function handleMessage(data) {
    if (data.type === 'sessions') {
        lastSessions = data.sessions;  // Store sessions for persistence
        renderSessions(data.sessions);
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
        if (data.events && data.events.length > 0) {
            events = data.events;  // Replace events with full history
            renderFeed();
            const totalText = data.total_events > data.events.length
                ? `Loaded ${data.events.length} of ${data.total_events} events`
                : `Loaded ${data.events.length} events`;
            document.getElementById('status-text').textContent = totalText;
        }
    } else if (data.type === 'event') {
        addEvent(data.event);
    } else if (data.type === 'context') {
        contexts[data.session_id] = data.context;
        if (selectedSession === data.session_id || !selectedSession) {
            renderContext(data.context);
            updateWorkingMemory(data.context);
        }
    } else if (data.type === 'session_intents') {
        // Intent tracker data for selected session
        updateIntentTracker(data.intents, data.stats);
    } else if (data.type === 'time_machine') {
        // Time Machine file snapshot data
        updateTimeMachine(data.files, data.total_snapshots);
    } else if (data.type === 'snapshot_content') {
        // Content of a specific file snapshot
        displaySnapshotContent(data.content, data.truncated);
    } else if (data.type === 'knowledge_graph') {
        // Knowledge graph file activity data
        updateKnowledgeGraph(data.files_read, data.files_modified, data.directories);
    }
}

// ============================================================================
// Session Management
// ============================================================================

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
        // Status label
        let statusLabel = '';
        if (s.status === 'open') statusLabel = '<div class="session-age">open</div>';
        else if (s.status === 'crashed') statusLabel = '<div class="session-age" style="color:#ef4444">crashed</div>';
        else if (s.status === 'orphaned') statusLabel = '<div class="session-age">ended</div>';

        // Source badge (CLU=Claude, COD=Codex, GEM=Gemini, SDK=SDK)
        const source = s.source || 'claude';
        const sourceColors = {
            claude: '#a855f7',  // purple
            codex: '#22c55e',   // green
            gemini: '#3b82f6',  // blue
            sdk: '#eab308',     // yellow
        };
        const sourceColor = sourceColors[source] || '#6b7280';
        const sourceBadge = `<span class="source-badge" style="color:${sourceColor}">${escapeHtml(source.slice(0, 3).toUpperCase())}</span>`;

        return `
            <div class="session-item ${selectedSession === s.session_id ? 'active' : ''}"
                 onclick="selectSession('${escapeHtml(s.session_id)}', '${escapeHtml(s.project_path)}')">
                <span class="session-status ${statusClass}"></span>
                ${sourceBadge}
                <span class="session-id">${escapeHtml(s.session_id.slice(0, 8))}</span>
                <div class="session-project">${escapeHtml(s.project_path.split('/').pop())}</div>
                ${statusLabel}
            </div>
        `;
    }).join('');

    container.innerHTML = html;
}

function selectSession(id, projectPath) {
    selectedSession = id;
    selectedProject = projectPath;
    renderSessions(lastSessions);
    updateBreadcrumbs();
    updateExportButton();
    renderFeed();  // Re-render feed with session filter
    if (contexts[id]) renderContext(contexts[id]);
    // Request context for this session
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'select_session', session_id: id }));
    }
}

function selectAllSessions() {
    selectedSession = null;
    selectedProject = null;
    renderSessions(lastSessions);
    updateBreadcrumbs();
    updateExportButton();
    renderFeed();  // Re-render feed to show all sessions
    renderContext(null);
    clearIntentTracker();  // Clear intent tracker when deselecting session
    clearTimeMachine();  // Clear time machine when deselecting session
    clearKnowledgeGraph();  // Clear knowledge graph when deselecting session
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
            <span class="breadcrumb-session">${selectedSession.slice(0, 8)}</span>
        `;
    }
}

// ============================================================================
// Event Feed
// ============================================================================

function addEvent(event) {
    events.unshift(event);
    if (events.length > maxEvents) events.pop();
    renderFeed();
}

function renderFeed() {
    const container = document.getElementById('feed');
    const resultsCounter = document.getElementById('results-count');

    if (events.length === 0) {
        container.innerHTML = '<div class="empty-state">Waiting for events...</div>';
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

    // Group events by sub-agent sessions
    const groupedEvents = groupEventsBySubAgent(filteredEvents);
    container.innerHTML = renderEventGroups(groupedEvents);
}

// Group events into sub-agent sessions
function groupEventsBySubAgent(events) {
    const groups = [];
    let currentGroup = null;

    for (let i = 0; i < events.length; i++) {
        const e = events[i];
        const depth = e.agent_depth || 0;

        if (e.event_type === 'spawn' && depth === 1) {
            // Start new sub-agent group
            if (currentGroup) {
                groups.push(currentGroup);
            }
            currentGroup = {
                type: 'subagent',
                spawnEvent: e,
                events: [],
                agentType: e.agent_type,
                collapsed: false
            };
        } else if (currentGroup && depth > 0) {
            // Add event to current sub-agent group
            currentGroup.events.push(e);
        } else {
            // Main agent event - close any open group and add as standalone
            if (currentGroup) {
                groups.push(currentGroup);
                currentGroup = null;
            }
            groups.push({ type: 'standalone', event: e });
        }
    }

    // Close any remaining group
    if (currentGroup) {
        groups.push(currentGroup);
    }

    return groups;
}

// Render grouped events
function renderEventGroups(groups) {
    return groups.map((group, groupIdx) => {
        if (group.type === 'standalone') {
            return renderEvent(group.event, groupIdx, false);
        } else {
            // Render sub-agent group with collapsible container
            const agentType = group.agentType || 'Agent';
            const lowerType = agentType.toLowerCase();
            let icon = '⚡';
            let typeClass = 'agent-general';
            if (lowerType.includes('explore')) {
                icon = '🔍';
                typeClass = 'agent-explore';
            } else if (lowerType.includes('plan')) {
                icon = '📋';
                typeClass = 'agent-plan';
            }

            const eventCount = group.events.length;
            const thinkCount = group.events.filter(e => e.event_type === 'thinking').length;
            const toolCount = group.events.filter(e => e.tool_name && e.event_type !== 'thinking').length;

            return `
                <div class="subagent-group ${typeClass}" data-group="${groupIdx}">
                    <div class="subagent-header" onclick="toggleSubagentGroup(${groupIdx})">
                        <span class="collapse-icon">▼</span>
                        <span class="subagent-badge">${icon} ${escapeHtml(agentType)}</span>
                        <span class="subagent-desc">${escapeHtml(group.spawnEvent.content || '')}</span>
                        <span class="subagent-count">${eventCount} events (${thinkCount} thoughts, ${toolCount} actions)</span>
                    </div>
                    <div class="subagent-events">
                        ${renderEvent(group.spawnEvent, groupIdx + '-spawn', true)}
                        ${group.events.map((e, idx) => renderEvent(e, `${groupIdx}-${idx}`, true)).join('')}
                    </div>
                </div>
            `;
        }
    }).join('');
}

// Render individual event
function renderEvent(e, idx, isInGroup) {
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

    // Apply depth for sub-agents (only when NOT in group, as group provides structure)
    const depth = e.agent_depth || 0;
    if (depth > 0 && !isInGroup) {
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

    // Agent badge with icon (only for sub-agents when NOT in group)
    let agentBadge = '';
    if (depth > 0 && e.agent_type && !isInGroup) {
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

    // Highlight THINK events in sub-agents
    let thinkHighlight = '';
    if (e.event_type === 'thinking' && depth > 0 && isInGroup) {
        thinkHighlight = 'subagent-think';
    }

    // Build expandable detail section for all event types
    let detailRows = [];
    if (e.file_path) detailRows.push(`<div class="detail-row"><span class="detail-label">Path:</span><span class="detail-value">${escapeHtml(e.file_path)}</span></div>`);
    if (e.tool_name) detailRows.push(`<div class="detail-row"><span class="detail-label">Tool:</span><span class="detail-value">${escapeHtml(e.tool_name)}</span></div>`);
    if (e.risk_level && e.risk_level !== 'safe') detailRows.push(`<div class="detail-row"><span class="detail-label">Risk:</span><span class="detail-value">${escapeHtml(e.risk_level)}</span></div>`);
    if (e.agent_type) detailRows.push(`<div class="detail-row"><span class="detail-label">Agent:</span><span class="detail-value">${escapeHtml(e.agent_type)} (depth ${depth})</span></div>`);
    if (e.event_type === 'spawn' && e.description) detailRows.push(`<div class="detail-row"><span class="detail-label">Task:</span><span class="detail-value">${escapeHtml(e.description)}</span></div>`);
    if (e.event_type === 'spawn' && e.model) detailRows.push(`<div class="detail-row"><span class="detail-label">Model:</span><span class="detail-value">${escapeHtml(e.model)}</span></div>`);

    // SPAWN events: add full prompt with expand/copy
    if (e.event_type === 'spawn' && e.prompt) {
        const promptPreview = escapeHtml(e.prompt.substring(0, 100));
        const hasMore = e.prompt.length > 100;
        detailRows.push(`
            <div class="detail-row spawn-prompt-row">
                <span class="detail-label">Prompt:</span>
                <div class="spawn-prompt-container">
                    <div class="spawn-prompt-preview" id="spawn-prompt-${idx}">${promptPreview}${hasMore ? '...' : ''}</div>
                    <div class="spawn-prompt-actions">
                        ${hasMore ? `<button class="spawn-expand-btn" onclick="event.stopPropagation(); toggleSpawnPrompt('${idx}')">Show Full</button>` : ''}
                        <button class="spawn-copy-btn" onclick="event.stopPropagation(); copySpawnText('${idx}', 'prompt')">Copy</button>
                    </div>
                </div>
            </div>
        `);
    }

    // SPAWN events: add full context with expand/copy (if available)
    if (e.event_type === 'spawn' && e.context) {
        const contextPreview = escapeHtml(e.context.substring(0, 100));
        const hasMore = e.context.length > 100;
        detailRows.push(`
            <div class="detail-row spawn-context-row">
                <span class="detail-label">Context:</span>
                <div class="spawn-context-container">
                    <div class="spawn-context-preview" id="spawn-context-${idx}">${contextPreview}${hasMore ? '...' : ''}</div>
                    <div class="spawn-context-actions">
                        ${hasMore ? `<button class="spawn-expand-btn" onclick="event.stopPropagation(); toggleSpawnContext('${idx}')">Show Full</button>` : ''}
                        <button class="spawn-copy-btn" onclick="event.stopPropagation(); copySpawnText('${idx}', 'context')">Copy</button>
                    </div>
                </div>
            </div>
        `);
    }

    detailRows.push(`<div class="detail-row"><span class="detail-label">Session:</span><span class="detail-value">${escapeHtml(e.session_id || 'unknown')}</span></div>`);

    let detailSection = detailRows.length > 1 ? `<div class="event-detail">${detailRows.join('')}</div>` : '';
    let hasDetails = detailSection !== '';

    return `
        <div class="event ${hasDetails ? 'event-expandable' : ''} ${eventTypeClass} ${depthClass} ${threadClass} ${agentTypeClass} ${errorClass} ${thinkHighlight}" ${hasDetails ? 'onclick="toggleEventExpand(this)"' : ''} data-idx="${idx}">
            <div class="event-header">
                <span class="event-time">${escapeHtml(e.timestamp || '')}</span>
                ${agentBadge}
                ${errorBadge}
                <span class="event-badge ${badgeClass}">${escapeHtml(badge)}</span>
                <span class="session-id">${escapeHtml((e.session_id || '').slice(0, 6))}</span>
                ${hasDetails ? '<span class="expand-icon">▶</span>' : ''}
            </div>
            <div class="event-content">${escapeHtml(e.content || '')}</div>
            ${detailSection}
        </div>
    `;
}

// ============================================================================
// Context Panel
// ============================================================================

function renderContext(ctx) {
    const container = document.getElementById('context');
    if (!ctx) {
        container.innerHTML = '<div class="empty-state">No context yet</div>';
        return;
    }
    let html = '';

    // FRICTION COUNT AT TOP (if any - but it's normal)
    if (ctx.friction_count && ctx.friction_count > 0) {
        html += `<div class="context-section">
            <div class="context-label" style="color:#f59e0b;">🔧 Friction (${ctx.friction_count})</div>
            <div class="context-item" style="border-left: 3px solid #f59e0b; background: rgba(245,158,11,0.1);">
                Working through ${ctx.friction_count} challenge${ctx.friction_count > 1 ? 's' : ''}
            </div>
        </div>`;
    }

    // TOOLS SECOND (most useful for understanding agent behavior)
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

    // Decisions (AI reasoning trail)
    if (ctx.decisions && ctx.decisions.length) {
        html += `<div class="context-section">
            <div class="context-label">💡 Decisions</div>
            ${ctx.decisions.map(d => `<div class="context-item" style="border-left: 2px solid #f59e0b;">→ ${escapeHtml(d)}</div>`).join('')}
        </div>`;
    }

    // Agent Tree Visualization
    if (ctx.agent_tree && ctx.agent_tree.length) {
        html += `<div class="context-section">
            <div class="context-label">🤖 Agent Tree (${ctx.agent_tree.length})</div>
            <div class="agent-tree-container">
                ${renderAgentTree(ctx.agent_tree)}
            </div>
        </div>`;
    }

    // Files Modified (important changes)
    if (ctx.files_modified && ctx.files_modified.length) {
        html += `<div class="context-section">
            <div class="context-label">✏️ Modified (${ctx.files_modified.length})</div>
            ${ctx.files_modified.map(f => `<div class="context-item file-modified">${escapeHtml(f)}</div>`).join('')}
        </div>`;
    }

    // Files Read (context gathering)
    if (ctx.files_read && ctx.files_read.length) {
        html += `<div class="context-section">
            <div class="context-label">📖 Files Read (${ctx.files_read.length})</div>
            ${ctx.files_read.slice(0, 8).map(f => `<div class="context-item file-read">${escapeHtml(f)}</div>`).join('')}
            ${ctx.files_read.length > 8 ? `<div class="context-item" style="opacity:0.6">+${ctx.files_read.length - 8} more</div>` : ''}
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
                    ${style.icon} ${agent.type}
                    ${statusBadge}
                </div>
                <div class="agent-node-desc">${escapeHtml(agent.desc)}</div>
                ${agent.prompt ? `<div class="agent-node-desc" style="margin-top:4px;opacity:0.7">${escapeHtml(agent.prompt.slice(0, 80))}...</div>` : ''}
            </div>
        `;
    }).join('');
}

// ============================================================================
// Utilities
// ============================================================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function toggleEventExpand(element) {
    element.classList.toggle('expanded');
}

function toggleSubagentGroup(groupIdx) {
    const group = document.querySelector(`[data-group="${groupIdx}"]`);
    if (group) {
        group.classList.toggle('collapsed');
    }
}

// ============================================================================
// SPAWN Prompt/Context Expand and Copy
// ============================================================================

function toggleSpawnPrompt(idx) {
    const el = document.getElementById(`spawn-prompt-${idx}`);
    const btn = el.parentElement.querySelector('.spawn-expand-btn');

    if (!el || !btn) return;

    // Find the event data
    const eventData = events.find((e, i) => String(i) === String(idx) || e.session_id && String(idx).includes(e.session_id));
    if (!eventData || !eventData.prompt) return;

    // Toggle between preview and full
    if (el.classList.contains('expanded')) {
        const promptPreview = escapeHtml(eventData.prompt.substring(0, 100));
        el.textContent = promptPreview + (eventData.prompt.length > 100 ? '...' : '');
        el.classList.remove('expanded');
        btn.textContent = 'Show Full';
    } else {
        el.textContent = escapeHtml(eventData.prompt);
        el.classList.add('expanded');
        btn.textContent = 'Show Less';
    }
}

function toggleSpawnContext(idx) {
    const el = document.getElementById(`spawn-context-${idx}`);
    const btn = el.parentElement.querySelector('.spawn-expand-btn');

    if (!el || !btn) return;

    // Find the event data
    const eventData = events.find((e, i) => String(i) === String(idx) || e.session_id && String(idx).includes(e.session_id));
    if (!eventData || !eventData.context) return;

    // Toggle between preview and full
    if (el.classList.contains('expanded')) {
        const contextPreview = escapeHtml(eventData.context.substring(0, 100));
        el.textContent = contextPreview + (eventData.context.length > 100 ? '...' : '');
        el.classList.remove('expanded');
        btn.textContent = 'Show Full';
    } else {
        el.textContent = escapeHtml(eventData.context);
        el.classList.add('expanded');
        btn.textContent = 'Show Less';
    }
}

async function copySpawnText(idx, type) {
    // Find the event data
    const eventData = events.find((e, i) => String(i) === String(idx) || e.session_id && String(idx).includes(e.session_id));
    if (!eventData) return;

    const textToCopy = type === 'prompt' ? eventData.prompt : eventData.context;
    if (!textToCopy) return;

    try {
        await navigator.clipboard.writeText(textToCopy);

        // Visual feedback
        const btn = document.querySelector(`#spawn-${type}-${idx}`)?.parentElement.querySelector('.spawn-copy-btn');
        if (btn) {
            const originalText = btn.textContent;
            btn.textContent = '✓ Copied!';
            btn.style.background = 'rgba(102, 255, 222, 0.3)';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
            }, 2000);
        }
    } catch (err) {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard. Please try again.');
    }
}

// ============================================================================
// Export Summary
// ============================================================================

async function exportSummary() {
    if (!selectedSession) {
        alert('Please select a session first');
        return;
    }

    const btn = document.getElementById('export-btn');
    const originalText = btn.textContent;
    btn.textContent = '⏳ Exporting...';
    btn.disabled = true;

    try {
        // Use relative URL to avoid port issues
        const response = await fetch(`/api/summary/${selectedSession}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.summary) {
            // Copy to clipboard
            await navigator.clipboard.writeText(data.summary);

            // Show success feedback
            btn.textContent = '✅ Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2000);
        } else {
            throw new Error('No summary in response');
        }
    } catch (error) {
        console.error('Export failed:', error);
        btn.textContent = '❌ Failed';
        setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        }, 2000);
    }
}

function updateExportButton() {
    const btn = document.getElementById('export-btn');
    if (btn) {
        btn.disabled = !selectedSession;
        btn.title = selectedSession ? 'Copy session summary to clipboard' : 'Select a session to export';
    }
}

// ============================================================================
// Initialization
// ============================================================================

// Initialize on load
initWorkingMemory();
initIntentTracker();
initTimeMachine();
initKnowledgeGraph();
connect();

// Heartbeat to keep connection alive
setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'heartbeat' }));
    }
}, 30000);
