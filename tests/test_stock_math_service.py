import unittest
import yfinance
import pandas as pd
from src.stock_math_service import stock_math_service
from src.stock import stock

class testStockMathService(unittest.TestCase):

    def test_get_market_returns(self):
        ticker = yfinance.Ticker("^GSPC")
        history: pd.DataFrame = ticker.history(period="10y",interval="1mo")
        history = history.drop(axis=1,columns=["Open","High","Low","Stock Splits", "Volume", "Dividends"]) 

        monthly_market_prices = history.resample('ME').last()

        factor = 10
        expected_return = (monthly_market_prices["Close"].iloc[-1-factor] - monthly_market_prices["Close"].iloc[-2-factor])/monthly_market_prices["Close"].iloc[-2-factor]

        returns = stock_math_service.get_market_returns()
        actual_return = returns.get(returns.size-1-factor)

        self.assertAlmostEqual(expected_return,actual_return)


    def test_calculate_monthly_stock_beta(self):
        test_stock: stock = stock("AAPL")
        print(stock_math_service.calculate_monthly_stock_beta(stock=test_stock))


if __name__ == "__main__":
    unittest.main()