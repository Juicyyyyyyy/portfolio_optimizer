from PortfolioOptimizer.MarketDataProvider import MarketDataProvider as md
from PortfolioOptimizer.BlackLitterman import BlackLitterman

import unittest
import numpy as np


class TestBlackLitterman(unittest.TestCase):
    def setUp(self):
        # Mock data to use in tests
        self.tickers = ['AAPL', 'MSFT', 'GOOGL']
        self.start_date = '2020-01-01'
        self.end_date = '2021-01-01'
        self.data = md.get_data(tickers=self.tickers, start_date=self.start_date, end_date=self.end_date)
        self.views = [
            {'type': 'absolute', 'asset': 'AAPL', 'return': 0.2},
            {'type': 'relative', 'asset1': 'GOOGL', 'asset2': 'MSFT', 'difference': 0.04}
        ]
        self.total_portfolio_value = 1000000

        self.bl = BlackLitterman(data=self.data, tickers=self.tickers, views=self.views)

    def test_optimize_with_black_litterman(self):
        cleaned_weights, performance = self.bl.optimize_with_black_litterman()
        print(cleaned_weights)


if __name__ == '__main__':
    unittest.main()
