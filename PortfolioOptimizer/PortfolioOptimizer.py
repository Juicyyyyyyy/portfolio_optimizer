from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

import numpy as np

import yfinance as yf
import ast
import datetime


class PortfolioOptimizer:

	def __init__(self, tickers, start_date, end_date, total_portfolio_value=10000):
		"""
		:param tickers: the tickers in a string format : "'[AAPL]', '[TSL]', '[BTC]'"
		"""
		self.tickers = tickers

		self.tickers = ast.literal_eval(self.tickers)
		self.tickers = self.validate_tickers()

		self.start_date = start_date
		self.end_date = end_date
		self.data = yf.download(self.tickers, start=self.start_date, end=self.end_date)['Adj Close']
		self.total_portfolio_value = total_portfolio_value

		self.mu = expected_returns.mean_historical_return(self.data)
		self.Sigma = risk_models.sample_cov(self.data)
		self.ef = EfficientFrontier(self.mu, self.Sigma)

	def validate_tickers(self) -> list[str]:

		valid_tickers = []
		for ticker in self.tickers:
			stock_data = yf.Ticker(ticker)
			# Check if the ticker has historical data as a proxy for validation
			if not stock_data.history(period="1d").empty:
				valid_tickers.append(ticker)
		return valid_tickers

	def compute_optimized_portfolio_data(self):

		raw_weights = self.ef.max_sharpe()
		cleaned_weights = self.ef.clean_weights()

		organized_cleaned_weights = {stock: f"{weight:.4f}" for stock, weight in cleaned_weights.items() if weight > 0}
		organized_cleaned_weights = dict(
			sorted(organized_cleaned_weights.items(), key=lambda item: item[1], reverse=True))
		organized_cleaned_weights_list = [f"{stock}: {weight}" for stock, weight in organized_cleaned_weights.items()]

		performance = self.ef.portfolio_performance(verbose=False)

		expected_annual_return, annual_volatility, sharpe_ratio = performance

		return {
			"weights": organized_cleaned_weights,
			"sharpe_ratio": sharpe_ratio,
			"expected_annual_return": expected_annual_return
		}

	def get_concrete_allocation(self, weights):

		latest_prices = get_latest_prices(self.data)

		concrete_allocation = DiscreteAllocation(weights, latest_prices, self.total_portfolio_value)

		allocation, leftover = concrete_allocation.greedy_portfolio()

		return {
			"concrete_allocation": allocation,
			"funds_remaining": leftover
		}

	def compute_optimized_portfolio_via_monte_carlo(self):
		"""
		Use Monte Carlo method to resample the efficient frontier inputs.
		This method will optimize the weight allocations based on the Monte Carlo simulation
		of expected returns and risks.

		:return: The optimized weight allocations and respective portfolio performance
		"""
		# Define the number of simulations
		num_portfolios = 10000
		results_array = np.zeros((3, num_portfolios))

		for i in range(num_portfolios):
			# Generate random weights
			random_weights = np.random.random(len(self.tickers))
			random_weights /= np.sum(random_weights)

			# Expected portfolio return
			expected_return = np.dot(self.mu, random_weights)

			# Expected portfolio volatility
			expected_volatility = np.sqrt(np.dot(random_weights.T, np.dot(self.Sigma, random_weights)))

			# Sharpe ratio
			sharpe_ratio = expected_return / expected_volatility

			# Store results
			results_array[0, i] = expected_return
			results_array[1, i] = expected_volatility
			results_array[2, i] = sharpe_ratio

		# Extract the portfolio with the highest Sharpe ratio
		max_sharpe_idx = np.argmax(results_array[2])

		# Extract the allocation of the max Sharpe ratio portfolio
		optimal_weights = np.random.random(len(self.tickers))
		optimal_weights /= np.sum(optimal_weights)

		optimal_weights = np.round(optimal_weights, 4)

		weights_dict = dict(zip(self.tickers, optimal_weights))

		return {
			"weights": weights_dict,
			"expected_return": results_array[0, max_sharpe_idx],
			"expected_volatility": results_array[1, max_sharpe_idx],
			"sharpe_ratio": results_array[2, max_sharpe_idx],
		}


