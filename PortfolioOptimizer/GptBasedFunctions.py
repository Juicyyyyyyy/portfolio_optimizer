from ChatGPT.ApiGpt import ApiGpt
from ChatGPT.Prompt import Prompt

import ast


class GptBasedFunctions:
    @staticmethod
    def generate_tickers(risk_tolerance: str, investment_area: str, investment_timeframe: str) -> list[str]:
        """
        Generate a list ot tickers using the GPT API based on the user parameters

        :param risk_tolerance: the risk tolerance of the user (high, moderate, low)
        :param investment_area: the different area where the user wants to invest (tech, commodities, ...)
        :param investment_timeframe: the investment timeframe of the user (short term, long term)
        :return: list of tickers
        """

        prompt = Prompt.generate_stock_recommendation_prompt(risk_tolerance, investment_area, investment_timeframe)
        response = ApiGpt.call_gpt(prompt=prompt)
        extracted_response = ApiGpt.extract_text_between_tags(response, '[stocks]', '[/stocks]')

        tickers = ast.literal_eval(extracted_response)

        return tickers
