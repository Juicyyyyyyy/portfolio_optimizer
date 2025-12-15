import pytest
import pandas as pd
import numpy as np
from PortfolioOptimizer.HRPCalculator import HRPCalculator

@pytest.fixture
def mock_price_data():
    dates = pd.date_range(start="2023-01-01", periods=100)
    data = {
        "A": np.random.normal(100, 1, 100),
        "B": np.random.normal(50, 0.5, 100),
        "C": np.random.normal(20, 0.2, 100)
    }
    return pd.DataFrame(data, index=dates)

def test_hrp_calculate_weights(mock_price_data):
    hrp = HRPCalculator(mock_price_data)
    weights = hrp.calculate_weights()
    
    assert isinstance(weights, dict)
    assert len(weights) == 3
    assert "A" in weights
    assert sum(weights.values()) == pytest.approx(1.0, rel=1e-4)

def test_hrp_calculate_performance(mock_price_data):
    hrp = HRPCalculator(mock_price_data)
    hrp.calculate_weights()
    exp_ret, vol, sharpe = hrp.calculate_performance(risk_free_rate=0.02)
    
    assert isinstance(exp_ret, float)
    assert isinstance(vol, float)
    assert isinstance(sharpe, float)
