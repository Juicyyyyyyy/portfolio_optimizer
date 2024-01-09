import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
import yfinance as yf
from PortfolioOptimizer.EfficientFrontierCalculator import EfficientFrontierCalculator

data = yf.download(["AAPL", "MSFT", "GOOGL"], start="2017-01-01", end="2021-01-01")['Adj Close']


class TestPortfolioOptimizer(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.calculator = EfficientFrontierCalculator(data)

    def test_efficient_frontier_weights(self):

        # Execute
        weights = self.calculator.calculate_efficient_frontier_weights()

        # Assert
        self.assertTrue(all(isinstance(weight, float) for weight in weights.values()))
        print(weights)

    def test_efficient_frontier_performance(self):
        # Setup
        self.calculator.calculate_efficient_frontier_weights()

        # Execute
        performance = self.calculator.calculate_efficient_frontier_performance()

        # Assert
        self.assertEqual(len(performance), 3)  # expected return, volatility, Sharpe ratio
        print(performance)

# More tests could be added for different scenarios, input data types, and error cases.

if __name__ == '__main__':
    unittest.main()
