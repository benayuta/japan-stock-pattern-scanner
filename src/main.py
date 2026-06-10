from data_loader import get_stock_data

from patterns import (
    detect_double_bottom,
    detect_inverse_head_shoulders,
    detect_ascending_triangle
)

from mailer import send_mail

TICKERS = {
    "7203.T": "トヨタ自動車",
    "6758.T": "ソニーグループ",
    "9984.T": "ソフトバンクグループ",
    "8035.T": "東京エレクトロン",
    "6501.T": "日立製作所",
    "7011.T": "三菱重工業",
    "8306.T": "三菱UFJFG",
    "9983.T": "ファーストリテイリング",
    "9432.T": "NTT",
    "8058.T": "三菱商事"
}


def score_pattern(close):

    recent = close.tail(20)

    high = recent.max()
    low = recent.min()

    if low == 0:
        return 0

    score = int(((high - low) / low) * 100)

    return min(score, 100)


def run():

    inverse_list = []
    double_list = []
    triangle_list = []

    for ticker, name in TICKERS.items():

        print(f"checking {ticker}")

        try:

            df = get_stock_data(ticker)

            if df.empty:
                continue

            if "Close" not in df.columns:
                continue

            close = df["Close"]

            score = score_pattern(close)

            if detect_inverse_head_shoulders(close):
                inverse_list.append(
                    f"{ticker} {name} 信頼度:{score}"
                )

            if detect_double_bottom(close):
                double_list.append(
                    f"{ticker} {name} 信頼度:{score}"
                )

            if detect_ascending_triangle(close):
                triangle_list.append(
                    f"{ticker} {name} 信頼度:{score}"
                )

        except Exception as e:
            print(e)

    body = "【日本株パターンスキャン】\n\n"

    body += "■逆三尊\n"

    if inverse_list:
        body += "\n".join(inverse_list)
    else:
        body += "該当なし"

    body += "\n\n■ダブルボトム\n"

    if double_list:
        body += "\n".join(double_list)
    else:
        body += "該当なし"

    body += "\n\n■上昇トライアングル\n"

    if triangle_list:
        body += "\n".join(triangle_list)
    else:
        body += "該当なし"

    send_mail(body)


if __name__ == "__main__":
    run()
