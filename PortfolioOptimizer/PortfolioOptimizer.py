from pypfopt.efficient_frontier import EfficientFrontier
import yfinance as yf
import pandas as pd
from typing import List, Any, Dict

import datetime

from ExpectedReturnCalculator import MeanHistoricalReturnCalculator, CapmCalculator
from CovarianceCalculator import SampleCovarianceCalculator


class PortfolioOptimizer:
    def __init__(self, data: pd.DataFrame, mu="capm"):
        self._data = data
        if mu == "capm":
            self._mu = CapmCalculator().calculate_expected_return(data.columns.tolist())
        elif mu == "mean historical return":
            self._mu = MeanHistoricalReturnCalculator().calculate_expected_return(data)
        self._Sigma = SampleCovarianceCalculator().calculate_covariance(data)
        self._ef = None

    def get_data(self):
        return self._data

    def calculate_efficient_frontier_weights(self):
        if self._ef is None:
            self._ef = EfficientFrontier(self._mu, self._Sigma)
        raw_weights = self._ef.max_sharpe()
        cleaned_weights = self._ef.clean_weights()
        return cleaned_weights

    def calculate_efficient_frontier_performance(self) -> tuple[float, float, float]:
        if self._ef is None:
            raise ValueError(
                "Efficient Frontier weights not calculated. Call calculate_efficient_frontier_weights() first.")
        return self._ef.portfolio_performance()