import pandas as pd
import yfinance

risk_free_rate: float = 0.0419

class stock_math_service:

    @staticmethod
    def get_market_returns(interval: str="1mo", period: str="10y"):
        ticker = yfinance.Ticker("^GSPC")
        history: pd.DataFrame = ticker.history(period=period,interval=interval)
        history = history.resample('ME').last()
        #print(history["Close"].pct_change())
        return history["Close"].pct_change()

    @staticmethod
    def calculate_stock_beta(stock_returns: pd.Series, market_returns: pd.Series):
        return stock_returns.cov(market_returns) / market_returns.var()
    
    @staticmethod
    def calculate_expected_returns() -> pd.Series:
        