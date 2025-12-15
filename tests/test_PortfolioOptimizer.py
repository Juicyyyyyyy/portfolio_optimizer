import unittest
from unittest.mock import MagicMock
import pandas as pd
import numpy as np
from PortfolioOptimizer.EfficientFrontierCalculator import EfficientFrontierCalculator

class TestPortfolioOptimizer(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range(start="2023-01-01", periods=100)
        # Create correlated data to ensure a valid covariance matrix
        # Independent returns
        r1 = np.random.normal(0.001, 0.02, 100)
        r2 = np.random.normal(0.001, 0.02, 100)
        r3 = np.random.normal(0.001, 0.02, 100)
        
        # Prices
        p1 = 100 * np.cumprod(1 + r1)
        p2 = 100 * np.cumprod(1 + r2)
        p3 = 100 * np.cumprod(1 + r3)
        
        self.data = pd.DataFrame({
            "AAPL": p1,
            "MSFT": p2,
            "GOOG": p3
        }, index=dates)
        self.calculator = EfficientFrontierCalculator(self.data)

    def test_efficient_frontier_weights(self):
        weights = self.calculator.calculate_efficient_frontier_weights()
        self.assertTrue(all(isinstance(weight, float) for weight in weights.values()))
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=4)

    def test_efficient_frontier_performance(self):
        self.calculator.calculate_efficient_frontier_weights()
        performance = self.calculator.calculate_efficient_frontier_performance()
        self.assertEqual(len(performance), 3)

if __name__ == '__main__':
    unittest.main()
