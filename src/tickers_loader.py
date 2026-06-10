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

    with open(csv_path, encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            tickers[
                row["ticker"]
            ] = row["name"]

    return tickers
