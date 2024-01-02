import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
import yfinance as yf
from PortfolioOptimizer.PortfolioOptimizer import (YFinanceDataProvider, MeanHistoricalReturnCalculator,
                       SampleCovarianceCalculator, MeanVarianceOptimizationCalculator, CapmCalculator)

tickers = ["AAPL", "MSFT", "GOOGL"]

data = yf.download(["AAPL", "MSFT", "GOOGL"], start="2000-01-01", end="2021-01-01")['Adj Close']

capm = CapmCalculator()

class TestPortfolioOptimizer(unittest.TestCase):

    def test_calculate_risk_free_rate(self):
        risk_free_rate = capm.calculate_risk_free_rate()
        print("The risk free rate is : " + str(risk_free_rate))

    def test_calculate_market_premium(self):
        market_premium = capm.calculate_market_premium()
        print("The market premium (Mkt-rf) is : " + str(market_premium))

    def test_calculate_beta(self):
        betas = capm.calculate_beta(tickers)
        print("The betas are :" + str(betas))

    def test_calculate_expected_return(self):
        expected_return = capm.calculate_expected_return(tickers)
        print("The expected return is : " + str(expected_return))