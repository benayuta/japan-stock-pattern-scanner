from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail

# テスト用100銘柄版（まず安定動作確認）
TICKERS = [
    "1301.T","1332.T","1333.T","1605.T","1721.T",
    "1801.T","1802.T","1803.T","1808.T","1812.T",
    "1925.T","1928.T","1963.T","2002.T","2269.T",
    "2282.T","2413.T","2501.T","2502.T","2503.T",
    "2768.T","2801.T","2802.T","2871.T","2914.T",
    "3086.T","3099.T","3382.T","3401.T","3402.T",
    "3861.T","3863.T","4004.T","4005.T","4021.T",
    "4042.T","4063.T","4183.T","4188.T","4208.T",
    "4324.T","4452.T","4502.T","4503.T","4506.T",
    "4519.T","4523.T","4543.T","4568.T","4578.T",
    "4689.T","4704.T","4751.T","4901.T","4902.T",
    "4911.T","5020.T","5101.T","5108.T","5201.T",
    "5332.T","5333.T","5401.T","5406.T","5411.T",
    "5711.T","5713.T","5801.T","5802.T","5803.T",
    "6098.T","6178.T","6301.T","6302.T","6367.T",
    "6501.T","6503.T","6504.T","6594.T","6701.T",
    "6723.T","6752.T","6758.T","6762.T","6902.T",
    "6954.T","6971.T","6981.T","7011.T","7012.T",
    "7013.T","7201.T","7203.T","7261.T","7267.T"
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
                results.append(f"{ticker} ダブルボトム")

            if detect_inverse_head_shoulders(close):
                results.append(f"{ticker} 逆三尊")

            if detect_ascending_triangle(close):
                results.append(f"{ticker} 上昇トライアングル")

        except Exception as e:
            print(f"ERROR {ticker}: {e}")

    body = "\n".join(results) if results else "本日は該当銘柄なし"

    send_mail(body)


if __name__ == "__main__":
    run()
