document.addEventListener('DOMContentLoaded', () => {
    // Set default end date to today
    document.getElementById('end-date').valueAsDate = new Date();

    const form = document.getElementById('optimizer-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');



    let allocationChart = null;
    let simulationChart = null;
    let views = [];

    // Elements for Views
    const strategySelect = document.getElementById('strategy');
    const blViewsSection = document.getElementById('bl-views-section');
    const viewTypeSelect = document.getElementById('view-type');
    const absoluteInputs = document.getElementById('absolute-inputs');
    const relativeInputs = document.getElementById('relative-inputs');
    const addViewBtn = document.getElementById('add-view-btn');
    const viewsList = document.getElementById('views-list');
    const tickerInputs = document.getElementById('tickers');

    // Toggle Views Section
    strategySelect.addEventListener('change', () => {
        if (strategySelect.value === 'black_litterman') {
            blViewsSection.classList.remove('hidden');
            updateTickerDropdowns();
        } else {
            blViewsSection.classList.add('hidden');
        }
    });

    // Toggle View Type Inputs
    viewTypeSelect.addEventListener('change', () => {
        if (viewTypeSelect.value === 'absolute') {
            absoluteInputs.classList.remove('hidden');
            relativeInputs.classList.add('hidden');
        } else {
            absoluteInputs.classList.add('hidden');
            relativeInputs.classList.remove('hidden');
        }
    });

    // Update Dropdowns when tickers change
    tickerInputs.addEventListener('change', updateTickerDropdowns);

    function updateTickerDropdowns() {
        const tickers = tickerInputs.value.split(',').map(t => t.trim()).filter(t => t);
        const selects = document.querySelectorAll('.ticker-select');

        selects.forEach(select => {
            const currentVal = select.value;
            select.innerHTML = '<option value="">Select Asset</option>';
            tickers.forEach(ticker => {
                const option = document.createElement('option');
                option.value = ticker;
                option.textContent = ticker;
                select.appendChild(option);
            });
            select.value = currentVal; // Try to restore selection
        });
    }

    // Add View Logic
    addViewBtn.addEventListener('click', () => {
        const type = viewTypeSelect.value;
        let view = {};

        if (type === 'absolute') {
            const asset = document.getElementById('abs-asset').value;
            const ret = parseFloat(document.getElementById('abs-return').value);
            if (!asset || isNaN(ret)) return alert('Please fill all fields');

            view = { type: 'absolute', asset: asset, return: ret / 100 };
            views.push(view);
            renderViews();
        } else {
            const asset1 = document.getElementById('rel-asset1').value;
            const asset2 = document.getElementById('rel-asset2').value;
            const diff = parseFloat(document.getElementById('rel-diff').value);
            if (!asset1 || !asset2 || isNaN(diff)) return alert('Please fill all fields');

            view = { type: 'relative', asset1: asset1, asset2: asset2, difference: diff / 100 };
            views.push(view);
            renderViews();
        }
    });

    function renderViews() {
        viewsList.innerHTML = '';
        views.forEach((view, index) => {
            const li = document.createElement('li');
            if (view.type === 'absolute') {
                li.textContent = `${view.asset} returns ${(view.return * 100).toFixed(1)}%`;
            } else {
                li.textContent = `${view.asset1} beats ${view.asset2} by ${(view.difference * 100).toFixed(1)}%`;
            }

            const delBtn = document.createElement('button');
            delBtn.textContent = 'x';
            delBtn.className = 'delete-view-btn';
            delBtn.onclick = () => {
                views.splice(index, 1);
                renderViews();
            };

            li.appendChild(delBtn);
            viewsList.appendChild(li);
        });
    }

    // Constraints Logic
    const constraintsContainer = document.getElementById('constraints-container');
    const addConstraintBtn = document.getElementById('add-constraint-btn');

    addConstraintBtn.addEventListener('click', () => {
        const constraintDiv = document.createElement('div');
        constraintDiv.className = 'input-wrapper mb-2'; // Use input-wrapper for flex layout
        constraintDiv.style.marginBottom = '0.5rem'; // Add spacing
        constraintDiv.innerHTML = `
            <input type="text" class="constraint-ticker" placeholder="Ticker (e.g., GLD)" style="flex: 1;">
            <input type="number" class="constraint-weight" placeholder="Max % (0.15)" step="0.01" min="0" max="1" style="flex: 1;">
            <button type="button" class="remove-constraint-btn" style="background: #ef4444; color: white; border: none; padding: 0 1rem; border-radius: 0.5rem; cursor: pointer;">X</button>
        `;
        constraintsContainer.appendChild(constraintDiv);

        constraintDiv.querySelector('.remove-constraint-btn').addEventListener('click', () => {
            constraintsContainer.removeChild(constraintDiv);
        });
    });

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
        const strategy = document.getElementById('strategy').value;

        // Collect Constraints
        const constraints = {};
        document.querySelectorAll('#constraints-container .input-wrapper').forEach(div => {
            const ticker = div.querySelector('.constraint-ticker').value.trim();
            const weight = parseFloat(div.querySelector('.constraint-weight').value);
            if (ticker && !isNaN(weight)) {
                constraints[ticker] = weight;
            }
        });

        analyzeBtn.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        try {
            // 1. Analyze Portfolio
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tickers: tickers,
                    start_date: startDate,
                    end_date: endDate,
                    investment_amount: investment,
                    risk_free_rate: riskRate,
                    strategy: strategy,
                    views: strategy === 'black_litterman' ? views : [],
                    constraints: Object.keys(constraints).length > 0 ? constraints : null
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Analysis failed');
            }

            const data = await response.json();
            displayResults(data);

            // 2. Run Simulation (Monte Carlo)
            // Use valid_tickers from analysis response to ensure consistency
            console.log("Starting simulation with:", data.valid_tickers);
            await runSimulation(data.valid_tickers, data.weights, startDate, endDate, investment);

        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            analyzeBtn.textContent = 'Analyze Portfolio';
            analyzeBtn.disabled = false;
        }
    });

    // ... (rest of the file: runSimulation, displayResults, renderChart, renderSimulationChart, AI Modal Logic)

    async function runSimulation(tickers, weights, startDate, endDate, initialValue) {
        try {
            if (!tickers || tickers.length === 0) {
                alert("No valid tickers for simulation");
                return;
            }

            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tickers: tickers,
                    weights: weights,
                    start_date: startDate,
                    end_date: endDate,
                    initial_portfolio_value: initialValue
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Simulation failed');
            }

            const simulationData = await response.json();
            renderSimulationChart(simulationData);
        } catch (error) {
            console.error("Simulation error:", error);
            alert("Simulation failed: " + error.message);
        }
    }

    function displayResults(data) {
        resultsSection.classList.remove('hidden');

        // Metrics
        document.getElementById('expected-return').textContent = (data.performance.expected_return * 100).toFixed(2) + '%';
        document.getElementById('volatility').textContent = (data.performance.volatility * 100).toFixed(2) + '%';
        document.getElementById('sharpe-ratio').textContent = data.performance.sharpe_ratio.toFixed(2);
        document.getElementById('sortino-ratio').textContent = data.performance.sortino_ratio ? data.performance.sortino_ratio.toFixed(2) : 'N/A';
        document.getElementById('var-95').textContent = data.performance.var_95 ? (data.performance.var_95 * 100).toFixed(2) + '%' : 'N/A';
        document.getElementById('cvar-95').textContent = data.performance.cvar_95 ? (data.performance.cvar_95 * 100).toFixed(2) + '%' : 'N/A';

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

    function renderSimulationChart(data) {
        const ctx = document.getElementById('simulation-chart').getContext('2d');

        if (simulationChart) {
            simulationChart.destroy();
        }

        simulationChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.days,
                datasets: [
                    {
                        label: '90th Percentile (Lucky)',
                        data: data.p90,
                        borderColor: '#10b981', // Green
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: false,
                        tension: 0.1,
                        pointRadius: 0
                    },
                    {
                        label: 'Median (Expected)',
                        data: data.p50,
                        borderColor: '#6366f1', // Blue
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: false,
                        tension: 0.1,
                        pointRadius: 0
                    },
                    {
                        label: '10th Percentile (Unlucky)',
                        data: data.p10,
                        borderColor: '#ef4444', // Red
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: false,
                        tension: 0.1,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#f8fafc' }
                    },
                    title: {
                        display: true,
                        text: `Projected Value: $${data.final_mean.toFixed(0)} (Range: $${data.final_min.toFixed(0)} - $${data.final_max.toFixed(0)})`,
                        color: '#94a3b8'
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Trading Days', color: '#94a3b8' },
                        ticks: { color: '#94a3b8' },
                        grid: { color: '#334155' }
                    },
                    y: {
                        title: { display: true, text: 'Portfolio Value ($)', color: '#94a3b8' },
                        ticks: { color: '#94a3b8' },
                        grid: { color: '#334155' }
                    }
                }
            }
        });
    }


});
