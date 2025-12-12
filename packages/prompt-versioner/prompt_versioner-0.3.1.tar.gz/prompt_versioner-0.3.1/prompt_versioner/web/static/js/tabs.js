/**
 * Tab Navigation System
 */

const TabSystem = {

    /**
     * Switch to a specific tab
     */
    switchTab(tabName) {
        // Remove active class from all tabs and content
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

        // Add active class to selected tab and content
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`tab-${tabName}`).classList.add('active');

        // Initialize specific tab content if needed
        this.initializeTabContent(tabName);
    },

    /**
     * Initialize content for specific tabs
     */
    initializeTabContent(tabName) {
        switch(tabName) {
            case 'prompts':
                // Prompts tab is already initialized by main.js
                break;
            case 'ab-testing':
                // Initialize AB testing if not already done
                if (typeof ABTesting !== 'undefined' && ABTesting.loadPromptsForAB) {
                    ABTesting.loadPromptsForAB();
                }
                break;
            case 'compare':
                // Initialize comparison if not already done
                if (typeof DiffComparison !== 'undefined' && DiffComparison.loadPromptsForDiff) {
                    // Check if prompts are already loaded by looking for actual prompt options (not just the placeholder)
                    const diffPromptSelect = document.getElementById('diff-prompt-select');
                    if (diffPromptSelect) {
                        const hasPromptsLoaded = Array.from(diffPromptSelect.options).some(option =>
                            option.value !== "" && option.value !== "no-prompts" && !option.disabled
                        );
                        if (!hasPromptsLoaded) {
                            DiffComparison.loadPromptsForDiff();
                        }
                    }
                }
                break;
            case 'alerts':
                // Load alerts if not already done
                if (typeof Alerts !== 'undefined' && Alerts.load) {
                    Alerts.load();
                }
                break;
        }
    },

    /**
     * Update alerts badge count
     */
    updateAlertsBadge(count) {
        const badge = document.getElementById('alerts-badge');
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    },

    /**
     * Refresh alerts
     */
    refreshAlerts() {
        if (typeof Alerts !== 'undefined' && Alerts.load) {
            Alerts.load();
        }
    },

    /**
     * Clear all alerts
     */
    clearAllAlerts() {
        const container = document.getElementById('alerts-container');
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-content">
                    <div class="empty-icon">✅</div>
                    <h3>No Active Alerts</h3>
                    <p>All alerts have been cleared</p>
                </div>
            </div>
        `;
        this.updateAlertsBadge(0);
    },

    /**
     * Filter alerts - delegates to Alerts module
     */
    filterAlerts() {
        if (typeof Alerts !== 'undefined' && Alerts.applyFilters) {
            Alerts.applyFilters();
        }
    },

    /**
     * Initialize the tab system
     */
    initialize() {
        // Set default tab
        this.switchTab('prompts');

        // Monitor for alert updates
        if (typeof Alerts !== 'undefined' && Alerts.load) {
            const originalLoad = Alerts.load;
            const self = this;
            Alerts.load = function() {
                originalLoad.call(this);
                // Count alerts and update badge after loading
                setTimeout(() => {
                    const alertElements = document.querySelectorAll('#alerts-container .alert-item, #alerts-container .alert-card');
                    self.updateAlertsBadge(alertElements.length);
                }, 100);
            };
        }

        // Override original toggle functions to use new tab system
        window.toggleABTesting = () => this.switchTab('ab-testing');
        window.toggleAlerts = () => this.switchTab('alerts');

        // Add compatibility for existing diff comparison toggle
        if (typeof DiffComparison !== 'undefined') {
            DiffComparison.toggleVersionComparison = () => this.switchTab('compare');
        }
    }
};

// Expose functions globally
window.switchTab = (tabName) => TabSystem.switchTab(tabName);
window.refreshAlerts = () => TabSystem.refreshAlerts();
window.clearAllAlerts = () => TabSystem.clearAllAlerts();
window.filterAlerts = () => TabSystem.filterAlerts();

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    TabSystem.initialize();
});
