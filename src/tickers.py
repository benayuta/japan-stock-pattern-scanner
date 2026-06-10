import csv
import os


def load_tickers():

    tickers = {}

    csv_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "topix500.csv"
    )

    with open(
        csv_path,
        encoding="cp932"
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            group = row["ニューインデックス区分"]

            if group in [
                "TOPIX Core30",
                "TOPIX Large70",
                "TOPIX Mid400"
            ]:

                ticker = str(
                    row["コード"]
                ) + ".T"

                tickers[ticker] = row["銘柄名"]

    return tickers
