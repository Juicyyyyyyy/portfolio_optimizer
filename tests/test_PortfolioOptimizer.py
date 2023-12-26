import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
import yfinance as yf
from PortfolioOptimizer.PortfolioOptimizer import (YFinanceDataProvider, MeanHistoricalReturnCalculator,
                       SampleCovarianceCalculator, MeanVarianceOptimizationCalculator)

data = yf.download(["AAPL", "MSFT", "GOOGL"], start="2020-01-01", end="2021-01-01")['Adj Close']


class TestMeanHistoricalReturnCalculator(unittest.TestCase):

    def test_calculate_expected_return(self):
        # Setup
        calculator = MeanHistoricalReturnCalculator()

        # Execute
        result = calculator.calculate_expected_return(data)

        # Assert
        self.assertEqual(len(result), len(data.columns))


class TestSampleCovarianceCalculator(unittest.TestCase):

    def test_calculate_covariance(self):
        # Setup
        calculator = SampleCovarianceCalculator()

        # Execute
        result = calculator.calculate_covariance(data)

        # Assert
        self.assertEqual(result.shape, (len(data.columns), len(data.columns)))
        print(result)


class TestMeanVarianceOptimizationCalculator(unittest.TestCase):

    def test_efficient_frontier_weights(self):
        # Setup
        calculator = MeanVarianceOptimizationCalculator(data)

        # Execute
        weights = calculator.calculate_efficient_frontier_weights()

        # Assert
        self.assertTrue(all(isinstance(weight, float) for weight in weights.values()))
        print(weights)

    def test_efficient_frontier_performance(self):
        # Setup
        calculator = MeanVarianceOptimizationCalculator(data)
        calculator.calculate_efficient_frontier_weights()

        # Execute
        performance = calculator.calculate_efficient_frontier_performance()

        # Assert
        self.assertEqual(len(performance), 3)  # expected return, volatility, Sharpe ratio
        print(performance)

# More tests could be added for different scenarios, input data types, and error cases.

if __name__ == '__main__':
    unittest.main()
