import pandas as pd
from functools import reduce

def transform_df(df: pd.DataFrame, s):
    # Standardize symbol to lowercase to use it as a column name
    symbol = s.lower()

    # Convert the raw timestamp (usually ms) to a proper datetime object
    df['date'] = pd.to_datetime(df['open_time'])

    # Select only the date and price, renaming the price column to the asset symbol
    # This structure is necessary to later join multiple assets by date
    df = df[['date', 'close_price']].rename(columns={'close_price':symbol})

    return df

def merge_assets(dfs):
    # Iteratively merge all DataFrames in the list using 'date' as the key
    # 'how=inner' ensures we only keep timestamps available for ALL assets (intersection)
    df_merged = reduce(lambda left, right: pd.merge(left, right, on= 'date', how='inner'), dfs)
    
    # Set the date as the index to facilitate time-series operations
    df_merged = df_merged.set_index('date')
    return df_merged