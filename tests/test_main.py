import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import pandas as pd
from main import app

client = TestClient(app)

@pytest.fixture
def mock_market_data():
    with patch("main.MarketDataProvider") as MockProvider, \
         patch("main.EfficientFrontierCalculator") as MockEF, \
         patch("main.BlackLitterman") as MockBL:
        
        # Mock Market Data
        instance = MockProvider.return_value
        df = pd.DataFrame({
            "AAPL": [100, 101, 102],
            "MSFT": [200, 202, 204]
        }, index=pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]))
        
        # Configure get_data to return different values based on arguments
        def get_data_side_effect(*args, **kwargs):
            if kwargs.get("return_updated_tickers"):
                return (df, ["AAPL", "MSFT"])
            return df
        
        instance.get_data.side_effect = get_data_side_effect
        
        # Mock Efficient Frontier
        ef_instance = MockEF.return_value
        ef_instance.calculate_efficient_frontier_weights.return_value = {"AAPL": 0.6, "MSFT": 0.4}
        ef_instance.calculate_efficient_frontier_performance.return_value = (0.1, 0.2, 1.5)

        # Mock Black Litterman
        bl_instance = MockBL.return_value
        bl_instance.optimize_with_black_litterman.return_value = ({"AAPL": 0.5, "MSFT": 0.5}, 0.1, 0.15, 1.2)
        
        yield instance

def test_analyze_max_sharpe(mock_market_data):
    response = client.post("/api/analyze", json={
        "tickers": ["AAPL", "MSFT"],
        "start_date": "2023-01-01",
        "end_date": "2023-01-03",
        "strategy": "max_sharpe"
    })
    assert response.status_code == 200
    data = response.json()
    assert "weights" in data
    assert "performance" in data

def test_analyze_hrp(mock_market_data):
    response = client.post("/api/analyze", json={
        "tickers": ["AAPL", "MSFT"],
        "start_date": "2023-01-01",
        "end_date": "2023-01-03",
        "strategy": "hrp"
    })
    assert response.status_code == 200
    data = response.json()
    assert "weights" in data

def test_analyze_black_litterman(mock_market_data):
    response = client.post("/api/analyze", json={
        "tickers": ["AAPL", "MSFT"],
        "start_date": "2023-01-01",
        "end_date": "2023-01-03",
        "strategy": "black_litterman",
        "views": [{"type": "absolute", "asset": "AAPL", "return": 0.1}]
    })
    assert response.status_code == 200
    data = response.json()
    assert "weights" in data

def test_simulate(mock_market_data):
    # Mocking MeanHistoricalReturnCalculator and SampleCovarianceCalculator inside main
    with patch("main.MeanHistoricalReturnCalculator") as MockMean, \
         patch("main.SampleCovarianceCalculator") as MockCov:
        
        MockMean.return_value.calculate_expected_return.return_value = pd.Series([0.1, 0.1], index=["AAPL", "MSFT"])
        MockCov.return_value.calculate_covariance.return_value = pd.DataFrame([[0.04, 0], [0, 0.04]], index=["AAPL", "MSFT"], columns=["AAPL", "MSFT"])

        response = client.post("/api/simulate", json={
            "tickers": ["AAPL", "MSFT"],
            "weights": {"AAPL": 0.5, "MSFT": 0.5},
            "start_date": "2023-01-01",
            "end_date": "2023-01-03"
        })
        assert response.status_code == 200
        data = response.json()
        assert "p50" in data
