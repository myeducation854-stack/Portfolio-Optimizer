import yfinance;
import pandas as pd;

class stock:

    def __init__(self, ticker: str):
        self.ticker_str: str = ticker
        self.ticker: yfinance.Ticker = yfinance.Ticker(ticker)
        
    def get_monthly_prices(self, period: str="10y", interval: str="1mo") -> pd.DataFrame:
        history: pd.DataFrame = self.ticker.history(period=period,interval=interval)
        eom_prices: pd.DataFrame = history.resample('ME').last()
        #eom_prices = history
        eom_prices = eom_prices.drop(axis=1,columns=["Open","High","Low","Stock Splits", "Volume", "Dividends"]).dropna()
        return eom_prices
    
    def get_monthly_returns(self, period: str="10y", interval: str="1mo") -> pd.Series:
        t = self.get_monthly_prices(period=period,interval=interval).pct_change()["Close"]
        return t
        