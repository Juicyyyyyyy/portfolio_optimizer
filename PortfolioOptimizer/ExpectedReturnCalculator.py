from abc import ABC, abstractmethod
from pypfopt import risk_models, expected_returns
import numpy as np
import yfinance as yf
import pandas as pd
from typing import List, Any, Dict
import datetime


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


class CapmCalculator(ExpectedReturnCalculator):

    def calculate_risk_free_rate(self):
        risk_free_rate = yf.download('^TNX', period='2y')['Adj Close']
        return risk_free_rate.iloc[-1] / 100

    def calculate_market_return(self):
        # Downloading the past 5 years of daily Adjusted Close prices for the S&P 500
        market_data = yf.download('^GSPC', period='5y')['Adj Close']

        # Calculating daily returns from daily adjusted close prices
        daily_returns = market_data.pct_change().dropna()

        # Calculating the average annualized market return
        # 252 is the typical number of trading days in a year
        avg_daily_return = daily_returns.mean()
        annualized_return = (1 + avg_daily_return) ** 252 - 1

        return annualized_return

    def calculate_market_premium(self):  # Mkt - Rf
        return self.calculate_market_return() - self.calculate_risk_free_rate()

    def calculate_beta(self, tickers):
        """

        :param tickers:
        :return:
        """
        betas = {}
        market_data = yf.download('^GSPC', period='5y')['Adj Close']
        market_returns = market_data.pct_change().dropna()

        for ticker in tickers:
            asset_data = yf.download(ticker, period='5y')['Adj Close']
            asset_returns = asset_data.pct_change().dropna()

            covariance = np.cov(asset_returns, market_returns)
            beta = covariance[0, 1] / covariance[1, 1]
            betas[ticker] = beta

        return betas

    def calculate_expected_return(self, tickers):
        # Calculate expected return using the CAPM formula for each ticker
        expected_returns = {}
        risk_free_rate = self.calculate_risk_free_rate()
        market_premium = self.calculate_market_premium()
        betas = self.calculate_beta(tickers)

        for ticker, beta in betas.items():
            # CAPM formula: Expected Return = Risk-Free Rate + Beta*(Market Premium)
            expected_returns[ticker] = risk_free_rate + beta * market_premium

        return expected_returns
