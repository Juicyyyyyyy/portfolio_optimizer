

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

    @staticmethod
    def generate_custom_recommendation_prompt(description, number_of_tickers):
        prompt = (
            f"Generate a comprehensive analysis for portfolio investment considering the following user description:\n"
            f"\"{description}\"\n"
            f"Based on this analysis, suggest a list of {number_of_tickers} stock tickers suitable for this profile. "
            "Please provide the tickers in a Python list format, ensuring they are recognized by major stock exchanges "
            "and compatible with Yahoo Finance. Avoid tickers with punctuation marks."
            "Format the response as [stocks]['TICKER1', 'TICKER2', ...][/stocks]."
        )
        return prompt

    @staticmethod
    def generate_stock_review_prompt(tickers: str):
        prompt = (
            f"""Based on the following list of stock tickers, create a short review based on real facts for each ticker. 
            The review must countain:
                1. The company full name
                2. A short text about the history of the company, their activities, their revenue, etc.
                3. In one sentence you must give a reason on why it could be interesting to invest on this asset.
            
            If you lack information for a ticker you must never write something that is not based on real verified facts, 
            instead you must precise that you lack information for this ticker.
            You must use markdown to style the reviews.
            
            List of stock tickers: <stocks> {tickers} </stocks>
            
            Format your response between <stocks-reviews> </stocks-reviews> tags for easy extraction.
            """
        )
        return prompt
