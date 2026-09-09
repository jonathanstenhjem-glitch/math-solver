/**
 * Main Application Logic
 */

// Use global scope since we're not using ES6 modules in the browser
const API_BASE_URL = 'http://localhost:5000';

class SolverApp {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.checkBackendHealth();
        this.loadFormulas();
    }

    initializeElements() {
        this.problemInput = document.getElementById('problem');
        this.contextInput = document.getElementById('context');
        this.solveBtn = document.getElementById('solve-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.errorMessage = document.getElementById('error-message');
        this.loading = document.getElementById('loading');
        this.solutionSection = document.getElementById('solution-section');
        this.closeSolutionBtn = document.getElementById('close-solution');
        this.categorySelect = document.getElementById('category-select');
        this.topicSelect = document.getElementById('topic-select');
        this.loadFormulasBtn = document.getElementById('load-formulas-btn');
    }

    attachEventListeners() {
        this.solveBtn.addEventListener('click', () => this.handleSolve());
        this.clearBtn.addEventListener('click', () => this.handleClear());
        this.closeSolutionBtn.addEventListener('click', () => this.closeSolution());
        this.loadFormulasBtn.addEventListener('click', () => this.handleLoadFormulas());
        this.categorySelect.addEventListener('change', () => this.updateTopicSelect());
        
        // Allow Enter key to solve
        this.problemInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.handleSolve();
            }
        });
    }

    async checkBackendHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            if (!response.ok) {
                this.showError('Backend er ikke tilgjengelig. Kontroller at serveren kjører.');
            }
        } catch (error) {
            this.showError('Kunne ikke koble til backend. Kontroller at serveren kjører på http://localhost:5000');
        }
    }

    async handleSolve() {
        const problem = this.problemInput.value.trim();
        const context = this.contextInput.value.trim();

        if (!problem) {
            this.showError('Skriv inn en matteoppgave først.');
            return;
        }

        this.clearError();
        this.showLoading();

        try {
            const response = await fetch(`${API_BASE_URL}/solve`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    problem,
                    context
                })
            });

            const data = await response.json();

            if (!data.success) {
                this.showError(data.error || 'Feil ved løsning av oppgaven.');
                return;
            }

            this.renderSolution(data);
        } catch (error) {
            console.error('Error:', error);
            this.showError(`Feil: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    renderSolution(data) {
        const sectionEl = this.solutionSection;

        // Show problem type
        if (data.problem_type) {
            const problemTypeBox = document.getElementById('problem-type-box');
            document.getElementById('problem-type').textContent = data.problem_type;
            problemTypeBox.style.display = 'block';
        }

        // Render steps
        if (data.solution && data.solution.steps) {
            this.renderSteps(data.solution.steps);
        }

        // Render final answer
        if (data.solution && data.solution.final_answer) {
            this.renderFinalAnswer(data.solution.final_answer);
        }

        // Render formulas used
        if (data.solution && data.solution.formulas_used && data.solution.formulas_used.length > 0) {
            this.renderFormulasUsed(data.solution.formulas_used);
        }

        // Render validation
        if (data.validation) {
            this.renderValidation(data.validation);
        }

        // Render note if present
        if (data.solution && data.solution.note) {
            this.renderNote(data.solution.note);
        }

        sectionEl.style.display = 'block';
        sectionEl.scrollIntoView({ behavior: 'smooth' });
    }

    renderSteps(steps) {
        const container = document.getElementById('steps-container');
        container.innerHTML = '';

        steps.forEach((step, index) => {
            const stepEl = document.createElement('div');
            stepEl.className = 'step';

            let html = `
                <div style="display: flex; align-items: flex-start; gap: 1rem;">
                    <span class="step-number">${step.step || index + 1}</span>
                    <div style="flex: 1;">
            `;

            if (step.description) {
                html += `<div class="step-title">${this.escapeHtml(step.description)}</div>`;
            }

            if (step.calculation) {
                html += `<div class="step-calculation">${this.escapeHtml(step.calculation)}</div>`;
            }

            if (step.result) {
                html += `<div class="step-result">= ${this.escapeHtml(step.result)}</div>`;
            }

            if (step.explanation) {
                html += `<div style="margin-top: 0.5rem; color: #64748b;">${this.escapeHtml(step.explanation)}</div>`;
            }

            html += `
                    </div>
                </div>
            `;

            stepEl.innerHTML = html;
            container.appendChild(stepEl);
        });
    }

    renderFinalAnswer(answer) {
        const answerBox = document.getElementById('answer-box');
        const finalAnswerEl = document.getElementById('final-answer');

        finalAnswerEl.textContent = answer;
        answerBox.style.display = 'block';
    }

    renderFormulasUsed(formulas) {
        const formulasBox = document.getElementById('formulas-box');
        const formulasList = document.getElementById('formulas-list');

        formulasList.innerHTML = '';

        formulas.forEach(formula => {
            const li = document.createElement('li');

            let html = `
                <span class="formula-id">${formula.formula_id || 'N/A'}</span>
                <span class="formula-name">${formula.description || 'Formula'}</span>
            `;

            if (formula.step) {
                html += `<span style="color: #64748b; font-size: 0.9rem;"> (Step ${formula.step})</span>`;
            }

            li.innerHTML = html;
            formulasList.appendChild(li);
        });

        formulasBox.style.display = 'block';
    }

    renderValidation(validation) {
        const validationBox = document.getElementById('validation-box');
        const validationResult = document.getElementById('validation-result');

        validationResult.innerHTML = '';

        // Show overall result
        const resultDiv = document.createElement('div');
        resultDiv.style.marginBottom = '1rem';
        resultDiv.style.fontWeight = '600';
        resultDiv.style.color = validation.valid ? '#10b981' : '#ef4444';
        resultDiv.textContent = validation.result || (validation.valid ? 'Valid' : 'Invalid');
        validationResult.appendChild(resultDiv);

        // Show checks if available
        if (validation.checks && validation.checks.length > 0) {
            const checksDiv = document.createElement('div');
            checksDiv.innerHTML = '<strong style="display: block; margin-bottom: 0.5rem;">Valideringskontroller:</strong>';

            validation.checks.forEach(check => {
                const checkDiv = document.createElement('div');
                checkDiv.className = `validation-check ${check.passed ? 'check-passed' : 'check-failed'}`;

                const icon = check.passed ? '✓' : '✗';
                checkDiv.innerHTML = `
                    <span class="check-icon">${icon}</span>
                    <span>
                        <strong>${check.name}</strong>
                        ${check.detail ? `: ${check.detail}` : ''}
                    </span>
                `;

                checksDiv.appendChild(checkDiv);
            });

            validationResult.appendChild(checksDiv);
        }

        validationBox.style.display = 'block';
    }

    renderNote(note) {
        const noteBox = document.getElementById('note-box');
        const noteText = document.getElementById('note-text');

        noteText.textContent = note;
        noteBox.style.display = 'block';
    }

    handleClear() {
        this.problemInput.value = '';
        this.contextInput.value = '';
        this.closeSolution();
        this.clearError();
    }

    closeSolution() {
        this.solutionSection.style.display = 'none';
    }

    async handleLoadFormulas() {
        const category = this.categorySelect.value || null;
        const topic = this.topicSelect.value || null;

        this.showLoading();

        try {
            let url = `${API_BASE_URL}/formulas`;
            const params = new URLSearchParams();

            if (category) params.append('category', category);
            if (topic) params.append('topic', topic);

            if (params.toString()) {
                url += `?${params.toString()}`;
            }

            const response = await fetch(url);
            const data = await response.json();

            if (!data.success) {
                this.showError(data.error || 'Feil ved henting av formler.');
                return;
            }

            this.renderFormulas(data.formulas);
        } catch (error) {
            console.error('Error loading formulas:', error);
            this.showError(`Feil: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    async loadFormulas() {
        try {
            const response = await fetch(`${API_BASE_URL}/formulas`);
            const data = await response.json();

            if (data.success) {
                this.renderFormulas(data.formulas);
            }
        } catch (error) {
            console.error('Error loading formulas:', error);
        }
    }

    async updateTopicSelect() {
        const category = this.categorySelect.value;
        this.topicSelect.innerHTML = '<option value="">Alle emner</option>';

        if (!category) return;

        try {
            const response = await fetch(`${API_BASE_URL}/formulas?category=${category}`);
            const data = await response.json();

            if (data.success) {
                const topics = new Set();
                data.formulas.forEach(f => {
                    if (f.topic) topics.add(f.topic);
                });

                topics.forEach(topic => {
                    const option = document.createElement('option');
                    option.value = topic;
                    option.textContent = this.formatTopicName(topic);
                    this.topicSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error updating topics:', error);
        }
    }

    renderFormulas(formulas) {
        const container = document.getElementById('formulas-display');
        container.innerHTML = '';

        if (!formulas || formulas.length === 0) {
            container.innerHTML = '<p style="color: #64748b;">Ingen formler funnet.</p>';
            return;
        }

        formulas.forEach(formula => {
            const formulaEl = document.createElement('div');
            formulaEl.className = 'formula-item';

            let html = `
                <div class="formula-item-header">
                    <span class="formula-item-title">${formula.name || 'Formula'}</span>
                    <span class="formula-id">${formula.id || 'N/A'}</span>
                </div>
            `;

            if (formula.formula) {
                html += `<div class="formula-code">${this.escapeHtml(formula.formula)}</div>`;
            }

            if (formula.description) {
                html += `<div style="font-size: 0.95rem; color: #64748b;">${formula.description}</div>`;
            }

            if (formula.conditions) {
                html += `<div class="formula-conditions"><strong>Forutsetninger:</strong> ${formula.conditions}</div>`;
            }

            if (formula.reference) {
                html += `<div class="formula-conditions"><strong>Referanse:</strong> ${formula.reference}</div>`;
            }

            if (formula.examples && formula.examples.length > 0) {
                html += `<div class="formula-conditions"><strong>Eksempel:</strong> ${formula.examples[0]}</div>`;
            }

            formulaEl.innerHTML = html;
            container.appendChild(formulaEl);
        });
    }

    formatTopicName(topic) {
        return topic.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.style.display = 'block';
    }

    clearError() {
        this.errorMessage.style.display = 'none';
    }

    showLoading() {
        this.loading.style.display = 'flex';
    }

    hideLoading() {
        this.loading.style.display = 'none';
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new SolverApp();
});
