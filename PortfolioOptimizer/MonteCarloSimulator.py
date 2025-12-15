import numpy as np
import pandas as pd
from typing import Dict, List

class MonteCarloSimulator:
    def __init__(self, mean_returns: pd.Series, covariance_matrix: pd.DataFrame, weights: Dict[str, float], initial_portfolio_value: float = 10000):
        self.mean_returns = mean_returns
        self.covariance_matrix = covariance_matrix
        self.weights = np.array([weights.get(ticker, 0) for ticker in mean_returns.index])
        self.initial_portfolio_value = initial_portfolio_value

    def simulate(self, num_simulations: int = 1000, time_horizon: int = 252) -> Dict:
        """
        Run Monte Carlo simulation.
        :param num_simulations: Number of simulation paths to run.
        :param time_horizon: Number of days to simulate (default 252 for 1 year).
        :return: Dictionary containing simulation results (percentiles).
        """
        # Monte Carlo Simulation
        # Formula: Pt = Pt-1 * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z)
        # But for portfolio level, we can simulate portfolio returns directly.
        
        # Calculate portfolio expected return and volatility
        port_return = np.dot(self.weights, self.mean_returns)
        port_volatility = np.sqrt(np.dot(self.weights.T, np.dot(self.covariance_matrix, self.weights)))
        
        # Daily parameters (assuming mean_returns and covariance are annualized)
        dt = 1/252
        daily_return = port_return * dt
        daily_volatility = port_volatility * np.sqrt(dt)
        
        # Simulation
        simulation_results = np.zeros((time_horizon, num_simulations))
        simulation_results[0] = self.initial_portfolio_value
        
        for t in range(1, time_horizon):
            random_shocks = np.random.normal(0, 1, num_simulations)
            # Geometric Brownian Motion
            # S_t = S_{t-1} * exp((mu - 0.5 * sigma^2) + sigma * Z)
            # Here mu and sigma are daily
            drift = (daily_return - 0.5 * daily_volatility**2)
            diffusion = daily_volatility * random_shocks
            
            simulation_results[t] = simulation_results[t-1] * np.exp(drift + diffusion)
            
        # Calculate percentiles for the chart (10th, 50th, 90th)
        percentiles = np.percentile(simulation_results, [10, 50, 90], axis=1)
        
        return {
            "days": list(range(time_horizon)),
            "p10": percentiles[0].tolist(),
            "p50": percentiles[1].tolist(),
            "p90": percentiles[2].tolist(),
            "final_min": np.min(simulation_results[-1]),
            "final_max": np.max(simulation_results[-1]),
            "final_mean": np.mean(simulation_results[-1])
        }
