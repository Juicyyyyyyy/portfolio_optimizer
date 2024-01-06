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

    # Calculate expected returns and sample covariance matrix
    mu = expected_returns.mean_historical_return(self.data)
    Sigma = risk_models.sample_cov(self.data)

    for i in range(num_portfolios):
        # Generate random weights
        random_weights = np.random.random(len(self.tickers))
        random_weights /= np.sum(random_weights)

        # Expected portfolio return
        expected_return = np.dot(mu, random_weights)

        # Expected portfolio volatility
        expected_volatility = np.sqrt(np.dot(random_weights.T, np.dot(Sigma, random_weights)))

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