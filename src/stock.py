import yfinance;
import pandas as pd;

class stock:

    def __init__(self, ticker: str):
        self.ticker = yfinance.Ticker(ticker)
        
    def get_monthly_prices(self, period: str="10y", interval: str="1mo") -> pd.DataFrame:
        history: pd.DataFrame = self.ticker.history(period=period,interval=interval)
        eom_prices: pd.DataFrame = history.resample('ME').last()
        eom_prices = eom_prices.drop(axis=1,columns=["Open","High","Low","Stock Splits", "Volume", "Dividends"]).dropna()
        return eom_prices
    
    def get_monthly_returns(self, period: str="10y", interval: str="1mo") -> pd.Series:
        t = self.get_monthly_prices(period=period,interval=interval).pct_change().iloc[:,0]
        return t
        