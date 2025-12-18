from pypfopt.efficient_frontier import EfficientFrontier
import pandas as pd
from typing import Tuple

import datetime

from PortfolioOptimizer.ExpectedReturnCalculator import CapmCalculator, MeanHistoricalReturnCalculator
from PortfolioOptimizer.CovarianceCalculator import SampleCovarianceCalculator


class EfficientFrontierCalculator:
    def __init__(self, data: pd.DataFrame, mu="capm", total_portfolio_value=10000):
        self._data = data
        if mu == "capm":
            self._mu = CapmCalculator(start_date=data.index[0], end_date=data.index[-1]).calculate_expected_return(data.columns.tolist())
        elif mu == "mean historical return":
            self._mu = MeanHistoricalReturnCalculator().calculate_expected_return(data)
        self.total_portfolio_value = total_portfolio_value
        self._Sigma = SampleCovarianceCalculator().calculate_covariance(data)
        self._ef = None

    def get_data(self):
        return self._data

    def calculate_efficient_frontier_weights(self, risk_free_rate=0.02):
        if self._ef is None:
            self._ef = EfficientFrontier(self._mu, self._Sigma)
        raw_weights = self._ef.max_sharpe(risk_free_rate=risk_free_rate)
        cleaned_weights = self._ef.clean_weights()
        return cleaned_weights

    def calculate_min_volatility_weights(self):
        if self._ef is None:
            self._ef = EfficientFrontier(self._mu, self._Sigma)
        raw_weights = self._ef.min_volatility()
        cleaned_weights = self._ef.clean_weights()
        return cleaned_weights

    def calculate_efficient_frontier_performance(self, risk_free_rate=0.02) -> Tuple[float, float, float]:
        if self._ef is None:
            raise ValueError(
                "Efficient Frontier weights not calculated. Call calculate_efficient_frontier_weights() first.")
        return self._ef.portfolio_performance(risk_free_rate=risk_free_rate)
