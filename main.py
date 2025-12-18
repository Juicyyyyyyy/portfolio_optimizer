from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
import numpy as np
import json
import logging

from PortfolioOptimizer.HRPCalculator import HRPCalculator
from PortfolioOptimizer.BlackLitterman import BlackLitterman
from PortfolioOptimizer.MonteCarloSimulator import MonteCarloSimulator
from PortfolioOptimizer.ExpectedReturnCalculator import MeanHistoricalReturnCalculator
from PortfolioOptimizer.CovarianceCalculator import SampleCovarianceCalculator
from PortfolioOptimizer.MarketDataProvider import MarketDataProvider
from PortfolioOptimizer.EfficientFrontierCalculator import EfficientFrontierCalculator


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
    strategy: str = "max_sharpe" # Options: max_sharpe, hrp, black_litterman, min_volatility
    views: Optional[List[dict]] = None # List of views for Black-Litterman
    constraints: Optional[Dict[str, float]] = None # Max weight constraints (e.g., {"GLD": 0.15})

class SimulationRequest(BaseModel):
    tickers: List[str]
    weights: dict
    start_date: str
    end_date: str
    initial_portfolio_value: float = 10000.0
    num_simulations: int = 1000
    time_horizon: int = 252


@app.post("/api/analyze")
async def analyze_portfolio(request: TickerRequest):
    try:
        logger.info(f"Analyzing tickers: {request.tickers} with strategy: {request.strategy}")
        
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

        cleaned_weights = {}
        performance = (0.0, 0.0, 0.0)

        if request.strategy == "hrp":
            hrp = HRPCalculator(prices_df)
            cleaned_weights = hrp.calculate_weights(constraints=request.constraints)
            performance = hrp.calculate_performance(risk_free_rate=request.risk_free_rate)
        
        elif request.strategy == "black_litterman":
            # Pass user views to BlackLitterman
            # Views should be a list of dicts, e.g., [{'type': 'absolute', 'asset': 'AAPL', 'return': 0.10}]
            views = request.views if request.views else []
            bl = BlackLitterman(prices_df, valid_tickers, views=views, total_portfolio_value=request.investment_amount)
            cleaned_weights, exp_ret, vol, sharpe = bl.optimize_with_black_litterman()
            performance = (exp_ret, vol, sharpe)
            
        elif request.strategy == "min_volatility":
            ef = EfficientFrontierCalculator(prices_df)
            cleaned_weights = ef.calculate_min_volatility_weights()
            performance = ef.calculate_efficient_frontier_performance(risk_free_rate=request.risk_free_rate)

        else: # Default to max_sharpe
            ef = EfficientFrontierCalculator(prices_df)
            cleaned_weights = ef.calculate_efficient_frontier_weights(risk_free_rate=request.risk_free_rate)
            performance = ef.calculate_efficient_frontier_performance(risk_free_rate=request.risk_free_rate)

        # Calculate Sortino Ratio
        # Sortino = (R - Rf) / Downside Deviation
        # We need daily returns for this
        daily_returns = prices_df.pct_change().dropna()
        portfolio_returns = daily_returns.dot(pd.Series(cleaned_weights))
        
        # Downside deviation
        target_return = 0
        downside_returns = portfolio_returns[portfolio_returns < target_return]
        downside_std = downside_returns.std() * np.sqrt(252) # Annualized
        
        expected_return = performance[0]
        sortino_ratio = (expected_return - request.risk_free_rate) / downside_std if downside_std > 0 else 0.0

        # Calculate VaR and CVaR (Monte Carlo Method, 95% confidence)
        # Simulate 10,000 daily returns based on portfolio mu and sigma
        mu_daily = performance[0] / 252
        sigma_daily = performance[1] / np.sqrt(252)
        
        # Generate 10,000 hypothetical daily returns
        simulated_returns = np.random.normal(mu_daily, sigma_daily, 10000)
        
        var_95 = np.percentile(simulated_returns, 5)
        cvar_95 = simulated_returns[simulated_returns <= var_95].mean()
        
        # Prepare response data
        response_data = {
            "weights": cleaned_weights,
            "performance": {
                "expected_return": performance[0],
                "volatility": performance[1],
                "sharpe_ratio": performance[2],
                "sortino_ratio": sortino_ratio,
                "var_95": var_95,
                "cvar_95": cvar_95
            },
            "valid_tickers": valid_tickers,
            "allocation": {
                ticker: weight * request.investment_amount 
                for ticker, weight in cleaned_weights.items() if weight > 0
            }
        }
        
        return response_data

    except Exception as e:
        logger.error(f"Error analyzing portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate")
async def simulate_portfolio(request: SimulationRequest):
    try:
        logger.info(f"Simulating portfolio for tickers: {request.tickers}")
        
        # 1. Download Data (Need historical data for mean returns and covariance)
        market_data_provider = MarketDataProvider()
        prices_df = market_data_provider.get_data(
            tickers=request.tickers,
            start_date=request.start_date,
            end_date=request.end_date
        )
        
        if prices_df.empty:
             raise HTTPException(status_code=400, detail="No data found for simulation.")

        # 2. Calculate Mean Returns and Covariance
        # Using Mean Historical Return for simplicity in simulation
        mu = MeanHistoricalReturnCalculator().calculate_expected_return(prices_df)
        S = SampleCovarianceCalculator().calculate_covariance(prices_df)
        
        # 3. Run Simulation
        simulator = MonteCarloSimulator(mu, S, request.weights, request.initial_portfolio_value)
        results = simulator.simulate(num_simulations=request.num_simulations, time_horizon=request.time_horizon)
        
        return results

    except Exception as e:
        logger.error(f"Error simulating portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Error analyzing portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')
