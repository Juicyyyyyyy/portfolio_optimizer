from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import logging
from abc import ABC, abstractmethod

import numpy as np

import yfinance as yf
import pandas as pd
from typing import List, Any, Dict

import datetime


class MarketDataProvider(ABC):
	@abstractmethod
	def get_data(self, tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
		pass


class YFinanceDataProvider(MarketDataProvider):
	def get_data(self, tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
		try:
			data = yf.download(tickers, start=start_date, end=end_date)
			return data['Adj Close']
		except Exception as e:
			logging.error(f"Error fetching data for {tickers} from {start_date} to {end_date}: {e}")
		raise ValueError("Failed to fetch data. Please check your tickers and date range.")


class ExpectedReturnCalculator(ABC):
	@abstractmethod
	def calculate_expected_return(self, data: pd.DataFrame) -> Any:
		"""
		Calculate the expected returns.
		:param data: Historical price data as panda DataFrame
		"""
		pass


class MeanHistoricalReturnCalculator(ExpectedReturnCalculator):
	def calculate_expected_return(self, data: pd.DataFrame) -> Any:
		return expected_returns.mean_historical_return(data)


class CovarianceCalculator(ABC):
	@abstractmethod
	def calculate_covariance(self, data: pd.DataFrame):
		"""
		Calculate the covariance matrix
		:param data: Historical price data as panda DataFrame
		"""
	pass


class SampleCovarianceCalculator(CovarianceCalculator):
	def calculate_covariance(self, data: pd.DataFrame):
		"""
		Calculate the covariance matrix using the sample covariance method
		:param data: Historical price data as panda DataFrame
		:return: The covariance matrix
		"""
		return risk_models.sample_cov(data)


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
