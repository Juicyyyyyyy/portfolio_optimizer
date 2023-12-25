import PortfolioOptimizer
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import BlackLittermanModel, black_litterman
import yfinance as yf

class BlackLitterman(PortfolioOptimizer):
	def __init__(self, tickers, start_date, end_date, total_portfolio_value):
		super().__init__(tickers, start_date, end_date, total_portfolio_value)

		self.delta = black_litterman.market_implied_risk_aversion(self.data.mean())
		# The lower the delta is the more influence the investor’s views has impact on the weights returned
		self.prior = self.calculate_equilibrium_expected_returns_CAPM()  # pi represents the equilibrium expected
		# returns of the assets in the market

		self.omega = None  # Omega is the covariance matrix of the investor's views
		self.P = None  # Picking matrix for the views
		self.Q = None  # Views matrix

	def set_black_litterman_views(self, P, Q, omega=None):
		"""
		Sets the views for the Black-Litterman model.
		:param P: Picking matrix
		:param Q: Views matrix
		:param omega: Uncertainty matrix (optional)
		"""
		self.P = P
		self.Q = Q
		self.omega = omega  # If omega is None, it will be calculated in the bl_model

	def user_input_to_pq(self, views):
		"""
		Convert user inputs into P and Q matrices for the Black-Litterman model.

		:param views: List of dictionaries containing the user's views.
		:return: P and Q matrices.

		assets = ['AssetA', 'AssetB', 'AssetC']
		views = [
			{'type': 'absolute', 'asset': 'AssetA', 'return': 0.05},
			{'type': 'relative', 'asset1': 'AssetB', 'asset2': 'AssetC', 'difference': 0.02}
		]

		P, Q = user_input_to_pq(assets, views)
		print("P Matrix:\n", P)
		print("Q Matrix:\n", Q)

		"""

		# Initialize P and Q
		P = np.zeros((len(views), len(self.tickers)))
		Q = np.zeros((len(views), 1))

		for i, view in enumerate(views):
			if view['type'] == 'absolute':
				# Find the index of the asset
				asset_index = self.tickers.index(view['asset'])
				# Set the corresponding values in P and Q
				P[i, asset_index] = 1
				Q[i] = view['return']
			elif view['type'] == 'relative':
				# Find the indexes of the assets
				asset_index_1 = self.tickers.index(view['asset1'])
				asset_index_2 = self.tickers.index(view['asset2'])
				# Set the corresponding values in P and Q
				P[i, asset_index_1] = 1
				P[i, asset_index_2] = -1
				Q[i] = view['difference']

		return P, Q

	def set_omega_proportional_to_prior(self, tau=0.05):
		"""
		Sets the omega matrix proportional to the diagonal elements of the prior covariance matrix scaled by tau.
		This approach assumes equal confidence in all views and scales the uncertainty by the variance of the assets.

		:param tau: A scaling factor for the variances, representing the uncertainty of the views.
					A smaller tau indicates higher confidence in the views. Default is 0.05.
		"""
		if self.P is None:
			raise ValueError("P matrix (picking matrix for the views) must be set before setting omega.")

		# Diagonal elements of the prior covariance matrix
		diag_prior = np.diag(self.Sigma)  # np.diag() creates a diagonal matrix

		# Scale the diagonal based on the picking matrix P and the scaling factor tau
		omega_diagonal = np.dot(np.dot(self.P, np.diag(diag_prior)), self.P.T) * tau

		# Ensuring that omega is a diagonal matrix with the scaled values
		self.omega = np.diag(np.diag(omega_diagonal))

	def get_omega(self):
		"""
		Returns the omega matrix. If omega has not been set or calculated, it attempts to calculate it using
		a default approach.
		"""
		if self.omega is None:
			self.set_omega_proportional_to_prior()  # or any other default method you wish to use

		return self.omega

	def optimize_with_black_litterman(self):
		"""
		Optimizes the portfolio using the Black-Litterman model.
		"""

		# Ensure that views have been set
		if self.P is None or self.Q is None:
			raise ValueError("Views (P and Q) must be set before optimization.")

		# Initialize the Black-Litterman model
		bl = BlackLittermanModel(self.Sigma, pi=self.prior, Q=self.Q, P=self.P, omega=self.omega)

		# Compute the posterior returns and covariances
		posterior_rets = bl.bl_returns()
		posterior_cov = bl.bl_cov()

		# Re-optimize the portfolio with the new posterior estimates
		ef = EfficientFrontier(posterior_rets, posterior_cov)
		raw_weights = ef.max_sharpe()
		cleaned_weights = ef.clean_weights()

		# Compute and return the portfolio performance
		performance = ef.portfolio_performance(verbose=False)
		return cleaned_weights, performance

	def calculate_beta(self, market_symbol, lookback_period='5y'):
		"""
		Calculate the beta of each asset in the portfolio against a market index.
		:param market_symbol: Symbol for the market index.
		:param lookback_period: Historical period over which to calculate beta.
		:return: A dictionary of beta values for each ticker.
		"""
		betas = {}
		market_data = yf.download(market_symbol, period=lookback_period)['Adj Close']
		market_returns = market_data.pct_change().dropna()

		for ticker in self.tickers:
			asset_data = yf.download(ticker, period=lookback_period)['Adj Close']
			asset_returns = asset_data.pct_change().dropna()

			covariance = np.cov(asset_returns, market_returns)
			beta = covariance[0, 1] / covariance[1, 1]
			betas[ticker] = beta

		return betas

	def get_risk_free_rate(self):
		# Example: Using the 3-month US Treasury Bill as the risk-free rate
		# The symbol for the 3-month Treasury bill can vary; 'DTB3' is often used
		t_bill = yf.Ticker("^IRX")  # 13 Week Treasury Bill as a proxy
		hist = t_bill.history(period="1d")
		# The rate is annualized, so divide by 100 to convert to decimal form
		current_yield = hist.iloc[-1]['Close'] / 100
		return current_yield

	def get_market_return(self, index_symbol='^GSPC', years=10):
		"""
		Calculate the historical annualized return of a market index over a specified number of years.

		:param index_symbol: The market index symbol (default is S&P 500).
		:param years: The number of years to look back.
		:return: The annualized return as a decimal.
		"""
		index_data = yf.download(index_symbol, period=f"{years}y")
		# Calculate daily returns
		daily_returns = index_data['Adj Close'].pct_change().dropna()
		# Convert daily returns to annualized returns
		annualized_return = (1 + daily_returns.mean()) ** 252 - 1  # 252 trading days
		return annualized_return

	def calculate_equilibrium_expected_returns_CAPM(self, risk_free_rate=0, market_return=0, market_symbol='^GSPC'):
		"""
		Calculates equilibrium expected returns using the CAPM model for each asset.
		:param risk_free_rate: Risk-free rate for the CAPM formula.
		:param market_return: Expected market return.
		:param market_symbol: The market index symbol to use for beta calculation.
		:return: A dictionary of equilibrium expected returns for each ticker.
		"""

		# if no parameters chosen we use the functions with default values
		risk_free_rate = self.get_risk_free_rate() if risk_free_rate == 0 else risk_free_rate
		market_return = self.get_market_return() if market_return == 0 else market_return

		# Obtain beta for each asset
		betas = self.calculate_beta(market_symbol=market_symbol)

		# Calculate expected returns using CAPM formula for each asset
		pi = {}
		for ticker, beta in betas.items():
			expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
			pi[ticker] = expected_return

		# Update prior (pi) for later use in Black-Litterman model
		self.prior = pi

		return pi