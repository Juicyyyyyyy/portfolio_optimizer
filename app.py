# Import necessary modules
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns
import yfinance as yf
import ast

# Import custom functions for AI integration
from OpenAi.functions import callGpt, extract_text_between_tags
import OpenAi.prompt as prompt

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


# Example user inputs (these should be dynamically obtained based on user interaction)
user_risk_tolerance = "moderate"  # Example user input
user_investment_focus = "technology and renewable energy"  # Example user input
user_investment_timeframe = "long-term"  # Example user input
# ... other user inputs for the prompts

# Generate prompts and get AI responses
industry_analysis = callGpt(prompt.industry_and_sector_analysis(user_risk_tolerance, user_investment_focus, user_investment_timeframe))
financial_news = callGpt(prompt.financial_news_summary(user_investment_focus, user_risk_tolerance, user_investment_timeframe))
analyst_reports = callGpt(prompt.analyst_reports_summary(user_investment_focus, user_risk_tolerance, user_investment_timeframe))
esg_analysis = callGpt(prompt.esg_factor_analysis(user_investment_focus))
regulatory_developments = callGpt(prompt.regulatory_developments_summary(user_investment_focus))

# Generate final prompt for stock symbols
final_prompt = prompt.generate_stock_symbols_prompt(industry_analysis, financial_news, analyst_reports, esg_analysis, regulatory_developments, user_risk_tolerance, user_investment_timeframe)
stock_recommendations = callGpt(final_prompt)

# Extract stock symbols from the final response
# (This requires a function to parse the AI response and extract stock symbols)
stock_symbols = extract_text_between_tags(stock_recommendations)
stock_symbols = ast.literal_eval(stock_symbols)

validated_stock_symbols = validate_tickers(stock_symbols)

# Proceed with fetching data for only the validated tickers
data = yf.download(validated_stock_symbols, start="2020-01-01", end="2023-01-01")['Adj Close']

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
