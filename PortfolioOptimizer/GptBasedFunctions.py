from typing import List

from ChatGPT.ApiGpt import ApiGpt
from ChatGPT.Prompt import Prompt

import ast
import markdown


class GptBasedFunctions:
    @staticmethod
    def generate_tickers(risk_tolerance: str, investment_area: str, investment_timeframe: str) -> List[str]:
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

    @staticmethod
    def generate_tickers_review(tickers: str):
        """
        :param tickers: a list of tickers name in str format
        :return: a short review of each ticker in Markdown -> HTML format
        """
        prompt = Prompt.generate_stock_review_prompt(tickers)
        response = ApiGpt.call_gpt(prompt=prompt)
        extracted_response = ApiGpt.extract_text_between_tags(response, '<stocks-reviews>', '</stocks-reviews>')

        return markdown.markdown(extracted_response)


