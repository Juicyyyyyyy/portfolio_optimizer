from typing import List

from PortfolioOptimizer.ExpectedReturnCalculator import CapmCalculator

import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import BlackLittermanModel, black_litterman, risk_models
import pandas as pd


class BlackLitterman:
    def __init__(self, data: pd.DataFrame, tickers: List[str], views, omega_tau: float = 0.05,
                 total_portfolio_value=10000):
        self.data = data
        self.Sigma = risk_models.sample_cov(self.data)
        self.delta = black_litterman.market_implied_risk_aversion(data.mean())
        # The lower the delta is the more influence the investor’s views has impact on the weights returned
        self.tickers = tickers
        self.total_portfolio_value = total_portfolio_value
        first_date = self.data.index[0].date()
        last_date = self.data.index[-1].date()
        self.prior = CapmCalculator(first_date, last_date).calculate_expected_return(tickers)  # pi represents the equilibrium expected
        # returns of the assets in the market

        self.P, self.Q = self.user_input_to_pq(views)
        self.omega = self.set_omega_proportional_to_prior(
            tau=omega_tau)  # Omega is the covariance matrix of the investor's views

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
        expected_return, volatility, sharpe_ratio = ef.portfolio_performance(verbose=False)

        return cleaned_weights, expected_return, volatility, sharpe_ratio
