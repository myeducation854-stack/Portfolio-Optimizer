
'''
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
'''

from src.stock import stock
from src.stock_math_service import stock_math_service
import yfinance
import pandas as pd
import numpy as np

from datetime import date
from dateutil.relativedelta import relativedelta

if __name__ == "__main__":

    symbol = "PLTR"
    stockc = stock(symbol)
    expected_market_return = stock_math_service.get_monthly_expected_market_return()
    risk_free = stock_math_service.get_annual_risk_free_rate()

    print(f"beta is {stock_math_service.calculate_monthly_stock_beta(stockc,period="5y",interval="1mo")}")
    print(risk_free)

    ticker = yfinance.Ticker(symbol)
    yfinance_beta = ticker.info.get('beta')
    print(f"Yahoo Finance beta: {yfinance_beta:.2f}")

    #annual_expected_return = (1 + expected_market_return) ** 12 - 1

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
    '''
    