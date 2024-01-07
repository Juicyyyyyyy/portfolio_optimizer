from abc import ABC, abstractmethod
from pypfopt import expected_returns
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider as md

import numpy as np
import yfinance as yf
import pandas as pd
from typing import List, Any, Dict


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

    def calculate_risk_free_rate(self) -> float:
        """
        Formula : Risk-free rate = Yield of 10-year U.S. Treasury Note

        :return: the latest 10-year US Treasury Note yield as a decimal
        """
        risk_free_rate = md.get_data('^TNX', period='2y')
        return risk_free_rate.iloc[-1] / 100

    def calculate_market_return(self) -> float:
        """
        formula : E(Rm) = Average annual return of the market benchmark (S&P 500 here)

        :return: the average annualized return of the sp500 on the last 5 years
        """
        market_data = md.get_data('^GSPC', period='5y')
        # Calculating daily returns from daily adjusted close prices
        daily_returns = market_data.pct_change().dropna()

        # Calculating the average annualized market return
        # 252 is the typical number of trading days in a year
        avg_daily_return = daily_returns.mean()
        annualized_return = (1 + avg_daily_return) ** 252 - 1

        return annualized_return

    def calculate_market_premium(self) -> float:  # Mkt - Rf
        return self.calculate_market_return() - self.calculate_risk_free_rate()

    def calculate_beta(self, tickers) -> dict:
        """
        Formula : beta = covariance(stock, market) / variance(market)

        :param tickers: list of tickers
        :return: A dictionary with tickers as keys and their corresponding beta values as values
        """
        betas = {}
        market_data = md.get_data('^GSPC', period='5y')
        market_returns = market_data.pct_change().dropna()

        for ticker in tickers:
            asset_data = md.get_data(ticker, period='5y')
            asset_returns = asset_data.pct_change().dropna()

            covariance = np.cov(asset_returns, market_returns)
            beta = covariance[0, 1] / covariance[1, 1]
            betas[ticker] = beta

        return betas

    def calculate_expected_return(self, tickers):
        """
        Calculate expected return using the CAPM formula for each ticker
        Formula : E(Ri) = Rf + beta * (E(Rm) - Rf)

        :param tickers: list of tickers
        :return: a panda series composed of each ticker and their corresponding expected return
        """
        expected_returns = {}
        risk_free_rate = self.calculate_risk_free_rate()
        market_premium = self.calculate_market_premium()
        betas = self.calculate_beta(tickers)

        for ticker, beta in betas.items():
            # CAPM formula: Expected Return = Risk-Free Rate + Beta*(Market Premium)
            expected_returns[ticker] = risk_free_rate + beta * market_premium

        series_expected_returns = pd.Series(expected_returns, name='Expected Return')

        return series_expected_returns
