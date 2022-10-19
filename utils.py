import pandas as pd

import gdown

STOCK_RICES_URL = (
    "https://drive.google.com/file/d/1RdHZNjjhiBLzeuYh6Pb3EywrnuCCBRhm/view?usp=sharing"
)
CRYPTO = (
    "https://drive.google.com/file/d/1mO51nSZfcL3iN-SptGD1G2F2dJZPo6pg/view?usp=sharing"
)
COMMODITIES = (
    "https://drive.google.com/file/d/1C4OcEOAs6Z1vj47dmX39rqp0bk0OYPhr/view?usp=sharing"
)

STOCK_PATH = "stock_prices.csv"
CRYPTO_PATH = "crypto.csv"
COMMODITIES_PATH = "commodities.csv"


def download_info():
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

    df = df[["date", *columns]]

    return df
