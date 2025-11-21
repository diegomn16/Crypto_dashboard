import pandas as pd
import plotly.express as px

def filer_by_date(df_plot, start_date, end_date):
    mask = (df_plot['date'] >= start_date) & (df_plot['date'] <= end_date)
    return df_plot.loc[mask].copy()

def plot_normalized_prices(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    cols = [f'{s}_norm' for s in symbols if f'{s}_norm' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x='date', y=cols, title="Normalized Prices Comparision")
    fig.update_layout(yaxis_title = 'Normalized prices', height = 900)

    return fig

def plot_daily_returns(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    cols = [f'{s}_return' for s in symbols if f'{s}_return' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x = 'date', y = cols, title = 'Daily return')
    fig.update_layout(yaxis_title = f'Daily Return', height = 900)

    return fig

def plot_volatility(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    cols = [f'{s}_vol_roll' for s in symbols if f'{s}_vol_roll' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x = 'date', y = cols, title= 'Rolling Volatility (30-day)')
    fig.update_layout(yaxis_title = 'Volatility', height = 900)

    return fig

def plot_drawdown(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    cols = [f'{s}_drawdown' for s in symbols if f'{s}_drawdown' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x = 'date', y = cols, title= 'Drawdown Comparison')
    fig.update_layout(yaxis_title = 'Drawdown', height = 900)

    return fig