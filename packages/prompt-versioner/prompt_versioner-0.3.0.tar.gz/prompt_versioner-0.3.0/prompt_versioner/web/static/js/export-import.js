/**
 * Export and Import functionality
 */

const ExportImport = {
    /**
     * Export all prompts as ZIP
     */
    async exportAll() {
        try {
            const blob = await API.exportAll();
            Utils.downloadBlob(blob, 'all_prompts.zip');
            Utils.showNotification('All prompts exported successfully', 'success');
        } catch (error) {
            Utils.showNotification('Export failed: ' + error.message, 'error');
        }
    },

    /**
     * Export single prompt as JSON
     */
    async exportSingle(promptName) {
        try {
            const blob = await API.exportPrompt(promptName);
            Utils.downloadBlob(blob, `${promptName}_export.json`);
            Utils.showNotification(`Exported "${promptName}"`, 'success');
        } catch (error) {
            Utils.showNotification('Export failed: ' + error.message, 'error');
        }
    },

    /**
     * Export specific version of a prompt as JSON
     */
    async exportVersion(promptName, version) {
        try {
            const blob = await API.exportVersion(promptName, version);
            Utils.downloadBlob(blob, `${promptName}_v${version}_export.json`);
            Utils.showNotification(`Exported "${promptName}" version ${version}`, 'success');
        } catch (error) {
            Utils.showNotification('Export failed: ' + error.message, 'error');
        }
    },

    /**
     * Import prompt from file
     */
    async import() {
        const fileInput = document.getElementById('import-file');
        const file = fileInput.files[0];

        if (!file) return;

        try {
            const result = await API.importPrompt(file);
            Utils.showNotification(
                `Imported: ${result.imported} versions, Skipped: ${result.skipped}`,
                'success'
            );

            // Reload prompts list
            Prompts.load();
        } catch (error) {
            Utils.showNotification('Import failed: ' + error.message, 'error');
        } finally {
            fileInput.value = ''; // Reset input
        }
    }
};

// Expose globally
window.exportAll = () => ExportImport.exportAll();
window.exportSinglePrompt = (name) => ExportImport.exportSingle(name);
window.exportVersion = (name, version) => ExportImport.exportVersion(name, version);
window.importPrompt = () => ExportImport.import();
