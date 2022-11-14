import os

import pandas as pd

import gdown

STOCK_RICES_URL = (
    "https://drive.google.com/file/d/17acVTQujQh_wpRRf27CmoMloPh3KP8p_/view?usp=sharing"
)
CRYPTO = (
    "https://drive.google.com/file/d/1oijN_RnjtQSGyJw05HoeWBvREmgb5OZB/view?usp=sharing"
)
COMMODITIES = (
    "https://drive.google.com/file/d/135dBIupepAgUDGxn407fXb-HS3hDV8kS/view?usp=sharing"
)


ROOT = os.path.normpath("./data")
STOCK_PATH = os.path.normpath(os.path.join(ROOT, "stock_prices.csv"))
CRYPTO_PATH = os.path.normpath(os.path.join(ROOT, "crypto.csv"))
COMMODITIES_PATH = os.path.normpath(os.path.join(ROOT, "commodities.csv"))


def download_info():
    if not os.path.exists(ROOT):
        os.makedirs(ROOT)
    gdown.download(STOCK_RICES_URL, STOCK_PATH, fuzzy=True)
    gdown.download(CRYPTO, CRYPTO_PATH, fuzzy=True)
    gdown.download(COMMODITIES, COMMODITIES_PATH, fuzzy=True)


def get_full_data(columns: list = None) -> pd.DataFrame():
    # It is possible to get only one type of data
    commodities = pd.read_csv(COMMODITIES_PATH, nrows=1)
    stock = pd.read_csv(STOCK_PATH, nrows=1)

    if columns[0] in commodities:
        df = pd.read_csv(COMMODITIES_PATH)
    elif columns[0] in stock:
        df = pd.read_csv(STOCK_PATH)
    else:
        df = pd.read_csv(CRYPTO_PATH)

    df = df.rename(columns={"Date": "date"})
    df = df[["date", *columns]]

    return df


if __name__ == "__main__":
    download_info()
