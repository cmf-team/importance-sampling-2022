import datetime

import pandas as pd
import numpy as np
from datetime import datetime as dt
import gdown

url_shares = 'https://drive.google.com/file/d/1wGqjII5tLSqoFzQ8rhNAw3YU1n02gD4t/view?usp=sharing'
url_commodities = 'https://drive.google.com/file/d/1wJ3plFuTWQbEnF3VYU0C5EC4t3Wa09Ku/view?usp=sharing'
url_crypto = 'https://drive.google.com/file/d/1wDvDU0e0as6zTnTzWXMHW2B60ixpE685/view?usp=sharing'

url_shares_common = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
url_commodities_common = 'https://drive.google.com/file/d/1GFq1jcV00BjFEa7hmZSO1xD7K4j4gv3O/view?usp=sharing'
url_crypto_common = 'https://drive.google.com/file/d/1mPP5Vb57Jc2mYPeLYZPgAJM8ogjiguSO/view?usp=sharing'

URLS = {'shares': url_shares_common,
        'commodities': url_commodities_common,
        'crypto': url_crypto_common}


def load_data(type):
    file = type + '.csv'
    gdown.download(URLS[type], file, fuzzy=True)
    df = pd.read_csv(file)
    df.rename(columns={'Date': 'date'}, inplace=True)
    df['date'] = pd.to_datetime(df['date']).map(lambda x: x.replace(tzinfo=None))
    return df


def calculate_returns(df, assets, weights, from_date, to_date, exchange=None):
    from_date = dt.strptime(from_date, '%m/%d/%Y') - datetime.timedelta(days=1)
    to_date = dt.strptime(to_date, '%m/%d/%Y')
    weights = np.array(weights)
    weights = weights / weights.sum()
    portfolio = pd.DataFrame(columns=['date', 'value'])

    for i, asset in enumerate(assets):
        data = df[(df['date'] >= from_date) & (df['date'] <= to_date)].reset_index(drop=True)

        asset_data = pd.DataFrame(columns=['date, value'])
        asset_data['date'] = data['date']
        asset_data['value'] = data[asset] * weights[i]

        merged = pd.concat([portfolio, asset_data], ignore_index=True, sort=False)
        new_portfolio = merged.groupby('date', as_index=False).sum()
        portfolio = new_portfolio
    result = (portfolio['value'].diff() / portfolio['value'].shift(1)).dropna()
    return result


def stocks_returns(assets, weights, from_date, to_date):
    df = load_data('shares')
    return calculate_returns(df, assets, weights, from_date, to_date, exchange='NASDAQ')


def commodities_returns(assets, weights, from_date, to_date):
    df = load_data('commodities')
    return calculate_returns(df, assets, weights, from_date, to_date, exchange='Commodity')


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    df = load_data('crypto')
    return calculate_returns(df, assets, weights, from_date, to_date)
