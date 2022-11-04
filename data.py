import pandas as pd
import numpy as np

def stocks_returns(assets, weights, from_date, to_date):
    df = load_data('shares')
    return calculate_returns(df, assets, weights, from_date, to_date, exchange='NASDAQ')


def commodities_returns(assets, weights, from_date, to_date):
    df = load_data('commodities')
    return calculate_returns(df, assets, weights, from_date, to_date, exchange='Commodity')


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    df = load_data('crypto')
    return calculate_returns(df, assets, weights, from_date, to_date)
