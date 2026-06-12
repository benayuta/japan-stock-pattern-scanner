from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail
from tickers_loader import load_tickers


def run():

    tickers = load_tickers()

    candidates = []

    for ticker, name in tickers.items():

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"].squeeze()

            if len(close) < 75:
                continue

            ma25 = close.rolling(25).mean()
            ma75 = close.rolling(75).mean()

            patterns = []

            if detect_inverse_head_shoulders(close):
                patterns.append("逆三尊")

            if detect_double_bottom(close):
                patterns.append("ダブルボトム")

            if detect_ascending_triangle(close):
                patterns.append("上昇トライアングル")

            if not patterns:
                continue

            score = 0

            if close.iloc[-1] > ma25.iloc[-1]:
                score += 1

            if ma25.iloc[-1] > ma75.iloc[-1]:
                score += 1

            if score == 0:
                continue

            candidates.append(
                (
                    score,
                    ticker,
                    name,
                    ",".join(patterns)
                )
            )

        except Exception as e:
            print(f"{ticker}: {e}")

    candidates.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    body = "【TOPIX500 ブレイクアウト候補】\n\n"

    body += f"監視銘柄数: {len(tickers)}\n"
    body += f"候補数: {len(candidates)}\n\n"

    for rank, item in enumerate(candidates[:30], start=1):

        score, ticker, name, pattern = item

        body += (
            f"{rank}位\n"
            f"{ticker} {name}\n"
            f"{pattern}\n"
            f"条件達成数:{score}/2\n\n"
        )

    send_mail(body)


if __name__ == "__main__":
    run()
