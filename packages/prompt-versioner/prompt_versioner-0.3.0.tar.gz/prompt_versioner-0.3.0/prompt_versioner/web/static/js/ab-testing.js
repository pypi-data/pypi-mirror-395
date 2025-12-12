/**
 * A/B Testing comparison logic
 */

const ABTesting = {
    /**
     * Toggle A/B Testing section
     */
    toggleABTesting() {
        const section = document.getElementById('ab-test-section');
        const button = document.getElementById('ab-toggle-btn');

        if (section.style.display === 'none') {
            section.style.display = 'block';
            button.textContent = '🧪 Hide A/B Testing';
            button.classList.add('active');
            this.loadPromptsForAB();
        } else {
            section.style.display = 'none';
            button.textContent = '🧪 Enable A/B Testing';
            button.classList.remove('active');
        }
    },

    /**
     * Load prompts for A/B testing (only those with 2+ versions)
     */
    async loadPromptsForAB() {
        try {
            const response = await fetch('/api/prompts');
            const data = await response.json();

            const promptSelect = document.getElementById('ab-prompt-select');
            const versionASelect = document.getElementById('ab-version-a-select');
            const versionBSelect = document.getElementById('ab-version-b-select');
            const resultsDiv = document.getElementById('ab-test-results');

            // Reset all selectors
            promptSelect.innerHTML = '<option value="">Select prompt...</option>';
            versionASelect.innerHTML = '<option value="">📊 Select Version A (baseline)...</option>';
            versionBSelect.innerHTML = '<option value="">🆚 Select Version B (comparison)...</option>';

            // Clear results
            if (resultsDiv) {
                resultsDiv.innerHTML = '';
            }

            if (data.prompts) {
                // Filter prompts that have at least 2 versions
                const promptsWithMultipleVersions = [];

                for (const prompt of data.prompts) {
                    try {
                        const versionsResponse = await fetch(`/api/prompts/${prompt.name}/versions`);
                        const versions = await versionsResponse.json();

                        if (Array.isArray(versions) && versions.length >= 2) {
                            promptsWithMultipleVersions.push(prompt);
                        }
                    } catch (error) {
                        console.warn(`Error checking versions for prompt ${prompt.name}:`, error);
                    }
                }

                // Add only prompts with multiple versions to the select
                promptsWithMultipleVersions.forEach(prompt => {
                    const option = document.createElement('option');
                    option.value = prompt.name;
                    option.textContent = prompt.name;
                    promptSelect.appendChild(option);
                });

                // Show message if no prompts have multiple versions
                if (promptsWithMultipleVersions.length === 0) {
                    const option = document.createElement('option');
                    option.value = "";
                    option.textContent = "No prompts with 2+ versions available";
                    option.disabled = true;
                    promptSelect.appendChild(option);
                }
            }
        } catch (error) {
            console.error('Error loading prompts for A/B testing:', error);
        }
    },

    /**
     * Show error message using template
     */
    showError(container, title, message) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('error-message-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.error-title').textContent = title;
        clone.querySelector('.error-text').textContent = message;

        container.appendChild(clone);
    },

    /**
     * Show loading message using template
     */
    showLoading(container, message) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('loading-message-template');
        const clone = template.content.cloneNode(true);

        clone.querySelector('.loading-text').textContent = message;

        container.appendChild(clone);
    },

    /**
     * Show A/B test results using template
     */
    showABResults(container, versionA, versionB, versionAData, versionBData, metric, metricA, metricB) {
        container.innerHTML = ''; // Clear previous content
        const template = document.getElementById('ab-results-template');
        const clone = template.content.cloneNode(true);

        // Populate version A data
        const versionACard = clone.querySelectorAll('.ab-version-result-card')[0];
        versionACard.querySelector('.ab-version-number').textContent = `v${versionA}`;
        versionACard.querySelector('.ab-metric-value').innerHTML = `${this.getMetricLabel(metric)}: <strong>${this.formatMetricValue(metricA, metric)}</strong>`;

        const modelInfoA = versionACard.querySelector('.ab-model-info');
        if (versionAData.model_name) {
            modelInfoA.textContent = `Model: ${versionAData.model_name}`;
        } else {
            modelInfoA.style.display = 'none';
        }

        // Populate version B data
        const versionBCard = clone.querySelectorAll('.ab-version-result-card')[1];
        versionBCard.querySelector('.ab-version-number').textContent = `v${versionB}`;
        versionBCard.querySelector('.ab-metric-value').innerHTML = `${this.getMetricLabel(metric)}: <strong>${this.formatMetricValue(metricB, metric)}</strong>`;

        const modelInfoB = versionBCard.querySelector('.ab-model-info');
        if (versionBData.model_name) {
            modelInfoB.textContent = `Model: ${versionBData.model_name}`;
        } else {
            modelInfoB.style.display = 'none';
        }

        // Calculate and populate summary
        const improvement = this.calculateImprovement(metricA, metricB, metric);
        const winner = improvement > 0 ? 'B' : 'A';
        const improvementText = Math.abs(improvement).toFixed(2);

        const summary = clone.querySelector('.ab-summary');
        summary.className = `ab-summary ${improvement > 0 ? 'success' : 'error'}`;

        const winnerText = clone.querySelector('.ab-winner-text');
        winnerText.className = `ab-winner-text ${improvement > 0 ? 'success' : 'error'}`;
        winnerText.textContent = `🏆 Winner: Version ${winner}`;

        const improvementTextEl = clone.querySelector('.ab-improvement-text');
        improvementTextEl.textContent = `${improvementText}% ${improvement > 0 ? 'improvement' : 'decline'} in ${this.getMetricLabel(metric).toLowerCase()}`;

        container.appendChild(clone);
    },

    /**
     * Load versions for selected prompt in A/B testing
     */
    async loadVersionsForAB() {
        const promptName = document.getElementById('ab-prompt-select').value;
        const versionASelect = document.getElementById('ab-version-a-select');
        const versionBSelect = document.getElementById('ab-version-b-select');
        const resultsDiv = document.getElementById('ab-test-results');

        // Clear version selects
        versionASelect.innerHTML = '<option value="">📊 Select Version A (baseline)...</option>';
        versionBSelect.innerHTML = '<option value="">🆚 Select Version B (comparison)...</option>';

        // Clear results
        if (resultsDiv) {
            resultsDiv.innerHTML = '';
        }

        if (!promptName) {
            return;
        }

        try {
            const response = await fetch(`/api/prompts/${promptName}/versions`);
            const versions = await response.json();

            if (Array.isArray(versions)) {
                // Sort versions by creation date (newest first)
                versions.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

                versions.forEach((version, index) => {
                    const modelDisplay = version.model_name ? ` (${version.model_name})` : '';

                    const optionA = document.createElement('option');
                    optionA.value = version.version;
                    optionA.textContent = `v${version.version}${modelDisplay}`;
                    versionASelect.appendChild(optionA);

                    const optionB = document.createElement('option');
                    optionB.value = version.version;
                    optionB.textContent = `v${version.version}${modelDisplay}`;
                    versionBSelect.appendChild(optionB);
                });

                // Auto-select the two most recent versions if available
                if (versions.length >= 2) {
                    versionASelect.value = versions[1].version; // Second most recent as baseline
                    versionBSelect.value = versions[0].version; // Most recent as comparison
                }
            }
        } catch (error) {
            console.error('Error loading versions for A/B testing:', error);
        }
    },

    /**
     * Run A/B test comparison
     */
    async runABTest() {
        const promptName = document.getElementById('ab-prompt-select').value;
        const versionA = document.getElementById('ab-version-a-select').value;
        const versionB = document.getElementById('ab-version-b-select').value;
        const metric = document.getElementById('ab-metric-select').value;
        const resultsDiv = document.getElementById('ab-test-results');

        if (!promptName || !versionA || !versionB || !metric) {
            this.showError(resultsDiv, 'Missing Selection', 'Please select prompt, both versions, and a metric');
            return;
        }

        if (versionA === versionB) {
            this.showError(resultsDiv, 'Invalid Selection', 'Please select different versions for comparison');
            return;
        }

        try {
            this.showLoading(resultsDiv, 'Loading A/B test comparison...');

            // Get metrics for both versions
            const [versionAResponse, versionBResponse] = await Promise.all([
                fetch(`/api/prompts/${promptName}/versions/${versionA}`),
                fetch(`/api/prompts/${promptName}/versions/${versionB}`)
            ]);

            const versionAData = await versionAResponse.json();
            const versionBData = await versionBResponse.json();

            // Calculate metric comparison
            const metricA = this.getMetricValue(versionAData, metric);
            const metricB = this.getMetricValue(versionBData, metric);

            const improvement = this.calculateImprovement(metricA, metricB, metric);

            // Display results using template
            this.showABResults(resultsDiv, versionA, versionB, versionAData, versionBData, metric, metricA, metricB);

        } catch (error) {
            console.error('Error running A/B test:', error);
            this.showError(resultsDiv, 'A/B Test Error', 'Error running A/B test. Please try again.');
        }
    },


    /**
     * Helper methods for A/B testing
     */
    getMetricValue(versionData, metric) {
        const summary = versionData.metrics_summary || {};
        switch (metric) {
            case 'quality_score': return summary.avg_quality || 0;
            case 'cost': return summary.total_cost || 0;
            case 'latency': return summary.avg_latency || 0;
            case 'accuracy': return summary.avg_accuracy || 0;
            default: return 0;
        }
    },


    calculateImprovement(valueA, valueB, metric) {
        if (valueA === 0) return 0;

        // For cost and latency, lower is better, so we invert the calculation
        if (metric === 'cost' || metric === 'latency') {
            return ((valueA - valueB) / valueA) * 100;
        } else {
            // For quality_score and accuracy, higher is better
            return ((valueB - valueA) / valueA) * 100;
        }
    },

    getMetricLabel(metric) {
        const labels = {
            'quality_score': 'Quality Score',
            'cost': 'Cost (EUR)',
            'latency': 'Latency (ms)',
            'accuracy': 'Accuracy'
        };
        return labels[metric] || metric;
    },

    formatMetricValue(value, metric) {
        switch (metric) {
            case 'cost': return `€${value.toFixed(4)}`;
            case 'latency': return `${value.toFixed(0)}ms`;
            case 'quality_score':
            case 'accuracy': return value.toFixed(2);
            default: return value.toString();
        }
    },

    /**
     * Create new A/B test - resets the form and loads available prompts
     */
    async createNewTest() {
        try {
            // Reset all form selections
            const promptSelect = document.getElementById('ab-prompt-select');
            const versionASelect = document.getElementById('ab-version-a-select');
            const versionBSelect = document.getElementById('ab-version-b-select');
            const metricSelect = document.getElementById('ab-metric-select');
            const resultsDiv = document.getElementById('ab-test-results');

            // Reset selectors to default values
            if (promptSelect) promptSelect.value = '';
            if (versionASelect) {
                versionASelect.innerHTML = '<option value="">📊 Select Version A (baseline)...</option>';
            }
            if (versionBSelect) {
                versionBSelect.innerHTML = '<option value="">🆚 Select Version B (comparison)...</option>';
            }
            if (metricSelect) metricSelect.value = 'quality_score'; // Default metric

            // Clear any existing results
            if (resultsDiv) {
                resultsDiv.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-content">
                            <div class="empty-icon">🧪</div>
                            <h3>New Test Created</h3>
                            <p>Select prompts and versions above to configure your A/B test</p>
                        </div>
                    </div>
                `;
            }

            // Reload prompts to ensure fresh data
            await this.loadPromptsForAB();

            // Show success feedback
            console.log('New A/B test created and form reset');

        } catch (error) {
            console.error('Error creating new A/B test:', error);

            // Show error message in results area
            const resultsDiv = document.getElementById('ab-test-results');
            if (resultsDiv) {
                resultsDiv.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-content">
                            <div class="empty-icon">❌</div>
                            <h3>Error</h3>
                            <p>Failed to create new test. Please try again.</p>
                        </div>
                    </div>
                `;
            }
        }
    },

};

// Expose globally
window.ABTesting = ABTesting;
window.toggleABTesting = () => ABTesting.toggleABTesting();
window.runABTest = () => ABTesting.runABTest();
