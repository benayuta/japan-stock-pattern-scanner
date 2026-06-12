from datetime import datetime

from data_loader import get_stock_data
from tickers_loader import load_tickers
from fundamentals import get_fundamentals

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from ta.trend import PSARIndicator


def send_mail(body):

    from mailer import send_mail as mail

    mail(body)


def is_psar_bullish(df):

    try:

        psar = PSARIndicator(
            high=df["High"].squeeze(),
            low=df["Low"].squeeze(),
            close=df["Close"].squeeze()
        )

        psar_values = psar.psar()

        close = df["Close"].squeeze()

        return close.iloc[-1] > psar_values.iloc[-1]

    except:

        return False


def score_stock(df):

    score = 0

    close = df["Close"].squeeze()
    volume = df["Volume"].squeeze()

    if len(close) < 75:
        return 0

    ma25 = close.rolling(25).mean()
    ma75 = close.rolling(75).mean()

    if close.iloc[-1] > ma25.iloc[-1]:
        score += 20

    if ma25.iloc[-1] > ma75.iloc[-1]:
        score += 20

    vol20 = volume.tail(20).mean()

    if vol20 > 0 and volume.iloc[-1] > vol20 * 1.2:
        score += 20

    high52 = close.tail(252).max()

    if close.iloc[-1] >= high52 * 0.95:
        score += 20

    if is_psar_bullish(df):
        score += 20

    return score


def run():

    tickers = load_tickers()

    candidates = []

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    for ticker, name in tickers.items():

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"].squeeze()

            current_price = round(
                float(close.iloc[-1]),
                2
            )

            prev_price = round(
                float(close.iloc[-2]),
                2
            )

            change_pct = round(
                (
                    current_price
                    - prev_price
                )
                / prev_price
                * 100,
                2
            )

            patterns = []

            if detect_inverse_head_shoulders(close):
                patterns.append("逆三尊")

            if detect_double_bottom(close):
                patterns.append("ダブルボトム")

            if detect_ascending_triangle(close):
                patterns.append("上昇トライアングル")

            if not patterns:
                continue

            score = score_stock(df)

            if score < 40:
                continue

            fund = get_fundamentals(
                ticker
            )

            candidates.append(
                (
                    score,
                    ticker,
                    name,
                    ",".join(patterns),
                    current_price,
                    change_pct,
                    fund["yield"],
                    fund["month"]
                )
            )

        except Exception as e:

            print(e)

    candidates.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    body = (
        f"【TOPIX500 有力候補 V7】\n"
        f"作成日:{today}\n\n"
    )

    body += (
        f"監視銘柄数:{len(tickers)}\n"
        f"候補数:{len(candidates)}\n\n"
    )

    for rank, item in enumerate(
        candidates[:30],
        start=1
    ):

        (
            score,
            ticker,
            name,
            pattern,
            price,
            change_pct,
            div_yield,
            div_month
        ) = item

        body += (
            f"{rank}位\n"
            f"{ticker} {name}\n"
            f"{pattern}\n"
            f"株価:{price}円\n"
            f"前日比:{change_pct}%\n"
            f"配当利回り:{div_yield}%\n"
            f"配当月:{div_month}\n"
            f"スコア:{score}\n"
            f"https://finance.yahoo.co.jp/quote/{ticker}\n\n"
        )

    send_mail(body)


if __name__ == "__main__":
    run()
