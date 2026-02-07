
'''
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
'''

from src.stock import stock
from src.stock_math_service import stock_math_service
from src.risky_portfolio import risky_portfolio
import yfinance
import pandas as pd
import numpy as np

from datetime import date
from dateutil.relativedelta import relativedelta
from pypfopt import EfficientFrontier, risk_models, expected_returns, plotting
import matplotlib.pyplot as plt

if __name__ == "__main__":

    '''
    stock_list: list[stock] = [
        stock("PLTR"),
        stock("NVDA"),
        stock("AMZN")
    ]
    rp = risky_portfolio(stocks=stock_list, budget=100)
    mu = rp.get_expected_returns(period="5y", interval="1mo")
    print("Expected Returns:")
    print(mu)
    
    df = rp.get_prices(period="5y", interval="1mo")
    print("\n=== PRICE DATA ===")
    print(f"Shape: {df.shape}")
    print("First 5 rows:")
    print(df.head())
    print("\nPrice statistics:")
    print(df.describe())
    
    # Calculate returns manually
    returns = df.pct_change().dropna()
    print("\n=== RETURNS DATA ===")
    print(f"Shape: {returns.shape}")
    print("First 5 returns:")
    print(returns.head())
    print("\nReturns statistics:")
    print(returns.describe())
    
    # Manual variance (this should be ~0.02-0.04)
    print("\n=== MANUAL CALCULATIONS ===")
    print("Manual variance (should be ~0.02-0.04):")
    print(returns.var())
    
    print("\nManual standard deviation (should be ~0.10-0.15):")
    print(returns.std())
    
    # Manual covariance
    manual_cov = returns.cov()
    print("\nManual covariance matrix:")
    print(manual_cov)
    
    # Try with returns_data=True
    print("\n=== PYPORTFOLIOOPT WITH returns_data=True ===")
    S_correct = risk_models.CovarianceShrinkage(returns, returns_data=True).ledoit_wolf()
    print("Covariance matrix (with returns_data=True):")
    print(S_correct)
    
    # What you're currently doing (wrong)
    print("\n=== PYPORTFOLIOOPT WITH PRICES (WRONG) ===")
    S_wrong = risk_models.CovarianceShrinkage(df, frequency=12).ledoit_wolf()
    print("Covariance matrix (with prices - WRONG):")
    print(S_wrong)
    
    # Show the difference
    print("\n=== COMPARISON ===")
    print("PLTR variance:")
    print(f"  Manual: {returns['PLTR'].var():.6f}")
    print(f"  Correct method: {S_correct.loc['PLTR', 'PLTR']:.6f}")
    print(f"  Wrong method: {S_wrong.loc['PLTR', 'PLTR']:.6f}")
    
    # Use the CORRECT covariance
    print("\n=== OPTIMIZATION WITH CORRECT COVARIANCE ===")
    S = S_correct  # Use the correct one!
    
    ef = EfficientFrontier(mu, S)
    rfm = stock_math_service.get_monthly_risk_free_rate()
    weights_sharpe = ef.max_sharpe(risk_free_rate=rfm)
    print("\nMax Sharpe weights:")
    print(ef.clean_weights())
    
    ef = EfficientFrontier(mu, S)
    weights_minvol = ef.min_volatility()
    print("\nMin Volatility weights:")
    print(ef.clean_weights())
    '''

    
    stock_list: list[stock] = [
        stock("PLTR"),
        stock("NVDA"),
        stock("AMZN")
    ]
    rp = risky_portfolio(stocks=stock_list,budget=100)
    mu = rp.get_expected_returns(period="5y",interval="1mo")
    print(mu)
    df = rp.get_prices(period="5y",interval="1mo")
    #returns = df.pct_change().dropna()
    print(df)
    returns = df.pct_change().dropna()
    S = risk_models.CovarianceShrinkage(returns, returns_data=True, frequency=12).ledoit_wolf()
    print(S)
    ef = EfficientFrontier(mu,S)

    rfm = stock_math_service.get_monthly_risk_free_rate()
    weights = ef.max_sharpe(risk_free_rate=rfm)
    print(weights)
    ef = EfficientFrontier(mu,S)
    print(ef.min_volatility())


    '''
    today = date.today()
    ten_years_ago = today - relativedelta(years=10)
    stock_ticker = "PLTR"
    market_ticker = "^GSPC"

    # Download adjusted close prices
    stock_data = yfinance.download(stock_ticker, start=ten_years_ago, end=today)['Close']
    market_data = yfinance.download(market_ticker, start=ten_years_ago, end=today)['Close']

    # Align by date
    data = pd.concat([stock_data, market_data], axis=1).dropna()
    data.columns = ['Stock', 'Market']

    # Calculate daily returns
    returns = data.pct_change().dropna()

    # Calculate beta
    beta = returns['Stock'].cov(returns['Market']) / returns['Market'].var()
    print(f"The beta of {stock_ticker} is: {beta:.2f}")







    symbol = "PLTR"
    stockc = stock(symbol)
    expected_market_return = stock_math_service.get_monthly_expected_market_return()
    risk_free = stock_math_service.get_annual_risk_free_rate()

    print(f"beta is {stock_math_service.calculate_monthly_stock_beta(stockc,period="5y",interval="1mo")}")
    print(risk_free)

    ticker = yfinance.Ticker(symbol)
    yfinance_beta = ticker.info.get('beta')
    print(f"Yahoo Finance beta: {yfinance_beta:.2f}")
    '''
    