import pandas as pd

df = pd.read_csv('data/processed/Joint_data.csv', parse_dates=['date'])
df = df.set_index('date')
df.columns = df.columns.str.replace('_close$', '', regex=True)

def calculate_drawdown(series):
    peak = series.cummax()
    drawdown = (series / peak) - 1
    return drawdown

#standard price calculation
df_norm = (df/df.iloc[0]).add_suffix('_norm')

#calculation of daily returns
df_return = df.pct_change().add_suffix('_return').fillna(0)

#calculation of cumulative returns
df_cumreturn = ((df_return+1).cumprod() - 1).fillna(0)
df_cumreturn.columns = df_cumreturn.columns.str.replace('_return$', '_cumreturn', regex = True)

#rolling volatility calculation
df_vol_roll = df_return.rolling(window=30).std()
df_vol_roll.columns = df_vol_roll.columns.str.replace('_return$', '_vol_roll', regex=True)

#drawdown
df_drawdown = df_norm.apply(calculate_drawdown, axis = 0)
df_drawdown.columns = df_drawdown.columns.str.replace('_norm$', '_drawdown', regex=True)

df = df.join([df_norm, df_return, df_cumreturn, df_vol_roll, df_drawdown])
df.to_csv('data/processed/Joint_features.csv')