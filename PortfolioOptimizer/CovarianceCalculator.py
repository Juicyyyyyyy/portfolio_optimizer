from pypfopt import risk_models
from abc import ABC, abstractmethod
import pandas as pd


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