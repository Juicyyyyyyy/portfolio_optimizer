import unittest
from unittest.mock import patch
import pandas as pd
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider

class TestMarketDataProvider(unittest.TestCase):
    @patch("PortfolioOptimizer.MarketDataProvider.yf.download")
    def test_get_data(self, mock_download):
        # Mock yfinance response
        mock_df = pd.DataFrame({
            "Adj Close": {
                ("2023-01-01", "AAPL"): 150.0,
                ("2023-01-02", "AAPL"): 152.0
            }
        })
        # yfinance returns a multi-index columns dataframe usually if grouped, 
        # but here we mock the structure we expect or just the 'Adj Close' access
        # MarketDataProvider expects yf.download to return a DF where we access ['Adj Close']
        
        # Let's mock the return value to be a DataFrame that has 'Adj Close'
        # If we request one ticker, yf returns a DF with columns as features (Open, High, ...)
        # If we request multiple, it returns MultiIndex columns (Feature, Ticker)
        
        # Simulating single ticker response
        mock_download.return_value = pd.DataFrame({
            "Adj Close": [150.0, 152.0],
            "Open": [149.0, 151.0]
        }, index=pd.to_datetime(["2023-01-01", "2023-01-02"]))
        
        provider = MarketDataProvider()
        data, tickers = provider.get_data(["AAPL"], "2023-01-01", "2023-01-02", return_updated_tickers=True)
        
        self.assertFalse(data.empty)
        self.assertEqual(tickers, ["AAPL"])

if __name__ == '__main__':
    unittest.main()
