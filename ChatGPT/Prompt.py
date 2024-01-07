
class Prompt:
    @staticmethod
    def generate_stock_recommendation_prompt(risk_tolerance, investment_area, investment_timeframe):
        prompt = (
            f"Generate a comprehensive analysis for portfolio investment considering the following parameters:\n"
        f"- Risk Tolerance: {risk_tolerance}\n"
        f"- Investment Areas: {investment_area}\n"
        f"- Investment Timeframe: {investment_timeframe}\n"
        "Based on this analysis, suggest a list of stock tickers suitable for the defined investment profile. "
        "Please provide the tickers in a Python list format, ensuring they are recognized by major stock exchanges "
        "and compatible with Yahoo Finance. Avoid tickers with punctuation marks like 'ORSTED.CO', 'SGRE.MC', 'NVO.CO'."
        "Format the response as [stocks]['TICKER1', 'TICKER2', ...][/stocks], including at least 30 different tickers."
        )
        return prompt





