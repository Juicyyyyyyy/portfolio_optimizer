from pypfopt.hierarchical_portfolio import HRPOpt
import pandas as pd
from typing import Tuple

class HRPCalculator:
    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._hrp = HRPOpt(returns=data.pct_change().dropna())

    def calculate_weights(self, constraints: dict = None):
        raw_weights = self._hrp.optimize()
        cleaned_weights = self._hrp.clean_weights()
        
        if constraints:
            cleaned_weights = self._apply_constraints(cleaned_weights, constraints)
            
        return cleaned_weights

    def _apply_constraints(self, weights: dict, constraints: dict) -> dict:
        """
        Iteratively apply max weight constraints and redistribute excess to other assets.
        """
        # 1. Validate constraints
        # Ensure constraints don't sum to less than 1 (impossible to satisfy)
        # But here we only have max constraints. If sum(max_constraints) < 1, it's impossible.
        # We'll assume user input is somewhat sane, but we can handle the case where we can't distribute.
        
        current_weights = weights.copy()
        
        for _ in range(100): # Max iterations to prevent infinite loops
            excess_weight = 0.0
            violations = False
            
            # Check for violations and cap
            for ticker, weight in current_weights.items():
                if ticker in constraints and weight > constraints[ticker]:
                    excess_weight += weight - constraints[ticker]
                    current_weights[ticker] = constraints[ticker]
                    violations = True
            
            if not violations and excess_weight < 1e-6:
                break
                
            # Redistribute excess
            # Find eligible assets (those not at their cap)
            eligible_assets = []
            total_eligible_weight = 0.0
            
            for ticker, weight in current_weights.items():
                # An asset is eligible if it's not constrained OR if it's constrained but below its cap
                # (We use a small epsilon for float comparison)
                limit = constraints.get(ticker, 1.0)
                if weight < limit - 1e-6:
                    eligible_assets.append(ticker)
                    total_eligible_weight += weight
            
            if not eligible_assets or total_eligible_weight == 0:
                # Cannot redistribute further (e.g. all assets hit caps)
                # This implies sum(constraints) < 1. 
                # We stop here. The weights will sum to < 1.
                break
                
            for ticker in eligible_assets:
                # Distribute proportional to current weight
                share = current_weights[ticker] / total_eligible_weight
                current_weights[ticker] += excess_weight * share
        
        # Final rounding to ensure clean output
        return {k: round(v, 5) for k, v in current_weights.items()}

    def calculate_performance(self, risk_free_rate=0.02) -> Tuple[float, float, float]:
        return self._hrp.portfolio_performance(risk_free_rate=risk_free_rate)
