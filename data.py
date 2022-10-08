import pandas as pd
import numpy as np
from investiny import historical_data, search_assets
from datetime import timedelta, date, datetime


def make_date(date, days_count):
    to_date_tmp = datetime.strptime(date, '%m/%d/%Y')
    to_date_tmp = to_date_tmp + timedelta(days=days_count)
    date = to_date_tmp.strftime('%m/%d/%Y')
    return date


def make_profit(data, weights):
    res = []
    for i in range(1, len(data[0]['close'])):
        sum_tek = 0
        sum_tom = 0
        r = 0
        for j in range(len(data)):
            sum_tek = sum_tek + data[j]['close'][i] * weights[j]
            sum_tom = sum_tom + data[j]['close'][i-1] * weights[j]

        r = (sum_tek - sum_tom)/sum_tom
        res.append(r)

    res_ser = pd.Series(data=res, index=data[0]['date'][1:])
    return res_ser


def stocks_returns(assets, weights, from_date, to_date):
    from_date = make_date(from_date, -1)
    to_date = make_date(to_date, 1)

    data = []
    for name in assets:
        results = search_assets(query=name, limit=1, type="Stock",
                                exchange="NASDAQ")

        investing_id = int(results[0]["ticker"])
        data.append(historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date))

    res_ser = make_profit(data, weights)
    return res_ser


def commodities_returns(assets, weights, from_date, to_date):
    from_date = make_date(from_date, -1)
    to_date = make_date(to_date, 1)

    data = []
    for name in assets:
        results = search_assets(query=name, limit=1, type="Commodity")

        investing_id = int(results[0]["ticker"])
        data.append(historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date))

    res_ser = make_profit(data, weights)
    return res_ser


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    from_date = make_date(from_date, -1)
    to_date = make_date(to_date, 1)

    data = []
    for name in assets:
        results = search_assets(query=name, limit=1)

        investing_id = int(results[0]["ticker"])
        data.append(historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date))
    res_ser = make_profit(data, weights)
    return res_ser

