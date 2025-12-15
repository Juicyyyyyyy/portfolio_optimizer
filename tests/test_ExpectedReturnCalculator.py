import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from PortfolioOptimizer.ExpectedReturnCalculator import CapmCalculator, MeanHistoricalReturnCalculator

class TestMeanHistoricalReturnCalculator(unittest.TestCase):
    def test_calculate_expected_return(self):
        data = pd.DataFrame({
            "A": [100, 101, 102],
            "B": [50, 51, 52]
        })
        calc = MeanHistoricalReturnCalculator()
        # pypfopt's mean_historical_return calculates annualized return
        # We just verify it returns a Series
        result = calc.calculate_expected_return(data)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), 2)

class TestCapmCalculator(unittest.TestCase):
    @patch("PortfolioOptimizer.ExpectedReturnCalculator.md")
    def test_calculate_risk_free_rate(self, mock_md):
        # Mock get_data for ^IRX
        mock_md.get_data.return_value = pd.Series([2.0], index=[pd.Timestamp("2023-01-01")])
        
        capm = CapmCalculator("2023-01-01", "2023-01-02")
        rf = capm.calculate_risk_free_rate()
        self.assertEqual(rf, 0.02)

    @patch("PortfolioOptimizer.ExpectedReturnCalculator.md")
    def test_calculate_market_return(self, mock_md):
        # Mock get_data for ^GSPC
        mock_md.get_data.return_value = pd.Series([100, 110], index=pd.to_datetime(["2023-01-01", "2023-01-02"]))
        
        capm = CapmCalculator("2023-01-01", "2023-01-02")
        mkt_ret = capm.calculate_market_return()
        self.assertIsInstance(mkt_ret, float)

if __name__ == '__main__':
    unittest.main()