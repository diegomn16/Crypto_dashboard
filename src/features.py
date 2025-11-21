import pandas as pd

#standard price calculation
def calc_norm_prices(df: pd.DataFrame):
    df_norm = (df/df.iloc[0]).add_suffix('_norm')
    return df_norm

#calculation of daily returns
def calc_daily_returns(df: pd.DataFrame):
    df_return = df.pct_change().add_suffix('_return').fillna(0)
    return df_return

#calculation of cumulative returns
def calc_cum_returns(df_daily: pd.DataFrame):
    df_cumreturn = ((df_daily+1).cumprod() - 1).fillna(0)
    df_cumreturn.columns = df_cumreturn.columns.str.replace('_return$', '_cumreturn', regex = True)
    return df_cumreturn

#rolling volatility calculation
def calc_vol_roll(df: pd.DataFrame):
    df_daily = calc_daily_returns(df)
    df_vol_roll = df_daily.rolling(window=30).std()
    df_vol_roll.columns = df_vol_roll.columns.str.replace('_return$', '_vol_roll', regex=True)
    return df_vol_roll

#drawdown
def calculate_drawdown(series: pd.Series):
    peak = series.cummax()
    drawdown = (series / peak) - 1
    return drawdown

def calc_drawdown(df_norm: pd.DataFrame):
    df_drawdown = df_norm.apply(calculate_drawdown, axis = 0)
    df_drawdown.columns = df_drawdown.columns.str.replace('_norm$', '_drawdown', regex=True)
    return df_drawdown