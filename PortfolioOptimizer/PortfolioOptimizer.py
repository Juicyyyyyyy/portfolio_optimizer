from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import logging
from abc import ABC, abstractmethod
import getFamaFrenchFactors as gff

import numpy as np

import yfinance as yf
import pandas as pd
from typing import List, Any, Dict

import datetime

from ExpectedReturnCalculator import MeanHistoricalReturnCalculator
from CovarianceCalculator import SampleCovarianceCalculator


class EfficientFrontierCalculator(ABC):
    @abstractmethod
    # The Efficient Frontier represents the set of portfolios that provide the highest expected return for
    # a given level of risk or the lowest risk for a given level of expected return
    def calculate_efficient_frontier_weights(self):
        """
		:return: asset weights
		"""
        pass

    def calculate_efficient_frontier_performance(self) -> tuple[float, float, float]:
        """
		:return: expected return, volatility, Sharpe ratio
		"""
        pass


class MeanVarianceOptimizationCalculator(EfficientFrontierCalculator):  # Original MPT

    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._mu = MeanHistoricalReturnCalculator().calculate_expected_return(data)
        self._Sigma = SampleCovarianceCalculator().calculate_covariance(data)
        self._ef = None

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
