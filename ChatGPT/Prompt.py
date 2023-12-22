
class Prompt:

    def __init__(self, risk_tolerance, investment_area, investment_timeframe):
        self.risk_tolerance = risk_tolerance
        self.investment_area = investment_area
        self.investment_timeframe = investment_timeframe

    def generate_stock_recommendation_prompt(self):
        prompt = (
            f"Generate a comprehensive analysis for portfolio investment considering the following parameters:\n"
        f"- Risk Tolerance: {self.risk_tolerance}\n"
        f"- Investment Areas: {self.investment_area}\n"
        f"- Investment Timeframe: {self.investment_timeframe}\n"
        "Based on this analysis, suggest a list of stock tickers suitable for the defined investment profile. "
        "Please provide the tickers in a Python list format, ensuring they are recognized by major stock exchanges "
        "and compatible with Yahoo Finance. Avoid tickers with punctuation marks like 'ORSTED.CO', 'SGRE.MC', 'NVO.CO'."
        "Format the response as [stocks]['TICKER1', 'TICKER2', ...][/stocks], including at least 30 different tickers."
        )
        return prompt





