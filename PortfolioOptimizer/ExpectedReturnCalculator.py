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
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def calculate_risk_free_rate(self) -> float:
        """
        Formula : Risk-free rate = Yield of 3-month U.S. Treasury Bill

        :return: the latest 3-month US Treasury Bill yield as a decimal
        """
        risk_free_rate = md.get_data('^IRX', period='2y')  # Update the ticker symbol to ^IRX
        return risk_free_rate.iloc[-1] / 100

    def calculate_market_return(self) -> float:
        """
        formula : E(Rm) = Average annual return of the market benchmark (S&P 500 here)

        :return: the average annualized return of the sp500 on the same years as the input data
        """
        market_data = md.get_data('^GSPC', start_date=self.start_date, end_date=self.end_date)
        # Calculating daily returns from daily adjusted close prices
        daily_returns = market_data.pct_change().dropna()

        # Calculating the average annualized market return
        # 252 is the typical number of trading days in a year
        avg_daily_return = daily_returns.mean()
        annualized_return = (1 + avg_daily_return) ** 252 - 1

        return annualized_return

    def calculate_market_premium(self) -> float:  # Mkt - Rf
        return self.calculate_market_return() - self.calculate_risk_free_rate()

    def calculate_beta(self, tickers: List[str]) -> Dict[str, float]:
        betas = {}
        # Fetch and resample market data to monthly
        market_data = md.get_data('^GSPC', start_date=self.start_date, end_date=self.end_date)
        monthly_market_data = market_data.resample('M').last()
        monthly_market_returns = monthly_market_data.pct_change().dropna()

        for ticker in tickers:
            # Fetch and resample stock data to monthly
            stock_data = md.get_data(ticker, start_date=self.start_date, end_date=self.end_date)
            monthly_stock_data = stock_data.resample('M').last()
            monthly_stock_returns = monthly_stock_data.pct_change().dropna()

            # Aligning monthly stock returns with market returns
            aligned_stock, aligned_market = monthly_stock_returns.align(monthly_market_returns, join='inner')

            # Calculating covariance and variance
            covariance = np.cov(aligned_stock, aligned_market)[0, 1]
            market_variance = np.var(aligned_market)

            # Calculating beta
            beta = covariance / market_variance
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
