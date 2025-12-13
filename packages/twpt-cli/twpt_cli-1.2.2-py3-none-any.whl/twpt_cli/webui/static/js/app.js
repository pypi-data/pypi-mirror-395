// ThreatWinds Pentest Terminal - Web UI Application

/**
 * TabContext - Represents an independent console tab with its own state
 */
class TabContext {
    constructor(tabId, title, terminal) {
        this.tabId = tabId;
        this.title = title;
        this.terminal = terminal;
        this.pentestId = null;
        this.eventSource = null;  // SSE connection for streaming
        this.status = null;
        this.commandHistory = [];
        this.historyIndex = -1;
    }

    log(type, message) {
        this.terminal.logToTab(this.tabId, type, message);
    }

    setStatus(status) {
        this.status = status;
        this.terminal.updateTabStatus(this.tabId, status);
    }

    closeEventSource() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

class PentestTerminal {
    constructor() {
        this.apiBase = '/api';
        this.pentests = [];
        this.servers = [];
        this.activeServer = null;
        this.selectedPentest = null;
        this.evidenceFiles = {};
        this.autoScroll = true;
        this.watchInterval = null;
        this.progressInterval = null;
        this.connectionCheckInterval = null;
        this.hasCredentials = false;

        // Tab management - each tab is fully independent
        this.tabs = new Map(); // tabId -> TabContext object
        this.activeTabId = 'main';
        this.tabCounter = 0;

        this.init();
    }

    async init() {
        this.bindElements();
        this.bindEvents();
        this.startClock();

        // Check if credentials exist first
        await this.checkCredentialsAndInit();
    }

    async checkCredentialsAndInit() {
        try {
            const status = await this.apiRequest('/status');
            this.hasCredentials = status.has_credentials;

            if (!this.hasCredentials) {
                // Force credentials modal on first use
                this.showCredentialsModal();
                this.log('system', 'Welcome! Please configure your API credentials to continue.');
            } else {
                // Normal initialization
                this.loadServers();
                this.checkConnection();
                this.loadPentests();
                this.getVersion();
                this.calculateAveragePentestDuration();

                // Start periodic connection check
                this.connectionCheckInterval = setInterval(() => this.checkConnection(), 30000);

                this.log('system', 'Terminal ready. Type "help" for available commands.');
            }
        } catch (error) {
            // API not available, show credentials modal
            this.showCredentialsModal();
            this.log('system', 'Welcome! Please configure your server connection.');
        }
    }

    bindElements() {
        // Servers section
        this.serversList = document.getElementById('servers-list');
        this.addServerBtn = document.getElementById('add-server');

        // Left panel
        this.pentestsList = document.getElementById('pentests-list');
        this.refreshPentestsBtn = document.getElementById('refresh-pentests');

        // Pentest details
        this.detailId = document.getElementById('detail-id');
        this.detailStatus = document.getElementById('detail-status');
        this.detailMode = document.getElementById('detail-mode');
        this.detailStyle = document.getElementById('detail-style');
        this.detailPhase = document.getElementById('detail-phase');
        this.detailSeverity = document.getElementById('detail-severity');
        this.detailFindings = document.getElementById('detail-findings');
        this.detailCreated = document.getElementById('detail-created');
        this.detailStarted = document.getElementById('detail-started');
        this.detailFinished = document.getElementById('detail-finished');

        // Connection status
        this.globeIcon = document.querySelector('.globe-icon');
        this.connectionText = document.getElementById('connection-text');
        this.serverAddress = document.getElementById('server-address');
        this.serverCountry = document.getElementById('server-country');

        // Console tabs
        this.consoleTabs = document.getElementById('console-tabs');
        this.consoleTabsContent = document.getElementById('console-tabs-content');
        this.newTabBtn = document.getElementById('new-tab');

        // Console
        this.consoleInput = document.getElementById('console-input');
        this.clearConsoleBtn = document.getElementById('clear-console');
        this.toggleAutoscrollBtn = document.getElementById('toggle-autoscroll');

        // Autocomplete elements
        this.autocompleteSuggestion = document.getElementById('autocomplete-suggestion');
        this.autocompleteDropdown = document.getElementById('autocomplete-dropdown');
        this.autocompleteSelectedIndex = -1;

        // Command definitions with descriptions
        this.commandDefinitions = [
            { name: 'help', desc: 'Show help message' },
            { name: 'clear', desc: 'Clear console output' },
            { name: 'cls', desc: 'Clear console output' },
            { name: 'list', desc: 'List all pentests' },
            { name: 'ls', desc: 'List all pentests' },
            { name: 'run', desc: 'Schedule pentest for target', usage: 'run <target>' },
            { name: 'runtab', desc: 'Schedule pentest in new tab', usage: 'runtab <target>' },
            { name: 'get', desc: 'Get pentest details', usage: 'get [id]' },
            { name: 'watch', desc: 'Watch pentest progress', usage: 'watch [id]' },
            { name: 'stop', desc: 'Stop watching pentest' },
            { name: 'download', desc: 'Download evidence', usage: 'download [id]' },
            { name: 'status', desc: 'Show connection status' },
            { name: 'version', desc: 'Show version info' },
            { name: 'refresh', desc: 'Refresh pentests list' },
            { name: 'servers', desc: 'List configured servers' },
            { name: 'init', desc: 'Add new server connection' },
            { name: 'newtab', desc: 'Create new console tab' },
            { name: 'tab', desc: 'Create new console tab' },
            { name: 'closetab', desc: 'Close current tab' },
            { name: 'tabs', desc: 'List all open tabs' },
            { name: 'open', desc: 'Open file in file explorer tab', usage: 'open <path>' },
            { name: 'files', desc: 'List files in current tab' },
            { name: 'chat', desc: 'Set chat context for pentest', usage: 'chat [id]' },
            { name: 'attach', desc: 'Attach to running pentest stream', usage: 'attach [id]' },
            { name: 'attachtab', desc: 'Attach to pentest in new tab', usage: 'attachtab [id]' },
            // Playbook commands
            { name: 'playbook', desc: 'Playbook management', usage: 'playbook <list|show|delete> [name]' },
            { name: 'playbooks', desc: 'List all playbooks' },
            // Memory commands
            { name: 'memory', desc: 'Memory management', usage: 'memory <list|show|delete> [name]' },
            { name: 'memories', desc: 'List all memory items' },
            // Task commands
            { name: 'task', desc: 'Run custom task', usage: 'task <description> -t <target>' },
            { name: 'tasks', desc: 'List custom tasks' }
        ];

        // Initialize main tab with TabContext
        this.tabs.set('main', new TabContext('main', 'MAIN', this));

        // Progress
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');

        // Right panel - Chat
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.chatSendBtn = document.getElementById('chat-send');
        this.clearChatBtn = document.getElementById('clear-chat');
        this.chatPentestContext = document.getElementById('chat-pentest-context');
        this.chatContextPentestId = null;

        // Quick actions
        this.btnNewPentest = document.getElementById('btn-new-pentest');
        this.btnWatch = document.getElementById('btn-watch');
        this.btnStop = document.getElementById('btn-stop');
        this.btnExport = document.getElementById('btn-export');

        // Pentest Modal
        this.newPentestModal = document.getElementById('new-pentest-modal');
        this.modalClose = document.getElementById('modal-close');
        this.modalCancel = document.getElementById('modal-cancel');
        this.modalSubmit = document.getElementById('modal-submit');
        this.targetInput = document.getElementById('target-input');
        this.scopeSelect = document.getElementById('scope-select');
        this.typeSelect = document.getElementById('type-select');
        this.styleSelect = document.getElementById('style-select');
        this.exploitCheckbox = document.getElementById('exploit-checkbox');

        // Credentials Modal
        this.credentialsModal = document.getElementById('credentials-modal');
        this.credApiKey = document.getElementById('cred-api-key');
        this.credApiSecret = document.getElementById('cred-api-secret');
        this.credServerHost = document.getElementById('cred-server-host');
        this.credServerPort = document.getElementById('cred-server-port');
        this.credSubmit = document.getElementById('cred-submit');

        // Add Server Modal
        this.addServerModal = document.getElementById('add-server-modal');
        this.serverModalClose = document.getElementById('server-modal-close');
        this.serverModalCancel = document.getElementById('server-modal-cancel');
        this.serverModalSubmit = document.getElementById('server-modal-submit');
        this.serverName = document.getElementById('server-name');
        this.serverHost = document.getElementById('server-host');
        this.serverPort = document.getElementById('server-port');
        this.serverGrpcPort = document.getElementById('server-grpc-port');
        this.serverUseExistingCreds = document.getElementById('server-use-existing-creds');
        this.serverNewCreds = document.getElementById('server-new-creds');
        this.serverApiKey = document.getElementById('server-api-key');
        this.serverApiSecret = document.getElementById('server-api-secret');

        // Header/Footer
        this.currentDatetime = document.getElementById('current-datetime');
        this.currentIp = document.getElementById('current-ip');
        this.versionInfo = document.getElementById('version-info');
        this.footerStatus = document.getElementById('footer-status');
    }

