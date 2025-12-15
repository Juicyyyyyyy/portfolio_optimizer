import pytest
import pandas as pd
import numpy as np
from PortfolioOptimizer.MonteCarloSimulator import MonteCarloSimulator

@pytest.fixture
def mock_simulation_inputs():
    mu = pd.Series([0.1, 0.15], index=["A", "B"])
    S = pd.DataFrame([[0.04, 0.01], [0.01, 0.09]], index=["A", "B"], columns=["A", "B"])
    weights = {"A": 0.6, "B": 0.4}
    initial_value = 10000
    return mu, S, weights, initial_value

def test_monte_carlo_simulate(mock_simulation_inputs):
    mu, S, weights, initial_value = mock_simulation_inputs
    simulator = MonteCarloSimulator(mu, S, weights, initial_value)
    
    results = simulator.simulate(num_simulations=100, time_horizon=50)
    
    assert isinstance(results, dict)
    assert "days" in results
    assert "p10" in results
    assert "p50" in results
    assert "p90" in results
    assert len(results["days"]) == 50 # 0 to 49
    assert len(results["p50"]) == 50
    assert results["p50"][0] == initial_value
