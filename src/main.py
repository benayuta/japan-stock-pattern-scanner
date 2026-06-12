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

    error_count = 0

    for ticker, name in tickers.items():

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"]
            volume = df["Volume"]

            patterns = []

            if detect_inverse_head_shoulders(close):
                patterns.append("逆三尊")

            if detect_double_bottom(close):
                patterns.append("ダブルボトム")

            if detect_ascending_triangle(close):
                patterns.append("上昇トライアングル")

            if patterns:

                candidates.append(
                    f"{ticker} {name} {'/'.join(patterns)}"
                )

        except Exception as e:

            error_count += 1

    body = f"""
【診断２】

監視銘柄数: {len(tickers)}

候補数: {len(candidates)}

エラー数: {error_count}

"""

    body += "\n".join(candidates[:20])

    send_mail(body)


if __name__ == "__main__":
    run()
