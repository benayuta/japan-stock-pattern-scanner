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

    inverse_count = 0
    double_count = 0
    triangle_count = 0

    samples = []

    for ticker, name in tickers.items():

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            close = df["Close"]

            if detect_inverse_head_shoulders(close):

                inverse_count += 1

                if len(samples) < 10:
                    samples.append(
                        f"{ticker} {name} 逆三尊"
                    )

            if detect_double_bottom(close):

                double_count += 1

                if len(samples) < 10:
                    samples.append(
                        f"{ticker} {name} ダブルボトム"
                    )

            if detect_ascending_triangle(close):

                triangle_count += 1

                if len(samples) < 10:
                    samples.append(
                        f"{ticker} {name} 上昇トライアングル"
                    )

        except Exception as e:
            print(e)

    body = f"""
【診断モード】

監視銘柄数: {len(tickers)}

逆三尊: {inverse_count}
ダブルボトム: {double_count}
上昇トライアングル: {triangle_count}

--- サンプル ---

{chr(10).join(samples)}
"""

    print(body)

    send_mail(body)


if __name__ == "__main__":
    run()
