from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
import yfinance as yf
import ast
import datetime


class ManageTickers:

	def __init__(self, tickers):
		self.tickers = tickers
		self.tickers = ast.literal_eval(self.tickers) # GPT returns a string so we convert it to list
		self.tickers = self.validate_tickers()

	def validate_tickers(self) -> list[str]:
		valid_tickers = []
		for ticker in self.tickers:
			stock_data = yf.Ticker(ticker)
			# Check if the ticker has historical data as a proxy for validation
			if not stock_data.history(period="1d").empty:
				valid_tickers.append(ticker)
		return valid_tickers

	def compute_optimized_portfolio_data(self):
		end_date = datetime.datetime.now()
		start_date = end_date - datetime.timedelta(days=10 * 365)

		data = yf.download(self.tickers, start=start_date, end=end_date)['Adj Close']

		# Portfolio optimization calculations
		mu = expected_returns.mean_historical_return(data)
		Sigma = risk_models.sample_cov(data)
		ef = EfficientFrontier(mu, Sigma)
		raw_weights = ef.max_sharpe()
		cleaned_weights = ef.clean_weights()

		organized_cleaned_weights = {stock: f"{weight:.4f}" for stock, weight in cleaned_weights.items() if weight > 0}
		organized_cleaned_weights = dict(
			sorted(organized_cleaned_weights.items(), key=lambda item: item[1], reverse=True))

		# Convert to list if necessary
		organized_cleaned_weights_list = [f"{stock}: {weight}" for stock, weight in organized_cleaned_weights.items()]

		# Additional data for future use
		performance = ef.portfolio_performance(verbose=False)

		return {
			"cleaned_weights": organized_cleaned_weights_list,
			"raw_weights": raw_weights,
			"performance": performance,
			"expected_returns": mu,
			"risk": Sigma,
		}
