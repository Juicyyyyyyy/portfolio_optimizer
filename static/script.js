document.addEventListener('DOMContentLoaded', () => {
    // Set default end date to today
    document.getElementById('end-date').valueAsDate = new Date();

    const form = document.getElementById('optimizer-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');

    // Modal elements
    const modal = document.getElementById('ai-modal');
    const aiSuggestBtn = document.getElementById('ai-suggest-btn');
    const closeModal = document.querySelector('.close-modal');
    const generateTickersBtn = document.getElementById('generate-tickers-btn');
    const aiLoading = document.getElementById('ai-loading');

    let allocationChart = null;

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const tickers = document.getElementById('tickers').value.split(',').map(t => t.trim()).filter(t => t);
        if (tickers.length === 0) {
            alert('Please enter at least one ticker.');
            return;
        }

        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        const investment = parseFloat(document.getElementById('investment').value);
        const riskRate = parseFloat(document.getElementById('risk-rate').value) / 100;

        analyzeBtn.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tickers: tickers,
                    start_date: startDate,
                    end_date: endDate,
                    investment_amount: investment,
                    risk_free_rate: riskRate
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            analyzeBtn.textContent = 'Analyze Portfolio';
            analyzeBtn.disabled = false;
        }
    });

    function displayResults(data) {
        resultsSection.classList.remove('hidden');

        // Metrics
        document.getElementById('expected-return').textContent = (data.performance.expected_return * 100).toFixed(2) + '%';
        document.getElementById('volatility').textContent = (data.performance.volatility * 100).toFixed(2) + '%';
        document.getElementById('sharpe-ratio').textContent = data.performance.sharpe_ratio.toFixed(2);

        // Table
        const tbody = document.querySelector('#allocation-table tbody');
        tbody.innerHTML = '';

        // Sort by weight desc
        const sortedAllocation = Object.entries(data.weights).sort(([, a], [, b]) => b - a);

        sortedAllocation.forEach(([ticker, weight]) => {
            if (weight > 0.001) { // Only show significant weights
                const row = document.createElement('tr');
                const value = data.allocation[ticker];
                row.innerHTML = `
                    <td>${ticker}</td>
                    <td>${(weight * 100).toFixed(2)}%</td>
                    <td>$${value.toFixed(2)}</td>
                `;
                tbody.appendChild(row);
            }
        });

        // Chart
        renderChart(data.weights);

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderChart(weights) {
        const ctx = document.getElementById('allocation-chart').getContext('2d');

        if (allocationChart) {
            allocationChart.destroy();
        }

        const labels = Object.keys(weights);
        const data = Object.values(weights);

        // Filter out zero weights for cleaner chart
        const filtered = labels.map((label, i) => ({ label, value: data[i] }))
            .filter(item => item.value > 0.001);

        allocationChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: filtered.map(item => item.label),
                datasets: [{
                    data: filtered.map(item => item.value),
                    backgroundColor: [
                        '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                        '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#64748b'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { color: '#f8fafc' }
                    }
                }
            }
        });
    }

    // AI Modal Logic
    aiSuggestBtn.addEventListener('click', () => {
        modal.classList.remove('hidden');
        modal.style.display = 'flex';
    });

    closeModal.addEventListener('click', () => {
        modal.classList.add('hidden');
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
            modal.style.display = 'none';
        }
    });

    generateTickersBtn.addEventListener('click', async () => {
        const prompt = document.getElementById('ai-prompt').value;
        const count = parseInt(document.getElementById('ai-count').value);

        if (!prompt) {
            alert('Please enter a description.');
            return;
        }

        aiLoading.classList.remove('hidden');
        generateTickersBtn.disabled = true;

        try {
            const response = await fetch('/api/generate_tickers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_input: prompt,
                    number_of_tickers: count
                })
            });

            if (!response.ok) throw new Error('Generation failed');

            const data = await response.json();
            document.getElementById('tickers').value = data.tickers.join(', ');

            modal.classList.add('hidden');
            modal.style.display = 'none';
        } catch (error) {
            alert('Error generating tickers: ' + error.message);
        } finally {
            aiLoading.classList.add('hidden');
            generateTickersBtn.disabled = false;
        }
    });
});
