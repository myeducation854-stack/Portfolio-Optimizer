import yfinance;
import pandas as pd;

class stock:

    def __init__(self, ticker: str):
        self.ticker = yfinance.Ticker(ticker)
        self.__interval = "1mo"
        self.__period = "10y"
        
    def get_monthly_prices(self):
        history: pd.DataFrame = self.ticker.history(period=self.__period,interval=self.__interval)
        eom_prices: pd.DataFrame = history.resample('ME').last()
        eom_prices = eom_prices.drop(axis=1,columns=["Open","High","Low","Stock Splits", "Volume", "Dividends"]).dropna()
        #eom_prices["Return"] = eom_prices["Close"].pct_change()
        return eom_prices
    
    def get_monthly_returns(self):
        return self.get_monthly_prices().pct_change()
        