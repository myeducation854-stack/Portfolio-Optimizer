import pandas as pd
url: str = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

tables = pd.read_html(url, storage_options=headers)

sp500_df = tables[0]

tickers = sp500_df['Symbol'].tolist()
print(len(tickers))

tickers_df = pd.DataFrame({'Ticker': tickers})
tickers_df.to_csv('stock_tickers.csv', index=False)