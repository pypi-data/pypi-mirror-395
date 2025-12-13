// ThreatWinds Pentest Dashboard - Modern UI
(function() {
    'use strict';

    // Application State
    const state = {
        connected: false,
        hasCredentials: false,
        servers: [],
        activeServer: null,
        pentests: [],
        selectedPentest: null,
        currentFilter: 'all',
        files: {},
        currentPath: [],
        selectedFile: null,
        // Stream state (auto-watching for active pentests)
        streamEventSource: null,
        streamAutoScroll: true,
        streamConnected: false,
    };

    // API Base
    const API = '/api';

    // DOM Elements
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    // Initialize
    function init() {
        bindEvents();
        startClock();
        // Don't render map initially - wait for credentials check
        // This prevents showing demo data and then changing to real data
        checkCredentialsAndConnect();
    }

    // Event Bindings
    function bindEvents() {
        // Switch UI
        $('#switch-ui-btn')?.addEventListener('click', () => {
            window.location.href = '/';
        });

        // Server Dropdown
        $('#server-btn')?.addEventListener('click', (e) => {
            e.stopPropagation();
            $('#server-selector').classList.toggle('open');
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('#server-selector')) {
                $('#server-selector')?.classList.remove('open');
            }
        });

        // Add Server
        $('#add-server-btn')?.addEventListener('click', () => {
            $('#server-selector').classList.remove('open');
            openModal('add-server-modal');
        });

        // Server credentials toggle
        $('#server-use-existing')?.addEventListener('change', (e) => {
            $('#server-creds-section').style.display = e.target.checked ? 'none' : 'block';
        });

        // New Pentest buttons
        $('#new-pentest-btn')?.addEventListener('click', () => openNewPentestModal());
        $('#welcome-new-btn')?.addEventListener('click', () => openNewPentestModal());
        $('#map-new-pentest-btn')?.addEventListener('click', () => openNewPentestModal());

        // Refresh
        $('#refresh-btn')?.addEventListener('click', () => {
            clearGeoCache();  // Force re-resolution of geolocations
            loadPentests();
        });

        // Filter buttons
        $$('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                $$('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.currentFilter = btn.dataset.filter;
                renderPentestsList();
            });
        });

        // Detail actions
        $('#btn-home')?.addEventListener('click', goHome);
        $('#btn-files')?.addEventListener('click', openFileExplorer);
        $('#btn-download')?.addEventListener('click', downloadEvidence);

        // Logo click to go home
        $('#logo-home-link')?.addEventListener('click', (e) => {
            e.preventDefault();
            goHome();
        });

        // Files navigation
        $('#files-back-btn')?.addEventListener('click', navigateUp);
        $('#files-download-all')?.addEventListener('click', downloadEvidence);

        // Modal close buttons
        $$('[data-close]').forEach(btn => {
            btn.addEventListener('click', () => {
                btn.closest('.modal')?.classList.remove('active');
            });
        });

        // Modal overlay clicks
        $$('.modal-overlay').forEach(overlay => {
            overlay.addEventListener('click', () => {
                overlay.closest('.modal')?.classList.remove('active');
            });
        });

        // Form submissions
        $('#submit-pentest')?.addEventListener('click', submitNewPentest);
        $('#submit-server')?.addEventListener('click', submitAddServer);
        $('#submit-credentials')?.addEventListener('click', submitCredentials);

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                $$('.modal.active').forEach(m => m.classList.remove('active'));
            }
        });

        // Stream controls
        $('#stream-autoscroll-btn')?.addEventListener('click', toggleStreamAutoScroll);
        $('#stream-clear-btn')?.addEventListener('click', clearStreamConsole);
    }

    // Clock
    function startClock() {
        const update = () => {
            const now = new Date();
            const time = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            const date = now.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: 'numeric' }).replace(/\//g, '.');
            $('#datetime').textContent = `${date} ${time}`;
        };
        update();
        setInterval(update, 1000);
    }

    // API Request
    async function apiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${API}${endpoint}`, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
            });
            if (!response.ok) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.error || `HTTP ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    // Connection & Credentials
    async function checkCredentialsAndConnect() {
        try {
            const status = await apiRequest('/status');
            state.hasCredentials = !!status.has_credentials;
            state.connected = status.connected;

            if (!state.hasCredentials) {
                openModal('credentials-modal');
                // Show demo map when no credentials
                await renderThreatMap();
                return;
            }

            updateConnectionStatus(status);
            loadServers();
            await loadPentests();  // This will render the map with real data
        } catch (error) {
            openModal('credentials-modal');
            // Show demo map on error
            await renderThreatMap();
        }
    }

    async function submitCredentials() {
        const apiKey = $('#cred-api-key').value.trim();
        const apiSecret = $('#cred-api-secret').value.trim();
        const host = $('#cred-host').value.trim() || 'localhost';
        const port = $('#cred-port').value.trim() || '9741';

        if (!apiKey || !apiSecret) {
            showToast('API Key and Secret are required', 'error');
            return;
        }

        try {
            const result = await apiRequest('/credentials', {
                method: 'POST',
                body: JSON.stringify({ api_key: apiKey, api_secret: apiSecret, host, port }),
            });

            if (result.success) {
                closeModal('credentials-modal');
                showToast('Connected successfully!', 'success');
                state.hasCredentials = true;
                checkCredentialsAndConnect();
            } else {
                showToast(result.error || 'Failed to connect', 'error');
            }
        } catch (error) {
            showToast(`Connection failed: ${error.message}`, 'error');
        }
    }

    function updateConnectionStatus(status) {
        const wasConnected = state.connected;
        state.connected = status.connected;

        // Clear geo cache when connection state changes
        if (wasConnected !== status.connected) {
            clearGeoCache();
        }

        const connectionStatus = $('#connection-status');
        const serverSelector = $('#server-selector');

        if (status.connected) {
            connectionStatus.classList.add('connected');
            serverSelector.classList.add('connected');
            $('#status-text').textContent = 'Connected';
            $('#status-server').textContent = status.server || '---';
            $('#connection-ip').textContent = `IP: ${status.ip || '---'}`;
            $('#connection-country').textContent = status.country || '---';
        } else {
            connectionStatus.classList.remove('connected');
            serverSelector.classList.remove('connected');
            $('#status-text').textContent = 'Disconnected';
            $('#status-server').textContent = '---';
            $('#connection-ip').textContent = 'IP: ---';
            $('#connection-country').textContent = '---';
        }
    }

    // Servers
    async function loadServers() {
        try {
            const data = await apiRequest('/servers');
            state.servers = data.servers || [];
            state.activeServer = data.active_server || null;
            renderServersList();
            updateCurrentServerName();
        } catch (error) {
            state.servers = [];
            renderServersList();
        }
    }

    function renderServersList() {
        const container = $('#server-list');
        if (!container) return;

        if (state.servers.length === 0) {
            container.innerHTML = '<div class="empty-state" style="padding:16px;font-size:12px;">No servers configured</div>';
            return;
        }

        container.innerHTML = state.servers.map(server => {
            const isActive = state.activeServer && state.activeServer.id === server.id;
            return `
                <div class="server-list-item ${isActive ? 'active' : ''}" data-id="${server.id}">
                    <span class="server-dot"></span>
                    <div class="server-list-item-info">
                        <div class="server-list-item-name">${escapeHtml(server.name)}</div>
                        <div class="server-list-item-host">${escapeHtml(server.host)}:${server.port}</div>
                    </div>
                    <button class="server-list-item-remove" data-id="${server.id}" title="Remove">&times;</button>
                </div>
            `;
        }).join('');

        // Click handlers
        container.querySelectorAll('.server-list-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.classList.contains('server-list-item-remove')) {
                    switchServer(item.dataset.id);
                }
            });
        });

        container.querySelectorAll('.server-list-item-remove').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                removeServer(btn.dataset.id);
            });
        });
    }

    function updateCurrentServerName() {
        const name = state.activeServer ? state.activeServer.name : 'Select Server';
        $('#current-server-name').textContent = name;
    }

    async function switchServer(serverId) {
        try {
            const result = await apiRequest('/servers/switch', {
                method: 'POST',
                body: JSON.stringify({ server_id: serverId }),
            });

            if (result.success) {
                showToast(`Switched to ${result.server_name}`, 'success');
                // Clear geo cache since server location changes
                clearGeoCache();
                loadServers();
                checkConnectionStatus();
                loadPentests();
            }
        } catch (error) {
            showToast(`Failed to switch server: ${error.message}`, 'error');
        }

        $('#server-selector').classList.remove('open');
    }

    async function removeServer(serverId) {
        if (!confirm('Remove this server connection?')) return;

        try {
            const result = await apiRequest(`/servers/${serverId}`, { method: 'DELETE' });
            if (result.success) {
                showToast('Server removed', 'success');
                loadServers();
            }
        } catch (error) {
            showToast(`Failed to remove server: ${error.message}`, 'error');
        }
    }

    async function submitAddServer() {
        const name = $('#server-name').value.trim();
        const host = $('#server-host').value.trim();
        const port = $('#server-port').value.trim() || '9741';
        const grpcPort = $('#server-grpc-port').value.trim() || '9742';
        const useExisting = $('#server-use-existing').checked;

        if (!name || !host) {
            showToast('Server name and host are required', 'error');
            return;
        }

        const serverData = { name, host, port, grpc_port: grpcPort, use_existing_credentials: useExisting };

        if (!useExisting) {
            const apiKey = $('#server-api-key').value.trim();
            const apiSecret = $('#server-api-secret').value.trim();
            if (!apiKey || !apiSecret) {
                showToast('API credentials are required', 'error');
                return;
            }
            serverData.api_key = apiKey;
            serverData.api_secret = apiSecret;
        }

        try {
            const result = await apiRequest('/servers', {
                method: 'POST',
                body: JSON.stringify(serverData),
            });

            if (result.success) {
                closeModal('add-server-modal');
                showToast(`Server "${name}" added`, 'success');
                loadServers();
                // Reset form
                $('#server-name').value = '';
                $('#server-host').value = '';
            } else {
                showToast(result.error || 'Failed to add server', 'error');
            }
        } catch (error) {
            showToast(`Failed to add server: ${error.message}`, 'error');
        }
    }

    async function checkConnectionStatus() {
        try {
            const status = await apiRequest('/status');
            updateConnectionStatus(status);
        } catch (error) {
            updateConnectionStatus({ connected: false });
        }
    }

    // Pentests
    async function loadPentests() {
        try {
            const data = await apiRequest('/pentests?page_size=100');
            state.pentests = data.pentests || [];
            renderPentestsList();
            updateStats();
            await renderThreatMap();  // Await to ensure geolocation resolves before returning
        } catch (error) {
            showToast(`Failed to load pentests: ${error.message}`, 'error');
        }
    }

    function renderPentestsList() {
        const container = $('#pentests-list');
        if (!container) return;

        let filtered = state.pentests;
        if (state.currentFilter !== 'all') {
            filtered = state.pentests.filter(p => p.status === state.currentFilter);
        }

        if (filtered.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                    <span>No pentests found</span>
                </div>
            `;
            return;
        }

        container.innerHTML = filtered.map(pentest => {
            const target = pentest.targets?.[0]?.target || 'Unknown';
            const isActive = state.selectedPentest?.id === pentest.id;
            const severity = (pentest.severity || 'none').toLowerCase();

            return `
                <div class="pentest-item ${isActive ? 'active' : ''}" data-id="${pentest.id}" data-status="${pentest.status}">
                    <div class="pentest-status-indicator"></div>
                    <div class="pentest-item-info">
                        <div class="pentest-item-target">${escapeHtml(target)}</div>
                        <div class="pentest-item-meta">
                            <span>${pentest.status}</span>
                            <span>${formatDate(pentest.created_at)}</span>
                        </div>
                    </div>
                    ${severity !== 'none' ? `<span class="pentest-item-severity ${severity}">${severity}</span>` : ''}
                </div>
            `;
        }).join('');

        // Click handlers
        container.querySelectorAll('.pentest-item').forEach(item => {
            item.addEventListener('click', () => selectPentest(item.dataset.id));
        });
    }

    function updateStats() {
        const total = state.pentests.length;
        const active = state.pentests.filter(p => p.status === 'IN_PROGRESS').length;
        const completed = state.pentests.filter(p => p.status === 'COMPLETED').length;
        const findings = state.pentests.reduce((sum, p) => sum + (p.findings || 0), 0);

        $('#stat-total').textContent = total;
        $('#stat-active').textContent = active;
        $('#stat-completed').textContent = completed;
        $('#stat-findings').textContent = findings;
    }

    async function selectPentest(pentestId) {
        const pentest = state.pentests.find(p => p.id === pentestId);
        if (!pentest) return;

        state.selectedPentest = pentest;

        // Update list selection
        $$('.pentest-item').forEach(item => {
            item.classList.toggle('active', item.dataset.id === pentestId);
        });

        // Load full details
        try {
            const details = await apiRequest(`/pentests/${pentestId}`);
            state.selectedPentest = details;
            showDetailView(details);
        } catch (error) {
            showToast(`Failed to load pentest details: ${error.message}`, 'error');
        }
    }

    // Go back to home/dashboard view
    function goHome() {
        // Disconnect any active stream
        disconnectStream();

        // Clear selected pentest
        state.selectedPentest = null;

        // Hide all views, show dashboard
        $('#detail-view').classList.remove('active');
        $('#files-view').classList.remove('active');
        $('#dashboard-view').classList.add('active');

        // Clear active state in pentest list
        $$('.pentest-item').forEach(el => el.classList.remove('active'));
    }

    function showDetailView(pentest) {
        // Hide dashboard, show detail
        $('#dashboard-view').classList.remove('active');
        $('#files-view').classList.remove('active');
        $('#detail-view').classList.add('active');

        const target = pentest.targets?.[0]?.target || 'Unknown';
        const status = pentest.status?.toLowerCase() || 'pending';

        // Header
        $('#detail-target').textContent = target;
        $('#detail-id').textContent = pentest.id;
        $('#detail-status-badge').innerHTML = `<span class="status-badge ${status}">${pentest.status}</span>`;

        // Show/hide action buttons based on status
        const btnDownload = $('#btn-download');
        const btnFiles = $('#btn-files');
        if (btnDownload) btnDownload.style.display = pentest.status === 'COMPLETED' ? 'flex' : 'none';
        if (btnFiles) btnFiles.style.display = pentest.status === 'COMPLETED' ? 'flex' : 'none';

        // Progress section
        const progressSection = $('#progress-section');
        if (pentest.status === 'IN_PROGRESS' || pentest.status === 'PENDING') {
            progressSection.style.display = 'block';
            updateProgress(pentest);
        } else if (pentest.status === 'COMPLETED') {
            progressSection.style.display = 'block';
            $('#progress-fill').style.width = '100%';
            $('#progress-percent').textContent = '100%';
            $('#progress-phase').textContent = 'Completed';
            $$('.stage').forEach(s => s.classList.add('completed'));
        } else {
            progressSection.style.display = 'none';
        }

        // Info cards
        const targetInfo = pentest.targets?.[0] || {};
        $('#info-scope').textContent = targetInfo.scope || '---';
        $('#info-type').textContent = targetInfo.type || '---';
        $('#info-style').textContent = pentest.style || '---';
        $('#info-exploit').textContent = pentest.exploit ? 'Enabled' : 'Disabled';

        $('#info-created').textContent = formatDateTime(pentest.created_at);
        $('#info-started').textContent = formatDateTime(pentest.started_at);
        $('#info-finished').textContent = formatDateTime(pentest.finished_at);
        $('#info-duration').textContent = calculateDuration(pentest.started_at, pentest.finished_at);

        // Findings (mock breakdown for now)
        const findings = pentest.findings || 0;
        $('#finding-critical').textContent = Math.floor(findings * 0.1);
        $('#finding-high').textContent = Math.floor(findings * 0.2);
        $('#finding-medium').textContent = Math.floor(findings * 0.4);
        $('#finding-low').textContent = Math.floor(findings * 0.3);

        // Targets list
        renderTargetsList(pentest.targets || []);

        // Live Progress Stream section
        // Note: Live streaming is only available for pentests started from THIS session.
        // Already running pentests cannot be streamed (gRPC limitation).
        const streamSection = $('#stream-section');
        if (streamSection) {
            const isActive = pentest.status === 'IN_PROGRESS' || pentest.status === 'PENDING';
            if (isActive && state.streamConnected && state.selectedPentest?.id === pentest.id) {
                // Keep stream section visible if we're already streaming this pentest
                streamSection.style.display = 'block';
            } else if (isActive) {
                // Show stream section with info message for already running pentests
                streamSection.style.display = 'block';
                const consoleEl = $('#stream-console');
                if (consoleEl && !state.streamConnected) {
                    consoleEl.innerHTML = '';
                    addStreamLine('This pentest is already running.', 'info');
                    addStreamLine('Live streaming is only available for pentests started from this session.', 'info');
                    addStreamLine(`Current status: ${pentest.status}`, 'status');
                    if (pentest.targets?.[0]?.phase) {
                        addStreamLine(`Current phase: ${pentest.targets[0].phase}`, 'phase');
                    }
                }
            } else {
                // Hide for completed/failed pentests
                streamSection.style.display = 'none';
                disconnectStream();
            }
        }
    }

    function updateProgress(pentest) {
        const targetInfo = pentest.targets?.[0] || {};
        const phase = targetInfo.phase || 'Initializing';

        // Estimate progress based on phase
        const phaseProgress = {
            'INITIALIZATION': 5,
            'RECONNAISSANCE': 25,
            'SCANNING': 50,
            'EXPLOITATION': 75,
            'REPORTING': 90,
        };

        const progress = phaseProgress[phase] || 0;

        $('#progress-fill').style.width = `${progress}%`;
        $('#progress-percent').textContent = `${progress}%`;
        $('#progress-phase').textContent = phase;

        // Update stages
        const stages = ['recon', 'scan', 'exploit', 'report'];
        const currentStageIndex = Math.floor(progress / 25);

        stages.forEach((stage, index) => {
            const el = $(`.stage[data-stage="${stage}"]`);
            if (el) {
                el.classList.remove('active', 'completed');
                if (index < currentStageIndex) {
                    el.classList.add('completed');
                } else if (index === currentStageIndex) {
                    el.classList.add('active');
                }
            }
        });
    }

    function renderTargetsList(targets) {
        const container = $('#targets-list');
        if (!container) return;

        if (targets.length === 0) {
            container.innerHTML = '<div class="empty-state" style="padding:16px;">No targets</div>';
            return;
        }

        container.innerHTML = targets.map(target => `
            <div class="target-item" data-status="${target.status || 'PENDING'}">
                <div class="target-item-status"></div>
                <div class="target-item-info">
                    <div class="target-item-name">${escapeHtml(target.target)}</div>
                    <div class="target-item-meta">${target.scope} | ${target.type} | ${target.status || 'PENDING'}</div>
                </div>
                <div class="target-item-findings">${target.findings || 0} findings</div>
            </div>
        `).join('');
    }

    // ============== LIVE PROGRESS STREAM ==============

    function connectToStream(pentestId) {
        // Disconnect existing stream if any
        disconnectStream();

        // Clear console and show connecting message
        const consoleEl = $('#stream-console');
        if (consoleEl) {
            consoleEl.innerHTML = '';
            addStreamLine('Connecting to pentest stream...', 'system');
        }

        // Update indicator
        const indicator = $('.stream-indicator');
        if (indicator) {
            indicator.classList.remove('connected');
            indicator.classList.add('connecting');
        }

        // Connect to SSE stream using the /watch endpoint (same as original webui)
        const eventSource = new EventSource(`${API}/pentests/${pentestId}/watch`);
        state.streamEventSource = eventSource;

        // Handle specific event types (matching server's SSE format)
        eventSource.addEventListener('message', (e) => {
            try {
                const data = JSON.parse(e.data);
                handleStreamMessage(data);
            } catch (err) {
                // Ignore parse errors
            }
        });

        eventSource.addEventListener('status', (e) => {
            try {
                const data = JSON.parse(e.data);
                handleStreamMessage(data);
            } catch (err) {}
        });

        eventSource.addEventListener('phase', (e) => {
            try {
                const data = JSON.parse(e.data);
                handleStreamMessage(data);
            } catch (err) {}
        });

        eventSource.addEventListener('finding', (e) => {
            try {
                const data = JSON.parse(e.data);
                handleStreamMessage(data);
            } catch (err) {}
        });

        eventSource.addEventListener('done', (e) => {
            try {
                const data = JSON.parse(e.data);
                addStreamLine(data.message || 'Stream completed', 'success');
                eventSource.close();
                state.streamEventSource = null;
                state.streamConnected = false;
                if (indicator) {
                    indicator.classList.remove('connected', 'connecting');
                }
                // Refresh pentests list to show updated status
                loadPentests();
            } catch (err) {}
        });

        eventSource.addEventListener('keepalive', (e) => {
            // Just ignore keepalives, they're for connection health
        });

        eventSource.addEventListener('error', (e) => {
            // Handle errors and reconnection
        });

        eventSource.onopen = () => {
            state.streamConnected = true;
            if (indicator) {
                indicator.classList.remove('connecting');
                indicator.classList.add('connected');
            }
            addStreamLine('Connected to real-time stream', 'success');
        };

        eventSource.onerror = (error) => {
            if (indicator) {
                indicator.classList.remove('connected', 'connecting');
            }
            if (eventSource.readyState === EventSource.CLOSED) {
                addStreamLine('Stream closed', 'info');
            } else if (state.streamConnected) {
                addStreamLine('Stream connection error, reconnecting...', 'warning');
            }
            state.streamConnected = false;
        };
    }

    function disconnectStream() {
        if (state.streamEventSource) {
            state.streamEventSource.close();
            state.streamEventSource = null;
        }
        state.streamConnected = false;

        const indicator = $('.stream-indicator');
        if (indicator) {
            indicator.classList.remove('connected', 'connecting');
        }
    }

    function handleStreamMessage(data) {
        const type = data.type;

        // Handle pentest_data - full pentest data update
        if (type === 'pentest_data') {
            const status = data.status;

            // Log pentest status update header
            addStreamLine('--- Pentest Status Update ---', 'status');
            addStreamLine(`  ID: ${data.id}`, 'output');
            addStreamLine(`  Status: ${status}`, 'output');
            addStreamLine(`  Findings: ${data.findings || 0}`, 'output');
            addStreamLine(`  Severity: ${data.severity || 'NONE'}`, 'output');

            // Log target info
            if (data.targets && data.targets.length > 0) {
                for (const target of data.targets) {
                    addStreamLine(`  Target: ${target.target}`, 'output');
                    addStreamLine(`    Status: ${target.status}`, 'output');
                    if (target.phase && target.phase !== 'PHASE_UNSPECIFIED') {
                        addStreamLine(`    Phase: ${target.phase}`, 'phase');
                    }
                    if (target.findings > 0) {
                        addStreamLine(`    Findings: ${target.findings}`, 'output');
                    }
                    if (target.severity && target.severity !== 'NONE') {
                        addStreamLine(`    Severity: ${target.severity}`, 'output');
                    }
                }
            }

            // Update selected pentest state and UI
            if (state.selectedPentest && state.selectedPentest.id === data.id) {
                state.selectedPentest = data;
                updateProgress(data);
            }

            // Check completion
            if (status === 'COMPLETED') {
                addStreamLine('Pentest completed successfully!', 'success');
                addStreamLine(`Final severity: ${data.severity || 'NONE'} | Findings: ${data.findings || 0}`, 'info');
                $('#progress-fill').style.width = '100%';
                $('#progress-percent').textContent = '100%';
            } else if (status === 'FAILED') {
                addStreamLine('Pentest failed', 'error');
            }
        }

        // Handle status_update - detailed status messages
        else if (type === 'status_update') {
            const updateType = data.update_type;
            const message = data.message;

            if (message) {
                // Map update types to log types
                let logType = 'output';
                if (updateType === 2 || updateType === 'ERROR') {
                    logType = 'error';
                } else if (updateType === 3 || updateType === 'STATUS') {
                    logType = 'status';
                } else if (updateType === 4 || updateType === 'DEBUG') {
                    logType = 'output';
                } else if (updateType === 1 || updateType === 'INFO') {
                    logType = 'info';
                }

                addStreamLine(message, logType);
            }

            // Handle nested pentest data
            if (data.data) {
                handleStreamMessage(data.data);
            }
        }

        // Handle schedule_response - when a new pentest is scheduled
        else if (type === 'schedule_response') {
            addStreamLine(`Pentest scheduled: ${data.pentest_id}`, 'success');
            if (data.message) {
                addStreamLine(data.message, 'info');
            }
            loadPentests();
        }

        // Handle error
        else if (type === 'error') {
            addStreamLine(`Error: ${data.error}`, 'error');
        }

        // Handle finding
        else if (type === 'finding') {
            const severity = (data.severity || 'info').toLowerCase();
            const msg = data.message || data.title || 'New finding detected';
            const logType = severity === 'critical' ? 'critical' : severity === 'high' ? 'error' : 'finding';
            addStreamLine(`[FINDING] ${msg}`, logType);
        }

        // Handle phase updates
        else if (type === 'phase' || data.phase) {
            const phase = data.phase || data.value;
            addStreamLine(`Phase: ${phase}`, 'phase');
            if (state.selectedPentest?.targets?.[0]) {
                state.selectedPentest.targets[0].phase = phase;
                updateProgress(state.selectedPentest);
            }
        }

        // Handle generic status updates
        else if (data.status && !type) {
            addStreamLine(`Status: ${data.status}`, 'status');
        }

        // Fallback for unknown message types
        else if (!type) {
            // Try to extract useful info
            if (data.message) {
                addStreamLine(data.message, 'info');
            }
        }
    }

    function addStreamLine(message, type = 'info') {
        const console = $('#stream-console');
        if (!console) return;

        const now = new Date();
        const time = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

        const line = document.createElement('div');
        line.className = `stream-line ${type}`;
        line.innerHTML = `
            <span class="stream-time">${time}</span>
            <span class="stream-msg">${escapeHtml(message)}</span>
        `;

        console.appendChild(line);

        // Auto-scroll if enabled
        if (state.streamAutoScroll) {
            console.scrollTop = console.scrollHeight;
        }

        // Limit lines to prevent memory issues (keep last 500)
        while (console.children.length > 500) {
            console.removeChild(console.firstChild);
        }
    }

    function clearStreamConsole() {
        const console = $('#stream-console');
        if (console) {
            console.innerHTML = '';
            addStreamLine('Console cleared', 'system');
        }
    }

    function toggleStreamAutoScroll() {
        state.streamAutoScroll = !state.streamAutoScroll;
        const btn = $('#stream-autoscroll-btn');
        if (btn) {
            btn.dataset.enabled = state.streamAutoScroll ? 'true' : 'false';
            btn.classList.toggle('active', state.streamAutoScroll);
            btn.title = state.streamAutoScroll ? 'Auto-scroll enabled' : 'Auto-scroll disabled';
        }
        showToast(state.streamAutoScroll ? 'Auto-scroll enabled' : 'Auto-scroll disabled', 'info');
    }

    // Open New Pentest Modal with playbook/memory loaded
    async function openNewPentestModal() {
        // Load playbooks
        try {
            const playbooksData = await apiRequest('/playbooks');
            const playbookSelect = $('#input-playbook');
            if (playbookSelect && playbooksData.success) {
                playbookSelect.innerHTML = '<option value="">None (Standard)</option>';
                (playbooksData.playbooks || []).forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p.name;
                    opt.textContent = p.name;
                    playbookSelect.appendChild(opt);
                });
            }
        } catch (e) {
            console.error('Failed to load playbooks:', e);
        }

        // Load memory items
        try {
            const memoryData = await apiRequest('/memory');
            const memorySelect = $('#input-memory');
            if (memorySelect && memoryData.success) {
                memorySelect.innerHTML = '';
                (memoryData.items || []).filter(i => i.name !== 'default').forEach(item => {
                    const opt = document.createElement('option');
                    opt.value = item.name;
                    opt.textContent = item.name;
                    memorySelect.appendChild(opt);
                });
                if (memorySelect.options.length === 0) {
                    const opt = document.createElement('option');
                    opt.value = '';
                    opt.textContent = 'No memory items';
                    opt.disabled = true;
                    memorySelect.appendChild(opt);
                }
            }
        } catch (e) {
            console.error('Failed to load memory items:', e);
        }

        openModal('new-pentest-modal');
    }

    // New Pentest - uses streaming endpoint for real-time updates
    async function submitNewPentest() {
        const target = $('#input-target').value.trim();
        const scope = $('#input-scope').value;
        const type = $('#input-type').value;
        const style = $('#input-style').value;
        const exploit = $('#input-exploit').checked;
        const playbook = $('#input-playbook')?.value || '';
        const memorySelect = $('#input-memory');
        const selectedMemory = memorySelect ? Array.from(memorySelect.selectedOptions).map(opt => opt.value).filter(v => v) : [];
        const includeDefaultMemory = $('#input-default-memory')?.checked ?? true;

        if (!target) {
            showToast('Please enter a target', 'error');
            return;
        }

        const request = {
            targets: [{ target, scope, type }],
            style,
            exploit,
        };

        // Add playbook if selected
        if (playbook) {
            request.playbook = playbook;
        }

        // Add memory items
        if (selectedMemory.length > 0) {
            request.memory = selectedMemory;
        }

        request.include_default_memory = includeDefaultMemory;

        // Close modal and show detail view with stream
        closeModal('new-pentest-modal');
        $('#input-target').value = '';

        // Prepare the detail view for streaming
        $('#dashboard-view').classList.remove('active');
        $('#files-view').classList.remove('active');
        $('#detail-view').classList.add('active');

        // Set up initial detail view
        $('#detail-target').textContent = target;
        $('#detail-id').textContent = 'Starting...';
        $('#detail-status-badge').innerHTML = '<span class="status-badge pending">STARTING</span>';
        $('#progress-section').style.display = 'block';
        $('#progress-fill').style.width = '0%';
        $('#progress-percent').textContent = '0%';
        $('#progress-phase').textContent = 'Initializing...';

        // Hide action buttons during streaming
        const btnDownload = $('#btn-download');
        const btnFiles = $('#btn-files');
        if (btnDownload) btnDownload.style.display = 'none';
        if (btnFiles) btnFiles.style.display = 'none';

        // Show stream section
        const streamSection = $('#stream-section');
        if (streamSection) {
            streamSection.style.display = 'block';
        }

        // Start streaming pentest
        startPentestWithStream(request);
    }

    // Start a pentest with real-time streaming using POST to /api/pentests/stream
    function startPentestWithStream(request) {
        // Disconnect any existing stream
        disconnectStream();

        // Clear console and show connecting message
        const consoleEl = $('#stream-console');
        if (consoleEl) {
            consoleEl.innerHTML = '';
            addStreamLine('Scheduling pentest with real-time streaming...', 'system');
        }

        // Update indicator
        const indicator = $('.stream-indicator');
        if (indicator) {
            indicator.classList.remove('connected');
            indicator.classList.add('connecting');
        }

        // Use fetch with readable stream for POST-based SSE
        fetch(`${API}/pentests/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            // Mark as connected
            state.streamConnected = true;
            if (indicator) {
                indicator.classList.remove('connecting');
                indicator.classList.add('connected');
            }
            addStreamLine('Connected to real-time stream', 'success');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            const processStream = () => {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        addStreamLine('Stream ended', 'info');
                        state.streamConnected = false;
                        if (indicator) {
                            indicator.classList.remove('connected', 'connecting');
                        }
                        // Refresh pentests list
                        loadPentests();
                        return;
                    }

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop(); // Keep incomplete line in buffer

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                handleStreamMessage(data);

                                // Update pentest ID in view if we got schedule response
                                if (data.type === 'schedule_response' && data.pentest_id) {
                                    $('#detail-id').textContent = data.pentest_id;
                                    state.selectedPentest = { id: data.pentest_id };
                                }

                                // Update detail view with pentest data
                                if (data.type === 'pentest_data') {
                                    state.selectedPentest = data;
                                    $('#detail-id').textContent = data.id;
                                    $('#detail-status-badge').innerHTML = `<span class="status-badge ${(data.status || 'pending').toLowerCase()}">${data.status}</span>`;
                                }
                            } catch (e) {
                                // Ignore parse errors
                            }
                        }
                    }

                    processStream();
                }).catch(error => {
                    addStreamLine(`Stream error: ${error.message}`, 'error');
                    state.streamConnected = false;
                    if (indicator) {
                        indicator.classList.remove('connected', 'connecting');
                    }
                });
            };

            processStream();

        }).catch(error => {
            addStreamLine(`Failed to start stream: ${error.message}`, 'error');
            showToast(`Failed to schedule pentest: ${error.message}`, 'error');
            state.streamConnected = false;
            if (indicator) {
                indicator.classList.remove('connected', 'connecting');
            }
        });
    }

    // File Explorer
    async function openFileExplorer() {
        if (!state.selectedPentest) return;

        // Switch to files view
        $('#dashboard-view').classList.remove('active');
        $('#detail-view').classList.remove('active');
        $('#files-view').classList.add('active');

        state.currentPath = [];
        state.selectedFile = null;

        // Try to load existing files
        try {
            const filesData = await apiRequest(`/pentests/${state.selectedPentest.id}/files`);
            state.files = filesData.files || {};

            if (Object.keys(state.files).length === 0) {
                // Need to download and extract
                showToast('Downloading evidence files...', 'info');
                await downloadAndExtract();
            } else {
                renderFilesList();
            }
        } catch (error) {
            // Try to download
            showToast('Downloading evidence files...', 'info');
            await downloadAndExtract();
        }
    }

    async function downloadAndExtract() {
        if (!state.selectedPentest) return;

        try {
            const result = await apiRequest(`/pentests/${state.selectedPentest.id}/download-and-extract`, {
                method: 'POST',
            });

            if (result.success) {
                const filesData = await apiRequest(`/pentests/${state.selectedPentest.id}/files`);
                state.files = filesData.files || {};
                renderFilesList();
                showToast('Evidence files loaded', 'success');
            } else {
                showToast(result.error || 'Failed to load files', 'error');
            }
        } catch (error) {
            showToast(`Failed to load files: ${error.message}`, 'error');
        }
    }

    function renderFilesList() {
        const container = $('#files-list');
        if (!container) return;

        // Navigate to current path
        let currentDir = state.files;
        for (const part of state.currentPath) {
            if (currentDir[part]?.type === 'directory') {
                currentDir = currentDir[part].children || {};
            }
        }

        // Update breadcrumb
        $('#files-path').textContent = '/' + state.currentPath.join('/');

        // Sort: directories first, then files
        const entries = Object.entries(currentDir).sort((a, b) => {
            const aIsDir = a[1].type === 'directory';
            const bIsDir = b[1].type === 'directory';
            if (aIsDir && !bIsDir) return -1;
            if (!aIsDir && bIsDir) return 1;
            return a[0].localeCompare(b[0]);
        });

        if (entries.length === 0) {
            container.innerHTML = '<div class="empty-state" style="padding:32px;">No files</div>';
            return;
        }

        // Add parent directory if not at root
        let html = '';
        if (state.currentPath.length > 0) {
            html += `
                <div class="file-item directory" data-type="parent" data-name="..">
                    <span class="file-item-icon">📁</span>
                    <span class="file-item-name">..</span>
                    <span class="file-item-meta">Parent Directory</span>
                </div>
            `;
        }

        html += entries.map(([name, info]) => {
            const isDir = info.type === 'directory';
            const icon = isDir ? '📁' : getFileIcon(name);
            const meta = isDir ? `${Object.keys(info.children || {}).length} items` : formatFileSize(info.size || 0);

            return `
                <div class="file-item ${isDir ? 'directory' : ''} ${state.selectedFile === name ? 'active' : ''}"
                     data-type="${info.type}" data-name="${escapeHtml(name)}">
                    <span class="file-item-icon">${icon}</span>
                    <span class="file-item-name">${escapeHtml(name)}</span>
                    <span class="file-item-meta">${meta}</span>
                </div>
            `;
        }).join('');

        container.innerHTML = html;

        // Click handlers
        container.querySelectorAll('.file-item').forEach(item => {
            item.addEventListener('click', () => {
                const name = item.dataset.name;
                const type = item.dataset.type;

                if (type === 'parent') {
                    navigateUp();
                } else if (type === 'directory') {
                    state.currentPath.push(name);
                    state.selectedFile = null;
                    renderFilesList();
                } else {
                    state.selectedFile = name;
                    $$('.file-item').forEach(i => i.classList.remove('active'));
                    item.classList.add('active');
                    previewFile(name);
                }
            });
        });
    }

    function navigateUp() {
        if (state.currentPath.length > 0) {
            state.currentPath.pop();
            state.selectedFile = null;
            renderFilesList();
        } else {
            // Go back to detail view
            $('#files-view').classList.remove('active');
            $('#detail-view').classList.add('active');
        }
    }

    async function previewFile(filename) {
        const preview = $('#file-preview');
        if (!preview || !state.selectedPentest) return;

        const fullPath = [...state.currentPath, filename].join('/');
        const pentestId = state.selectedPentest.id;

        preview.innerHTML = '<div class="preview-placeholder"><span>Loading preview...</span></div>';

        try {
            const data = await apiRequest(`/files/preview?path=${encodeURIComponent(pentestId + '/' + fullPath)}`);
            const content = data.content || '';
            const truncated = content.length > 5000 ? content.substring(0, 5000) + '\n\n... [truncated]' : content;
            preview.innerHTML = `<pre class="preview-content">${escapeHtml(truncated)}</pre>`;
        } catch (error) {
            preview.innerHTML = `<div class="preview-placeholder"><span>Unable to preview file</span></div>`;
        }
    }

    function downloadEvidence() {
        if (!state.selectedPentest) return;
        window.location.href = `${API}/pentests/${state.selectedPentest.id}/download`;
    }

    // Helpers
    function getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const icons = {
            'txt': '📄', 'log': '📄', 'md': '📝', 'json': '📋', 'xml': '📋',
            'html': '🌐', 'htm': '🌐', 'css': '🎨', 'js': '📜',
            'py': '🐍', 'sh': '⚙️', 'bash': '⚙️',
            'png': '🖼️', 'jpg': '🖼️', 'jpeg': '🖼️', 'gif': '🖼️', 'svg': '🖼️',
            'pdf': '📕', 'doc': '📘', 'docx': '📘',
            'zip': '📦', 'tar': '📦', 'gz': '📦',
            'csv': '📊', 'xlsx': '📊', 'xls': '📊',
        };
        return icons[ext] || '📄';
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    function formatDate(dateStr) {
        if (!dateStr) return '---';
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: '2-digit' });
    }

    function formatDateTime(dateStr) {
        if (!dateStr) return '---';
        const date = new Date(dateStr);
        return date.toLocaleString('en-GB', {
            day: '2-digit', month: '2-digit', year: '2-digit',
            hour: '2-digit', minute: '2-digit',
        });
    }

    function calculateDuration(startStr, endStr) {
        if (!startStr) return '---';
        const start = new Date(startStr);
        const end = endStr ? new Date(endStr) : new Date();
        const diff = end - start;

        const hours = Math.floor(diff / 3600000);
        const minutes = Math.floor((diff % 3600000) / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);

        if (hours > 0) return `${hours}h ${minutes}m`;
        if (minutes > 0) return `${minutes}m ${seconds}s`;
        return `${seconds}s`;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ============== THREAT MAP (ECharts) ==============
    let echartsMap = null;
    let worldMapLoaded = false;
    let serverOrigin = null;  // Server location [lon, lat]
    let serverOriginFetched = false;  // Track if we've fetched server location
    const targetGeoCache = new Map();  // Cache for resolved target coordinates
    let mapRenderLock = false;  // Prevent concurrent map renders
    let pendingMapRender = false;  // Track if a render is pending

    // Fetch server geolocation to use as attack origin
    async function fetchServerGeolocation(forceRefresh = false) {
        if (serverOriginFetched && !forceRefresh) {
            return serverOrigin;
        }

        try {
            const response = await fetch('/api/geolocation/server');
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.lat && data.lon) {
                    serverOrigin = [data.lon, data.lat];
                    serverOriginFetched = true;
                    console.log('Server origin set to:', serverOrigin, `(${data.city}, ${data.country})`);
                    return serverOrigin;
                }
            }
        } catch (error) {
            console.error('Failed to fetch server geolocation:', error);
        }
        // Default fallback
        serverOrigin = [-98.5, 39.8]; // Center of US
        serverOriginFetched = true;
        return serverOrigin;
    }

    // Clear geo cache when needed (e.g., on refresh)
    function clearGeoCache() {
        targetGeoCache.clear();
        serverOriginFetched = false;
        serverOrigin = null;
    }

    // Batch resolve targets to get their real geolocations
    async function resolveTargetGeolocations(targets) {
        // Filter out targets already in cache
        const targetsToResolve = targets.filter(t => !targetGeoCache.has(t));

        if (targetsToResolve.length === 0) return;

        try {
            const response = await fetch('/api/geolocation/batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ targets: targetsToResolve })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.results) {
                    data.results.forEach(result => {
                        if (result.success && result.lat && result.lon) {
                            targetGeoCache.set(result.target, [result.lon, result.lat]);
                            console.log(`Resolved ${result.target} to [${result.lon}, ${result.lat}]`);
                        } else {
                            // Cache the TLD-based fallback to avoid re-trying failed resolutions
                            const fallbackCoords = getTargetCoordinates(result.target);
                            targetGeoCache.set(result.target, fallbackCoords);
                            console.log(`Using TLD fallback for ${result.target}: [${fallbackCoords[0]}, ${fallbackCoords[1]}]`);
                        }
                    });
                }
            }
        } catch (error) {
            console.error('Failed to batch resolve targets:', error);
            // On error, cache TLD-based fallbacks for all targets
            targetsToResolve.forEach(target => {
                if (!targetGeoCache.has(target)) {
                    const fallbackCoords = getTargetCoordinates(target);
                    targetGeoCache.set(target, fallbackCoords);
                }
            });
        }
    }

    // Load world map GeoJSON
    async function loadWorldMap() {
        if (worldMapLoaded) return true;

        try {
            // Use a reliable GeoJSON source for world map
            const response = await fetch('https://cdn.jsdelivr.net/npm/echarts@4.9.0/map/json/world.json');
            if (!response.ok) throw new Error('Failed to fetch world map');

            const worldGeoJson = await response.json();
            echarts.registerMap('world', worldGeoJson);
            worldMapLoaded = true;
            return true;
        } catch (error) {
            console.error('Failed to load world map:', error);
            return false;
        }
    }

    // Major city coordinates for TLD/domain-based positioning
    const cityCoordinates = {
        // North America
        'us': [-98.5, 39.8], 'com': [-122.0, 37.4], 'ca': [-106.3, 56.1], 'mx': [-102.5, 23.6],
        // South America
        'br': [-51.9, -14.2], 'ar': [-63.6, -38.4], 'cl': [-71.5, -35.7], 'co': [-74.1, 4.6],
        // Europe
        'uk': [-0.1, 51.5], 'de': [10.4, 51.2], 'fr': [2.2, 46.2], 'es': [-3.7, 40.5],
        'it': [12.6, 41.9], 'nl': [5.3, 52.1], 'ch': [8.2, 46.8], 'eu': [4.4, 50.9],
        'ie': [-7.7, 53.1], 'pl': [19.1, 51.9], 'ru': [105.3, 61.5], 'se': [18.6, 60.1],
        'no': [8.5, 60.5], 'pt': [-9.1, 38.7], 'at': [14.6, 47.5], 'be': [4.5, 50.5],
        // Asia
        'cn': [104.2, 35.9], 'jp': [138.3, 36.2], 'kr': [127.8, 35.9], 'in': [79.0, 20.6],
        'sg': [103.8, 1.4], 'hk': [114.1, 22.4], 'tw': [121.0, 23.7], 'ae': [53.8, 23.4],
        'il': [34.9, 31.0], 'th': [100.9, 15.9], 'vn': [108.3, 14.1], 'my': [101.9, 4.2],
        'ph': [121.8, 12.9], 'id': [113.9, -0.8], 'pk': [69.3, 30.4],
        // Oceania
        'au': [133.8, -25.3], 'nz': [174.9, -40.9],
        // Africa
        'za': [22.9, -30.6], 'eg': [30.8, 26.8], 'ng': [8.7, 9.1], 'ke': [37.9, 0.0],
        'ma': [-7.1, 31.8], 'gh': [-1.0, 7.9],
        // Middle East
        'sa': [45.1, 23.9], 'tr': [35.2, 38.9], 'qa': [51.2, 25.3],
        // Default/generic
        'net': [-74.0, 40.7], 'org': [-122.3, 47.6], 'io': [-0.1, 51.5], 'sh': [-0.1, 51.5],
    };

    // Get TLD from domain
    function getTLD(target) {
        const parts = target.split('.');
        return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : 'com';
    }

    // Convert domain/IP to [longitude, latitude]
    function getTargetCoordinates(target) {
        const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
        let lon, lat;

        if (ipRegex.test(target)) {
            const parts = target.split('.').map(Number);
            if (parts[0] < 100) { lat = 40; lon = -100; }
            else if (parts[0] < 150) { lat = 50; lon = 10; }
            else if (parts[0] < 200) { lat = 35; lon = 105; }
            else { lat = -25; lon = 135; }
            lat += (parts[1] - 128) * 0.1;
            lon += (parts[2] - 128) * 0.2;
        } else {
            const tld = getTLD(target);
            const coords = cityCoordinates[tld] || cityCoordinates['com'];
            lon = coords[0]; lat = coords[1];
        }

        // Add small deterministic variance to spread overlapping points
        // Keep variance small (±1°) to prevent points from going off land
        let hash = 0;
        for (let i = 0; i < target.length; i++) {
            hash = ((hash << 5) - hash) + target.charCodeAt(i);
            hash = hash & hash;
        }
        lat += ((hash % 100) - 50) * 0.02;  // ±1° latitude max
        lon += (((hash >> 8) % 100) - 50) * 0.02;  // ±1° longitude max

        return [lon, lat];
    }

    // Render the threat map
    async function renderThreatMap() {
        // Prevent concurrent renders
        if (mapRenderLock) {
            pendingMapRender = true;
            return;
        }
        mapRenderLock = true;
        pendingMapRender = false;

        try {
            await doRenderThreatMap();
        } finally {
            mapRenderLock = false;
            // If a render was requested while we were busy, do it now
            if (pendingMapRender) {
                setTimeout(() => renderThreatMap(), 100);
            }
        }
    }

    // Internal render function
    async function doRenderThreatMap() {
        // Ensure world map is loaded
        if (!await loadWorldMap()) {
            console.error('World map not available');
            return;
        }

        if (!echartsMap) {
            // Try to initialize if not done
            const container = document.getElementById('echarts-map');
            if (container && typeof echarts !== 'undefined') {
                echartsMap = echarts.init(container, null, { renderer: 'canvas' });
                // Handle resize
                window.addEventListener('resize', () => {
                    echartsMap?.resize();
                });
            } else {
                return;
            }
        }

        // Fetch server origin - don't block on this
        if (state.connected && !serverOriginFetched) {
            // Start async fetch, don't await
            fetchServerGeolocation(true).then(() => {
                // Re-render when server location is resolved
                if (serverOrigin) {
                    renderThreatMap();
                }
            });
        }

        // Use default if not yet fetched
        if (!serverOrigin) {
            serverOrigin = [-98.5, 39.8];
        }

        // Collect targets that need resolution (don't block, resolve async)
        const unresolvedTargets = [];
        if (state.pentests.length > 0 && state.connected) {
            state.pentests.forEach(pentest => {
                if (pentest.targets) {
                    pentest.targets.forEach(t => {
                        if (t.target && !targetGeoCache.has(t.target)) {
                            unresolvedTargets.push(t.target);
                        }
                    });
                }
            });

            // Start async resolution in background (don't await)
            if (unresolvedTargets.length > 0) {
                console.log('Starting async resolution for:', unresolvedTargets);
                resolveTargetGeolocations(unresolvedTargets).then(() => {
                    // Re-render map when resolutions complete
                    console.log('Resolution complete, re-rendering map');
                    renderThreatMap();
                });
            }
        }

        // Update stats - use correct API status values
        const activeCount = state.pentests.filter(p => p.status === 'IN_PROGRESS').length;
        const completedCount = state.pentests.filter(p => p.status === 'COMPLETED').length;
        const mapActive = document.getElementById('map-active');
        const mapCompleted = document.getElementById('map-completed');
        if (mapActive) mapActive.textContent = activeCount;
        if (mapCompleted) mapCompleted.textContent = completedCount;

        // Origin point - use server location or default
        const origin = serverOrigin || [-98.5, 39.8];

        // Prepare data
        const scatterData = [];
        const linesData = [];
        const effectScatterData = [];
        const processedTargets = new Map();

        // Status colors
        const statusColors = {
            active: '#ff9500',
            completed: '#00ff9d',
            critical: '#ff3b5c',
            scheduled: '#00d4ff'
        };

        // Process pentests - only show demo if NOT connected (no credentials/server)
        const showDemo = state.pentests.length === 0 && !state.connected;

        if (state.pentests.length > 0) {
            state.pentests.forEach((pentest, index) => {
                const target = pentest.targets?.[0]?.target || `target-${index}`;
                if (processedTargets.has(target)) return;
                processedTargets.set(target, pentest);

                // Use cached geolocation if available, otherwise fallback to TLD-based
                const coords = targetGeoCache.get(target) || getTargetCoordinates(target);
                // Map API status to legend status - correct mapping:
                // IN_PROGRESS -> active (orange)
                // COMPLETED -> completed (green) or critical (red) if severity is CRITICAL
                // PENDING -> scheduled (cyan)
                const status = pentest.status === 'IN_PROGRESS' ? 'active' :
                              pentest.status === 'COMPLETED' ?
                                (pentest.severity === 'CRITICAL' ? 'critical' : 'completed') :
                              pentest.status === 'PENDING' ? 'scheduled' : 'completed';

                const color = statusColors[status];

                // Add scatter point
                scatterData.push({
                    name: target,
                    value: coords,
                    status: status,
                    pentest: pentest,
                    itemStyle: { color: color }
                });

                // Add effect scatter for active/critical
                if (status === 'active' || status === 'critical') {
                    effectScatterData.push({
                        name: target,
                        value: coords,
                        pentest: pentest,
                        itemStyle: { color: color }
                    });
                }

                // Add line from origin to target
                linesData.push({
                    coords: [origin, coords],
                    lineStyle: {
                        color: color,
                        width: status === 'active' ? 2 : 1,
                        opacity: status === 'active' ? 0.8 : 0.4,
                        curveness: 0.3
                    }
                });
            });
        } else if (showDemo) {
            // Demo data - only show when not connected
            const demoTargets = [
                { name: 'New York', coords: [-74.0, 40.7], status: 'completed' },
                { name: 'London', coords: [-0.1, 51.5], status: 'active' },
                { name: 'Tokyo', coords: [139.7, 35.7], status: 'completed' },
                { name: 'Sydney', coords: [151.2, -33.9], status: 'scheduled' },
                { name: 'São Paulo', coords: [-46.6, -23.6], status: 'critical' },
                { name: 'Berlin', coords: [13.4, 52.5], status: 'completed' },
                { name: 'Singapore', coords: [103.8, 1.4], status: 'active' },
                { name: 'Dubai', coords: [55.3, 25.3], status: 'completed' },
                { name: 'Mumbai', coords: [72.9, 19.1], status: 'completed' },
                { name: 'Toronto', coords: [-79.4, 43.7], status: 'scheduled' },
            ];

            demoTargets.forEach(demo => {
                const color = statusColors[demo.status];
                scatterData.push({
                    name: demo.name,
                    value: demo.coords,
                    status: demo.status,
                    itemStyle: { color: color }
                });
                if (demo.status === 'active' || demo.status === 'critical') {
                    effectScatterData.push({
                        name: demo.name,
                        value: demo.coords,
                        itemStyle: { color: color }
                    });
                }
                linesData.push({
                    coords: [origin, demo.coords],
                    lineStyle: {
                        color: color,
                        width: demo.status === 'active' ? 2 : 1,
                        opacity: demo.status === 'active' ? 0.8 : 0.4,
                        curveness: 0.3
                    }
                });
            });
        }

        // ECharts option
        const option = {
            backgroundColor: 'transparent',
            geo: {
                map: 'world',
                roam: true,
                zoom: 1.2,
                center: [0, 20],
                silent: false,
                itemStyle: {
                    areaColor: 'rgba(0, 212, 255, 0.05)',
                    borderColor: 'rgba(0, 212, 255, 0.3)',
                    borderWidth: 0.5
                },
                emphasis: {
                    itemStyle: {
                        areaColor: 'rgba(0, 212, 255, 0.15)',
                        borderColor: 'rgba(0, 212, 255, 0.6)',
                    },
                    label: {
                        show: false
                    }
                },
                select: {
                    disabled: true
                }
            },
            series: [
                // Attack lines
                {
                    type: 'lines',
                    coordinateSystem: 'geo',
                    zlevel: 1,
                    effect: {
                        show: true,
                        period: 4,
                        trailLength: 0.3,
                        symbol: 'circle',
                        symbolSize: 4,
                        color: '#00d4ff'
                    },
                    lineStyle: {
                        width: 1,
                        opacity: 0.5,
                        curveness: 0.3
                    },
                    data: linesData
                },
                // Origin point (Server location)
                {
                    type: 'effectScatter',
                    coordinateSystem: 'geo',
                    zlevel: 2,
                    rippleEffect: {
                        brushType: 'stroke',
                        scale: 4,
                        period: 3
                    },
                    itemStyle: {
                        color: '#00d4ff',
                        shadowBlur: 10,
                        shadowColor: '#00d4ff'
                    },
                    symbolSize: 14,
                    label: {
                        show: true,
                        formatter: 'Server',
                        position: 'right',
                        fontSize: 10,
                        color: '#00d4ff'
                    },
                    data: [{
                        name: 'Server',
                        value: origin
                    }]
                },
                // Target points (static)
                {
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    zlevel: 2,
                    symbol: 'circle',
                    symbolSize: 8,
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 212, 255, 0.5)'
                    },
                    label: {
                        show: false
                    },
                    emphasis: {
                        scale: 1.5,
                        label: {
                            show: true,
                            formatter: '{b}',
                            position: 'top',
                            color: '#fff',
                            fontSize: 11,
                            backgroundColor: 'rgba(10, 14, 20, 0.8)',
                            padding: [4, 8],
                            borderRadius: 4
                        }
                    },
                    data: scatterData
                },
                // Active/Critical points (animated)
                {
                    type: 'effectScatter',
                    coordinateSystem: 'geo',
                    zlevel: 3,
                    rippleEffect: {
                        brushType: 'stroke',
                        scale: 3,
                        period: 2
                    },
                    symbolSize: 10,
                    label: {
                        show: false
                    },
                    emphasis: {
                        scale: 1.5,
                        label: {
                            show: true,
                            formatter: '{b}',
                            position: 'top',
                            color: '#fff',
                            fontSize: 11,
                            backgroundColor: 'rgba(10, 14, 20, 0.8)',
                            padding: [4, 8],
                            borderRadius: 4
                        }
                    },
                    data: effectScatterData
                }
            ]
        };

        echartsMap.setOption(option);

        // Click event for selecting pentest (both scatter and effectScatter series)
        echartsMap.off('click');
        echartsMap.on('click', (params) => {
            // Handle clicks on scatter and effectScatter series
            if ((params.seriesType === 'scatter' || params.seriesType === 'effectScatter') &&
                params.data?.pentest?.id) {
                selectPentest(params.data.pentest.id);
            }
        });
    }

    // Modals
    function openModal(id) {
        $(`#${id}`)?.classList.add('active');
    }

    function closeModal(id) {
        $(`#${id}`)?.classList.remove('active');
    }

    // Toasts
    function showToast(message, type = 'info') {
        const container = $('#toast-container');
        if (!container) return;

        const icons = {
            success: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>',
            error: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
            warning: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            info: '<svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        };

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            ${icons[type] || icons.info}
            <span class="toast-message">${escapeHtml(message)}</span>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // Start application
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
