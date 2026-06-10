import csv


def load_tickers():

    tickers = {}

    with open("data/topix500.csv", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            tickers[row["ticker"]] = row["name"]

    return tickers
