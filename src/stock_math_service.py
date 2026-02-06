import pandas as pd
import yfinance
from stock import stock

class stock_math_service:

    @staticmethod
    def get_market_returns(interval: str="1mo", period: str="10y"):
        ticker = yfinance.Ticker("^GSPC")
        history: pd.DataFrame = ticker.history(period=period,interval=interval)
        history = history.resample('ME').last()
        #print(history["Close"].pct_change())
        return history["Close"].pct_change()

    @staticmethod
    def calculate_monthly_stock_beta(stock: stock) -> float:
        monthly_stock_returns: pd.Series = stock.get_monthly_returns()
        monthly_market_returns: pd.Series = stock_math_service.get_market_returns()
        return monthly_stock_returns.cov(monthly_market_returns) / monthly_market_returns.var()
    
    @staticmethod
    def get_annual_risk_free_rate(period: str="10y") -> float:
        tnx = yfinance.Ticker("^TNX")
        data = tnx.history(period=period)
        latest_yield: float = data["Close"].iloc[-1] / 100 
        return latest_yield


    @staticmethod
    def get_monthly_expected_market_return() -> float:
        return stock_math_service.get_market_returns().mean()
    
    @staticmethod
    def calculate_monthly_expected_return(stock: stock) -> float:
        monthly_beta: float = stock_math_service.calculate_monthly_stock_beta(stock)

        annual_risk_free_rate: float = stock_math_service.get_annual_risk_free_rate()
        monthly_risk_free_rate: float = (1 + annual_risk_free_rate) ** (1/12) - 1

        monthly_expected_market_return: float = stock_math_service.get_monthly_expected_market_return()
        monthly_risk_premium: float = monthly_expected_market_return - monthly_risk_free_rate

        return monthly_risk_free_rate + (monthly_beta * monthly_risk_premium)