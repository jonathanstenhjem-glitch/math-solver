/**
 * Solution Renderer
 * Renders solution data to HTML
 */

class SolutionRenderer {
    static renderSolution(data) {
        const sectionEl = document.getElementById('solution-section');
        
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
    }

    static renderSteps(steps) {
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
                html += `<div class="step-title">${step.description}</div>`;
            }

            if (step.calculation) {
                html += `<div class="step-calculation">${this.escapeHtml(step.calculation)}</div>`;
            }

            if (step.result) {
                html += `<div class="step-result">= ${this.escapeHtml(step.result)}</div>`;
            }

            if (step.explanation) {
                html += `<div style="margin-top: 0.5rem; color: #64748b;">${step.explanation}</div>`;
            }

            html += `
                    </div>
                </div>
            `;

            stepEl.innerHTML = html;
            container.appendChild(stepEl);
        });
    }

    static renderFinalAnswer(answer) {
        const answerBox = document.getElementById('answer-box');
        const finalAnswerEl = document.getElementById('final-answer');
        
        finalAnswerEl.textContent = answer;
        answerBox.style.display = 'block';
    }

    static renderFormulasUsed(formulas) {
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

    static renderValidation(validation) {
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

    static renderNote(note) {
        const noteBox = document.getElementById('note-box');
        const noteText = document.getElementById('note-text');
        
        noteText.textContent = note;
        noteBox.style.display = 'block';
    }

    static renderFormulas(formulas) {
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

    static escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    static clearSolution() {
        document.getElementById('solution-section').style.display = 'none';
        document.getElementById('steps-container').innerHTML = '';
        document.getElementById('problem-type-box').style.display = 'none';
        document.getElementById('answer-box').style.display = 'none';
        document.getElementById('formulas-box').style.display = 'none';
        document.getElementById('validation-box').style.display = 'none';
        document.getElementById('note-box').style.display = 'none';
    }

    static showError(message) {
        const errorEl = document.getElementById('error-message');
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }

    static clearError() {
        const errorEl = document.getElementById('error-message');
        errorEl.style.display = 'none';
    }

    static showLoading() {
        document.getElementById('loading').style.display = 'flex';
    }

    static hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }
}

export default SolutionRenderer;
