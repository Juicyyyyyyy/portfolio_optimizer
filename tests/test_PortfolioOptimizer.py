# test_portfolio_optimizer.py
import pytest
from PortfolioOptimizer.PortfolioOptimizer import PortfolioOptimizer

# Sample data for tests
tickers = ['AAPL', 'TSLA', 'BTC']
start_date = "2021-01-01"
end_date = "2022-01-01"
total_portfolio_value = 10000

@pytest.fixture
def optimizer():
    """Fixture to create a PortfolioOptimizer object for testing"""
    return PortfolioOptimizer(tickers, start_date, end_date, total_portfolio_value)

def test_init(optimizer):
    """Test the initialization and attributes of PortfolioOptimizer"""
    assert optimizer.tickers is not None
    assert optimizer.start_date == start_date
    assert optimizer.end_date == end_date
    assert optimizer.total_portfolio_value == total_portfolio_value

def test_compute_optimized_portfolio_data(optimizer):
    """Test the portfolio computation method"""
    data = optimizer.compute_optimized_portfolio_data()
    assert "weights" in data
    assert "sharpe_ratio" in data
    assert "expected_annual_return" in data
    print(data)

def test_get_concrete_allocation(optimizer):
    """Test concrete allocation calculation"""
    # Example: Assuming the method requires weights as input
    weights = {'AAPL': 0.5, 'TSLA': 0.3, 'BTC': 0.2}  # Example weights
    allocation = optimizer.get_concrete_allocation(weights)
    assert "concrete_allocation" in allocation
    assert "funds_remaining" in allocation
    # Add more assertions to validate the allocation details

def test_compute_optimized_portfolio_via_monte_carlo(optimizer):
    """Test the Monte Carlo optimization method"""
    results = optimizer.compute_optimized_portfolio_via_monte_carlo()
    assert "weights" in results
    assert "expected_return" in results
    assert "expected_volatility" in results
    assert "sharpe_ratio" in results
    print(results)

if __name__ == "__main__":
    pytest.main()
