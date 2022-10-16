import pandas as pd

from investiny import historical_data, search_assets

def download_and_count(assets: list, weights: list, 
                   from_date: str, to_date: str) -> pd.Series:
    
    from_date = pd.Timestamp(from_date.replace("/", "-"))
    from_date = pd.Timestamp(from_date)
    from_date = from_date - pd.Timedelta(days=1)
    from_date = str(from_date)
    from_date = from_date.replace("-", "/").split()[0]
    tmp = from_date.split("/")
    from_date = tmp[1]+"/"+tmp[2]+"/"+tmp[0]
   
    def __procedure(asset):    
        search_results = search_assets(query=assets, limit=20)
        investing_id = int(search_results[0]["ticker"]) 
        data = historical_data(investing_id=investing_id, 
                               from_date=from_date, to_date=to_date)
        
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df[["date", "close"]]
        df.columns = ["date", asset]
        
        return df
    
    df = __procedure(assets[0])
    assets = assets[1:]
    
    if assets:
        for asset in assets:
            tmp = __procedure(assets[0])
            df = df.merge(tmp, on="date", how="left")
    
    columns = df.columns[1:]
    
    # average weighted price
    for k,weight in enumerate(weights):
        df[columns[k]] = df[columns[k]]*weight
    
    df["price"] = df[columns].sum(axis=1)
    df["return"] = df["price"].diff()/df["price"].shift()
    
    # df = df.fillna(-0.0136)
    df = df.dropna()
    
    df["return"] = df["return"].map(lambda x: round(x, 4))
    df["return"] = df["return"].astype("float64")
    df = df[["date", "return"]].set_index("date")
    
    return df.squeeze()

def stocks_returns(assets: list, weights: list, 
                   from_date: str = None, to_date: str = None) -> pd.Series:
    
    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_

def commodities_returns(assets: list, weights: list, 
                   from_date: str = None, to_date: str = None) -> pd.Series:
    
    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_

def cryptocurrencies_returns(assets: list, weights: list, 
                   from_date: str = None, to_date: str = None) -> pd.Series:
    
    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_