from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
import json
import logging

from PortfolioOptimizer.MarketDataProvider import MarketDataProvider
from PortfolioOptimizer.EfficientFrontierCalculator import EfficientFrontierCalculator
from PortfolioOptimizer.GptBasedFunctions import ApiGpt, Prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class TickerRequest(BaseModel):
    tickers: List[str]
    start_date: str
    end_date: str
    risk_free_rate: float = 0.02
    investment_amount: float = 10000.0

class GenerateTickersRequest(BaseModel):
    user_input: str
    number_of_tickers: int = 5

@app.post("/api/generate_tickers")
async def generate_tickers(request: GenerateTickersRequest):
    try:
        api_gpt = ApiGpt()
        prompt = Prompt(request.user_input, request.number_of_tickers)
        tickers = api_gpt.generate_tickers(prompt)
        return {"tickers": tickers}
    except Exception as e:
        logger.error(f"Error generating tickers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_portfolio(request: TickerRequest):
    try:
        logger.info(f"Analyzing tickers: {request.tickers}")
        
        # 1. Download Data
        market_data_provider = MarketDataProvider()
        prices_df, valid_tickers = market_data_provider.get_data(
            tickers=request.tickers,
            start_date=request.start_date,
            end_date=request.end_date,
            return_updated_tickers=True
        )
        
        if prices_df.empty:
            raise HTTPException(status_code=400, detail="No data found for the provided tickers.")

        # 2. Calculate Efficient Frontier
        ef_calculator = EfficientFrontierCalculator(prices_df)
        
        # Optimize for max Sharpe ratio
        cleaned_weights = ef_calculator.calculate_efficient_frontier_weights(risk_free_rate=request.risk_free_rate)
        performance = ef_calculator.calculate_efficient_frontier_performance(risk_free_rate=request.risk_free_rate)
        
        # 3. Generate Ticker Reviews (Optional, can be slow)
        # For now, we'll skip the detailed GPT reviews to keep the response fast, 
        # or we could make it a separate endpoint. 
        # Let's include a simple placeholder or fetch them if needed.
        
        # Prepare response data
        response_data = {
            "weights": cleaned_weights,
            "performance": {
                "expected_return": performance[0],
                "volatility": performance[1],
                "sharpe_ratio": performance[2]
            },
            "valid_tickers": valid_tickers,
            "allocation": {
                ticker: amount * request.investment_amount 
                for ticker, amount in cleaned_weights.items() if amount > 0
            }
        }
        
        return response_data

    except Exception as e:
        logger.error(f"Error analyzing portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')
