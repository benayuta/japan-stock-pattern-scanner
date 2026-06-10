from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail
from tickers import TICKERS


def score_pattern(close, volume):

    score = 0

    ma25 = close.rolling(25).mean()
    ma75 = close.rolling(75).mean()

    if ma25.iloc[-1] > ma75.iloc[-1]:
        score += 30

    if close.iloc[-1] > ma25.iloc[-1]:
        score += 20

    vol20 = volume.tail(20).mean()

    if volume.iloc[-1] > vol20 * 1.5:
        score += 30

    momentum = (
        (close.iloc[-1] - close.iloc[-20])
        / close.iloc[-20]
    ) * 100

    score += min(max(int(momentum), 0), 20)

    return min(score, 100)


def run():

    candidates = []

    for ticker, name in TICKERS.items():

        print(f"checking {ticker}")

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"]
            volume = df["Volume"]

            ma25 = close.rolling(25).mean()
            ma75 = close.rolling(75).mean()

            if len(ma75.dropna()) == 0:
                continue

            if ma25.iloc[-1] <= ma75.iloc[-1]:
                continue

            if close.iloc[-1] <= ma25.iloc[-1]:
                continue

            vol20 = volume.tail(20).mean()

            if volume.iloc[-1] < vol20 * 1.5:
                continue

            pattern = None

            if detect_inverse_head_shoulders(close):
                pattern = "逆三尊"

            elif detect_double_bottom(close):
                pattern = "ダブルボトム"

            elif detect_ascending_triangle(close):
                pattern = "上昇トライアングル"

            if pattern:

                score = score_pattern(
                    close,
                    volume
                )

                candidates.append(
                    (
                        score,
                        ticker,
                        name,
                        pattern
                    )
                )

        except Exception as e:
            print(e)

    candidates.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    body = "【日本株ブレイクアウト監視】\n\n"

    if len(candidates) == 0:

        body += "本日は有力候補なし"

    else:

        for score, ticker, name, pattern in candidates[:10]:

            stars = "★" * max(
                1,
                min(5, score // 20)
            )

            body += (
                f"{stars}\n"
                f"{ticker} {name}\n"
                f"{pattern}\n"
                f"スコア:{score}\n\n"
            )

    send_mail(body)


if __name__ == "__main__":
    run()
