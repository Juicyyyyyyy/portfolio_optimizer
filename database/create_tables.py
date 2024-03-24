from .models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))

# Create a Session class and bind it to the engine
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)
