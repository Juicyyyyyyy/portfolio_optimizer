# fetch_and_store_data.py

import yfinance as yf
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider as md

risk_free_rate = yf.download('^TNX', period='2y')['Adj Close']
md = md.get_data('^TNX', period='2y')

print("risk free rate from yf download" + str(risk_free_rate))
print("risk free rate from MarketDataProvider" + str(md))