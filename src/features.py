import pandas as pd
import numpy as np

#standard price calculation
def calc_norm_prices(df: pd.DataFrame, initial_prices:dict = None):
    if initial_prices:
        target_cols = list(initial_prices.keys())
        valid_cols = [c for c in target_cols if c in df.columns]
        initial_series = pd.Series(initial_prices)
        df_norm = df[valid_cols].div(initial_series[valid_cols], axis=1).add_suffix('_norm')
    else:
        df_norm = (df/df.iloc[0]).add_suffix('_norm')
    return df_norm

#calculation of daily returns
def calc_daily_returns(df: pd.DataFrame):
    df_return = df.pct_change().add_suffix('_return').fillna(0)
    return df_return

#calculation of cumreturns
def calc_cum_return(df_norm: pd.DataFrame):
    df_cum_return = (df_norm - 1)
    df_cum_return.columns = df_cum_return.columns.str.replace('_norm$', '_cumreturn', regex=True)
    return df_cum_return

#rolling volatility calculation
def calc_vol_roll(df: pd.DataFrame):
    df_daily = calc_daily_returns(df)
    df_vol_roll = df_daily.rolling(window=30).std()
    df_vol_roll.columns = df_vol_roll.columns.str.replace('_return$', '_vol_roll', regex=True)
    return df_vol_roll

#drawdown
def calc_drawdown(df_norm: pd.DataFrame, prev_peaks: dict = None):

    df_drawdown = pd.DataFrame(index=df_norm.index)

    for col in df_norm.columns:
        series = df_norm[col]
        col_name = col.replace('_norm', '_drawdown')

        prev_peak = prev_peaks.get(col, -np.inf) if prev_peaks else -np.inf

        current_peaks = series.cummax()
        if prev_peaks:
            real_peaks = current_peaks.clip(lower=prev_peak)
        else:
            real_peaks = current_peaks
        df_drawdown[col_name] = (series / real_peaks) - 1

    return df_drawdown