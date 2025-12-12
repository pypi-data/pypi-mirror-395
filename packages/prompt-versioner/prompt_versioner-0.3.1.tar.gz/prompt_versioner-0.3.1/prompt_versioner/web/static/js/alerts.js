/**
 * Performance alerts management
 */

const Alerts = {
    allAlerts: [], // Store all alerts for filtering
    currentFilters: {
        severity: 'all',
        type: 'all'
    },

    /**
     * Toggle Alerts section
     */
    toggle() {
        const section = document.getElementById('alerts-section');
        const button = document.getElementById('alerts-toggle-btn');

        if (section.style.display === 'none') {
            section.style.display = 'block';
            button.textContent = '⚠️ Hide Alerts';
            button.classList.add('active');
            // Ricarica gli alert quando viene mostrata la sezione
            this.load();
        } else {
            section.style.display = 'none';
            button.textContent = '⚠️ Show Alerts';
            button.classList.remove('active');
        }
    },

    /**
     * Initialize filter dropdowns
     */
    initializeFilters() {
        // Severity filter
        const severitySelect = document.getElementById('alert-severity-filter');
        if (severitySelect) {
            severitySelect.addEventListener('change', (e) => {
                this.currentFilters.severity = e.target.value;
                this.applyFilters();
            });
        }

        // Type filter
        const typeSelect = document.getElementById('alert-type-filter');
        if (typeSelect) {
            typeSelect.addEventListener('change', (e) => {
                this.currentFilters.type = e.target.value;
                this.applyFilters();
            });
        }
    },

    /**
     * Apply current filters to alerts
     */
    applyFilters() {
        let filteredAlerts = this.allAlerts;

        // Filter by severity
        if (this.currentFilters.severity !== 'all') {
            filteredAlerts = filteredAlerts.filter(alert => {
                const severity = Utils.getAlertSeverity(alert.change_percent, alert.threshold);
                return severity === this.currentFilters.severity;
            });
        }

        // Filter by type
        if (this.currentFilters.type !== 'all') {
            filteredAlerts = filteredAlerts.filter(alert =>
                alert.type === this.currentFilters.type
            );
        }

        this.render(filteredAlerts);
    },

    /**
     * Populate type filter with available types
     */
    populateTypeFilter() {
        const typeSelect = document.getElementById('alert-type-filter');
        if (!typeSelect || this.allAlerts.length === 0) return;

        // Get unique alert types
        const types = [...new Set(this.allAlerts.map(alert => alert.type))];

        // Clear existing options (except "All")
        const allOption = typeSelect.querySelector('option[value="all"]');
        typeSelect.innerHTML = '';
        if (allOption) {
            typeSelect.appendChild(allOption.cloneNode(true));
        } else {
            const defaultOption = document.createElement('option');
            defaultOption.value = 'all';
            defaultOption.textContent = 'All Types';
            typeSelect.appendChild(defaultOption);
        }

        // Add type options
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type.replace('_', ' ').toUpperCase();
            typeSelect.appendChild(option);
        });
    },

    /**
     * Load all alerts from API
     */
    async load() {
        console.log('Loading alerts...');
        try {
            const alerts = await API.getAllAlerts();
            console.log('Alerts loaded:', alerts);
            const container = document.getElementById('alerts-container');

            if (!container) {
                console.error('Alerts container not found');
                return;
            }

            // Store all alerts for filtering
            this.allAlerts = alerts || [];

            if (this.allAlerts.length === 0) {
                console.log('No alerts found, showing empty state');
                // Mostra messaggio di "nessun alert"
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-content">
                            <div class="empty-icon">✅</div>
                            <h3>No Active Alerts</h3>
                            <p>All systems are running normally</p>
                        </div>
                    </div>
                `;
                return;
            }

            console.log(`Loaded ${this.allAlerts.length} alerts`);

            // Initialize filters after loading data
            this.populateTypeFilter();
            this.initializeFilters();

            // Apply current filters and render
            this.applyFilters();
        } catch (error) {
            console.error('Error loading alerts:', error);
            const container = document.getElementById('alerts-container');
            if (container) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-content">
                            <div class="empty-icon">❌</div>
                            <h3>Error Loading Alerts</h3>
                            <p>Error: ${error.message}</p>
                        </div>
                    </div>
                `;
            }
        }
    },

    /**
     * Render alerts list
     */
    render(alerts) {
        const container = document.getElementById('alerts-container');

        container.innerHTML = alerts.map(alert => {
            const icon = Utils.getAlertIcon(alert.type);
            const severity = Utils.getAlertSeverity(alert.change_percent, alert.threshold);

            return `
                <div class="alert-card ${severity}">
                    <div class="alert-header">
                        <span class="alert-type">${icon} ${alert.type.replace('_', ' ')}</span>
                        <span class="prompt-meta">${alert.prompt_name}</span>
                    </div>
                    <div class="alert-message">${alert.message}</div>
                    <div class="alert-details">
                        ${alert.baseline_version} → ${alert.current_version} |
                        Baseline: ${alert.baseline_value.toFixed(4)} |
                        Current: ${alert.current_value.toFixed(4)}
                    </div>
                </div>
            `;
        }).join('');

        // Update alerts badge with filtered count
        if (typeof TabSystem !== 'undefined' && TabSystem.updateAlertsBadge) {
            TabSystem.updateAlertsBadge(alerts.length);
        }
    },

    /**
     * Reset all filters to default values
     */
    resetFilters() {
        this.currentFilters = {
            severity: 'all',
            type: 'all'
        };

        // Reset UI selects
        const severitySelect = document.getElementById('alert-severity-filter');
        const typeSelect = document.getElementById('alert-type-filter');

        if (severitySelect) severitySelect.value = 'all';
        if (typeSelect) typeSelect.value = 'all';

        // Apply filters (will show all alerts)
        this.applyFilters();
    }
};

// Expose functions globally
window.toggleAlerts = () => Alerts.toggle();
window.resetAlertFilters = () => Alerts.resetFilters();
window.filterAlerts = () => Alerts.applyFilters();
