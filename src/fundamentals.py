import yfinance as yf
from datetime import datetime


def get_fundamentals(ticker):

    try:

        info = yf.Ticker(ticker).info

        dividend_yield = info.get(
            "dividendYield",
            None
        )

        if dividend_yield is not None:
            dividend_yield = round(
                dividend_yield * 100,
                2
            )

        ex_dividend = info.get(
            "exDividendDate",
            None
        )

        month = "-"

        if ex_dividend:

            month = datetime.fromtimestamp(
                ex_dividend
            ).strftime("%Y-%m")

        return {
            "yield": dividend_yield,
            "month": month
        }

    except Exception:

        return {
            "yield": None,
            "month": "-"
        }
