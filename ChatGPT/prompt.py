
class Prompt:

    def __init__(self, risk_tolerance, investment_area, investment_timeframe):
        self.risk_tolerance = risk_tolerance
        self.investment_area = investment_area
        self.investment_timeframe = investment_timeframe

    @staticmethod
    def generate_stock_recommendation_prompt(risk_tolerance, investment_area, investment_timeframe):
        prompt = (
            "Conduct a comprehensive investment analysis using the following criteria for portfolio construction:\n"
            f"1. Risk Tolerance Profile: '{risk_tolerance}'\n"
            f"2. Investment Focus Areas: '{investment_area}'\n"
            f"3. Investment Time Horizon: '{investment_timeframe}'\n"
            "This analysis should incorporate current market trends, financial news, and analyst insights to identify a substantial set of stock tickers, specifically more than 30 different stocks. "
            "These tickers should be well-suited to the investor's risk profile and investment focus, with potential for solid performance "
            "within the stated time horizon. "
            "Please present the stock ticker recommendations in a Python list format, ensuring they are in a format recognized by major stock exchanges "
            "and compatible with Yahoo Finance. Exclude tickers containing punctuation, such as 'ORSTED.CO', 'SGRE.MC', 'NVO.CO'. "
            "The aim is to provide a diversified selection of stocks based on thorough research and data analysis, tailored to the specific criteria outlined."
            "Format the response as [stocks]['TICKER1', 'TICKER2', ...][/stocks], including at least 30 different tickers."
        )
        return prompt





