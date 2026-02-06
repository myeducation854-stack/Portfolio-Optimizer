import yfinance;
import pandas as pd;
from stock_math_service import stock_math_service

class stock:

    def __init__(self, ticker: str):
        self.ticker = yfinance.Ticker(ticker)

    def get_prices(self, interval: str="1mo", period: str="10y"):
        history: pd.DataFrame = self.ticker.history(period=period,interval=interval)
        eom_prices: pd.DataFrame = history.resample('ME').last()
        eom_prices = eom_prices.drop(axis=1,columns=["Open","High","Low","Stock Splits", "Volume", "Dividends"]) 
        #eom_prices["Return"] = eom_prices["Close"].pct_change()
        return eom_prices
    
    def get_returns(self, prices: pd.Series):
        return prices.pct_change()
        