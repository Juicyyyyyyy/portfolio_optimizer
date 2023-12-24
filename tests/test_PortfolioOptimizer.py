import unittest
from PortfolioOptimizer.PortfolioOptimizer import PortfolioOptimizer
import numpy as np
import pandas as pd

# Mocking yfinance to avoid actual API calls during testing
import yfinance as yf
from unittest.mock import patch


class TestPortfolioOptimizer(unittest.TestCase):

    @patch('yfinance.Ticker')
    @patch('yfinance.download')
    def setUp(self, mock_download, mock_ticker):
        # Mocking yfinance responses
        mock_data = pd.DataFrame(np.random.random((50, 4)), columns=['AAPL', 'MSFT', 'GOOGL', 'AMZN'])
        mock_download.return_value = {'Adj Close': mock_data}

        # Initialize PortfolioOptimizer with test data
        tickers = "['AAPL', 'MSFT']"
        self.optimizer = PortfolioOptimizer(tickers, "2021-01-01", "2021-12-31")

    def test_validate_tickers(self):
        # Test if tickers are validated and returned correctly
        valid_tickers = self.optimizer.validate_tickers()
        self.assertIsInstance(valid_tickers, list, "Tickers should be a list")

    def test_compute_optimized_portfolio_data(self):
        # Test if compute_optimized_portfolio_data returns expected keys
        optimized_data = self.optimizer.compute_optimized_portfolio_data()
        self.assertIn("weights", optimized_data, "Optimized data should contain weights")
        self.assertIn("sharpe_ratio", optimized_data, "Optimized data should contain sharpe_ratio")
        self.assertIn("expected_annual_return", optimized_data, "Optimized data should contain expected_annual_return")

    def test_get_concrete_allocation(self):
        # Test get_concrete_allocation with sample weights
        sample_weights = {'AAPL': 0.6, 'MSFT': 0.4}  # Example weights
        allocation = self.optimizer.get_concrete_allocation(sample_weights)
        self.assertIn("concrete_allocation", allocation, "Allocation should contain concrete_allocation")
        self.assertIn("funds_remaining", allocation, "Allocation should contain funds_remaining")

    def test_compute_optimized_portfolio_via_monte_carlo(self):
        # Test compute_optimized_portfolio_via_monte_carlo returns expected keys
        monte_carlo_result = self.optimizer.compute_optimized_portfolio_via_monte_carlo()
        self.assertIn("weights", monte_carlo_result, "Result should contain weights")
        self.assertIn("expected_return", monte_carlo_result, "Result should contain expected_return")
        self.assertIn("expected_volatility", monte_carlo_result, "Result should contain expected_volatility")
        self.assertIn("sharpe_ratio", monte_carlo_result, "Result should contain sharpe_ratio")

    def test_set_black_litterman_views(self):
        # Simplistic test for set_black_litterman_views
        P = np.array([[1]])  # Simplistic view matrix
        Q = np.array([0.05])  # Simplistic returns vector
        self.optimizer.set_black_litterman_views(P, Q)
        self.assertIsNotNone(self.optimizer.P, "P should be set")
        self.assertIsNotNone(self.optimizer.Q, "Q should be set")

    def test_user_input_to_pq(self):
        # Simplistic test for user_input_to_pq
        views = [
            {'type': 'absolute', 'asset': 'AAPL', 'return': 0.05},
            {'type': 'relative', 'asset1': 'AAPL', 'asset2': 'MSFT', 'difference': 0.02}
        ]
        P, Q = self.optimizer.user_input_to_pq(views)
        self.assertEqual(P.shape[0], len(views), "P matrix rows should match number of views")
        self.assertEqual(Q.shape[0], len(views), "Q matrix rows should match number of views")

    def test_calculate_beta(self):
        # Simplistic test for calculate_beta
        betas = self.optimizer.calculate_beta('^GSPC')
        self.assertIsInstance(betas, dict, "Betas should be returned as a dictionary")
        self.assertTrue(all(isinstance(beta, (float, int)) for beta in betas.values()), "Beta values should be numeric")

    def test_get_risk_free_rate(self):
        risk_free_rate = self.optimizer.get_risk_free_rate()
        self.assertTrue(risk_free_rate, "risk_free_rate should not be empty")
        print(risk_free_rate)

    def test_get_market_return(self):
        market_return = self.optimizer.get_market_return()
        self.assertTrue(market_return, "risk_free_rate should not be empty")
        print(market_return)

    def test_calculate_equilibrium_expected_returns_CAPM(self):
        pi = self.optimizer.calculate_equilibrium_expected_returns_CAPM()
        print(pi)

    def tearDown(self):
        # Clean up any code or data after the tests are finished
        pass


if __name__ == '__main__':
    unittest.main()
