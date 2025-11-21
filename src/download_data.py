from data_fetcher import get_klines
from transform_data import (transform_df, merge_assets)
from features import (calc_norm_prices, calc_daily_returns, calc_cum_returns, calc_vol_roll, calc_drawdown)

if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT']

    dfs = []

    for s in symbols:
        df = get_klines(s, limit= 1000)
        df = transform_df(df, s)
        dfs.append(df)
    
    df_merged = merge_assets(dfs)

    df_norm = calc_norm_prices(df_merged)
    df_daily_return = calc_daily_returns(df_merged)
    df_cumreturn = calc_cum_returns(df_daily_return)
    df_vol_roll = calc_vol_roll(df_merged)
    df_drawdown = calc_drawdown(df_norm)

    df_features = df_merged.join([df_norm, df_daily_return, df_cumreturn, df_vol_roll, df_drawdown])

    df_features.to_csv('data/processed/Joint_features.csv')

    print(df_features.head())