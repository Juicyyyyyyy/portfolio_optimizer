import logging
import yfinance as yf
import pandas as pd
from typing import List, Any, Dict


class MarketDataProvider:
    @staticmethod
    def get_data(tickers: List[str] or str, start_date: str = None, end_date: str = None, period: str = None,
                 frequency: str = 'Adj Close') -> pd.DataFrame:
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