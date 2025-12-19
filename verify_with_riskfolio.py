import riskfolio as rp
import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# 1. Data
tickers = ["AGED.L", "NQ=F", "VWCE.DE", "GOOGL", "RMS.PA", "MCD", "RL", "GLD"]
start_date = "2015-01-01"
end_date = "2025-12-18"

print("Downloading data...")
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
data = data.dropna()

# 2. Riskfolio Optimization (HRP)
print("\nRunning Riskfolio-Lib HRP Optimization...")
port = rp.Portfolio(returns=data.pct_change().dropna())
port.assets_stats(method_mu='hist', method_cov='hist')

# Estimate optimal portfolio:
# model='HRP' (Hierarchical Risk Parity)
# codependence='pearson' (Correlation matrix)
# rm='MV' (Variance)
# rf=0.02 (Risk free rate)
# link='single' (Linkage method, standard HRP uses single or ward)
w_rp = port.optimization(model='HRP', codependence='pearson', rm='MV', rf=0.02, link='single')

print("\nRiskfolio-Lib Weights:")
print(w_rp.sort_values(by='weights', ascending=False))
