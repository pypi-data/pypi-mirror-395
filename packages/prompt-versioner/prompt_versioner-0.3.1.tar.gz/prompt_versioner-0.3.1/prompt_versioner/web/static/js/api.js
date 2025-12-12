/**
 * API communication layer
 */

const API = {
    /**
     * Get all prompts with metadata
     */

    async handleResponse(response) {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    },

    async getPrompts() {
        const response = await fetch('/api/prompts');
        return await response.json();
    },

    /**
     * Get versions for a specific prompt with diffs
     */
    async getVersionsWithDiffs(promptName) {
        const response = await fetch(`/api/prompts/${promptName}/versions/with-diffs`);
        return await response.json();
    },

    /**
     * Get A/B test options for a prompt
     */
    async getABTestOptions(promptName) {
        const response = await fetch(`/api/prompts/${promptName}/ab-tests`);
        return await response.json();
    },

    /**
     * Compare two versions
     */
    async compareVersions(promptName, versionA, versionB, metric) {
        const response = await fetch(
            `/api/prompts/${promptName}/compare?version_a=${versionA}&version_b=${versionB}&metric=${metric}`
        );
        return await response.json();
    },

    /**
     * Get all alerts
     */
    async getAllAlerts() {
        const response = await fetch('/api/alerts');
        return await response.json();
    },

    /**
     * Export single prompt
     */
    async exportPrompt(promptName) {
        const response = await fetch(`/api/prompts/${promptName}/export`);
        return await response.blob();
    },

    /**
     * Export specific version of a prompt
     */
    async exportVersion(promptName, version) {
        const response = await fetch(`/api/prompts/${promptName}/versions/${version}/export`);
        return await response.blob();
    },

    /**
     * Export all prompts
     */
    async exportAll() {
        const response = await fetch('/api/export-all');
        return await response.blob();
    },

    /**
     * Import prompt from file
     */
    async importPrompt(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/prompts/import', {
            method: 'POST',
            body: formData
        });

        return await response.json();
    }
};
