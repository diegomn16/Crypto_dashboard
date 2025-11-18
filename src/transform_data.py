import pandas as pd
from pathlib import Path
from functools import reduce

def load_asset_csv(path: Path):
    symbol = path.stem.split('_')[0]
    df = pd.read_csv(path)

    df['date'] = pd.to_datetime(df['open_time'])

    df = df[['date', 'close_price']].rename(columns={'close_price':f'{symbol.lower()}_close'})

    return df

def load_all_assets(folder_path):
    path = Path(folder_path)
    csv_files = list(path.glob('*.csv'))

    dfs = [load_asset_csv(file) for file in csv_files]
    return dfs

def merge_assets(dfs):
    df_merged = reduce(lambda left, right: pd.merge(left, right, on= 'date', how='inner'), dfs)
    df_merged = df_merged.set_index('date')
    return df_merged

if __name__ == '__main__':
    dfs = load_all_assets('data/raw')
    df_merged = merge_assets(dfs)
    df_merged.to_csv('data/processed/Joint_data.csv')