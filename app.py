# Import necessary modules
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
import yfinance as yf
import ast
import datetime

# Import custom functions for AI integration
from ChatGPT.functions import callGpt, extract_text_between_tags
from ChatGPT.prompt import Prompt

def validate_tickers(tickers):
    valid_tickers = []
    for ticker in tickers:
        stock_data = yf.Ticker(ticker)
        # Check if the ticker has historical data as a proxy for validation
        if not stock_data.history(period="1d").empty:
            valid_tickers.append(ticker)
        else:
            print(f"Ticker {ticker} is not valid or delisted.")
    return valid_tickers


# Dynamically obtaining user inputs
user_risk_tolerance = input("Enter your risk tolerance (e.g., 'low', 'moderate', 'high'): ") or "moderate"
user_investment_area = input("Enter your investment focus areas (e.g., 'technology, renewable energy'): ") or "technology, research, AI, medical"
user_investment_timeframe = input("Enter your investment timeframe (e.g., 'short-term', 'long-term'): ") or "long-term"

# Generate final prompt for stock symbols
final_prompt = Prompt.generate_stock_recommendation_prompt(user_risk_tolerance, user_investment_area, user_investment_timeframe)
stock_recommendations = callGpt(final_prompt)

# Extract stock symbols from the final response
# (This requires a function to parse the AI response and extract stock symbols)
stock_symbols = extract_text_between_tags(stock_recommendations)
try:
    stock_symbols = ast.literal_eval(stock_symbols)
except:
    stock_symbols = ast.literal_eval(callGpt(final_prompt))

validated_stock_symbols = validate_tickers(stock_symbols)

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=10*365)  # Subtract 10 years (approximately)

# Proceed with fetching data for only the validated tickers
data = yf.download(validated_stock_symbols, start=start_date, end=end_date)['Adj Close']

# Portfolio optimization calculations
mu = expected_returns.mean_historical_return(data)
Sigma = risk_models.sample_cov(data)
ef = EfficientFrontier(mu, Sigma)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()

for stock, weight in cleaned_weights.items():
    if weight > 0:
        print(f"{stock}: {weight:.4f}")  # Display non-zero weights

# Display portfolio performance
ef.portfolio_performance(verbose=True)
