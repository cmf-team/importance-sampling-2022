import pandas as pd
import numpy as np
from investiny import historical_data, search_assets


def new_data(time, shift):
    new_time = pd.Timestamp(time) + pd.Timedelta(f'{shift} day')
    res = new_time.strftime('%m/%d/%Y')
    return res


def get_assets(assets, weights, from_date, to_date):
    df = pd.DataFrame()
    return_list = [None,]
    for i, asset in enumerate(assets):
        series_aux = pd.Series(dtype='float64')
        search_results = search_assets(query=asset, limit=1)
        invest_id = int(search_results[0]["ticker"])
        data = historical_data(investing_id=invest_id, from_date=new_data(from_date, -1), to_date=new_data(to_date, 1))
        series_aux = pd.Series(data['close'], pd.to_datetime(data['date']))
        dr = pd.date_range(new_data(from_date, -1), to_date, freq='D')
        df[f'{asset}'] = series_aux.reindex(index=dr,  method='ffill')
        df[asset] = df[asset] * weights[i]
        df.rename(columns={f"{asset}": f"weighted {asset}"}, inplace=True)
    df.fillna(method='bfill', inplace=True)
    df['price'] = df.sum(axis=1)
    prices_list = df['price'].to_list()
    for i in range(1, df.shape[0]):
        return_list.append((prices_list[i] - prices_list[i - 1]) / prices_list[i - 1])
    df['return'] = return_list
    df.drop(index=pd.to_datetime(new_data(from_date, -1)), axis=0, inplace=True)
    df.drop(df[df['return'] == 0].index, axis=0, inplace=True)
    return df['return']


class Dataloader:
    def __init__(
            self,
            series: pd.Series,
            window_size: int,
            step_size: int,
            horizon: int,
            first_pred: int
    ):
        self.series = series
        self.window_size = window_size
        self.step_size = step_size
        self.horizon = horizon
        self.first_pred = first_pred
        assert self.first_pred > self.window_size
        feat_idx = []
        target_idx = []
        for i in range(self.first_pred, self.series.shape[0], self.step_size):
            feat_idx.append(range(i - self.horizon - self.window_size, i - self.horizon))
            target_idx.append(i)
        self.feat_idx = feat_idx
        self.target_idx = target_idx

    def __len__(self):
        return len(self.feat_idx)

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.feat_idx):
            feat = self.series.iloc[self.feat_idx[self.iter]]
            target = self.series.iloc[self.target_idx[self.iter]]
            self.iter += 1
            return feat, target
        else:
            raise StopIteration


def stocks_returns(assets, weights, from_date, to_date):
    return get_assets(assets, weights, from_date, to_date)



def commodities_returns(assets, weights, from_date, to_date):
    return get_assets(assets, weights, from_date, to_date)



def cryptocurrencies_returns(assets, weights, from_date, to_date):
    return get_assets(assets, weights, from_date, to_date)
