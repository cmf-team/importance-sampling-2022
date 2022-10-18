import datetime

import pandas as pd
import numpy as np
from datetime import datetime as dt
import investiny as inv


def calculate_returns(assets, weights, from_date, to_date, exchange=None):
    from_date = dt.strftime(dt.strptime(from_date, '%m/%d/%Y') - datetime.timedelta(days=1), '%m/%d/%Y')
    weights = np.array(weights)
    weights = weights / weights.sum()
    portfolio = pd.DataFrame(columns=['date', 'value'])

    for i, asset in enumerate(assets):
        id = inv.search_assets(query=asset, limit=1, exchange=exchange)[0]["ticker"]
        data = pd.DataFrame(inv.historical_data(investing_id=id, from_date=from_date, to_date=to_date))[
            ['date', 'close']]

        data['value'] = data['close'] * weights[i]
        data.drop('close', axis=1, inplace=True)

        merged = pd.concat([portfolio, data], ignore_index=True, sort=False)
        new_portfolio = merged.groupby('date', as_index=False).sum()
        portfolio = new_portfolio
    result = (portfolio['value'].diff() / portfolio['value'].shift(1)).dropna()
    return result


def stocks_returns(assets, weights, from_date, to_date):
    return calculate_returns(assets, weights, from_date, to_date, exchange='NASDAQ')


def commodities_returns(assets, weights, from_date, to_date):
    return calculate_returns(assets, weights, from_date, to_date, exchange='Commodity')


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    return calculate_returns(assets, weights, from_date, to_date)
