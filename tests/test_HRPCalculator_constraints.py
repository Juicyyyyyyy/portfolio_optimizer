import unittest
import pandas as pd
import numpy as np
from PortfolioOptimizer.HRPCalculator import HRPCalculator

class TestHRPCalculatorConstraints(unittest.TestCase):
    def setUp(self):
        # Create dummy data for 4 assets
        dates = pd.date_range(start="2020-01-01", periods=100)
        data = {
            "A": np.random.normal(0.001, 0.02, 100).cumsum() + 100,
            "B": np.random.normal(0.001, 0.02, 100).cumsum() + 100,
            "C": np.random.normal(0.001, 0.02, 100).cumsum() + 100,
            "D": np.random.normal(0.001, 0.02, 100).cumsum() + 100
        }
        self.df = pd.DataFrame(data, index=dates)
        self.hrp = HRPCalculator(self.df)

    def test_no_constraints(self):
        weights = self.hrp.calculate_weights()
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=4)

    def test_single_constraint_active(self):
        # Force A to be max 0.1 (it would likely be higher naturally)
        constraints = {"A": 0.1}
        weights = self.hrp.calculate_weights(constraints=constraints)
        
        self.assertLessEqual(weights["A"], 0.10001)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=4)
        
        # Check if excess was redistributed
        # We can't easily check exact redistribution without knowing original weights,
        # but we know sum is 1.0 and A is <= 0.1

    def test_multiple_constraints(self):
        constraints = {"A": 0.1, "B": 0.2}
        weights = self.hrp.calculate_weights(constraints=constraints)
        
        self.assertLessEqual(weights["A"], 0.10001)
        self.assertLessEqual(weights["B"], 0.20001)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=4)

    def test_constraint_higher_than_natural(self):
        # If we constrain A to 0.9, but it was naturally 0.25, it should stay 0.25
        # We need to know natural weight first
        natural_weights = self.hrp.calculate_weights()
        natural_A = natural_weights["A"]
        
        constraints = {"A": 0.9}
        weights = self.hrp.calculate_weights(constraints=constraints)
        
        self.assertAlmostEqual(weights["A"], natural_A, places=4)

    def test_impossible_constraints(self):
        # If constraints sum to < 1 (e.g. all max 0.1 for 4 assets = max 0.4 total)
        # The algorithm should do its best (cap all at 0.1) and return sum < 1
        constraints = {"A": 0.1, "B": 0.1, "C": 0.1, "D": 0.1}
        weights = self.hrp.calculate_weights(constraints=constraints)
        
        self.assertLessEqual(weights["A"], 0.10001)
        self.assertLessEqual(weights["B"], 0.10001)
        self.assertLessEqual(weights["C"], 0.10001)
        self.assertLessEqual(weights["D"], 0.10001)
        # Sum should be approx 0.4
        self.assertAlmostEqual(sum(weights.values()), 0.4, places=1)

    def test_zero_constraint(self):
        constraints = {"A": 0.0}
        weights = self.hrp.calculate_weights(constraints=constraints)
        self.assertAlmostEqual(weights["A"], 0.0, places=4)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=4)

if __name__ == '__main__':
    unittest.main()
