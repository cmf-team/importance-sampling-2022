import pandas as pd

from utils import *


def download_and_count(
    assets: list, weights: list, from_date: str, to_date: str
) -> pd.Series:
    from_date = pd.Timestamp(from_date)
    from_date = from_date - pd.Timedelta(days=1)

    download_info()
    df = get_full_data(assets)

    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= from_date) & (df["date"] <= to_date)]
    df = df.set_index("date")

    dict_mul = {col: mul for col, mul in zip(assets, weights)}
    df = df.multiply(dict_mul)

    df["price"] = df.sum(axis=1)
    df["return"] = df["price"].diff() / df["price"].shift()
    df = df[1:]
    df["return"] = df["return"].astype("float64")

    df = df["return"].squeeze()

    return df


def stocks_returns(
    assets: list, weights: list, from_date: str = None, to_date: str = None
) -> pd.Series:

    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_


def commodities_returns(
    assets: list, weights: list, from_date: str = None, to_date: str = None
) -> pd.Series:

    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_


def cryptocurrencies_returns(
    assets: list, weights: list, from_date: str = None, to_date: str = None
) -> pd.Series:

    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_
