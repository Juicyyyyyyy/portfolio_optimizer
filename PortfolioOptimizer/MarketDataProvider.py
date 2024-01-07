import logging
import yfinance as yf
import pandas as pd
from typing import List, Union, Any, Dict


class MarketDataProvider:
    @staticmethod
    def get_data(tickers: Union[List[str], str], start_date: str = None, end_date: str = None, period: str = None,
                 frequency: str = 'Adj Close') -> pd.DataFrame:
        """
        Fetches stock market data for specified tickers using Yahoo Finance API.

            :param tickers: A list of stock ticker symbols or a single ticker symbol as string.
            :param start_date: The start date for data fetching in 'YYYY-MM-DD' format.
            :param end_date: The end date for data fetching in 'YYYY-MM-DD' format.
            :param period: The period for data fetching as a string. Overrides start_date and end_date if provided.
                           Examples of valid periods include '1d', '1mo', '1y', etc.
            :param frequency: The data frequency to fetch. Default is 'Adj Close', but can be any column name returned by
                              yfinance such as 'Open', 'Close', 'High', 'Low', 'Volume'.
            :return: A pandas DataFrame containing the fetched data with dates as index and tickers as columns.
        """
        try:
            # Decide whether to use period or start and end dates
            if period:
                data = yf.download(tickers, period=period)
            else:
                if not start_date or not end_date:
                    raise ValueError("Start date and end date must be specified if not using period.")
                data = yf.download(tickers, start=start_date, end=end_date)
            return data[frequency]
        except Exception as e:
            logging.error(f"Error fetching data for {tickers} from {start_date} to {end_date}: {e}")
            raise