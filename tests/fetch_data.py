# fetch_and_store_data.py

import yfinance as yf
import pandas as pd

# Expanded list of tickers
tickers = ["AAPL", "MSFT", "GOOGL"]

# Fetching data for the tickers for a specific time range
data = yf.download(tickers, start="2020-01-01", end="2021-01-01")['Adj Close']

# Saving the data to a CSV file
data.to_csv("historical_data.csv")
