import pandas as pd
import plotly.express as px
df = pd.read_csv('data/processed/Joint_features.csv', parse_dates=['date'])
df = df.set_index('date')

def plot_normalized_prices(df):
    df_plot = df.reset_index()

    norm_cols = [col for col in df_plot.columns if col.endswith("_norm")]
    fig = px.line(df_plot, x='date', y=norm_cols, title="Normalized Prices Comparision")

    return fig

def plot_daily_returns(df, symbol, start_date, end_date):
    symbol = symbol.lower()
    df_plot = df.reset_index()

    return_col = df_plot[['date', f'{symbol}_return']]
    mask = (return_col['date'] >= start_date) & (return_col['date'] <= end_date)
    return_col = return_col.loc[mask].copy()
    fig = px.line(return_col, x = 'date', y = f'{symbol}_return', title = 'Daily return')

    return fig

def plot_volatility(df):
    df_plot = df.reset_index()
    vol_cols = [col for col in df_plot.columns if col.endswith('_vol_roll')]
    fig = px.line(df_plot, x = 'date', y = vol_cols, title= 'Rolling Volatility (30-day)',)

    return fig

def plot_drawdown(df):
    df_plot = df.reset_index()
    drawdown_cols = [col for col in df_plot.columns if col.endswith('_drawdown')]
    fig = px.line(df_plot, x = 'date', y = drawdown_cols, title= 'Drawdown Comparision')
    fig.update_layout(yaxis_title = 'Drawdown')

    return fig


if __name__ == '__main__':
    fig = plot_daily_returns(df, symbol='btcusdt', start_date='2025-01-01', end_date='2025-02-01')
    fig.show()
    fig = plot_normalized_prices(df)
    fig.show()
    fig = plot_volatility(df)
    fig.show()
    fig = plot_drawdown(df)
    fig.show()