import unittest
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider as md
from PortfolioOptimizer.MonteCarlo import MonteCarlo

class TestMonteCarlo(unittest.TestCase):
	def setUp(self) -> None:
		self.tickers = ['AAPL', 'MSFT', 'GOOGL']
		self.start_date = '2020-01-01'
		self.end_date = '2024-01-01'
		self.data = md.get_data(tickers=self.tickers, start_date=self.start_date, end_date=self.end_date)

		self.monte_carlo = MonteCarlo(self.data, self.tickers)

	def test_resample_efficient_frontier_inputs_via_monte_carlo(self):
		print(self.monte_carlo.resample_efficient_frontier_inputs_via_monte_carlo())
