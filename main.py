from src.stock import stock
from src.stock_math_service import stock_math_service
import yfinance
import pandas as pd

if __name__ == "__main__":
    ticker = yfinance.Ticker("^GSPC")
    history: pd.DataFrame = ticker.history(period="10y",interval="1mo")
    history = history.drop(axis=1,columns=["Open","High","Low","Stock Splits", "Volume", "Dividends"]) 
    history = history.resample('ME').last()

    stockc = stock("AAPL")

    test = stock_math_service.calculate_monthly_stock_beta(stockc)
    print(test)
