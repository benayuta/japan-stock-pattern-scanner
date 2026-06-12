import yfinance as yf


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

        dividend_month = info.get(
            "exDividendDate",
            None
        )

        return {
            "yield": dividend_yield,
            "month": dividend_month
        }

    except:

        return {
            "yield": None,
            "month": None
        }
