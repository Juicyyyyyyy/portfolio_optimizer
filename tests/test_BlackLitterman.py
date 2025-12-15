import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from PortfolioOptimizer.BlackLitterman import BlackLitterman

class TestBlackLitterman(unittest.TestCase):
    def setUp(self):
        self.tickers = ['AAPL', 'GOOGL']
        dates = pd.date_range(start="2023-01-01", periods=50)
        self.data = pd.DataFrame({
            "AAPL": np.random.normal(100, 1, 50),
            "GOOGL": np.random.normal(100, 1, 50)
        }, index=dates)
        
        self.views = [
            {'type': 'absolute', 'asset': 'AAPL', 'return': 0.10},
            {'type': 'absolute', 'asset': 'GOOGL', 'return': 0.11}
        ]

    @patch("PortfolioOptimizer.BlackLitterman.CapmCalculator")
    def test_optimize_with_black_litterman(self, MockCapm):
        # Mock CAPM prior
        MockCapm.return_value.calculate_expected_return.return_value = pd.Series([0.05, 0.06], index=self.tickers)
        
        bl = BlackLitterman(data=self.data, tickers=self.tickers, views=self.views)
        cleaned_weights, exp_ret, vol, sharpe = bl.optimize_with_black_litterman()
        
        self.assertIsInstance(cleaned_weights, dict)
        self.assertAlmostEqual(sum(cleaned_weights.values()), 1.0, places=4)
        self.assertIsInstance(exp_ret, float)

if __name__ == '__main__':
    unittest.main()
