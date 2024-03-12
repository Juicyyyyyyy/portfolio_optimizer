from PortfolioOptimizer.MarketDataProvider import MarketDataProvider as md
from PortfolioOptimizer.BlackLitterman import BlackLitterman

import unittest


class TestBlackLitterman(unittest.TestCase):
    def setUp(self):
        # Mock data to use in tests
        self.tickers = ['AAPL', 'GOOGL']
        self.start_date = '2014-01-20'
        self.end_date = '2024-01-18'
        self.data = md.get_data(tickers=self.tickers, start_date=self.start_date, end_date=self.end_date)
        self.views = [
            {'type': 'absolute', 'asset': 'AAPL', 'return': 10},
            {'type': 'absolute', 'asset': 'GOOGL', 'return': 11}
        ]
        self.total_portfolio_value = 1000000

        self.bl = BlackLitterman(data=self.data, tickers=self.tickers, views=self.views)

    def test_optimize_with_black_litterman(self):
        cleaned_weights, performance = self.bl.optimize_with_black_litterman()
        print(cleaned_weights, performance)


if __name__ == '__main__':
    unittest.main()
