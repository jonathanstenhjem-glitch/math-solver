/**
 * Solver API Client
 * Handles communication with backend
 */

const API_BASE_URL = 'http://localhost:5000';

class SolverAPI {
    static async solve(problem, context = '') {
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

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Solver API error:', error);
            throw error;
        }
    }

    static async getFormulas(category = null, topic = null) {
        try {
            let url = `${API_BASE_URL}/formulas`;
            const params = new URLSearchParams();

            if (category) params.append('category', category);
            if (topic) params.append('topic', topic);

            if (params.toString()) {
                url += `?${params.toString()}`;
            }

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Formulas API error:', error);
            throw error;
        }
    }

    static async getFormula(formulaId) {
        try {
            const response = await fetch(`${API_BASE_URL}/formulas/${formulaId}`);

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Formula API error:', error);
            throw error;
        }
    }

    static async getHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            return response.ok;
        } catch (error) {
            console.error('Health check error:', error);
            return false;
        }
    }
}

export default SolverAPI;
