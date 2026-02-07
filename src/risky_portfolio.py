import yfinance 
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from pypfopt import EfficientFrontier, risk_models, expected_returns, plotting
from src.stock_math_service import stock_math_service
from src.stock import stock

class risky_portfolio:

    def __init__(self, stocks: list[stock], budget: float):
        self.stocks: list[stock] = stocks
        self.budget: float = budget

    def get_expected_returns(self,period: str="5y", interval: str="1mo") -> pd.Series:
        ers: list[float] = []
        tickers: list[str] = []
        for stock in self.stocks:
            ers.append(stock_math_service.calculate_monthly_expected_return(
                stock=stock,
                period=int(period[0]),
                period_unit=period[1:],
                interval=int(interval[0]),
                interval_unit=interval[1:]
            ))
            tickers.append(stock.ticker_str)
        return pd.Series(ers,index=tickers)
    
    def get_prices(self, period: str="5y", interval: str="1mo") -> pd.DataFrame:
        price_data = {}
        for stock in self.stocks:
            price_data[stock.ticker_str] = stock.get_monthly_prices(period=period,interval=interval).iloc[:,0]

        df = pd.DataFrame(price_data)
        return df