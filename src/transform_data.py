import pandas as pd
from functools import reduce

def transform_df(df: pd.DataFrame, s):
    symbol = s.lower()

    df['date'] = pd.to_datetime(df['open_time'])

    df = df[['date', 'close_price']].rename(columns={'close_price':symbol})

    return df

def merge_assets(dfs):
    df_merged = reduce(lambda left, right: pd.merge(left, right, on= 'date', how='inner'), dfs)
    df_merged = df_merged.set_index('date')
    return df_merged