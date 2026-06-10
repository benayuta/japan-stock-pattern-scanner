from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail

TICKERS = [
    "7203.T",
    "6758.T",
    "9984.T",
    "8035.T",
]


def run():

    results = []

    for ticker in TICKERS:

        print(f"checking {ticker}")

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            if "Close" not in df.columns:
                continue

            close = df["Close"]

            if detect_double_bottom(close):
                results.append(
                    f"{ticker} ダブルボトム"
                )

            if detect_inverse_head_shoulders(close):
                results.append(
                    f"{ticker} 逆三尊"
                )

            if detect_ascending_triangle(close):
                results.append(
                    f"{ticker} 上昇トライアングル"
                )

        except Exception as e:
            print(f"ERROR {ticker}: {e}")

    if results:
        body = "\n".join(results)
    else:
        body = "本日は該当銘柄なし"

    print(body)

    send_mail(body)


if __name__ == "__main__":
    run()
