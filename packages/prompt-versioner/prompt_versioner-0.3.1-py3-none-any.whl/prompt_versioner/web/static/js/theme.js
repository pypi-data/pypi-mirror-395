/**
 * Theme management (Dark/Light mode)
 */

const Theme = {
    /**
     * Initialize theme from localStorage
     */
    init() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        if (savedTheme === 'light') {
            document.body.classList.add('light-mode');
            document.getElementById('theme-icon').textContent = '☀️';
        }
    },

    /**
     * Toggle between dark and light mode
     */
    toggle() {
        const body = document.body;
        const icon = document.getElementById('theme-icon');

        if (body.classList.contains('light-mode')) {
            body.classList.remove('light-mode');
            icon.textContent = '🌙';
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.add('light-mode');
            icon.textContent = '☀️';
            localStorage.setItem('theme', 'light');
        }
    }
};

// Make toggle function globally available for onclick
window.toggleTheme = () => Theme.toggle();
