/**
 * Utility functions
 */

const Utils = {
    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Render diff segments with highlighting
     */
    renderDiff(diffSegments) {
        if (!diffSegments || diffSegments.length === 0) {
            return '';
        }

        return diffSegments.map(segment => {
            const text = this.escapeHtml(segment.text);
            if (segment.type === 'added') {
                return `<span class="diff-added">${text}</span>`;
            } else if (segment.type === 'removed') {
                return `<span class="diff-removed">${text}</span>`;
            } else {
                return text;
            }
        }).join(' ');
    },

    /**
     * Format metric value based on type
     */
    formatMetricValue(value, metric) {
        if (metric === 'cost') {
            return `$${value.toFixed(4)}`;
        } else if (metric === 'latency') {
            return `${Math.round(value)}ms`;
        } else if (metric === 'quality_score' || metric === 'accuracy') {
            return `${(value * 100).toFixed(1)}%`;
        }
        return value.toFixed(2);
    },

    /**
     * Download blob as file
     */
    downloadBlob(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    },

    /**
     * Show toast notification
     */
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            background: ${type === 'success' ? '#10b981' : '#ef4444'};
            color: white;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 1001;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    /**
     * Get alert icon by type
     */
    getAlertIcon(type) {
        const icons = {
            'cost_increase': '💰',
            'latency_increase': '⏱️',
            'quality_decrease': '📉',
            'error_rate_increase': '❌'
        };
        return icons[type] || '⚠️';
    },

    /**
     * Get alert severity level
     */
    getAlertSeverity(changePercent, threshold) {
        const change = Math.abs(changePercent);
        if (change > threshold * 2) return 'error';
        if (change > threshold * 1.5) return 'warning';
        return 'info';
    }
};
