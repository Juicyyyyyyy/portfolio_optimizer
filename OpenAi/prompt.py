
def industry_and_sector_analysis(risk_tolerance="", investment_focus="", investment_timeframe=""):
    prompt = f"What are the current trends and most promising sectors for investment, "
    if investment_focus:
        prompt += f"focusing on {investment_focus}, "
    prompt += f"suitable for an investor with {risk_tolerance if risk_tolerance else 'a balanced'} risk tolerance"
    prompt += f" and a {investment_timeframe if investment_timeframe else 'long-term'} investment horizon?"
    return prompt

def financial_news_summary(sector_focus="", risk_tolerance="", investment_timeframe=""):
    prompt = f"Summarize the latest financial news and reports highlighting significant developments "
    if sector_focus:
        prompt += f"in {sector_focus} sectors "
    prompt += f"that are relevant for a {risk_tolerance if risk_tolerance else 'moderate-risk'} investor "
    prompt += f"focusing on {investment_timeframe if investment_timeframe else 'long-term growth'}."
    return prompt

def analyst_reports_summary(sector_focus="", risk_tolerance="", investment_timeframe=""):
    prompt = f"Provide a summary of recent analyst reports and stock recommendations for companies "
    if sector_focus:
        prompt += f"in the {sector_focus} sectors, "
    prompt += f"suitable for an investor focusing on {investment_timeframe if investment_timeframe else 'long-term growth'} "
    prompt += f"with {risk_tolerance if risk_tolerance else 'moderate'} risk tolerance."
    return prompt

def esg_factor_analysis(sector_focus="", investment_values=""):
    prompt = f"List companies in "
    prompt += f"{sector_focus if sector_focus else 'various'} sectors "
    prompt += f"with strong ESG ratings and practices, suitable for an investor who "
    prompt += f"prioritizes {investment_values if investment_values else 'ethical and sustainable investing'}."
    return prompt

def regulatory_developments_summary(sector_focus="", global_focus=""):
    prompt = f"Summarize any recent regulatory or political developments affecting "
    prompt += f"{sector_focus if sector_focus else 'various'} sectors "
    prompt += f"globally, and how they might impact investments in these areas. "
    prompt += f"Focus on {global_focus if global_focus else 'key markets globally'}."
    return prompt

def generate_stock_symbols_prompt(industry_analysis, financial_news, analyst_reports, esg_analysis, regulatory_developments, risk_tolerance="moderate", investment_timeframe="long-term"):
    prompt = (
        "Based on the following insights, suggest a list of stock tickers for portfolio investment:\n"
        "1. Industry Analysis: " + industry_analysis + "\n"
        "2. Financial News Summary: " + financial_news + "\n"
        "3. Analyst Reports Summary: " + analyst_reports + "\n"
        "4. ESG Factor Analysis: " + esg_analysis + "\n"
        "5. Regulatory Developments: " + regulatory_developments + "\n"
        f"Please provide a list of stock tickers in a Python list format between [stocks] tags, "
        f"suitable for a {investment_timeframe} investment strategy with {risk_tolerance} risk tolerance. "
        "Format the response as [stocks]['TICKER1', 'TICKER2', ...][/stocks]. "
        "Ensure all tickers are in a format recognized by major stock exchanges and compatible with Yahoo Finance. "
        "Avoid region-specific or exchange-specific ticker formats. Focus on standard, widely-recognized ticker symbols."
        "Avoid every ticker with a point inside the ticker name, example : 'ORSTED.CO', 'SGRE.MC', 'NVO.CO'."
    )
    return prompt



