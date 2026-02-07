import pandas as pd
import yfinance
from src.stock import stock

class stock_math_service:

    @staticmethod
    def get_market_returns(interval: str="1mo", period: str="5y"):
        ticker = yfinance.Ticker("^GSPC")
        history: pd.DataFrame = ticker.history(period=period,interval=interval)
        history = history.resample('ME').last()
        return history["Close"].pct_change()

    @staticmethod
    def calculate_monthly_stock_beta(stock: stock, interval: str="1mo", period: str="5y") -> float:
        monthly_stock_returns: pd.Series = stock.get_monthly_returns(period=period,interval=interval)
        monthly_market_returns: pd.Series = stock_math_service.get_market_returns(period=period,interval=interval)
        returns = pd.concat([monthly_stock_returns, monthly_market_returns], axis=1).dropna()
        returns.columns = ['Stock', 'Market']
        beta = returns['Stock'].cov(returns['Market']) / returns['Market'].var()
        return beta
    
    @staticmethod
    def get_annual_risk_free_rate(period: str="5y") -> float:
        tnx = yfinance.Ticker("^TNX")
        data = tnx.history(period=period)
        latest_yield: float = data["Close"].iloc[-1] / 100
        return latest_yield
    
    @staticmethod
    def get_monthly_risk_free_rate(period: str="5y", interval: int=1) -> float:
        rfa = stock_math_service.get_annual_risk_free_rate(period=period) 
        rf_monthly = (1 + rfa) ** (interval/12) - 1
        return rf_monthly

    @staticmethod
    def get_monthly_expected_market_return(interval: str="1mo", period: str="5y") -> float:
        return stock_math_service.get_market_returns(interval=interval,period=period).mean()
    
    @staticmethod
    def calculate_monthly_expected_return(
        stock: stock,
        period: int,
        period_unit: str,
        interval: int,
        interval_unit: str
    ) -> float:

        VALID_PERIODS = ("1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max")
        VALID_INTERVALS = ("1d","5d","1wk","1mo","3mo")
        
        if (not interval or not period):
            raise ValueError("period nor interval can be None")
        if (not interval_unit or not period_unit):
            raise ValueError("period_unit nor interval_unit can be None")
        
        passed_interval = str(interval) + interval_unit
        passed_period = str(period) + period_unit
        
        if passed_period not in VALID_PERIODS:
            raise ValueError(f"Invalid period")

        if passed_interval not in VALID_INTERVALS:
            raise ValueError(f"Invalid interval")
        
        beta: float = stock_math_service.calculate_monthly_stock_beta(stock,interval=passed_interval,period=passed_period)

        annual_risk_free_rate: float = stock_math_service.get_annual_risk_free_rate(period=passed_period)
        adjusted_risk_free_rate: float
        if (interval_unit == "d"):
            adjusted_risk_free_rate = (1 + annual_risk_free_rate) ** (interval/365) - 1
        elif (interval_unit == "wk"):
            adjusted_risk_free_rate = (1 + annual_risk_free_rate) ** (interval/52) - 1
        else:
            adjusted_risk_free_rate = (1 + annual_risk_free_rate) ** (interval/12) - 1
    
        expected_market_return: float = stock_math_service.get_monthly_expected_market_return(interval=passed_interval,period=passed_period)
        market_risk_premium: float = expected_market_return - adjusted_risk_free_rate

        return adjusted_risk_free_rate + (beta * market_risk_premium)
    


        '''
        monthly_stock_returns: pd.Series = stock.get_monthly_returns()
        monthly_market_returns: pd.Series = stock_math_service.get_market_returns()
        return monthly_stock_returns.cov(monthly_market_returns) / monthly_market_returns.var()
        '''