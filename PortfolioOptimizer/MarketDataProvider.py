import logging
from abc import ABC, abstractmethod
import yfinance as yf
import pandas as pd
from typing import List, Any, Dict


class MarketDataProvider(ABC):
    @abstractmethod
    def get_data(self, tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
        pass


class YFinanceDataProvider(MarketDataProvider):
    def get_data(self, tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
        try:
            data = yf.download(tickers, start=start_date, end=end_date)
            return data['Adj Close']
        except Exception as e:
            logging.error(f"Error fetching data for {tickers} from {start_date} to {end_date}: {e}")
        raise ValueError("Failed to fetch data. Please check your tickers and date range.")