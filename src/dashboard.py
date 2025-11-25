import streamlit as st
import pandas as pd
from charts import (
    plot_normalized_prices,
    plot_daily_returns,
    plot_volatility,
    plot_drawdown
)


# Website configuration
# Sets the browser tab title and enables "wide mode" to use the full screen width
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

st.title("Crypto Dashboard")


# Cache function
# @st.cache_data is crucial for performance. It prevents the app from re-reading 
# the CSV file on every user interaction (like changing a date), which would be slow.
# The data is loaded once and stored in memory until the cache is cleared.
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/Joint_features.csv", parse_dates=["date"])
    df = df.set_index("date")
    return df


# Sidebar: Data Reload Controls
st.sidebar.header("Controles")

# If the user clicks "Recargar datos", we invalidate the cache and force a rerun.
# This is useful to fetch the latest data after the ETL script (download_data.py) has run.
if st.sidebar.button("Recargar datos"):
    st.cache_data.clear()   # Wipe the memory cache
    st.rerun()              # Restart the script execution to reload fresh data


# Load data into memory
df = load_data()


# Sidebar: Asset Selection
# Dynamically extract available symbols from column names (e.g., 'btc_return' -> 'btc')
# This makes the dashboard robust: if you add 'SOL' to the CSV, it appears here automatically.
all_symbols = sorted({col.split("_")[0] for col in df.columns if col.endswith("_return")})

selected_symbols = st.sidebar.multiselect(
    "Criptos",
    all_symbols,
    default=[all_symbols[0]]   # Select the first asset by default to avoid empty charts
)

# Validation: Stop execution if no asset is selected to prevent plotting errors
if not selected_symbols:
    st.warning("Select at least one crypto.")
    st.stop()

# Date Range Selection
# Determine the absolute limits based on the available data
min_date = df.index.min().date()
max_date = df.index.max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date), # Default to the full history
    min_value=min_date,
    max_value=max_date
)

# Handle the date_input return values. It returns a tuple (start, end) usually,
# but can return a single date while the user is still picking the second one.
if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    # Fallback if only one date is picked (rare edge case in UI interaction)
    start_date = date_range
    end_date = date_range

# Chart Type Selector
chart_type = st.sidebar.selectbox(
    "Graphic",
    [
        "Normalized prices",
        "Daily returns",
        "Rolling volatility",
        "Drawdown"
    ]
)

# Convert standard Python dates to Pandas Timestamps for filtering compatibility
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Main Area: Visualization Logic
# Conditional rendering based on the dropdown selection.
# Each block calls the specific plotting function from charts.py

if chart_type == "Normalized prices":
    st.subheader("Normalized prices (base = 1)")
    fig = plot_normalized_prices(
        df,
        symbols=selected_symbols,
        start_date=start_date,
        end_date=end_date
    )
    # Render the interactive Plotly figure
    st.plotly_chart(fig, width="stretch")

elif chart_type == "Daily returns":
    st.subheader("Daily returns")
    fig = plot_daily_returns(
        df,
        symbols=selected_symbols,
        start_date=start_date,
        end_date=end_date
    )
    st.plotly_chart(fig, width="stretch")

elif chart_type == "Rolling volatility":
    st.subheader("Rolling volatility (30 days)")
    fig = plot_volatility(
        df,
        symbols=selected_symbols,
        start_date=start_date,
        end_date=end_date
    )
    st.plotly_chart(fig, width="stretch")

elif chart_type == "Drawdown":
    st.subheader("Drawdown Comparison")
    fig = plot_drawdown(
        df,
        symbols=selected_symbols,
        start_date=start_date,
        end_date=end_date
    )
    st.plotly_chart(fig, width="stretch")