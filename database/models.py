from sqlalchemy import Column, Integer, String, Sequence, ARRAY, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    assets_weights = Column(JSON)  # JSON of assets that compose the portfolio and their corresponding weights
    expected_return = Column(Float)
    expected_volatility = Column(Float)
    sharpe_ratio = Column(Float)
    portfolio_value = Column(Float)
    assets_review = Column(Text)
    date_created = Column(DateTime, default=datetime.utcnow)
