from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail
from tickers_loader import load_tickers


def score_pattern(close, volume):

    score = 50

    ma25 = close.rolling(25).mean()
    ma75 = close.rolling(75).mean()

    if ma25.iloc[-1] > ma75.iloc[-1]:
        score += 15

    if close.iloc[-1] > ma25.iloc[-1]:
        score += 10

    vol20 = volume.tail(20).mean()

    if volume.iloc[-1] > vol20:
        score += 15

    momentum = (
        (close.iloc[-1] - close.iloc[-20])
        / close.iloc[-20]
    ) * 100

    score += min(max(int(momentum), 0), 10)

    return min(score, 100)


def run():

    tickers = load_tickers()

    candidates = []

    for ticker, name in tickers.items():

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"]
            volume = df["Volume"]

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

        except:
            pass

    candidates.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    body = "【TOPIX500 パターンスキャン】\n\n"

    body += f"監視銘柄数: {len(tickers)}\n\n"

    if not candidates:

        body += "該当なし"

    else:

        for score, ticker, name, pattern in candidates[:30]:

            body += (
                f"{ticker} "
                f"{name}\n"
                f"{pattern}\n"
                f"スコア:{score}\n\n"
            )

    send_mail(body)


if __name__ == "__main__":
    run()
