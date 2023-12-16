from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd
import yfinance as yf
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# Update the ticker symbols as needed (e.g., change 'FB' to 'META' if required)
stock_symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "META"]  # Changed 'FB' to 'META'
start_date = "2020-01-01"
end_date = "2023-01-01"

# Fetching data from Yahoo Finance
data = yf.download(stock_symbols, start=start_date, end=end_date)['Adj Close']

# Check and handle missing values
data.ffill(inplace=True)
if data.isnull().sum().sum() > 0:
    print("Warning: Some data are missing after forward fill.")

# Calculate expected annualized returns and sample covariance
mu = expected_returns.mean_historical_return(data)
Sigma = risk_models.sample_cov(data)

# Optimize for the efficient frontier
ef = EfficientFrontier(mu, Sigma)
try:
    raw_weights = ef.min_volatility()
    cleaned_weights = ef.clean_weights()
    ef.portfolio_performance(verbose=True)
except ValueError as e:
    print("Error in optimization:", e)
