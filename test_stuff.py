
'''
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
'''

import yfinance as yf
import pandas as pd
import numpy as np

from src.stock import stock
from src.stock_math_service import stock_math_service
from src.risky_portfolio import risky_portfolio

from datetime import date
from dateutil.relativedelta import relativedelta
from pypfopt import EfficientFrontier, risk_models, expected_returns, plotting
from pypfopt.risk_models import CovarianceShrinkage
import matplotlib.pyplot as plt

if __name__ == "__main__":
    stock_list: list[stock] = [
        stock("NVDA"),
        stock("AMZN"),
        stock("PLTR")
    ]
    rp = risky_portfolio(stocks=stock_list,budget=100)
    mu1 = rp.get_expected_returns(period="5y",interval="1mo")
    mu1_annual = (1 + mu1) ** 12 - 1
    print(mu1_annual)

    '''
    tickers = ['NVDA', 'AMZN', 'PLTR']
    df = yf.download(tickers, start='2020-01-01', end='2024-01-01')['Close']
    mu = mean_historical_return(df)
    print(mu)
    '''


    S = CovarianceShrinkage(rp.get_prices(), frequency=12).ledoit_wolf()
    
    '''
    returns = df.pct_change().dropna()
    '''

    print("Covariance Matrix:")
    print(S)

    ef = EfficientFrontier(mu1_annual, S)
    weights = ef.max_sharpe()
    print("Optimal weights:", ef.clean_weights())   

    ef = EfficientFrontier(mu1_annual, S)
    fig, ax = plt.subplots(figsize=(10, 6))
    plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)

    ax.set_title('Efficient Frontier')
    ax.set_xlabel('Volatility (Risk)')
    ax.set_ylabel('Expected Return')
    ax.legend()
    ax.grid(True)

    plt.show()
   