from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail
from tickers_loader import load_tickers


def score_stock(df):

    score = 50

    try:

        close = df["Close"].astype(float)

        if len(close) >= 75:

            ma25 = close.rolling(25).mean()
            ma75 = close.rolling(75).mean()

            if ma25.iloc[-1] > ma75.iloc[-1]:
                score += 15

            if close.iloc[-1] > ma25.iloc[-1]:
                score += 15

        if "Volume" in df.columns:

            volume = df["Volume"].astype(float)

            if len(volume) >= 20:

                vol20 = volume.tail(20).mean()

                if vol20 > 0 and volume.iloc[-1] > vol20:
                    score += 10

        if len(close) >= 20:

            momentum = (
                (close.iloc[-1] - close.iloc[-20])
                / close.iloc[-20]
            ) * 100

            score += min(max(int(momentum), 0), 10)

    except Exception as e:

        print(f"score error: {e}")

    return int(score)


def run():

    tickers = load_tickers()

    candidates = []

    for ticker, name in tickers.items():

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"]

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

            candidates.append(
                (
                    score,
                    ticker,
                    name,
                    ",".join(patterns)
                )
            )

        except Exception as e:

            print(f"error {ticker}: {e}")

    candidates.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    body = "【TOPIX500 有力候補ランキング】\n\n"

    body += f"監視銘柄数: {len(tickers)}\n"
    body += f"候補数: {len(candidates)}\n\n"

    for rank, item in enumerate(candidates[:20], start=1):

        score, ticker, name, pattern = item

        body += (
            f"{rank}位\n"
            f"{ticker} {name}\n"
            f"{pattern}\n"
            f"スコア:{score}\n\n"
        )

    send_mail(body)


if __name__ == "__main__":
    run()
