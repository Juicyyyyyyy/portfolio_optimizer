import unittest
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider
import pandas as pd


class TestMarketDataProvider(unittest.TestCase):

    def test_single_ticker_data_fetch(self):
        """Test data fetching for a single ticker."""
        ticker = 'AAPL'
        start_date = '2021-01-01'
        end_date = '2021-02-01'
        data = MarketDataProvider.get_data(ticker, start_date, end_date)

        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        self.assertIn(ticker, data.columns)

    def test_multiple_tickers_data_fetch(self):
        """Test data fetching for multiple tickers."""
        tickers = ['AAPL', 'MSFT']
        start_date = '2021-01-01'
        end_date = '2021-02-01'
        data = MarketDataProvider.get_data(tickers, start_date, end_date)
        first_date = data.index[0]
        last_date = data.index[-1]
        print(first_date, last_date)

        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        for ticker in tickers:
            self.assertIn(ticker, data.columns)

if __name__ == '__main__':
    unittest.main()
