/**
 * Gestione Layout a Due Colonne per Prompts
 */

// Variabili globali per il layout a due colonne
let currentSelectedPrompt = null;
let promptsData = new Map();

const PromptsLayout = {
    allData: [],

    /**
     * Inizializza il layout a due colonne
     */
    init() {
        this.loadPrompts();
        this.setupEventListeners();
    },

    /**
     * Setup event listeners per ricerca e ordinamento
     */
    setupEventListeners() {
        // Input di ricerca
        const searchInput = document.querySelector('.search-input-minimal');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce(() => this.searchPrompts(), 300));
        }

        // Select per ordinamento
        const sortSelect = document.querySelector('.sort-select-minimal');
        if (sortSelect) {
            sortSelect.addEventListener('change', () => this.searchPrompts());
        }
    },

    /**
     * Carica tutti i prompts dall'API
     */
    async loadPrompts() {
        try {
            const response = await fetch('/api/prompts');
            const data = await response.json();

            // Verifica che ci siano i dati corretti
            if (!data || !Array.isArray(data.prompts)) {
                throw new Error('Risposta API non valida: prompts non trovati');
            }

            this.allData = data.prompts;

            // Aggiorna le statistiche
            this.updateStats(data);

            // Popola la mappa dei dati
            promptsData.clear();
            data.prompts.forEach(prompt => {
                // Aggiungi proprietà computed necessarie
                prompt.versions = new Array(prompt.version_count || 0);
                prompt.updated_at = prompt.latest_timestamp || new Date().toISOString();
                promptsData.set(prompt.name, prompt);
            });

            // Mostra i prompts nella sidebar
            this.displayPromptsInSidebar(data.prompts);

        } catch (error) {
            console.error('Errore nel caricamento dei prompts:', error);
            this.showError('Errore nel caricamento dei prompts: ' + error.message);
        }
    },

    /**
     * Aggiorna le statistiche nell'header
     */
    updateStats(data) {
        const elements = {
            'total-prompts': data.prompts.length,
            'total-versions': data.total_versions,
            'total-cost': (data.total_cost || 0).toFixed(4),
            'total-tokens': (data.total_tokens || 0).toLocaleString(),
            'total-calls': (data.total_calls || 0).toLocaleString()
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) element.textContent = value;
        });
    },

    /**
     * Mostra i prompts nella sidebar sinistra
     */
    displayPromptsInSidebar(prompts) {
        const promptList = document.querySelector('.prompt-list-minimal');
        if (!promptList) return;

        promptList.innerHTML = '';

        if (prompts.length === 0) {
            promptList.appendChild(this.createEmptyState({
                icon: '📄',
                title: 'Nessun prompt trovato',
                message: 'Prova a modificare i filtri di ricerca'
            }));
            this.showEmptyState();
            return;
        }

        prompts.forEach(prompt => {
            const promptElement = this.createPromptItem(prompt);
            promptList.appendChild(promptElement);
        });
    },

    /**
     * Crea un elemento prompt usando il template
     */
    createPromptItem(prompt) {
        const template = document.getElementById('prompt-item-template');
        const clone = template.content.cloneNode(true);

        const promptElement = clone.querySelector('.prompt-item-minimal');
        promptElement.dataset.promptName = prompt.name;

        // Popola i dati
        const nameElement = clone.querySelector('.prompt-name-minimal');
        nameElement.textContent = prompt.name;

        const metaElement = clone.querySelector('.prompt-meta-minimal');
        const lastUpdate = prompt.latest_timestamp || prompt.updated_at || new Date().toISOString();
        metaElement.textContent = `${prompt.version_count || 0} versions · Last: ${this.formatDate(lastUpdate)}`;

        // Aggiungi event listeners
        const deleteBtn = clone.querySelector('.delete-prompt-btn');
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            this.deletePrompt(prompt.name);
        };

        promptElement.addEventListener('click', (e) => {
            if (!e.target.closest('.btn-icon')) {
                this.selectPrompt(prompt.name);
            }
        });

        return clone;
    },

    /**
     * Seleziona un prompt e mostra le sue versioni
     */
    selectPrompt(promptName) {
        // Rimuovi selezione precedente
        document.querySelectorAll('.prompt-item-minimal.active').forEach(item => {
            item.classList.remove('active');
        });

        // Verifica che il prompt esista nei dati
        if (!promptsData.has(promptName)) {
            console.error('Prompt non trovato nei dati:', promptName);
            this.showEmptyState();
            return;
        }

        // Seleziona il nuovo prompt
        const promptElement = document.querySelector(`[data-prompt-name="${promptName}"]`);
        if (promptElement) {
            promptElement.classList.add('active');
            currentSelectedPrompt = promptName;
            this.displayVersionsForPrompt(promptName);
        }
    },

    /**
     * Mostra le versioni per il prompt selezionato
     */
    displayVersionsForPrompt(promptName) {
        const versionsPanel = document.querySelector('.versions-panel');
        const prompt = promptsData.get(promptName);

        if (!prompt || !versionsPanel) return;

        // Usa il template per il version header
        const template = document.getElementById('version-header-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.version-header-name').textContent = promptName;
        const countSpan = clone.querySelector('.version-header-count');
        countSpan.textContent = `${prompt.version_count || 0} versions`;
        countSpan.style.fontWeight = 'normal';
        countSpan.style.color = '#94a3b8';
        countSpan.style.fontSize = '0.9rem';

        versionsPanel.innerHTML = '';
        versionsPanel.appendChild(clone);

        // Mostra loading state
        const versionList = document.getElementById('versionListClean');
        versionList.appendChild(this.createLoadingState());

        // Carica le versioni dettagliate
        this.loadVersionsForPrompt(promptName);
    },

    /**
     * Carica le versioni dettagliate per un prompt
     */
    async loadVersionsForPrompt(promptName) {
        try {
            const url = `/api/prompts/${encodeURIComponent(promptName)}/versions`;
            const response = await fetch(url);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Errore HTTP response:', errorText);
                throw new Error(`HTTP ${response.status}: ${response.statusText}. ${errorText}`);
            }

            const versions = await response.json();

            if (!Array.isArray(versions)) {
                console.error('Tipo di risposta non valido:', typeof versions, versions);

                // Se è un oggetto con proprietà error, mostra il messaggio
                if (versions && typeof versions === 'object' && versions.error) {
                    throw new Error(`Errore API: ${versions.error}`);
                }

                throw new Error('Risposta API non valida: atteso un array di versioni');
            }

            // Verifica che ogni versione abbia le proprietà minime necessarie
            const validVersions = versions.filter(version => {
                return version && typeof version === 'object';
            });

            this.displayVersionsList(validVersions);
        } catch (error) {
            console.error('Errore completo nel caricamento delle versioni:', error);
            const versionList = document.getElementById('versionListClean');
            if (versionList) {
                versionList.innerHTML = '';
                versionList.appendChild(this.createErrorState({
                    title: 'Errore nel caricamento',
                    message: error.message,
                    onRetry: () => this.loadVersionsForPrompt(promptName)
                }));
            }
        }
    },

    /**
     * Mostra la lista delle versioni nel pannello destro
     */
    displayVersionsList(versions) {
        const versionList = document.getElementById('versionListClean');
        if (!versionList) return;

        versionList.innerHTML = '';

        if (!versions || versions.length === 0) {
            versionList.appendChild(this.createEmptyState({
                icon: '📝',
                title: 'Nessuna versione',
                message: 'Questo prompt non ha ancora versioni'
            }));
            return;
        }

        versions.forEach((version) => {
            if (!version) return;

            const versionElement = this.createVersionItem(version);
            versionList.appendChild(versionElement);
        });
    },

    /**
     * Crea un elemento versione usando il template
     */
    createVersionItem(version) {
        const template = document.getElementById('version-item-template');
        const clone = template.content.cloneNode(true);

        const versionNumber = version.version || 'N/A';
        const promptName = version.prompt_name || version.name || 'N/A';
        const createdAt = version.created_at || version.timestamp || new Date().toISOString();

        // Popola i dati base
        const versionTag = clone.querySelector('.version-tag-clean');
        versionTag.textContent = `v${versionNumber}`;

        const versionMeta = clone.querySelector('.version-meta');
        versionMeta.textContent = `${this.formatDate(createdAt)}`;

        // Aggiungi metriche
        const metricsContainer = clone.querySelector('.version-metrics-container');
        const summary = version.summary || version.metrics_summary || {};
        const hasMetrics = summary && (summary.call_count > 0 || summary.avg_total_tokens > 0 || summary.total_cost > 0);

        if (hasMetrics) {
            metricsContainer.appendChild(this.createMetricsRow(summary));
        } else {
            metricsContainer.appendChild(this.createNoMetrics());
        }

        // Aggiungi event listeners
        const viewBtn = clone.querySelector('.view-details-btn');
        viewBtn.onclick = () => this.viewVersionDetails(promptName, versionNumber);

        const exportBtn = clone.querySelector('.export-version-btn');
        exportBtn.onclick = () => this.exportVersion(promptName, versionNumber);

        const deleteBtn = clone.querySelector('.delete-version-btn');
        deleteBtn.onclick = () => this.deleteVersion(promptName, versionNumber);

        return clone;
    },

    /**
     * Funzione di ricerca e filtro
     */
    searchPrompts() {
        const searchTerm = document.querySelector('.search-input-minimal')?.value.toLowerCase() || '';
        const sortBy = document.querySelector('.sort-select-minimal')?.value || 'name';

        // Filtra i prompts
        let filteredPrompts = this.allData.filter(prompt =>
            prompt.name.toLowerCase().includes(searchTerm)
        );

        // Ordina i prompts
        filteredPrompts.sort((a, b) => {
            switch(sortBy) {
                case 'updated':
                    const dateA = new Date(a.latest_timestamp || a.updated_at || 0);
                    const dateB = new Date(b.latest_timestamp || b.updated_at || 0);
                    return dateB - dateA;
                case 'versions':
                    return (b.version_count || 0) - (a.version_count || 0);
                default:
                    return a.name.localeCompare(b.name);
            }
        });

        // Aggiorna i dati nella mappa
        promptsData.clear();
        filteredPrompts.forEach(prompt => {
            promptsData.set(prompt.name, prompt);
        });

        this.displayPromptsInSidebar(filteredPrompts);

        // Mantieni la selezione se ancora valida
        if (currentSelectedPrompt && filteredPrompts.find(p => p.name === currentSelectedPrompt)) {
            this.selectPrompt(currentSelectedPrompt);
        } else {
            this.showEmptyState();
        }
    },

    /**
     * Visualizza dettagli di una versione specifica
     */
    async viewVersionDetails(promptName, version) {
        try {
            // Carica i dettagli completi della versione
            const response = await fetch(`/api/prompts/${encodeURIComponent(promptName)}/versions/${version}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const versionData = await response.json();
            this.showVersionModal(versionData);

        } catch (error) {
            console.error('Errore nel caricamento dei dettagli:', error);
            alert('Errore nel caricamento dei dettagli della versione: ' + error.message);
        }
    },

    /**
     * Mostra i dettagli della versione in un modal
     */
    async showVersionModal(versionData) {
        // Rimuovi modal esistente se presente
        const existingModal = document.getElementById('versionModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Carica i dati dei modelli PRIMA di creare il modal
        let modelsData = null;
        try {
            const url = `/api/prompts/${encodeURIComponent(versionData.name || versionData.prompt_name)}/versions/${versionData.version}/models`;
            const response = await fetch(url);
            if (response.ok) {
                const data = await response.json();
                modelsData = data.models;
            }
        } catch (error) {
            console.error('Error loading models data for metrics:', error);
        }

        // Crea modal usando il template
        const template = document.getElementById('version-modal-template');
        const modal = template.content.cloneNode(true);

        // Popola i dati del modal passando anche i dati dei modelli
        this.populateModalData(modal, versionData, modelsData);

        // Aggiungi il modal al body
        document.body.appendChild(modal);

        // Aggiungi event listeners
        this.setupModalEventListeners();

        // Ora che il modal è nel DOM, carica il confronto modelli (per la sezione visuale)
        this.loadModelComparison(
            versionData.name || versionData.prompt_name,
            versionData.version,
            versionData.id,
            modelsData // Passa i dati già caricati per evitare doppia chiamata
        );
    },

    /**
     * Popola i dati nel modal template
     */
    populateModalData(modal, versionData, modelsData = null) {
        const systemPrompt = versionData.system_prompt || 'Nessun prompt di sistema';
        const userPrompt = versionData.user_prompt || 'Nessun prompt utente';
        const metadata = versionData.metadata ? JSON.stringify(versionData.metadata, null, 2) : 'Nessun metadata';
        const model = versionData.model_name || versionData.model || versionData.metadata?.model || 'N/A';

        // Popola header
        modal.querySelector('.modal-prompt-name').textContent = versionData.name || versionData.prompt_name;
        modal.querySelector('.modal-version-number').textContent = `v${versionData.version}`;

        // Popola contenuti prompt
        modal.querySelector('.system-prompt-content').textContent = systemPrompt;
        modal.querySelector('.user-prompt-content').textContent = userPrompt;

        const createdBySection = modal.querySelector('.created-by-section');
        if (versionData.created_by) {
            createdBySection.style.display = 'block';
            modal.querySelector('.created-by').textContent = versionData.created_by;
        }

        const metadataSection = modal.querySelector('.metadata-json-section');
        if (versionData.metadata && Object.keys(versionData.metadata).length > 0) {
            metadataSection.style.display = 'block';
            modal.querySelector('.metadata-json').textContent = metadata;
        }

        // Popola metriche con dati aggregati di tutti i modelli
        const metricsSection = modal.querySelector('.metrics-section');
        metricsSection.appendChild(this.createModalMetricsSection(versionData, modelsData));

        // Aggiungi sezione model comparison dopo le metriche nel modal-body
        const modalBody = modal.querySelector('.modal-body');
        const comparisonTemplate = document.getElementById('model-comparison-section-template');
        const comparisonSection = comparisonTemplate.content.cloneNode(true);

        // Inserisci dopo la metrics-section
        const metadataGrid = modalBody.querySelector('.metadata-grid');
        if (metadataGrid) {
            modalBody.insertBefore(comparisonSection, metadataGrid);
        } else {
            modalBody.appendChild(comparisonSection);
        }

        // NOTA: loadModelComparison verrà chiamato dopo che il modal è nel DOM
        // vedi showVersionModal()
    },

    /**
     * Crea la sezione metriche del modal (aggregata per tutti i modelli)
     */
    createModalMetricsSection(versionData, modelsData = null) {
        const summary = versionData.metrics_summary || {};
        const hasMetrics = summary.call_count > 0;

        if (!hasMetrics) {
            const template = document.getElementById('modal-metrics-section-template');
            const clone = template.content.cloneNode(true);

            // Modifica per no-metrics
            const section = clone.querySelector('.modal-metrics-section');
            section.style.borderLeftColor = '#64748b';
            clone.querySelector('.metrics-title').style.color = '#64748b';
            clone.querySelector('.metrics-title').textContent = '📊 Performance Metrics (All Models)';

            const container = clone.querySelector('.metrics-grid');
            const noMetricsTemplate = document.getElementById('no-metrics-message-template');
            container.innerHTML = '';
            container.appendChild(noMetricsTemplate.content.cloneNode(true));

            return clone;
        }

        const template = document.getElementById('modal-metrics-section-template');
        const clone = template.content.cloneNode(true);

        // Se abbiamo dati dei modelli, calcola metriche aggregate
        let callCount, avgTokens, totalCost, avgLatency, avgQuality, successRate;

        if (modelsData && Object.keys(modelsData).length > 0) {
            // Aggrega dati da tutti i modelli
            const models = Object.values(modelsData);

            callCount = models.reduce((sum, m) => sum + (m.call_count || 0), 0);
            totalCost = models.reduce((sum, m) => sum + (m.total_cost || 0), 0);

            // Media pesata per tokens, latency e quality
            const totalCalls = callCount || 1; // evita divisione per zero
            avgTokens = Math.round(
                models.reduce((sum, m) => sum + (m.avg_total_tokens || 0) * (m.call_count || 0), 0) / totalCalls
            );
            avgLatency = Math.round(
                models.reduce((sum, m) => sum + (m.avg_latency || 0) * (m.call_count || 0), 0) / totalCalls
            );
            avgQuality =
                models.reduce((sum, m) => sum + (m.avg_quality || 0) * (m.call_count || 0), 0) / totalCalls;

            // Success rate aggregato
            const totalSuccess = models.reduce((sum, m) => sum + ((m.success_rate || 0) * (m.call_count || 0)), 0);
            successRate = (totalSuccess / totalCalls) * 100;
        } else {
            // Fallback ai dati originali
            callCount = summary.call_count || 0;
            avgTokens = Math.round(summary.avg_total_tokens || 0);
            totalCost = summary.total_cost || 0;
            avgLatency = Math.round(summary.avg_latency || 0);
            avgQuality = summary.avg_quality || 0;
            successRate = (summary.success_rate * 100) || 0;
        }

        successRate = Math.min(successRate, 100);

        // Aggiorna il titolo per chiarire che sono dati aggregati
        clone.querySelector('.metrics-title').textContent = '📊 Performance Metrics (All Models)';

        // Popola i valori
        clone.querySelector('.metric-calls .metric-value').textContent = callCount;
        clone.querySelector('.metric-tokens .metric-value').textContent = avgTokens;
        clone.querySelector('.metric-cost .metric-value').textContent = `€${totalCost.toFixed(4)}`;
        clone.querySelector('.metric-latency .metric-value').textContent = `${avgLatency}ms`;
        clone.querySelector('.metric-quality .metric-value').textContent = avgQuality.toFixed(2);
        clone.querySelector('.metric-success .metric-value').textContent = `${successRate.toFixed(1)}%`;

        return clone;
    },

    /**
     * Setup event listeners per il modal
     */
    setupModalEventListeners() {
        const modal = document.getElementById('versionModal');
        if (!modal) return;

        // Chiudi modal con bottone
        const closeBtn = modal.querySelector('.modal-close-btn');
        closeBtn.onclick = () => modal.remove();

        // Chiudi modal cliccando fuori
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        // Chiudi modal con ESC
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
    },

    /**
     * Elimina una versione specifica
     */
    async deleteVersion(promptName, version) {
        if (!confirm(`Sei sicuro di voler eliminare la versione ${version} del prompt "${promptName}"?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/prompts/${encodeURIComponent(promptName)}/versions/${version}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                // Ricarica le versioni per il prompt corrente
                if (currentSelectedPrompt === promptName) {
                    this.loadVersionsForPrompt(promptName);
                }
                // Ricarica anche la lista dei prompts per aggiornare i contatori
                this.loadPrompts();
            } else {
                const errorData = await response.json();
                const errorMessage = errorData.error || 'Errore durante l\'eliminazione della versione';
                alert(errorMessage);
            }
        } catch (error) {
            console.error('Errore:', error);
            alert('Errore durante l\'eliminazione della versione');
        }
    },

    /**
     * Esporta una versione specifica
     */
    async exportVersion(promptName, version) {
        try {
            await window.exportVersion(promptName, version);
        } catch (error) {
            console.error('Errore durante l\'export della versione:', error);
            alert('Errore durante l\'export della versione');
        }
    },

    /**
     * Elimina un intero prompt
     */
    async deletePrompt(promptName) {
        if (!confirm(`Sei sicuro di voler eliminare il prompt "${promptName}" e tutte le sue versioni?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/prompts/${encodeURIComponent(promptName)}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                // Rimuovi dai dati locali
                promptsData.delete(promptName);
                this.allData = this.allData.filter(p => p.name !== promptName);

                // Se era il prompt selezionato, resetta la selezione
                if (currentSelectedPrompt === promptName) {
                    currentSelectedPrompt = null;
                    this.showEmptyState();
                }

                // Ricarica la lista
                this.loadPrompts();
            } else {
                alert('Errore durante l\'eliminazione del prompt');
            }
        } catch (error) {
            console.error('Errore:', error);
            alert('Errore durante l\'eliminazione del prompt');
        }
    },

    /**
     * Mostra stato vuoto nel pannello versioni
     */
    showEmptyState() {
        const versionsPanel = document.querySelector('.versions-panel');
        if (versionsPanel) {
            versionsPanel.innerHTML = '';
            versionsPanel.appendChild(this.createEmptyState({
                icon: '📄',
                title: 'Choose a prompt',
                message: 'Select a prompt from the list to view its versions',
                className: 'versions-placeholder'
            }));
        }
    },

    /**
     * Mostra errore
     */
    showError(message) {
        const promptList = document.querySelector('.prompt-list-minimal');
        if (promptList) {
            promptList.innerHTML = '';
            promptList.appendChild(this.createErrorState({
                title: 'Errore',
                message: message
            }));
        }
    },

    // Template Helper Functions

    /**
     * Crea un loading state usando il template
     */
    createLoadingState() {
        const template = document.getElementById('loading-state-template');
        return template.content.cloneNode(true);
    },

    /**
     * Crea un empty state usando il template
     */
    createEmptyState(options) {
        const template = document.getElementById('empty-state-template');
        const clone = template.content.cloneNode(true);

        const container = clone.querySelector('.empty-state');
        if (options.className) {
            container.className = options.className;
        }

        clone.querySelector('.empty-icon').textContent = options.icon;
        clone.querySelector('.empty-title').textContent = options.title;
        clone.querySelector('.empty-message').textContent = options.message;

        return clone;
    },

    /**
     * Crea un error state usando il template
     */
    createErrorState(options) {
        const template = document.getElementById('error-state-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.error-title').textContent = options.title;
        clone.querySelector('.error-message').textContent = options.message;

        if (options.onRetry) {
            const retryBtn = clone.querySelector('.retry-btn');
            retryBtn.onclick = options.onRetry;
        }

        return clone;
    },

    /**
     * Crea una riga di metriche usando il template
     */
    createMetricsRow(summary) {
        const template = document.getElementById('metrics-row-template');
        const clone = template.content.cloneNode(true);

        const callCount = summary.call_count || 0;
        const avgTokens = Math.round(summary.avg_total_tokens || 0);
        const totalCost = (summary.total_cost || 0).toFixed(4);
        const avgLatency = Math.round(summary.avg_latency || 0);
        const avgQuality = (summary.avg_quality || 0).toFixed(2);
        const successRate = (summary.success_rate * 100 || 0).toFixed(1);

        clone.querySelector('.metric-calls .value').textContent = callCount;
        clone.querySelector('.metric-tokens .value').textContent = avgTokens;
        clone.querySelector('.metric-cost .value').textContent = totalCost;
        clone.querySelector('.metric-latency .value').textContent = avgLatency;
        clone.querySelector('.metric-quality .value').textContent = avgQuality;
        clone.querySelector('.metric-success .value').textContent = successRate;

        return clone;
    },

    /**
     * Crea un indicatore "no metrics" usando il template
     */
    createNoMetrics() {
        const template = document.getElementById('no-metrics-template');
        return template.content.cloneNode(true);
    },

    /**
     * Utilità per formattare le date
     */
    formatDate(dateString) {
        if (!dateString) {
            return 'Data non disponibile';
        }

        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                return 'Data non valida';
            }

            return date.toLocaleDateString('it-IT', {
                day: '2-digit',
                month: '2-digit',
                year: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            return 'Data non valida';
        }
    },

    /**
     * Utilità per troncare il testo
     */
    truncateText(text, maxLength) {
        if (!text || typeof text !== 'string') {
            return 'Contenuto non disponibile';
        }

        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    /**
     * Utilità per escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Debounce per la ricerca
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Carica e mostra il confronto tra modelli per una versione
     */
    async loadModelComparison(promptName, version, versionId, preloadedModelsData = null) {
        const container = document.getElementById('model-comparison-grid');

        if (!container) {
            console.error('model-comparison-grid container not found');
            return;
        }

        const loadingTemplate = document.getElementById('model-comparison-loading-template');
        container.innerHTML = '';
        container.appendChild(loadingTemplate.content.cloneNode(true));

        try {
            let data;

            // Usa i dati precaricati se disponibili
            if (preloadedModelsData) {
                data = { models: preloadedModelsData, total_models: Object.keys(preloadedModelsData).length };
            } else {
                // Altrimenti carica da API
                const url = `/api/prompts/${encodeURIComponent(promptName)}/versions/${version}/models`;
                const response = await fetch(url);

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('API Error:', response.status, errorText);
                    throw new Error(`Failed to load model comparison: ${response.status} - ${errorText}`);
                }

                data = await response.json();
            }

            if (!data.models || Object.keys(data.models).length === 0) {
                const emptyTemplate = document.getElementById('model-comparison-empty-template');
                const emptyClone = emptyTemplate.content.cloneNode(true);

                emptyClone.querySelector('.empty-icon-large').textContent = '📊';
                emptyClone.querySelector('.empty-message-primary').textContent = 'No model-specific data available yet';
                const secondaryMsg = emptyClone.querySelector('.empty-message-secondary');
                secondaryMsg.textContent = 'Start logging metrics with different models to see performance comparison';
                secondaryMsg.style.fontSize = '0.85rem';
                secondaryMsg.style.marginTop = '0.5rem';
                secondaryMsg.style.opacity = '0.8';

                container.innerHTML = '';
                container.appendChild(emptyClone);
                return;
            }

            // Ordina i modelli per numero di chiamate (più usati prima)
            const sortedModels = Object.entries(data.models)
                .sort(([, a], [, b]) => b.call_count - a.call_count);

            // Identifica i migliori modelli per ogni metrica
            const best = this.findBestModels(data.models);

            container.innerHTML = sortedModels
                .map(([modelName, stats]) => this.createModelCard(modelName, stats, best))
                .join('');

        } catch (error) {
            console.error('Error loading model comparison:', error);

            const emptyTemplate = document.getElementById('model-comparison-empty-template');
            const errorClone = emptyTemplate.content.cloneNode(true);
            const emptyDiv = errorClone.querySelector('.model-comparison-empty');

            emptyDiv.style.color = '#ef4444';
            errorClone.querySelector('.empty-icon-large').textContent = '⚠️';
            errorClone.querySelector('.empty-message-primary').textContent = 'Error loading model comparison';
            const secondaryMsg = errorClone.querySelector('.empty-message-secondary');
            secondaryMsg.textContent = error.message;
            secondaryMsg.style.fontSize = '0.85rem';
            secondaryMsg.style.marginTop = '0.5rem';

            container.innerHTML = '';
            container.appendChild(errorClone);
        }
    },

    /**
     * Identifica i modelli migliori per ogni metrica
     */
    findBestModels(models) {
        const modelList = Object.entries(models);

        if (modelList.length === 0) return {};

        const best = {
            latency: modelList.reduce(([nameA, a], [nameB, b]) =>
                (b.avg_latency && (!a.avg_latency || b.avg_latency < a.avg_latency)) ? [nameB, b] : [nameA, a]
            ),
            cost: modelList.reduce(([nameA, a], [nameB, b]) =>
                (b.avg_cost && (!a.avg_cost || b.avg_cost < a.avg_cost)) ? [nameB, b] : [nameA, a]
            ),
            quality: modelList.reduce(([nameA, a], [nameB, b]) =>
                ((b.avg_quality || 0) > (a.avg_quality || 0)) ? [nameB, b] : [nameA, a]
            ),
            success_rate: modelList.reduce(([nameA, a], [nameB, b]) =>
                (b.success_rate > a.success_rate) ? [nameB, b] : [nameA, a]
            )
        };

        return {
            latency: best.latency[0],
            cost: best.cost[0],
            quality: best.quality[0],
            success_rate: best.success_rate[0]
        };
    },

    /**
     * Crea una card per un modello usando il template HTML
     */
    createModelCard(modelName, stats, best) {
        const isBestLatency = best.latency === modelName;
        const isBestCost = best.cost === modelName;
        const isBestQuality = best.quality === modelName;
        const isBestSuccess = best.success_rate === modelName;

        // Clona il template della card
        const template = document.getElementById('model-card-template');
        const card = template.content.cloneNode(true);
        const cardElement = card.querySelector('.model-card');

        // Aggiungi classe highlight se è il migliore in qualche metrica
        if (isBestLatency || isBestCost || isBestQuality || isBestSuccess) {
            cardElement.classList.add('highlight');
        }

        // Aggiungi badge per i migliori modelli usando il template
        const badgesContainer = card.querySelector('.model-badges');
        const badgeTemplate = document.getElementById('best-badge-template');
        const badgeConfigs = [];

        if (isBestLatency) badgeConfigs.push({ icon: '⚡', text: 'Fastest' });
        if (isBestCost) badgeConfigs.push({ icon: '💰', text: 'Cheapest' });
        if (isBestQuality) badgeConfigs.push({ icon: '⭐', text: 'Best Quality' });
        if (isBestSuccess) badgeConfigs.push({ icon: '✅', text: 'Most Reliable' });

        if (badgeConfigs.length > 0) {
            badgeConfigs.forEach(config => {
                const badge = badgeTemplate.content.cloneNode(true);
                const badgeSpan = badge.querySelector('.best-badge');
                badgeSpan.textContent = `${config.icon} ${config.text}`;
                badgesContainer.appendChild(badge);
            });
        } else {
            badgesContainer.remove();
        }

        // Popola header
        card.querySelector('.model-name').textContent = `🤖 ${modelName}`;
        card.querySelector('.model-badge').textContent = `${stats.call_count} calls`;

        // Popola metriche
        if (stats.total_cost) {
            card.querySelector('.metric-total-cost .metric-value').textContent =
                `€${stats.total_cost.toFixed(4)}`;
        } else {
            card.querySelector('.metric-total-cost').remove();
        }

        if (stats.min_latency && stats.max_latency) {
            card.querySelector('.metric-latency-range .metric-value').textContent =
                `${stats.min_latency}ms - ${stats.max_latency}ms`;
            card.querySelector('.metric-latency-range .metric-value').style.fontSize = '0.85rem';
        } else {
            card.querySelector('.metric-latency-range').remove();
        }

        if (stats.avg_total_tokens) {
            card.querySelector('.metric-avg-tokens .metric-value').textContent =
                Math.round(stats.avg_total_tokens);
        } else {
            card.querySelector('.metric-avg-tokens').remove();
        }

        if (stats.avg_quality !== null) {
            card.querySelector('.metric-avg-quality .metric-value').textContent =
                `${(stats.avg_quality * 100).toFixed(1)}%`;
        } else {
            card.querySelector('.metric-avg-quality').remove();
        }

        return cardElement.outerHTML;
    }
};

// Mantengo la compatibilità con il codice esistente
const Prompts = {
    async load() {
        PromptsLayout.init();
    }
};

// Espongo le funzioni globalmente per i nuovi layout handlers
window.PromptsLayout = PromptsLayout;
