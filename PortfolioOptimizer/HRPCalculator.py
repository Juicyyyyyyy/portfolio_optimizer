from pypfopt.hierarchical_portfolio import HRPOpt
import pandas as pd
from typing import Tuple

class HRPCalculator:
    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._hrp = HRPOpt(returns=data.pct_change().dropna())

    def calculate_weights(self):
        raw_weights = self._hrp.optimize()
        cleaned_weights = self._hrp.clean_weights()
        return cleaned_weights

    def calculate_performance(self, risk_free_rate=0.02) -> Tuple[float, float, float]:
        return self._hrp.portfolio_performance(risk_free_rate=risk_free_rate)
