import plotly.express as px

def filer_by_date(df_plot, start_date, end_date):
    # Helper function to slice the DataFrame based on the user-selected date range
    # It returns a .copy() to ensure subsequent operations don't trigger SettingWithCopy warnings
    mask = (df_plot['date'] >= start_date) & (df_plot['date'] <= end_date)
    return df_plot.loc[mask].copy()

def plot_normalized_prices(df, symbols, start_date, end_date):
    # Reset index to make 'date' a regular column, which is required by Plotly for the x-axis
    df_plot = df.reset_index()
    
    # Apply date filtering
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    # Dynamic Column Selection:
    # 1. Convert input symbols to lowercase to match DataFrame column naming convention
    # 2. List comprehension checks if the constructed column name actually exists in the data
    symbols = [s.lower() for s in symbols]
    cols = [f'{s}_norm' for s in symbols if f'{s}_norm' in df_plot.columns]

    # Subset the DataFrame to keep only the date and the relevant columns for plotting
    df_plot = df_plot[['date'] + cols]

    # Create an interactive line chart using Plotly Express
    fig = px.line(df_plot, x='date', y=cols, title="Normalized Prices Comparision")
    fig.update_layout(yaxis_title = 'Normalized prices', height = 900)

    return fig

def plot_daily_returns(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    # Select columns with suffix '_return' corresponding to daily percentage changes
    cols = [f'{s}_return' for s in symbols if f'{s}_return' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x = 'date', y = cols, title = 'Daily return')
    fig.update_layout(yaxis_title = f'Daily Return', height = 900)

    return fig

def plot_volatility(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    # Select columns with suffix '_vol_roll' (30-day rolling standard deviation)
    cols = [f'{s}_vol_roll' for s in symbols if f'{s}_vol_roll' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x = 'date', y = cols, title= 'Rolling Volatility (30-day)')
    fig.update_layout(yaxis_title = 'Volatility', height = 900)

    return fig

def plot_drawdown(df, symbols, start_date, end_date):
    df_plot = df.reset_index()
    df_plot = filer_by_date(df_plot = df_plot, start_date = start_date, end_date = end_date)

    symbols = [s.lower() for s in symbols]
    # Select columns with suffix '_drawdown' (percentage drop from historical peak)
    cols = [f'{s}_drawdown' for s in symbols if f'{s}_drawdown' in df_plot.columns]

    df_plot = df_plot[['date'] + cols]

    fig = px.line(df_plot, x = 'date', y = cols, title= 'Drawdown Comparison')
    fig.update_layout(yaxis_title = 'Drawdown', height = 900)

    return fig