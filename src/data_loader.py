import yfinance as yf
import pandas as pd

def get_stock_data(ticker):
    try:
        df = yf.download(
            ticker,
            period="12mo",
            interval="1d",
            auto_adjust=True,
            progress=False
        )
        return df
    except Exception:
        return pd.DataFrame()