    bindEvents() {
        // Console input
        this.consoleInput.addEventListener('keydown', (e) => this.handleConsoleInput(e));
        this.consoleInput.addEventListener('input', (e) => this.handleAutocompleteInput(e));
        this.consoleInput.addEventListener('blur', () => this.hideAutocompleteDropdown());

        // Tab management
        this.newTabBtn.addEventListener('click', () => this.createNewTab());

        // Main tab click handler (existing tab from HTML template)
        const mainTab = this.consoleTabs.querySelector('.tab[data-tab-id="main"]');
        if (mainTab) {
            mainTab.addEventListener('click', (e) => {
                if (!e.target.classList.contains('tab-close')) {
                    this.switchTab('main');
                }
            });
        }

        // Server management
        this.addServerBtn.addEventListener('click', () => this.openAddServerModal());

        // UI Switching
        const switchUiBtn = document.getElementById('switch-ui-btn');
        if (switchUiBtn) {
            switchUiBtn.addEventListener('click', () => {
                window.location.href = '/simple';
            });
        }

        // Refresh pentests
        this.refreshPentestsBtn.addEventListener('click', () => this.loadPentests());

        // Console controls
        this.clearConsoleBtn.addEventListener('click', () => this.clearConsole());
        this.toggleAutoscrollBtn.addEventListener('click', () => this.toggleAutoscroll());

        // Quick actions
        this.btnNewPentest.addEventListener('click', () => this.openNewPentestModal());
        this.btnWatch.addEventListener('click', () => this.watchPentest());
        this.btnStop.addEventListener('click', () => this.stopWatch());
        this.btnExport.addEventListener('click', () => this.exportResults());

        // Chat
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendChatMessage();
            }
        });
        this.chatSendBtn.addEventListener('click', () => this.sendChatMessage());
        this.clearChatBtn.addEventListener('click', () => this.clearChat());

        // Pentest Modal
        this.modalClose.addEventListener('click', () => this.closeModal());
        this.modalCancel.addEventListener('click', () => this.closeModal());
        this.modalSubmit.addEventListener('click', () => this.submitNewPentest());

        // Credentials Modal
        this.credSubmit.addEventListener('click', () => this.submitCredentials());

        // Add Server Modal
        this.serverModalClose.addEventListener('click', () => this.closeAddServerModal());
        this.serverModalCancel.addEventListener('click', () => this.closeAddServerModal());
        this.serverModalSubmit.addEventListener('click', () => this.submitAddServer());
        this.serverUseExistingCreds.addEventListener('change', (e) => {
            this.serverNewCreds.style.display = e.target.checked ? 'none' : 'block';
        });

        // Close modal on outside click
        this.newPentestModal.addEventListener('click', (e) => {
            if (e.target === this.newPentestModal) {
                this.closeModal();
            }
        });

        this.addServerModal.addEventListener('click', (e) => {
            if (e.target === this.addServerModal) {
                this.closeAddServerModal();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
                this.closeAddServerModal();
            }

            // Handle file explorer keyboard navigation
            const tabContext = this.tabs.get(this.activeTabId);
            if (tabContext && tabContext.fileExplorerActive) {
                // Don't capture if user is typing in an input
                if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
                    return;
                }

                if (this.handleFileExplorerKeyboard(this.activeTabId, e.key)) {
                    e.preventDefault();
                }
            }
        });
    }

    // Clock
    startClock() {
        const updateClock = () => {
            const now = new Date();
            const dateStr = now.toLocaleDateString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            }).replace(/\//g, '.');

            const timeStr = now.toLocaleTimeString('en-GB', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });

            this.currentDatetime.textContent = `${dateStr} ${timeStr}`;
        };

        updateClock();
        setInterval(updateClock, 1000);
    }

    // API Methods
    async apiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    // Credentials Management
    showCredentialsModal() {
        this.credentialsModal.classList.add('active');
        this.credApiKey.focus();
    }

    async submitCredentials() {
        const apiKey = this.credApiKey.value.trim();
        const apiSecret = this.credApiSecret.value.trim();
        const serverHost = this.credServerHost.value.trim() || 'localhost';
        const serverPort = this.credServerPort.value.trim() || '9741';

        if (!apiKey || !apiSecret) {
            this.log('error', 'API Key and Secret are required');
            return;
        }

        this.log('info', 'Validating credentials...');

        try {
            const data = await this.apiRequest('/credentials', {
                method: 'POST',
                body: JSON.stringify({
                    api_key: apiKey,
                    api_secret: apiSecret,
                    host: serverHost,
                    port: serverPort
                })
            });

            if (data.success) {
                this.credentialsModal.classList.remove('active');
                this.hasCredentials = true;
                this.log('success', 'Credentials saved successfully');

                // Initialize the rest of the app
                this.loadServers();
                this.checkConnection();
                this.loadPentests();
                this.getVersion();
                this.calculateAveragePentestDuration();

                this.connectionCheckInterval = setInterval(() => this.checkConnection(), 30000);
            } else {
                this.log('error', data.error || 'Failed to save credentials');
            }
        } catch (error) {
            this.log('error', `Credentials error: ${error.message}`);
        }
    }

    // Server Management
    async loadServers() {
        try {
            const data = await this.apiRequest('/servers');
            this.servers = data.servers || [];
            this.activeServer = data.active_server || null;
            this.renderServersList();
        } catch (error) {
            this.servers = [];
            this.renderServersList();
        }
    }

    renderServersList() {
        if (this.servers.length === 0) {
            this.serversList.innerHTML = '<div class="empty-state" style="padding: 8px; font-size: 10px;">No servers configured</div>';
            return;
        }

        this.serversList.innerHTML = this.servers.map(server => {
            const isActive = this.activeServer && this.activeServer.id === server.id;
            return `
                <div class="server-item ${isActive ? 'active' : ''}" data-id="${server.id}">
                    <span class="server-status-dot"></span>
                    <span class="server-name">${this.escapeHtml(server.name)}</span>
                    <span class="server-host">${this.escapeHtml(server.host)}</span>
                    <button class="server-remove" data-id="${server.id}" title="Remove">&times;</button>
                </div>
            `;
        }).join('');

        // Add click handlers for server selection
        this.serversList.querySelectorAll('.server-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.classList.contains('server-remove')) {
                    this.switchServer(item.dataset.id);
                }
            });
        });

        // Add click handlers for remove buttons
        this.serversList.querySelectorAll('.server-remove').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.removeServer(btn.dataset.id);
            });
        });
    }

    async switchServer(serverId) {
        try {
            const data = await this.apiRequest('/servers/switch', {
                method: 'POST',
                body: JSON.stringify({ server_id: serverId })
            });

            if (data.success) {
                this.log('info', `Switched to server: ${data.server_name}`);
                this.loadServers();
                this.checkConnection();
                this.loadPentests();
            }
        } catch (error) {
            this.log('error', `Failed to switch server: ${error.message}`);
        }
    }

    async removeServer(serverId) {
        if (!confirm('Remove this server connection?')) return;

        try {
            const data = await this.apiRequest(`/servers/${serverId}`, {
                method: 'DELETE'
            });

            if (data.success) {
                this.log('info', 'Server removed');
                this.loadServers();
            }
        } catch (error) {
            this.log('error', `Failed to remove server: ${error.message}`);
        }
    }

    openAddServerModal() {
        if (!this.hasCredentials) {
            this.showCredentialsModal();
            return;
        }

        this.addServerModal.classList.add('active');
        this.serverName.focus();
    }

    closeAddServerModal() {
        this.addServerModal.classList.remove('active');
        this.serverName.value = '';
        this.serverHost.value = '';
        this.serverPort.value = '9741';
        this.serverGrpcPort.value = '9742';
        this.serverUseExistingCreds.checked = true;
        this.serverNewCreds.style.display = 'none';
        this.serverApiKey.value = '';
        this.serverApiSecret.value = '';
    }

    async submitAddServer() {
        const name = this.serverName.value.trim();
        const host = this.serverHost.value.trim();
        const port = this.serverPort.value.trim() || '9741';
        const grpcPort = this.serverGrpcPort.value.trim() || '9742';
        const useExistingCreds = this.serverUseExistingCreds.checked;

        if (!name || !host) {
            this.log('error', 'Server name and host are required');
            return;
        }

        const serverData = {
            name,
            host,
            port,
            grpc_port: grpcPort,
            use_existing_credentials: useExistingCreds
        };

        if (!useExistingCreds) {
            const apiKey = this.serverApiKey.value.trim();
            const apiSecret = this.serverApiSecret.value.trim();

            if (!apiKey || !apiSecret) {
                this.log('error', 'API Key and Secret are required for new credentials');
                return;
            }

            serverData.api_key = apiKey;
            serverData.api_secret = apiSecret;
        }

        try {
            const data = await this.apiRequest('/servers', {
                method: 'POST',
                body: JSON.stringify(serverData)
            });

            if (data.success) {
                this.closeAddServerModal();
                this.log('success', `Server "${name}" added successfully`);
                this.loadServers();
            } else {
                this.log('error', data.error || 'Failed to add server');
            }
        } catch (error) {
            this.log('error', `Failed to add server: ${error.message}`);
        }
    }

    async checkConnection() {
        try {
            const data = await this.apiRequest('/status');
            this.globeIcon.classList.add('connected');
            this.connectionText.textContent = 'Connected';
            this.serverAddress.textContent = data.server || 'localhost';
            this.currentIp.textContent = data.ip || '---';
            this.hasCredentials = data.has_credentials;

            // Update country display
            if (data.country) {
                this.serverCountry.textContent = data.country;
            } else {
                // For local/private IPs show "Local"
                const server = data.server || '';
                if (server.startsWith('localhost') || server.startsWith('127.') ||
                    server.startsWith('192.168.') || server.startsWith('10.') || server.startsWith('172.')) {
                    this.serverCountry.textContent = 'Local';
                } else {
                    this.serverCountry.textContent = '---';
                }
            }

            return true;
        } catch (error) {
            this.globeIcon.classList.remove('connected');
            this.connectionText.textContent = 'Disconnected';
            this.serverAddress.textContent = '---';
            this.serverCountry.textContent = '---';
            return false;
        }
    }

    async getVersion() {
        try {
            const data = await this.apiRequest('/version');
            this.versionInfo.textContent = `v${data.version || '1.0.0'}`;
        } catch (error) {
            this.versionInfo.textContent = 'v1.0.0';
        }
    }

    // Calculate average pentest duration from historical data
    async calculateAveragePentestDuration() {
        try {
            const data = await this.apiRequest('/pentests?page_size=50');
            const pentests = data.pentests || [];

            // Filter completed pentests with valid timestamps
            const completedPentests = pentests.filter(p =>
                p.status === 'COMPLETED' && p.started_at && p.finished_at
            );

            if (completedPentests.length > 0) {
                const totalDuration = completedPentests.reduce((sum, p) => {
                    const start = new Date(p.started_at).getTime();
                    const end = new Date(p.finished_at).getTime();
                    return sum + (end - start);
                }, 0);

                this.averagePentestDuration = totalDuration / completedPentests.length;
                this.log('debug', `Average pentest duration: ${Math.round(this.averagePentestDuration / 60000)} minutes`);
            }
        } catch (error) {
            // Keep default 1 hour
        }
    }

    async loadPentests() {
        this.pentestsList.innerHTML = '<div class="loading-indicator">Loading pentests</div>';

        try {
            const data = await this.apiRequest('/pentests');
            this.pentests = data.pentests || [];
            this.renderPentestsList();

            if (this.pentests.length > 0) {
                this.log('info', `Loaded ${this.pentests.length} pentest(s)`);
            } else {
                this.log('info', 'No pentests found');
            }
        } catch (error) {
            this.pentestsList.innerHTML = '<div class="empty-state">Failed to load pentests</div>';
        }
    }

    renderPentestsList() {
        if (this.pentests.length === 0) {
            this.pentestsList.innerHTML = '<div class="empty-state">No pentests found</div>';
            return;
        }

        this.pentestsList.innerHTML = this.pentests.map(pentest => {
            const target = pentest.targets && pentest.targets.length > 0
                ? pentest.targets[0].target
                : 'Unknown';
            const statusClass = `status-${pentest.status.toLowerCase().replace(' ', '_')}`;
            const isSelected = this.selectedPentest && this.selectedPentest.id === pentest.id;
            const isRunning = pentest.status === 'IN_PROGRESS';

            return `
                <div class="pentest-item ${statusClass} ${isSelected ? 'selected' : ''}"
                     data-id="${pentest.id}">
                    <span class="pentest-status-dot"></span>
                    <div class="pentest-info">
                        <div class="pentest-target">${this.escapeHtml(target)}</div>
                        <div class="pentest-meta">${pentest.status} | ${this.formatDate(pentest.created_at)}</div>
                    </div>
                    ${isRunning ? `
                    <div class="pentest-item-actions">
                        <button class="pentest-action-btn" data-action="watch" title="Watch Progress">&#9654;</button>
                    </div>
                    ` : ''}
                </div>
            `;
        }).join('');

        // Add click handlers for pentest items
        this.pentestsList.querySelectorAll('.pentest-item').forEach(item => {
            item.addEventListener('click', (e) => {
                // Don't handle if clicking an action button
                if (e.target.classList.contains('pentest-action-btn')) return;
                const id = item.dataset.id;
                const pentest = this.pentests.find(p => p.id === id);

                if (pentest && pentest.status === 'COMPLETED') {
                    // For completed pentests, download and open file explorer
                    this.openCompletedPentest(pentest);
                } else if (pentest && pentest.status === 'IN_PROGRESS') {
                    // For running pentests, open in new tab and attach to stream
                    this.openRunningPentest(pentest);
                } else {
                    // For other states (PENDING, FAILED), just select
                    this.selectPentest(id);
                }
            });
        });

        // Add click handlers for watch/attach action button (only for running pentests)
        // Using attach instead of watch allows reconnection if browser was closed
        this.pentestsList.querySelectorAll('.pentest-action-btn[data-action="watch"]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const pentestId = btn.closest('.pentest-item').dataset.id;
                // Use attach endpoint to enable late-join/reconnect capability
                this.startAttachInTab(this.activeTabId, pentestId, true);
            });
        });
    }

    // Open a completed pentest: download evidence and show file explorer
    async openCompletedPentest(pentest) {
        const target = pentest.targets && pentest.targets.length > 0
            ? pentest.targets[0].target
            : 'Unknown';

        // Select the pentest
        this.selectPentest(pentest.id);

        // Create file explorer tab
        const tabId = this.createNewTab(`📁 ${target.substring(0, 12)}`);
        const tabContext = this.tabs.get(tabId);
        tabContext.pentestId = pentest.id;
        tabContext.isFileExplorer = true;

        this.logToTab(tabId, 'system', `Opening pentest results for: ${target}`);
        this.logToTab(tabId, 'info', `Pentest ID: ${pentest.id}`);

        // Check if evidence is already downloaded, if not download it
        this.logToTab(tabId, 'system', 'Checking for evidence files...');

        try {
            // First try to load existing files
            const filesData = await this.apiRequest(`/pentests/${pentest.id}/files`);
            const files = filesData.files || {};

            if (Object.keys(files).length === 0) {
                // No files found, need to download
                this.logToTab(tabId, 'info', 'Evidence not yet downloaded. Downloading and extracting...');
                await this.downloadAndExtractEvidence(tabId, pentest.id);
            } else {
                // Files already exist
                this.logToTab(tabId, 'success', 'Evidence files loaded.');
                this.displayFileExplorer(tabId, files);
            }
        } catch (error) {
            // Error loading files, try to download
            this.logToTab(tabId, 'info', 'Downloading evidence...');
            await this.downloadAndExtractEvidence(tabId, pentest.id);
        }
    }

    // Open a running pentest: attach to stream in a new tab (or switch to existing)
    openRunningPentest(pentest) {
        const target = pentest.targets && pentest.targets.length > 0
            ? pentest.targets[0].target
            : 'Unknown';

        // Select the pentest
        this.selectPentest(pentest.id);

        // Check if there's already a tab attached to this pentest
        let existingTabId = null;
        this.tabs.forEach((tabContext, tabId) => {
            if (tabContext.pentestId === pentest.id && tabContext.eventSource) {
                existingTabId = tabId;
            }
        });

        if (existingTabId) {
            // Switch to existing tab that's already streaming
            this.switchTab(existingTabId);
            this.log('info', `Switched to existing stream for: ${target}`);
        } else {
            // Create new tab and attach to stream
            const tabId = this.createNewTab(`▶ ${target.substring(0, 15)}`);
            const tabContext = this.tabs.get(tabId);
            tabContext.pentestId = pentest.id;

            this.logToTab(tabId, 'system', `Connecting to running pentest: ${target}`);
            this.logToTab(tabId, 'info', `Pentest ID: ${pentest.id}`);

            // Attach to the stream with history replay
            this.startAttachInTab(tabId, pentest.id, true);
        }
    }

    async downloadAndExtractEvidence(tabId, pentestId) {
        try {
            const response = await this.apiRequest(`/pentests/${pentestId}/download-and-extract`, {
                method: 'POST'
            });

            if (response.success) {
                this.logToTab(tabId, 'success', 'Evidence downloaded and extracted successfully.');

                // Load the files
                const filesData = await this.apiRequest(`/pentests/${pentestId}/files`);
                const files = filesData.files || {};
                this.displayFileExplorer(tabId, files);
            } else {
                this.logToTab(tabId, 'error', `Failed to download evidence: ${response.error || 'Unknown error'}`);
            }
        } catch (error) {
            this.logToTab(tabId, 'error', `Failed to download evidence: ${error.message}`);
            this.logToTab(tabId, 'info', 'You can try manually with the "download" command.');
        }
    }

    displayFileExplorer(tabId, files) {
        const tabContext = this.tabs.get(tabId);
        if (tabContext) {
            tabContext.files = files;
            tabContext.currentPath = [];
            tabContext.selectedIndex = 0;
            tabContext.fileExplorerActive = true;
        }

        if (Object.keys(files).length === 0) {
            this.logToTab(tabId, 'info', 'No evidence files available.');
            return;
        }

        // Render the interactive file explorer
        this.renderInteractiveFileExplorer(tabId);
    }

    renderInteractiveFileExplorer(tabId) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext || !tabContext.files) return;

        const consoleElement = this.consoleTabsContent.querySelector(`[data-tab-id="${tabId}"]`);
        if (!consoleElement) return;

        // Get current directory contents
        let currentDir = tabContext.files;
        const pathParts = tabContext.currentPath || [];

        for (const part of pathParts) {
            if (currentDir[part] && currentDir[part].type === 'directory') {
                currentDir = currentDir[part].children || {};
            }
        }

        // Build file list
        const entries = Object.entries(currentDir).sort((a, b) => {
            // Directories first, then files
            const aIsDir = a[1].type === 'directory';
            const bIsDir = b[1].type === 'directory';
            if (aIsDir && !bIsDir) return -1;
            if (!aIsDir && bIsDir) return 1;
            return a[0].localeCompare(b[0]);
        });

        // Clear console and render explorer
        consoleElement.innerHTML = '';

        // Header
        const header = document.createElement('div');
        header.className = 'file-explorer-header';
        const currentPathStr = '/' + pathParts.join('/');
        header.innerHTML = `
            <div class="explorer-title">📁 FILE EXPLORER</div>
            <div class="explorer-path">${this.escapeHtml(currentPathStr)}</div>
            <div class="explorer-help">↑↓ Navigate | Enter Open | Backspace Back | Q Close | V View</div>
        `;
        consoleElement.appendChild(header);

        // File list container
        const fileList = document.createElement('div');
        fileList.className = 'file-explorer-list';
        fileList.id = `file-list-${tabId}`;

        // Add parent directory entry if not at root
        if (pathParts.length > 0) {
            const parentEntry = document.createElement('div');
            parentEntry.className = 'file-explorer-item directory';
            parentEntry.dataset.index = '-1';
            parentEntry.dataset.name = '..';
            parentEntry.dataset.type = 'parent';
            parentEntry.innerHTML = `<span class="file-icon">📁</span><span class="file-name">..</span><span class="file-meta">Parent Directory</span>`;
            if (tabContext.selectedIndex === -1) {
                parentEntry.classList.add('selected');
            }
            fileList.appendChild(parentEntry);
        }

        // Add entries
        entries.forEach(([name, info], index) => {
            const actualIndex = pathParts.length > 0 ? index : index;
            const adjustedIndex = pathParts.length > 0 ? index : index;

            const entry = document.createElement('div');
            const isDir = info.type === 'directory';
            entry.className = `file-explorer-item ${isDir ? 'directory' : 'file'}`;
            entry.dataset.index = adjustedIndex.toString();
            entry.dataset.name = name;
            entry.dataset.type = info.type;

            const icon = isDir ? '📁' : this.getFileIcon(name);
            const size = isDir ? '' : this.formatFileSize(info.size || 0);
            const childCount = isDir && info.children ? Object.keys(info.children).length : 0;
            const meta = isDir ? `${childCount} items` : size;

            entry.innerHTML = `<span class="file-icon">${icon}</span><span class="file-name">${this.escapeHtml(name)}</span><span class="file-meta">${meta}</span>`;

            if (tabContext.selectedIndex === adjustedIndex) {
                entry.classList.add('selected');
            }

            fileList.appendChild(entry);
        });

        // Store entries count for navigation
        tabContext.entriesCount = entries.length;
        tabContext.hasParent = pathParts.length > 0;

        consoleElement.appendChild(fileList);

        // Preview pane
        const preview = document.createElement('div');
        preview.className = 'file-explorer-preview';
        preview.id = `file-preview-${tabId}`;
        preview.innerHTML = '<div class="preview-placeholder">Select a file to preview</div>';
        consoleElement.appendChild(preview);

        // Add click handlers
        fileList.querySelectorAll('.file-explorer-item').forEach(item => {
            item.addEventListener('click', () => {
                const idx = parseInt(item.dataset.index);
                tabContext.selectedIndex = idx;
                this.renderInteractiveFileExplorer(tabId);
            });
            item.addEventListener('dblclick', () => {
                this.fileExplorerOpen(tabId);
            });
        });

        // Update preview for selected item
        this.updateFilePreview(tabId);
    }

    getFileIcon(filename) {
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

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    async updateFilePreview(tabId) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        const preview = document.getElementById(`file-preview-${tabId}`);
        if (!preview) return;

        // Get selected entry
        const selectedIndex = tabContext.selectedIndex;

        if (selectedIndex === -1) {
            // Parent directory selected
            preview.innerHTML = '<div class="preview-placeholder">📁 Parent Directory</div>';
            return;
        }

        let currentDir = tabContext.files;
        for (const part of tabContext.currentPath || []) {
            if (currentDir[part] && currentDir[part].type === 'directory') {
                currentDir = currentDir[part].children || {};
            }
        }

        const entries = Object.entries(currentDir).sort((a, b) => {
            const aIsDir = a[1].type === 'directory';
            const bIsDir = b[1].type === 'directory';
            if (aIsDir && !bIsDir) return -1;
            if (!aIsDir && bIsDir) return 1;
            return a[0].localeCompare(b[0]);
        });

        if (selectedIndex >= entries.length) return;

        const [name, info] = entries[selectedIndex];

        if (info.type === 'directory') {
            const childCount = info.children ? Object.keys(info.children).length : 0;
            preview.innerHTML = `<div class="preview-placeholder">📁 Directory: ${this.escapeHtml(name)}<br>${childCount} items</div>`;
        } else {
            // Try to preview file content
            const fullPath = [...(tabContext.currentPath || []), name].join('/');
            const pentestId = tabContext.pentestId;

            preview.innerHTML = '<div class="preview-loading">Loading preview...</div>';

            try {
                const data = await this.apiRequest(`/files/preview?path=${encodeURIComponent(pentestId + '/' + fullPath)}`);
                const content = data.content || '';
                const truncated = content.length > 2000 ? content.substring(0, 2000) + '\n\n... [truncated]' : content;
                preview.innerHTML = `<pre class="preview-content">${this.escapeHtml(truncated)}</pre>`;
            } catch (error) {
                preview.innerHTML = `<div class="preview-placeholder">Unable to preview: ${this.escapeHtml(name)}</div>`;
            }
        }
    }

    fileExplorerNavigate(tabId, direction) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        const minIndex = tabContext.hasParent ? -1 : 0;
        const maxIndex = tabContext.entriesCount - 1;

        if (direction === 'up') {
            tabContext.selectedIndex = Math.max(minIndex, tabContext.selectedIndex - 1);
        } else if (direction === 'down') {
            tabContext.selectedIndex = Math.min(maxIndex, tabContext.selectedIndex + 1);
        }

        this.renderInteractiveFileExplorer(tabId);
    }

    fileExplorerOpen(tabId) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        const selectedIndex = tabContext.selectedIndex;

        if (selectedIndex === -1) {
            // Go to parent directory
            tabContext.currentPath.pop();
            tabContext.selectedIndex = 0;
            this.renderInteractiveFileExplorer(tabId);
            return;
        }

        let currentDir = tabContext.files;
        for (const part of tabContext.currentPath || []) {
            if (currentDir[part] && currentDir[part].type === 'directory') {
                currentDir = currentDir[part].children || {};
            }
        }

        const entries = Object.entries(currentDir).sort((a, b) => {
            const aIsDir = a[1].type === 'directory';
            const bIsDir = b[1].type === 'directory';
            if (aIsDir && !bIsDir) return -1;
            if (!aIsDir && bIsDir) return 1;
            return a[0].localeCompare(b[0]);
        });

        if (selectedIndex >= entries.length) return;

        const [name, info] = entries[selectedIndex];

        if (info.type === 'directory') {
            // Enter directory
            tabContext.currentPath.push(name);
            tabContext.selectedIndex = 0;
            this.renderInteractiveFileExplorer(tabId);
        } else {
            // Open file in full view
            this.openFileFullView(tabId, name);
        }
    }

    fileExplorerBack(tabId) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext || !tabContext.currentPath || tabContext.currentPath.length === 0) return;

        tabContext.currentPath.pop();
        tabContext.selectedIndex = 0;
        this.renderInteractiveFileExplorer(tabId);
    }

    async openFileFullView(tabId, filename) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        const fullPath = [...(tabContext.currentPath || []), filename].join('/');
        const pentestId = tabContext.pentestId;

        const consoleElement = this.consoleTabsContent.querySelector(`[data-tab-id="${tabId}"]`);
        if (!consoleElement) return;

        // Show loading
        consoleElement.innerHTML = `<div class="file-viewer-header">
            <div class="viewer-title">📄 ${this.escapeHtml(filename)}</div>
            <div class="viewer-path">${this.escapeHtml('/' + fullPath)}</div>
            <div class="viewer-help">Q or Backspace to return to explorer</div>
        </div>
        <div class="file-viewer-content"><div class="preview-loading">Loading file...</div></div>`;

        try {
            const data = await this.apiRequest(`/files/preview?path=${encodeURIComponent(pentestId + '/' + fullPath)}`);
            const content = data.content || '(empty file)';

            consoleElement.innerHTML = `<div class="file-viewer-header">
                <div class="viewer-title">📄 ${this.escapeHtml(filename)}</div>
                <div class="viewer-path">${this.escapeHtml('/' + fullPath)}</div>
                <div class="viewer-help">Q or Backspace to return to explorer | ${this.formatFileSize(data.size || 0)}</div>
            </div>
            <div class="file-viewer-content"><pre class="file-content">${this.escapeHtml(content)}</pre></div>`;

            tabContext.viewingFile = true;
        } catch (error) {
            consoleElement.innerHTML = `<div class="file-viewer-header">
                <div class="viewer-title">📄 ${this.escapeHtml(filename)}</div>
                <div class="viewer-path">${this.escapeHtml('/' + fullPath)}</div>
                <div class="viewer-help">Q or Backspace to return to explorer</div>
            </div>
            <div class="file-viewer-content"><div class="preview-placeholder">Error loading file: ${this.escapeHtml(error.message)}</div></div>`;

            tabContext.viewingFile = true;
        }
    }

    closeFileViewer(tabId) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        tabContext.viewingFile = false;
        this.renderInteractiveFileExplorer(tabId);
    }

    // Handle keyboard navigation for file explorer
    handleFileExplorerKeyboard(tabId, key) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext || !tabContext.fileExplorerActive) return false;

        if (tabContext.viewingFile) {
            // In file view mode
            if (key === 'q' || key === 'Q' || key === 'Backspace' || key === 'Escape') {
                this.closeFileViewer(tabId);
                return true;
            }
            return false;
        }

        // In explorer mode
        switch (key) {
            case 'ArrowUp':
                this.fileExplorerNavigate(tabId, 'up');
                return true;
            case 'ArrowDown':
                this.fileExplorerNavigate(tabId, 'down');
                return true;
            case 'Enter':
                this.fileExplorerOpen(tabId);
                return true;
            case 'Backspace':
                this.fileExplorerBack(tabId);
                return true;
            case 'q':
            case 'Q':
                this.closeFileExplorerTab(tabId);
                return true;
            case 'v':
            case 'V':
                // View file directly
                this.fileExplorerOpen(tabId);
                return true;
            default:
                return false;
        }
    }

    closeFileExplorerTab(tabId) {
        const tabContext = this.tabs.get(tabId);
        if (tabContext) {
            tabContext.fileExplorerActive = false;
        }
        this.closeTab(tabId);
    }

    // Open a file explorer tab for a pentest
    openFileExplorerTab(pentestId, target) {
        const tabId = this.createNewTab(`Files: ${target.substring(0, 12)}`);
        const tabContext = this.tabs.get(tabId);
        tabContext.pentestId = pentestId;
        tabContext.isFileExplorer = true;

        this.logToTab(tabId, 'system', `Loading evidence files for pentest: ${pentestId}`);
        this.loadFilesForTab(tabId, pentestId);
    }

    async loadFilesForTab(tabId, pentestId) {
        try {
            const data = await this.apiRequest(`/pentests/${pentestId}/files`);
            const files = data.files || {};

            if (Object.keys(files).length === 0) {
                this.logToTab(tabId, 'info', 'No evidence files available. Try downloading evidence first.');
                return;
            }

            // Display file tree in console
            this.logToTab(tabId, 'info', 'Available files:');
            this.renderFileTreeToTab(tabId, files, '');
            this.logToTab(tabId, 'system', 'Use "open <path>" to view a file or "download" to download all evidence.');

            // Store files in tab context
            const tabContext = this.tabs.get(tabId);
            if (tabContext) {
                tabContext.files = files;
            }
        } catch (error) {
            this.logToTab(tabId, 'error', `Failed to load files: ${error.message}`);
            this.logToTab(tabId, 'info', 'Try running "download" to fetch evidence first.');
        }
    }

    renderFileTreeToTab(tabId, node, prefix, isLast = true) {
        const entries = Object.entries(node);
        entries.forEach(([name, value], index) => {
            const isLastEntry = index === entries.length - 1;
            const connector = isLastEntry ? '└── ' : '├── ';
            const icon = value.type === 'directory' ? '📁' : '📄';

            this.logToTab(tabId, 'output', `${prefix}${connector}${icon} ${name}`);

            if (value.type === 'directory' && value.children) {
                const newPrefix = prefix + (isLastEntry ? '    ' : '│   ');
                this.renderFileTreeToTab(tabId, value.children, newPrefix);
            }
        });
    }

    selectPentest(id) {
        const pentest = this.pentests.find(p => p.id === id);
        if (!pentest) return;

        this.selectedPentest = pentest;
        this.renderPentestsList();
        this.updatePentestDetails(pentest);
        this.loadEvidenceFiles(id);

        // Start time-based progress tracking
        this.startProgressTracking(pentest);

        // Set chat context for completed pentests
        if (pentest.status === 'COMPLETED') {
            const target = pentest.targets && pentest.targets.length > 0
                ? pentest.targets[0].target
                : 'Unknown';
            this.chatContextPentestId = id;
            this.chatPentestContext.textContent = target;
            this.chatInput.disabled = false;
            this.chatSendBtn.disabled = false;
            this.chatInput.placeholder = `Ask about ${target}...`;
        }

        this.log('info', `Selected pentest: ${id}`);
    }

    updatePentestDetails(pentest) {
        const target = pentest.targets && pentest.targets.length > 0
            ? pentest.targets[0]
            : {};

        this.detailId.textContent = pentest.id.substring(0, 12) + '...';
        this.detailId.title = pentest.id;

        this.detailStatus.textContent = pentest.status;
        this.detailStatus.className = `detail-value status-${pentest.status.toLowerCase().replace(' ', '_')}`;

        this.detailMode.textContent = target.type || '---';
        this.detailStyle.textContent = pentest.style || '---';
        this.detailPhase.textContent = target.phase || '---';

        const severity = pentest.severity || 'NONE';
        this.detailSeverity.textContent = severity;
        this.detailSeverity.className = `detail-value severity-${severity.toLowerCase()}`;

        this.detailFindings.textContent = pentest.findings || '0';
        this.detailCreated.textContent = this.formatDate(pentest.created_at);
        this.detailStarted.textContent = this.formatDate(pentest.started_at) || '---';
        this.detailFinished.textContent = this.formatDate(pentest.finished_at) || '---';

        // Update progress based on time
        this.updateTimeBasedProgress(pentest);
    }

    // Time-based progress tracking
    startProgressTracking(pentest) {
        // Clear existing interval
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }

        // Only track progress for in-progress pentests
        if (pentest.status !== 'IN_PROGRESS') {
            this.updateTimeBasedProgress(pentest);
            return;
        }

        // Update progress every second
        this.progressInterval = setInterval(() => {
            if (this.selectedPentest && this.selectedPentest.id === pentest.id) {
                this.updateTimeBasedProgress(this.selectedPentest);
            }
        }, 1000);
    }

    updateTimeBasedProgress(pentest) {
        let progress = 0;
        const status = pentest.status.toLowerCase();

        if (status === 'completed') {
            progress = 100;
        } else if (status === 'queued' || status === 'pending') {
            progress = 0;
        } else if (status === 'in_progress' && pentest.started_at) {
            // Calculate progress based on elapsed time vs 1 hour baseline
            const ONE_HOUR_MS = 3600000;
            const startTime = new Date(pentest.started_at).getTime();
            const now = Date.now();
            const elapsed = now - startTime;

            // Progress = (elapsed / 1 hour) * 100, capped between 1% and 99%
            progress = Math.min(99, Math.max(1, Math.round((elapsed / ONE_HOUR_MS) * 100)));
        }
        // For failed or other unknown statuses, progress stays at 0

        this.progressFill.style.width = `${progress}%`;
        this.progressText.textContent = `${progress}%`;
    }

    async loadEvidenceFiles(pentestId) {
        try {
            const data = await this.apiRequest(`/pentests/${pentestId}/files`);
            this.evidenceFiles = data.files || {};
            this.renderFileTree();
        } catch (error) {
            this.fileTree.innerHTML = '<div class="empty-state">No evidence available</div>';
        }
    }

    renderFileTree() {
        if (!this.evidenceFiles || Object.keys(this.evidenceFiles).length === 0) {
            this.fileTree.innerHTML = '<div class="empty-state">No evidence downloaded</div>';
            return;
        }

        const renderNode = (name, node, path = '') => {
            const fullPath = path ? `${path}/${name}` : name;

            if (node.type === 'directory') {
                return `
                    <div class="folder-item" data-path="${fullPath}">
                        <span class="folder-toggle">&#9654;</span>
                        <span class="folder-icon">&#128193;</span>
                        <span class="folder-name">${this.escapeHtml(name)}</span>
                    </div>
                    <div class="folder-contents">
                        ${Object.entries(node.children || {}).map(([childName, childNode]) =>
                            renderNode(childName, childNode, fullPath)
                        ).join('')}
                    </div>
                `;
            } else {
                return `
                    <div class="file-item" data-path="${fullPath}">
                        <span class="file-icon">&#128196;</span>
                        <span class="file-name">${this.escapeHtml(name)}</span>
                    </div>
                `;
            }
        };

        this.fileTree.innerHTML = Object.entries(this.evidenceFiles).map(([name, node]) =>
            renderNode(name, node)
        ).join('');

        // Add click handlers
        this.fileTree.querySelectorAll('.file-item').forEach(item => {
            item.addEventListener('click', () => {
                this.fileTree.querySelectorAll('.file-item').forEach(i => i.classList.remove('selected'));
                item.classList.add('selected');
                this.previewFile(item.dataset.path);
            });
        });

        this.fileTree.querySelectorAll('.folder-item').forEach(item => {
            item.addEventListener('click', () => {
                const contents = item.nextElementSibling;
                if (contents && contents.classList.contains('folder-contents')) {
                    contents.style.display = contents.style.display === 'none' ? 'block' : 'none';
                    item.querySelector('.folder-toggle').innerHTML =
                        contents.style.display === 'none' ? '&#9654;' : '&#9660;';
                }
            });
        });
    }

    async previewFile(path) {
        this.resultPreview.innerHTML = '<div class="loading-indicator">Loading preview</div>';

        try {
            const data = await this.apiRequest(`/files/preview?path=${encodeURIComponent(path)}`);
            this.resultPreview.innerHTML = `<pre class="preview-content">${this.escapeHtml(data.content)}</pre>`;
            this.log('info', `Previewing: ${path}`);
        } catch (error) {
            this.resultPreview.innerHTML = '<div class="preview-placeholder">Unable to preview file</div>';
        }
    }

    // Console Methods
    handleConsoleInput(e) {
        const dropdownVisible = this.autocompleteDropdown.classList.contains('active');
        const items = this.autocompleteDropdown.querySelectorAll('.autocomplete-item');
        const tabContext = this.tabs.get(this.activeTabId);

        if (e.key === 'Enter') {
            e.preventDefault();
            // If dropdown is open and item is selected, use that
            if (dropdownVisible && this.autocompleteSelectedIndex >= 0 && items[this.autocompleteSelectedIndex]) {
                const selectedCmd = items[this.autocompleteSelectedIndex].dataset.cmd;
                this.consoleInput.value = selectedCmd + ' ';
                this.hideAutocompleteDropdown();
                this.clearInlineSuggestion();
                return;
            }

            const command = this.consoleInput.value.trim();
            if (command) {
                // Use tab's own command history
                if (tabContext) {
                    tabContext.commandHistory.unshift(command);
                    tabContext.historyIndex = -1;
                }
                this.executeCommand(command);
                this.consoleInput.value = '';
                this.hideAutocompleteDropdown();
                this.clearInlineSuggestion();
            }
        } else if (e.key === 'ArrowUp') {
            if (dropdownVisible && items.length > 0) {
                e.preventDefault();
                this.autocompleteSelectedIndex = Math.max(0, this.autocompleteSelectedIndex - 1);
                this.updateDropdownSelection(items);
            } else if (tabContext) {
                e.preventDefault();
                if (tabContext.historyIndex < tabContext.commandHistory.length - 1) {
                    tabContext.historyIndex++;
                    this.consoleInput.value = tabContext.commandHistory[tabContext.historyIndex];
                    this.clearInlineSuggestion();
                }
            }
        } else if (e.key === 'ArrowDown') {
            if (dropdownVisible && items.length > 0) {
                e.preventDefault();
                this.autocompleteSelectedIndex = Math.min(items.length - 1, this.autocompleteSelectedIndex + 1);
                this.updateDropdownSelection(items);
            } else if (tabContext) {
                e.preventDefault();
                if (tabContext.historyIndex > 0) {
                    tabContext.historyIndex--;
                    this.consoleInput.value = tabContext.commandHistory[tabContext.historyIndex];
                    this.clearInlineSuggestion();
                } else {
                    tabContext.historyIndex = -1;
                    this.consoleInput.value = '';
                    this.clearInlineSuggestion();
                }
            }
        } else if (e.key === 'Tab') {
            e.preventDefault();
            // Accept inline suggestion
            if (this.autocompleteSuggestion.textContent) {
                this.consoleInput.value = this.autocompleteSuggestion.textContent;
                this.clearInlineSuggestion();
                this.hideAutocompleteDropdown();
            } else if (dropdownVisible && this.autocompleteSelectedIndex >= 0 && items[this.autocompleteSelectedIndex]) {
                const selectedCmd = items[this.autocompleteSelectedIndex].dataset.cmd;
                this.consoleInput.value = selectedCmd + ' ';
                this.hideAutocompleteDropdown();
            }
        } else if (e.key === 'Escape') {
            this.hideAutocompleteDropdown();
            this.clearInlineSuggestion();
        }
    }

    handleAutocompleteInput(e) {
        const input = this.consoleInput.value.toLowerCase();
        const parts = input.split(/\s+/);
        const cmdPart = parts[0];

        // Only autocomplete if typing the command (first word)
        if (parts.length === 1 && cmdPart) {
            const matches = this.commandDefinitions.filter(c => c.name.startsWith(cmdPart));

            if (matches.length > 0) {
                // Show inline suggestion for first match
                this.autocompleteSuggestion.textContent = matches[0].name;

                // Show dropdown with all matches
                this.showAutocompleteDropdown(matches);
            } else {
                this.clearInlineSuggestion();
                this.hideAutocompleteDropdown();
            }
        } else {
            this.clearInlineSuggestion();
            this.hideAutocompleteDropdown();
        }
    }

    showAutocompleteDropdown(matches) {
        if (matches.length === 0) {
            this.hideAutocompleteDropdown();
            return;
        }

        this.autocompleteDropdown.innerHTML = matches.map((cmd, idx) => `
            <div class="autocomplete-item ${idx === this.autocompleteSelectedIndex ? 'selected' : ''}"
                 data-cmd="${cmd.name}" data-idx="${idx}">
                <span class="cmd-name">${this.escapeHtml(cmd.usage || cmd.name)}</span>
                <span class="cmd-desc">${this.escapeHtml(cmd.desc)}</span>
            </div>
        `).join('');

        // Add click handlers
        this.autocompleteDropdown.querySelectorAll('.autocomplete-item').forEach(item => {
            item.addEventListener('mousedown', (e) => {
                e.preventDefault();
                this.consoleInput.value = item.dataset.cmd + ' ';
                this.hideAutocompleteDropdown();
                this.clearInlineSuggestion();
                this.consoleInput.focus();
            });
        });

        this.autocompleteDropdown.classList.add('active');
        this.autocompleteSelectedIndex = 0;
        this.updateDropdownSelection(this.autocompleteDropdown.querySelectorAll('.autocomplete-item'));
    }

    hideAutocompleteDropdown() {
        this.autocompleteDropdown.classList.remove('active');
        this.autocompleteSelectedIndex = -1;
    }

    updateDropdownSelection(items) {
        items.forEach((item, idx) => {
            item.classList.toggle('selected', idx === this.autocompleteSelectedIndex);
        });
    }

    clearInlineSuggestion() {
        this.autocompleteSuggestion.textContent = '';
    }

    executeCommand(command) {
        this.log('command', command);

        const parts = command.split(/\s+/);
        const cmd = parts[0].toLowerCase();
        const args = parts.slice(1);

        switch (cmd) {
            case 'help':
                this.showHelp();
                break;
            case 'clear':
            case 'cls':
                this.clearConsole();
                break;
            case 'list':
            case 'ls':
                this.listPentests();
                break;
            case 'run':
            case 'schedule':
                this.scheduleFromCommand(args);
                break;
            case 'runtab':
            case 'run-tab':
                this.runInNewTab(args);
                break;
            case 'get':
                this.getPentest(args[0]);
                break;
            case 'watch':
                this.watchFromCommand(args[0]);
                break;
            case 'stop':
                this.stopWatch();
                break;
            case 'download':
                this.downloadFromCommand(args[0]);
                break;
            case 'status':
                this.showStatus();
                break;
            case 'version':
                this.log('info', `Version: ${this.versionInfo.textContent}`);
                break;
            case 'refresh':
                this.loadPentests();
                break;
            case 'servers':
                this.listServers();
                break;
            case 'init':
                this.openAddServerModal();
                break;
            case 'newtab':
            case 'tab':
                this.createNewTab();
                break;
            case 'closetab':
                this.closeTab(this.activeTabId);
                break;
            case 'tabs':
                this.listTabs();
                break;
            case 'open':
                this.openFileFromCommand(args);
                break;
            case 'files':
                this.listFilesInTab();
                break;
            case 'chat':
                this.setChatContextFromCommand(args[0]);
                break;
            case 'attach':
                this.attachFromCommand(args[0]);
                break;
            case 'attachtab':
            case 'attach-tab':
                this.attachInNewTab(args[0]);
                break;
            // Playbook commands
            case 'playbook':
            case 'plan':
                this.handlePlaybookCommand(args);
                break;
            case 'playbooks':
                this.listPlaybooks();
                break;
            // Memory commands
            case 'memory':
                this.handleMemoryCommand(args);
                break;
            case 'memories':
                this.listMemoryItems();
                break;
            // Task commands
            case 'task':
                this.handleTaskCommand(args);
                break;
            case 'tasks':
                this.listCustomTasks();
                break;
            default:
                this.log('error', `Unknown command: ${cmd}. Type 'help' for available commands.`);
        }
    }

    showHelp() {
        const helpText = `
Available commands:
  help              - Show this help message
  clear, cls        - Clear console output
  list, ls          - List all pentests
  run <target>      - Schedule new pentest for target
  runtab <target>   - Schedule pentest in a new tab
  get <id>          - Get pentest details
  watch [id]        - Watch pentest progress (uses selected if no id)
  attach [id]       - Attach to running pentest (reconnect to stream)
  attachtab [id]    - Attach to pentest in a new tab
  stop              - Stop watching pentest
  download [id]     - Download evidence (uses selected if no id)
  status            - Show connection status
  version           - Show version information
  refresh           - Refresh pentests list
  servers           - List configured servers
  init              - Add a new server connection

Playbook commands:
  playbooks         - List all saved playbooks
  playbook list     - List all saved playbooks
  playbook show <n> - Show playbook content
  playbook delete   - Delete a playbook

Memory commands:
  memories          - List all memory items
  memory list       - List all memory items
  memory show <n>   - Show memory item content
  memory delete <n> - Delete a memory item

Task commands:
  tasks             - List custom tasks
  task <desc> -t <target> - Run a custom task

Tab commands:
  newtab, tab       - Create a new console tab
  closetab          - Close current tab
  tabs              - List all open tabs
  files             - List files in current tab (file explorer)
  open <path>       - Open file content (in file explorer tab)

Chat commands:
  chat [id]         - Set chat context for a completed pentest

Quick keys:
  Up/Down arrows    - Navigate command history
  Tab               - Autocomplete command
  Escape            - Close modal

Pentest list interactions:
  Click running     - Opens new tab and attaches to stream
  Click completed   - Opens file explorer with evidence
  ▶ on running      - Attach to pentest stream (reconnectable)
`;
        this.log('output', helpText);
    }

    showStatus() {
        const connected = this.globeIcon.classList.contains('connected');
        this.log('info', `Connection: ${connected ? 'Connected' : 'Disconnected'}`);
        this.log('info', `Server: ${this.serverAddress.textContent}`);
        this.log('info', `Country: ${this.serverCountry.textContent}`);
        this.log('info', `Pentests loaded: ${this.pentests.length}`);
        this.log('info', `Average pentest duration: ${Math.round(this.averagePentestDuration / 60000)} minutes`);
        if (this.selectedPentest) {
            this.log('info', `Selected: ${this.selectedPentest.id}`);
        }
        if (this.chatContextPentestId) {
            this.log('info', `Chat context: ${this.chatPentestContext.textContent}`);
        }
    }

    listServers() {
        if (this.servers.length === 0) {
            this.log('info', 'No servers configured. Use "init" to add one.');
            return;
        }

        this.log('output', '\nConfigured Servers:');
        this.servers.forEach(s => {
            const active = this.activeServer && this.activeServer.id === s.id ? ' [ACTIVE]' : '';
            this.log('output', `  ${s.name} - ${s.host}:${s.port}${active}`);
        });
    }

    listTabs() {
        this.log('output', '\nOpen Tabs:');
        this.tabs.forEach((tabContext, tabId) => {
            const active = tabId === this.activeTabId ? ' [ACTIVE]' : '';
            const status = tabContext.status ? ` (${tabContext.status})` : '';
            const streaming = tabContext.eventSource ? ' [STREAMING]' : '';
            const pentestInfo = tabContext.pentestId ? ` - Pentest: ${tabContext.pentestId.substring(0, 8)}...` : '';
            this.log('output', `  ${tabContext.title || tabId}${pentestInfo}${status}${streaming}${active}`);
        });
    }

    async openFileFromCommand(args) {
        if (args.length === 0) {
            this.log('error', 'Path required. Usage: open <path>');
            return;
        }

        const path = args.join(' ');
        const tabContext = this.tabs.get(this.activeTabId);

        if (!tabContext || !tabContext.pentestId) {
            this.log('error', 'No pentest context in current tab. Use "explore" action on a pentest first.');
            return;
        }

        this.log('info', `Opening file: ${path}`);

        try {
            const data = await this.apiRequest(`/files/preview?path=${encodeURIComponent(path)}&pentest_id=${tabContext.pentestId}`);
            this.log('output', '\n--- File Content ---');
            this.log('output', data.content || '(empty file)');
            this.log('output', '--- End of File ---\n');
        } catch (error) {
            this.log('error', `Failed to open file: ${error.message}`);
        }
    }

    listFilesInTab() {
        const tabContext = this.tabs.get(this.activeTabId);

        if (!tabContext || !tabContext.pentestId) {
            this.log('error', 'No pentest context in current tab.');
            return;
        }

        if (!tabContext.files || Object.keys(tabContext.files).length === 0) {
            this.log('info', 'No files loaded. Loading...');
            this.loadFilesForTab(this.activeTabId, tabContext.pentestId);
            return;
        }

        this.log('info', 'Available files:');
        this.renderFileTreeToTab(this.activeTabId, tabContext.files, '');
    }

    // ==========================================
    // Playbook Command Handlers
    // ==========================================

    async handlePlaybookCommand(args) {
        const subCmd = args[0]?.toLowerCase();
        const name = args.slice(1).join(' ');

        switch (subCmd) {
            case 'list':
            case undefined:
                await this.listPlaybooks();
                break;
            case 'show':
                if (!name) {
                    this.log('error', 'Playbook name required. Usage: playbook show <name>');
                    return;
                }
                await this.showPlaybook(name);
                break;
            case 'delete':
                if (!name) {
                    this.log('error', 'Playbook name required. Usage: playbook delete <name>');
                    return;
                }
                await this.deletePlaybook(name);
                break;
            default:
                this.log('error', `Unknown playbook command: ${subCmd}. Use: list, show <name>, delete <name>`);
        }
    }

    async listPlaybooks() {
        this.log('info', 'Loading playbooks...');
        try {
            const data = await this.apiRequest('/playbooks');
            if (!data.success) {
                this.log('error', data.error || 'Failed to load playbooks');
                return;
            }

            if (!data.playbooks || data.playbooks.length === 0) {
                this.log('info', 'No playbooks found.');
                this.log('info', `Playbooks folder: ${data.path || 'playbooks/'}`);
                return;
            }

            this.log('output', '\nSaved Playbooks:');
            this.log('output', '─'.repeat(50));
            data.playbooks.forEach(p => {
                const size = p.size < 1024 ? `${p.size} B` : `${Math.round(p.size / 1024)} KB`;
                this.log('output', `  ${p.name.padEnd(25)} ${size.padStart(10)}`);
            });
            this.log('output', '');
            this.log('info', `Total: ${data.playbooks.length} playbook(s)`);
            this.log('info', `Path: ${data.path}`);
        } catch (error) {
            this.log('error', `Failed to list playbooks: ${error.message}`);
        }
    }

    async showPlaybook(name) {
        try {
            const data = await this.apiRequest(`/playbooks/${encodeURIComponent(name)}`);
            if (!data.success) {
                this.log('error', data.error || 'Failed to load playbook');
                return;
            }

            const playbook = data.playbook;
            this.log('output', '\n' + '═'.repeat(50));
            this.log('output', `Playbook: ${playbook.name}`);
            this.log('output', '═'.repeat(50));
            this.log('output', `File: ${playbook.file_path}`);
            this.log('output', '─'.repeat(50));
            this.log('output', playbook.content);
            this.log('output', '─'.repeat(50));
        } catch (error) {
            this.log('error', `Failed to show playbook: ${error.message}`);
        }
    }

    async deletePlaybook(name) {
        try {
            const data = await this.apiRequest(`/playbooks/${encodeURIComponent(name)}`, {
                method: 'DELETE'
            });
            if (data.success) {
                this.log('success', `Playbook deleted: ${name}`);
            } else {
                this.log('error', data.error || 'Failed to delete playbook');
            }
        } catch (error) {
            this.log('error', `Failed to delete playbook: ${error.message}`);
        }
    }

    // ==========================================
    // Memory Command Handlers
    // ==========================================

    async handleMemoryCommand(args) {
        const subCmd = args[0]?.toLowerCase();
        const name = args.slice(1).join(' ');

        switch (subCmd) {
            case 'list':
            case undefined:
                await this.listMemoryItems();
                break;
            case 'show':
                if (!name) {
                    this.log('error', 'Memory name required. Usage: memory show <name>');
                    return;
                }
                await this.showMemoryItem(name);
                break;
            case 'delete':
                if (!name) {
                    this.log('error', 'Memory name required. Usage: memory delete <name>');
                    return;
                }
                await this.deleteMemoryItem(name);
                break;
            default:
                this.log('error', `Unknown memory command: ${subCmd}. Use: list, show <name>, delete <name>`);
        }
    }

    async listMemoryItems() {
        this.log('info', 'Loading memory items...');
        try {
            const data = await this.apiRequest('/memory');
            if (!data.success) {
                this.log('error', data.error || 'Failed to load memory items');
                return;
            }

            if (!data.items || data.items.length === 0) {
                this.log('info', 'No memory items found.');
                this.log('info', `Memory folder: ${data.path || 'memory/'}`);
                return;
            }

            this.log('output', '\nSaved Memory Items:');
            this.log('output', '─'.repeat(50));
            data.items.forEach(item => {
                const size = item.size < 1024 ? `${item.size} B` : `${Math.round(item.size / 1024)} KB`;
                const type = item.is_default ? '[DEFAULT]' : '';
                this.log('output', `  ${item.name.padEnd(20)} ${size.padStart(10)} ${type}`);
            });
            this.log('output', '');
            this.log('info', `Total: ${data.items.length} item(s)`);
            this.log('info', `Path: ${data.path}`);
        } catch (error) {
            this.log('error', `Failed to list memory items: ${error.message}`);
        }
    }

    async showMemoryItem(name) {
        try {
            const data = await this.apiRequest(`/memory/${encodeURIComponent(name)}`);
            if (!data.success) {
                this.log('error', data.error || 'Failed to load memory item');
                return;
            }

            const item = data.item;
            this.log('output', '\n' + '═'.repeat(50));
            this.log('output', `Memory: ${item.name}${item.name === 'default' ? ' (DEFAULT - auto-included)' : ''}`);
            this.log('output', '═'.repeat(50));
            this.log('output', `File: ${item.file_path}`);
            this.log('output', '─'.repeat(50));
            this.log('output', item.content);
            this.log('output', '─'.repeat(50));
        } catch (error) {
            this.log('error', `Failed to show memory item: ${error.message}`);
        }
    }

    async deleteMemoryItem(name) {
        try {
            const data = await this.apiRequest(`/memory/${encodeURIComponent(name)}`, {
                method: 'DELETE'
            });
            if (data.success) {
                this.log('success', `Memory item deleted: ${name}`);
            } else {
                this.log('error', data.error || 'Failed to delete memory item');
            }
        } catch (error) {
            this.log('error', `Failed to delete memory item: ${error.message}`);
        }
    }

    // ==========================================
    // Custom Task Command Handlers
    // ==========================================

    async handleTaskCommand(args) {
        if (args.length === 0) {
            this.log('error', 'Task description required. Usage: task <description> -t <target>');
            return;
        }

        // Parse args to find -t flag for target
        const targetIdx = args.findIndex(a => a === '-t' || a === '--target');
        let description, target;

        if (targetIdx !== -1) {
            description = args.slice(0, targetIdx).join(' ');
            target = args.slice(targetIdx + 1).join(' ');
        } else {
            this.log('error', 'Target required. Usage: task <description> -t <target>');
            return;
        }

        if (!description || !target) {
            this.log('error', 'Both description and target required. Usage: task <description> -t <target>');
            return;
        }

        this.log('info', `Submitting task: "${description}" for target: ${target}`);
        this.log('info', 'Task submission via web UI is planned for future release.');
        this.log('info', 'Use CLI: twpt task "<description>" -t <target> --watch');
    }

    async listCustomTasks() {
        this.log('info', 'Loading custom tasks...');
        try {
            const data = await this.apiRequest('/tasks');
            if (data.error) {
                this.log('error', data.error);
                return;
            }

            const tasks = data.tasks || [];
            if (tasks.length === 0) {
                this.log('info', 'No custom tasks found.');
                return;
            }

            this.log('output', '\nCustom Tasks:');
            this.log('output', '─'.repeat(80));
            tasks.forEach(task => {
                const status = task.status || 'PENDING';
                const target = (task.target || '-').substring(0, 20);
                const desc = (task.description || '-').substring(0, 30);
                const id = (task.id || 'N/A').substring(0, 20);
                this.log('output', `  ${id.padEnd(22)} ${status.padEnd(12)} ${target.padEnd(22)} ${desc}`);
            });
            this.log('output', '');
            this.log('info', `Total: ${data.total || tasks.length} task(s)`);
        } catch (error) {
            this.log('error', `Failed to list tasks: ${error.message}`);
        }
    }

    setChatContextFromCommand(id) {
        if (!id) {
            if (this.selectedPentest) {
                id = this.selectedPentest.id;
            } else {
                this.log('error', 'No pentest ID provided and none selected');
                return;
            }
        }

        const pentest = this.pentests.find(p => p.id === id);
        if (!pentest) {
            this.log('error', `Pentest not found: ${id}`);
            return;
        }

        if (pentest.status !== 'COMPLETED') {
            this.log('error', 'Chat is only available for completed pentests');
            return;
        }

        const target = pentest.targets && pentest.targets.length > 0
            ? pentest.targets[0].target
            : 'Unknown';

        this.setChatContext(id, target);
        this.log('success', `Chat context set to: ${target}`);
    }

    runInNewTab(args) {
        if (args.length === 0) {
            this.log('error', 'Target required. Usage: runtab <target>');
            return;
        }

        const target = args[0];
        this.startPentestInNewTab(target);
    }

    listPentests() {
        if (this.pentests.length === 0) {
            this.log('info', 'No pentests found');
            return;
        }

        this.log('output', '\nPentests:');
        this.pentests.forEach(p => {
            const target = p.targets && p.targets.length > 0 ? p.targets[0].target : 'Unknown';
            this.log('output', `  ${p.id.substring(0, 8)}... | ${target} | ${p.status}`);
        });
    }

    async scheduleFromCommand(args) {
        if (args.length === 0) {
            this.openNewPentestModal();
            return;
        }

        const target = args[0];
        // Use streaming for the run command - same as runtab but in main tab
        this.log('info', `Scheduling pentest for: ${target} with real-time streaming...`);

        const request = {
            targets: [{
                target: target,
                scope: 'TARGETED',
                type: 'BLACK_BOX'
            }],
            style: 'AGGRESSIVE',
            exploit: true
        };

        // Start streaming in the current (main) tab
        this.startStreamInTab('main', request);
    }

    async getPentest(id) {
        if (!id) {
            if (this.selectedPentest) {
                id = this.selectedPentest.id;
            } else {
                this.log('error', 'No pentest ID provided and none selected');
                return;
            }
        }

        try {
            const data = await this.apiRequest(`/pentests/${id}`);
            this.log('output', JSON.stringify(data, null, 2));
        } catch (error) {
            this.log('error', `Failed to get pentest: ${error.message}`);
        }
    }

    watchFromCommand(id) {
        if (!id && this.selectedPentest) {
            id = this.selectedPentest.id;
        }

        if (!id) {
            this.log('error', 'No pentest ID provided and none selected');
            return;
        }

        // Start watching in current tab using SSE
        this.startWatchInTab(this.activeTabId, id);
    }

    downloadFromCommand(id) {
        if (!id && this.selectedPentest) {
            id = this.selectedPentest.id;
        }

        if (!id) {
            this.log('error', 'No pentest ID provided and none selected');
            return;
        }

        this.downloadEvidence(id);
    }

    // Attach to a running pentest stream (late-join with history replay)
    attachFromCommand(id) {
        if (!id && this.selectedPentest) {
            id = this.selectedPentest.id;
        }

        if (!id) {
            this.log('error', 'No pentest ID provided and none selected');
            return;
        }

        // Start attach in current tab
        this.startAttachInTab(this.activeTabId, id);
    }

    // Attach to a pentest in a new dedicated tab
    attachInNewTab(id) {
        if (!id && this.selectedPentest) {
            id = this.selectedPentest.id;
        }

        if (!id) {
            this.log('error', 'No pentest ID provided and none selected');
            return;
        }

        // Find the target name for the tab title
        const pentest = this.pentests.find(p => p.id === id);
        let tabTitle = id.substring(0, 8);
        if (pentest && pentest.targets && pentest.targets.length > 0) {
            tabTitle = pentest.targets[0].target;
        }

        // Create new tab and start attach
        const tabId = this.createNewTab(`📡 ${tabTitle}`);
        this.startAttachInTab(tabId, id);
    }

    // Start attach streaming to a tab using the /attach endpoint
    startAttachInTab(tabId, pentestId, includeHistory = true) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        // Close any existing stream
        tabContext.closeEventSource();

        this.logToTab(tabId, 'info', `Attaching to pentest: ${pentestId}`);
        this.logToTab(tabId, 'system', 'Connecting to stream (with history replay)...');

        tabContext.pentestId = pentestId;

        // Use EventSource for GET-based SSE with attach endpoint
        const historyParam = includeHistory ? 'true' : 'false';
        const eventSource = new EventSource(`${this.apiBase}/pentests/${pentestId}/attach?include_history=${historyParam}`);
        tabContext.eventSource = eventSource;

        eventSource.addEventListener('subscribed', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.logToTab(tabId, 'success', `Attached to pentest stream`);
                if (data.is_running) {
                    this.logToTab(tabId, 'info', 'Pentest is currently running');
                } else {
                    this.logToTab(tabId, 'info', 'Pentest has completed');
                }
                if (data.message) {
                    this.logToTab(tabId, 'info', data.message);
                }
            } catch (err) {}
        });

        eventSource.addEventListener('message', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.handleStreamEvent(tabId, data);
            } catch (err) {}
        });

        eventSource.addEventListener('status', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.handleStreamEvent(tabId, data);
            } catch (err) {}
        });

        eventSource.addEventListener('done', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.logToTab(tabId, 'success', data.message || 'Stream completed');
                eventSource.close();
                tabContext.eventSource = null;
            } catch (err) {}
        });

        eventSource.addEventListener('error', (e) => {
            if (eventSource.readyState === EventSource.CLOSED) {
                this.logToTab(tabId, 'info', 'Stream closed');
            } else {
                this.logToTab(tabId, 'error', 'Stream connection error - will retry...');
            }
            tabContext.eventSource = null;
        });
    }

    log(type, message) {
        // Log to currently active tab
        this.logToTab(this.activeTabId, type, message);
    }

    getActiveConsoleOutput() {
        return this.consoleTabsContent.querySelector(`[data-tab-id="${this.activeTabId}"]`);
    }

    clearConsole() {
        const activeConsole = this.getActiveConsoleOutput();
        if (activeConsole) {
            activeConsole.innerHTML = '';
        }
        this.log('system', 'Console cleared');
    }

    toggleAutoscroll() {
        this.autoScroll = !this.autoScroll;
        this.toggleAutoscrollBtn.classList.toggle('active', this.autoScroll);
        this.log('info', `Auto-scroll ${this.autoScroll ? 'enabled' : 'disabled'}`);
    }

    // Watch functionality with live output using SSE streaming
    watchPentest() {
        if (!this.selectedPentest) {
            this.log('error', 'No pentest selected');
            return;
        }

        // Use streaming instead of polling
        this.startWatchInTab(this.activeTabId, this.selectedPentest.id);
    }

    startWatch(pentestId) {
        if (this.watchInterval) {
            this.stopWatch();
        }

        this.log('info', `Watching pentest: ${pentestId}`);
        this.footerStatus.textContent = 'Watching...';

        let lastPhase = null;
        let lastFindings = 0;

        const poll = async () => {
            try {
                const data = await this.apiRequest(`/pentests/${pentestId}`);
                const target = data.targets && data.targets.length > 0 ? data.targets[0] : {};

                // Log phase changes
                if (target.phase && target.phase !== lastPhase) {
                    this.log('info', `Phase: ${target.phase}`);
                    lastPhase = target.phase;
                }

                // Log new findings
                if (data.findings > lastFindings) {
                    const newFindings = data.findings - lastFindings;
                    this.log('warning', `New findings detected: +${newFindings} (Total: ${data.findings})`);
                    lastFindings = data.findings;
                }

                // Log status
                this.log('debug', `Status: ${data.status} | Severity: ${data.severity || 'NONE'}`);

                // Update UI
                if (this.selectedPentest && this.selectedPentest.id === data.id) {
                    this.selectedPentest = data;
                    this.updatePentestDetails(data);
                }

                // Update pentest in list
                const idx = this.pentests.findIndex(p => p.id === data.id);
                if (idx >= 0) {
                    this.pentests[idx] = data;
                    this.renderPentestsList();
                }

                if (data.status === 'COMPLETED') {
                    this.stopWatch();
                    this.log('success', 'Pentest completed successfully!');
                    this.log('info', `Final severity: ${data.severity || 'NONE'} | Findings: ${data.findings || 0}`);
                } else if (data.status === 'FAILED') {
                    this.stopWatch();
                    this.log('error', 'Pentest failed');
                }
            } catch (error) {
                this.log('error', `Watch error: ${error.message}`);
            }
        };

        poll();
        this.watchInterval = setInterval(poll, 5000);
    }

    stopWatch() {
        if (this.watchInterval) {
            clearInterval(this.watchInterval);
            this.watchInterval = null;
            this.footerStatus.textContent = 'Ready';
        }

        // Stop streaming for current tab
        const tabContext = this.tabs.get(this.activeTabId);
        if (tabContext) {
            tabContext.closeEventSource();
            this.log('info', 'Streaming stopped');
        }
    }

    // Tab Management Methods
    createNewTab(title = null, pentestId = null) {
        this.tabCounter++;
        const tabId = `tab-${this.tabCounter}`;
        const tabTitle = title || `TAB ${this.tabCounter}`;

        // Create tab element
        const tabElement = document.createElement('div');
        tabElement.className = 'tab';
        tabElement.dataset.tabId = tabId;
        tabElement.innerHTML = `
            <span class="tab-status"></span>
            <span class="tab-title">${this.escapeHtml(tabTitle)}</span>
            <button class="tab-close" title="Close tab">&times;</button>
        `;

        // Add click handlers
        tabElement.addEventListener('click', (e) => {
            if (!e.target.classList.contains('tab-close')) {
                this.switchTab(tabId);
            }
        });

        tabElement.querySelector('.tab-close').addEventListener('click', (e) => {
            e.stopPropagation();
            this.closeTab(tabId);
        });

        this.consoleTabs.appendChild(tabElement);

        // Create console output for this tab
        const consoleElement = document.createElement('div');
        consoleElement.className = 'console-output';
        consoleElement.id = `console-output-${tabId}`;
        consoleElement.dataset.tabId = tabId;
        this.consoleTabsContent.appendChild(consoleElement);

        // Create TabContext for this tab
        const tabContext = new TabContext(tabId, tabTitle, this);
        tabContext.pentestId = pentestId;
        this.tabs.set(tabId, tabContext);

        // Switch to new tab
        this.switchTab(tabId);

        // Log welcome message to new tab
        this.logToTab(tabId, 'system', 'New console tab created.');
        this.logToTab(tabId, 'system', 'Type "help" for available commands.');

        return tabId;
    }

    switchTab(tabId) {
        if (!this.tabs.has(tabId)) return;

        // Update active states for tabs
        this.consoleTabs.querySelectorAll('.tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tabId === tabId);
        });

        // Update active states for console outputs
        this.consoleTabsContent.querySelectorAll('.console-output').forEach(output => {
            output.classList.toggle('active', output.dataset.tabId === tabId);
        });

        this.activeTabId = tabId;

        // Update progress bar for this tab's pentest
        const tabData = this.tabs.get(tabId);
        if (tabData && tabData.pentestId) {
            const pentest = this.pentests.find(p => p.id === tabData.pentestId);
            if (pentest) {
                this.updateTimeBasedProgress(pentest);
            }
        }
    }

    closeTab(tabId) {
        // Cannot close main tab
        if (tabId === 'main') {
            this.logToTab('main', 'info', 'Cannot close main tab');
            return;
        }

        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        // Close any SSE connection
        tabContext.closeEventSource();

        // Remove tab element
        const tabElement = this.consoleTabs.querySelector(`[data-tab-id="${tabId}"]`);
        if (tabElement) {
            tabElement.remove();
        }

        // Remove console output
        const consoleElement = this.consoleTabsContent.querySelector(`[data-tab-id="${tabId}"]`);
        if (consoleElement) {
            consoleElement.remove();
        }

        // Remove from tabs map
        this.tabs.delete(tabId);

        // Switch to main tab if this was active
        if (this.activeTabId === tabId) {
            this.switchTab('main');
        }
    }

    updateTabStatus(tabId, status) {
        const tabElement = this.consoleTabs.querySelector(`[data-tab-id="${tabId}"]`);
        if (!tabElement) return;

        const statusDot = tabElement.querySelector('.tab-status');
        if (!statusDot) return;

        // Remove all status classes
        statusDot.classList.remove('running', 'completed', 'failed');

        // Add appropriate class
        if (status === 'IN_PROGRESS') {
            statusDot.classList.add('running');
        } else if (status === 'COMPLETED') {
            statusDot.classList.add('completed');
        } else if (status === 'FAILED') {
            statusDot.classList.add('failed');
        }

        // Update tab data
        const tabData = this.tabs.get(tabId);
        if (tabData) {
            tabData.status = status;
        }
    }

    updateTabTitle(tabId, title) {
        const tabElement = this.consoleTabs.querySelector(`[data-tab-id="${tabId}"]`);
        if (!tabElement) return;

        const titleElement = tabElement.querySelector('.tab-title');
        if (titleElement) {
            titleElement.textContent = title;
        }

        const tabContext = this.tabs.get(tabId);
        if (tabContext) {
            tabContext.title = title;
        }
    }

    logToTab(tabId, type, message) {
        const consoleElement = this.consoleTabsContent.querySelector(`[data-tab-id="${tabId}"]`);
        if (!consoleElement) return;

        const line = document.createElement('div');
        line.className = `console-line ${type}`;

        if (type !== 'command') {
            const timestamp = new Date().toLocaleTimeString('en-GB');
            // Format the message for console display (handle multiline, code blocks, etc.)
            const formattedMessage = this.formatConsoleMessage(message);
            line.innerHTML = `<span class="timestamp">[${timestamp}]</span>${formattedMessage}`;
        } else {
            line.textContent = message;
        }

        consoleElement.appendChild(line);

        if (this.autoScroll && tabId === this.activeTabId) {
            consoleElement.scrollTop = consoleElement.scrollHeight;
        }
    }

    /**
     * Format a console message for display, handling:
     * - Multiline messages
     * - Code blocks (```language\ncode\n```)
     * - Bold text (**text**)
     * - Step dividers (━━━ Step N ━━━)
     */
    formatConsoleMessage(message) {
        if (!message) return '';

        // First escape HTML for safety
        let formatted = this.escapeHtml(message);

        // Handle code blocks: ```language\ncode\n```
        formatted = formatted.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre class="code-block${lang ? ' language-' + lang : ''}">${code.trim()}</pre>`;
        });

        // Handle inline code: `code`
        formatted = formatted.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

        // Handle bold text: **text**
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Handle step dividers (━━━ Step N ━━━ or similar patterns)
        formatted = formatted.replace(/(━+\s*(?:Step\s*\d+|[\w\s]+)\s*━+)/g, '<div class="step-divider">$1</div>');

        // Handle section headers starting with ##
        formatted = formatted.replace(/^##\s+(.+)$/gm, '<div class="section-header">$1</div>');

        // Convert newlines to <br> for proper display (but not inside code blocks)
        // Split by code blocks, process non-code parts, then rejoin
        const parts = formatted.split(/(<pre class="code-block[^"]*">[\s\S]*?<\/pre>)/g);
        formatted = parts.map(part => {
            if (part.startsWith('<pre')) {
                return part; // Don't modify code blocks
            }
            return part.replace(/\n/g, '<br>');
        }).join('');

        return formatted;
    }

    // Start a pentest in a new tab with real-time SSE streaming
    startPentestInNewTab(target, options = {}) {
        const tabId = this.createNewTab(target);
        const tabContext = this.tabs.get(tabId);

        this.logToTab(tabId, 'info', `Scheduling pentest for: ${target}`);
        this.logToTab(tabId, 'system', 'Starting real-time streaming...');

        const request = {
            targets: [{
                target: target,
                scope: options.scope || 'TARGETED',
                type: options.type || 'BLACK_BOX'
            }],
            style: options.style || 'AGGRESSIVE',
            exploit: options.exploit !== undefined ? options.exploit : true
        };

        // Update tab title
        this.updateTabTitle(tabId, `${target.substring(0, 15)}`);
        this.updateTabStatus(tabId, 'IN_PROGRESS');

        // Start SSE stream for this pentest
        this.startStreamInTab(tabId, request);
    }

    // Start SSE streaming in a specific tab
    startStreamInTab(tabId, request) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        // Close any existing stream
        tabContext.closeEventSource();

        // Create a new fetch request for SSE (POST with body)
        fetch(`${this.apiBase}/pentests/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            const processStream = () => {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        this.logToTab(tabId, 'info', 'Stream ended');
                        return;
                    }

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n');
                    buffer = lines.pop(); // Keep incomplete line in buffer

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const data = JSON.parse(line.substring(6));
                                this.handleStreamEvent(tabId, data);
                            } catch (e) {
                                // Ignore parse errors
                            }
                        }
                    }

                    processStream();
                }).catch(error => {
                    this.logToTab(tabId, 'error', `Stream error: ${error.message}`);
                });
            };

            processStream();

        }).catch(error => {
            this.logToTab(tabId, 'error', `Failed to start stream: ${error.message}`);
        });
    }

    // Watch an existing pentest in a specific tab via SSE
    startWatchInTab(tabId, pentestId) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        // Close any existing stream
        tabContext.closeEventSource();

        this.logToTab(tabId, 'info', `Watching pentest: ${pentestId}`);
        this.logToTab(tabId, 'system', 'Connecting to real-time stream...');

        tabContext.pentestId = pentestId;

        // Use EventSource for GET-based SSE
        const eventSource = new EventSource(`${this.apiBase}/pentests/${pentestId}/watch`);
        tabContext.eventSource = eventSource;

        eventSource.addEventListener('message', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.handleStreamEvent(tabId, data);
            } catch (err) {
                // Ignore parse errors
            }
        });

        eventSource.addEventListener('status', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.handleStreamEvent(tabId, data);
            } catch (err) {}
        });

        eventSource.addEventListener('phase', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.handleStreamEvent(tabId, data);
            } catch (err) {}
        });

        eventSource.addEventListener('finding', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.handleStreamEvent(tabId, data);
            } catch (err) {}
        });

        eventSource.addEventListener('done', (e) => {
            try {
                const data = JSON.parse(e.data);
                this.logToTab(tabId, 'success', data.message || 'Stream completed');
                eventSource.close();
                tabContext.eventSource = null;
            } catch (err) {}
        });

        eventSource.addEventListener('error', (e) => {
            if (eventSource.readyState === EventSource.CLOSED) {
                this.logToTab(tabId, 'info', 'Stream closed');
            } else {
                this.logToTab(tabId, 'error', 'Stream connection error');
            }
            tabContext.eventSource = null;
        });
    }

    // Handle stream events for a tab
    handleStreamEvent(tabId, data) {
        const tabContext = this.tabs.get(tabId);
        if (!tabContext) return;

        const type = data.type;

        if (type === 'schedule_response') {
            this.logToTab(tabId, 'success', `Pentest scheduled: ${data.pentest_id}`);
            if (data.message) {
                this.logToTab(tabId, 'info', data.message);
            }
            tabContext.pentestId = data.pentest_id;
            this.loadPentests();

        } else if (type === 'pentest_data') {
            // Full pentest data update - format like CLI
            const status = data.status;
            this.updateTabStatus(tabId, status);

            // Log pentest status update header (like CLI's "◆ Pentest Status Update")
            this.logToTab(tabId, 'status', '--- Pentest Status Update ---');
            this.logToTab(tabId, 'output', `  ID: ${data.id}`);
            this.logToTab(tabId, 'output', `  Status: ${status}`);
            this.logToTab(tabId, 'output', `  Findings: ${data.findings || 0}`);
            this.logToTab(tabId, 'output', `  Severity: ${data.severity || 'NONE'}`);

            // Log target info (like CLI)
            if (data.targets && data.targets.length > 0) {
                for (const target of data.targets) {
                    this.logToTab(tabId, 'output', `  Target: ${target.target}`);
                    this.logToTab(tabId, 'output', `    Status: ${target.status}`);
                    if (target.phase && target.phase !== 'PHASE_UNSPECIFIED') {
                        this.logToTab(tabId, 'output', `    Phase: ${target.phase}`);
                    }
                    if (target.findings > 0) {
                        this.logToTab(tabId, 'output', `    Findings: ${target.findings}`);
                    }
                    if (target.severity && target.severity !== 'NONE') {
                        this.logToTab(tabId, 'output', `    Severity: ${target.severity}`);
                    }
                }
            }

            // Update progress if this tab is active
            if (this.activeTabId === tabId) {
                this.updateTimeBasedProgress(data);
            }

            // Update pentest list
            if (data.id) {
                const idx = this.pentests.findIndex(p => p.id === data.id);
                if (idx >= 0) {
                    this.pentests[idx] = data;
                    this.renderPentestsList();
                }
            }

            // Check completion
            if (status === 'COMPLETED') {
                this.logToTab(tabId, 'success', 'Pentest completed successfully!');
                this.logToTab(tabId, 'info', `Final severity: ${data.severity || 'NONE'} | Findings: ${data.findings || 0}`);
                // Set progress to 100% on completion
                this.progressFill.style.width = '100%';
                this.progressText.textContent = '100%';
            } else if (status === 'FAILED') {
                this.logToTab(tabId, 'error', 'Pentest failed');
            }

        } else if (type === 'status_update') {
            const updateType = data.update_type;
            const message = data.message;

            if (message) {
                // Map update types to log types (matching CLI)
                // UpdateType enum: INFO=1, ERROR=2, STATUS=3, DEBUG=4
                let logType = 'output';  // Use 'output' for better visibility

                if (updateType === 2 || updateType === 'ERROR') {
                    logType = 'error';
                } else if (updateType === 3 || updateType === 'STATUS') {
                    logType = 'status';
                } else if (updateType === 4 || updateType === 'DEBUG') {
                    // DEBUG messages contain the step-by-step agent output
                    logType = 'output';
                } else if (updateType === 1 || updateType === 'INFO') {
                    logType = 'info';
                }

                // Log the message directly - formatConsoleMessage will handle formatting
                this.logToTab(tabId, logType, message);
            }

            // Handle nested pentest data
            if (data.data) {
                this.handleStreamEvent(tabId, data.data);
            }

        } else if (type === 'error') {
            this.logToTab(tabId, 'error', `Error: ${data.error}`);
            if (data.details) {
                this.logToTab(tabId, 'error', `Details: ${data.details}`);
            }
        }
    }

    // Download functionality
    async downloadEvidence(pentestId) {
        const id = pentestId || (this.selectedPentest ? this.selectedPentest.id : null);

        if (!id) {
            this.log('error', 'No pentest selected');
            return;
        }

        this.log('info', `Downloading evidence for: ${id}`);
        this.footerStatus.textContent = 'Downloading...';

        try {
            const response = await fetch(`${this.apiBase}/pentests/${id}/download`);

            if (!response.ok) {
                throw new Error(`Download failed: ${response.status}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `pentest_${id}_evidence.zip`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            this.log('success', 'Evidence downloaded successfully');
            this.loadEvidenceFiles(id);
        } catch (error) {
            this.log('error', `Download failed: ${error.message}`);
        } finally {
            this.footerStatus.textContent = 'Ready';
        }
    }

    // Export functionality
    async exportResults() {
        if (!this.selectedPentest) {
            this.log('error', 'No pentest selected');
            return;
        }

        this.log('info', 'Exporting results...');
        this.downloadEvidence();
    }

    // Modal Methods
    async openNewPentestModal() {
        if (!this.hasCredentials) {
            this.showCredentialsModal();
            return;
        }

        // Load playbooks and memory items for the dropdowns
        await this.loadPlaybooksForModal();
        await this.loadMemoryForModal();

        this.newPentestModal.classList.add('active');
        this.targetInput.focus();
    }

    async loadPlaybooksForModal() {
        try {
            const data = await this.apiRequest('/playbooks');
            const select = document.getElementById('playbook-select');
            select.innerHTML = '<option value="">None (Standard Pentest)</option>';

            if (data.success && data.playbooks) {
                data.playbooks.forEach(playbook => {
                    const option = document.createElement('option');
                    option.value = playbook.name;
                    option.textContent = playbook.name;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Failed to load playbooks:', error);
        }
    }

    async loadMemoryForModal() {
        try {
            const data = await this.apiRequest('/memory');
            const select = document.getElementById('memory-select');
            select.innerHTML = '';

            if (data.success && data.items) {
                data.items.forEach(item => {
                    if (item.name !== 'default') { // Skip default, it has its own checkbox
                        const option = document.createElement('option');
                        option.value = item.name;
                        option.textContent = item.name + (item.is_default ? ' (default)' : '');
                        select.appendChild(option);
                    }
                });
            }

            if (select.options.length === 0) {
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'No memory items available';
                option.disabled = true;
                select.appendChild(option);
            }
        } catch (error) {
            console.error('Failed to load memory items:', error);
        }
    }

    closeModal() {
        this.newPentestModal.classList.remove('active');
        this.targetInput.value = '';
        // Reset playbook and memory selections
        document.getElementById('playbook-select').value = '';
        document.getElementById('memory-select').selectedIndex = -1;
        document.getElementById('include-default-memory').checked = true;
    }

    async submitNewPentest() {
        const target = this.targetInput.value.trim();

        if (!target) {
            this.log('error', 'Target is required');
            return;
        }

        const playbook = document.getElementById('playbook-select').value;
        const memorySelect = document.getElementById('memory-select');
        const selectedMemory = Array.from(memorySelect.selectedOptions).map(opt => opt.value).filter(v => v);
        const includeDefaultMemory = document.getElementById('include-default-memory').checked;

        const request = {
            targets: [{
                target: target,
                scope: this.scopeSelect.value,
                type: this.typeSelect.value
            }],
            style: this.styleSelect.value,
            exploit: this.exploitCheckbox.checked
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

        this.closeModal();

        let logMessage = `Scheduling pentest for: ${target}`;
        if (playbook) logMessage += ` (playbook: ${playbook})`;
        if (selectedMemory.length > 0) logMessage += ` (memory: ${selectedMemory.join(', ')})`;
        this.log('info', logMessage);

        try {
            const data = await this.apiRequest('/pentests/schedule', {
                method: 'POST',
                body: JSON.stringify(request)
            });

            this.log('success', `Pentest scheduled: ${data.pentest_id}`);
            await this.loadPentests();

            // Auto-select and attach to the new pentest stream
            // Using attach allows reconnection if browser tab is closed
            setTimeout(() => {
                this.selectPentest(data.pentest_id);
                // Use attach endpoint for real-time streaming with reconnect capability
                this.startAttachInTab(this.activeTabId, data.pentest_id, false);
            }, 500);

        } catch (error) {
            this.log('error', `Failed to schedule: ${error.message}`);
        }
    }

    // Utility Methods
    formatDate(dateStr) {
        if (!dateStr) return '---';

        try {
            const date = new Date(dateStr);
            return date.toLocaleString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return '---';
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Chat Methods
    setChatContext(pentestId, target) {
        this.chatContextPentestId = pentestId;
        this.chatPentestContext.textContent = target || pentestId.substring(0, 12) + '...';
        this.chatInput.disabled = false;
        this.chatSendBtn.disabled = false;
        this.chatInput.placeholder = `Ask about ${target}...`;

        // Add system message about context change
        this.addChatMessage('assistant', `Context set to pentest: ${target}. You can now ask questions about this pentest's findings, vulnerabilities, and recommendations.`);

        // Focus the chat input
        this.chatInput.focus();
    }

    async sendChatMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        if (!this.chatContextPentestId) {
            this.addChatMessage('assistant', 'Please select a completed pentest first to ask questions about it.');
            return;
        }

        // Add user message to chat
        this.addChatMessage('user', message);
        this.chatInput.value = '';

        // Disable input while waiting for response
        this.chatInput.disabled = true;
        this.chatSendBtn.disabled = true;

        // Show thinking indicator
        const thinkingId = this.addChatMessage('assistant', 'Analyzing pentest data...', true);

        try {
            // Call the real chat API
            const response = await fetch(`${this.apiBase}/pentests/${this.chatContextPentestId}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            });

            const result = await response.json();

            // Remove thinking indicator
            this.removeChatMessage(thinkingId);

            if (result.success && result.answer) {
                this.addChatMessage('assistant', result.answer);
            } else {
                const errorMsg = result.error || 'Failed to get response from the AI assistant.';
                this.addChatMessage('assistant', `Error: ${errorMsg}`);
            }
        } catch (error) {
            // Remove thinking indicator
            this.removeChatMessage(thinkingId);
            this.addChatMessage('assistant', `Error: Failed to communicate with the server. ${error.message}`);
        } finally {
            // Re-enable input
            this.chatInput.disabled = false;
            this.chatSendBtn.disabled = false;
            this.chatInput.focus();
        }
    }

    addChatMessage(type, content, isThinking = false) {
        const messageId = `msg-${Date.now()}`;
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}${isThinking ? ' thinking' : ''}`;
        messageDiv.id = messageId;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;

        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        return messageId;
    }

    removeChatMessage(messageId) {
        const message = document.getElementById(messageId);
        if (message) {
            message.remove();
        }
    }

    clearChat() {
        // Keep only the welcome message
        this.chatMessages.innerHTML = `
            <div class="chat-message assistant">
                <div class="message-content">
                    Welcome! Select a completed pentest to ask questions about its findings, vulnerabilities, and recommendations.
                </div>
            </div>
        `;

        // Reset context
        this.chatContextPentestId = null;
        this.chatPentestContext.textContent = 'No pentest selected';
        this.chatInput.disabled = true;
        this.chatSendBtn.disabled = true;
        this.chatInput.placeholder = 'Ask about this pentest...';
        this.chatInput.value = '';
    }
}

// Initialize the terminal when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.terminal = new PentestTerminal();
});
