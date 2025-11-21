import streamlit as st
import pandas as pd
from charts import (
    plot_normalized_prices,
    plot_daily_returns,
    plot_volatility,
    plot_drawdown
)


#Website configuration
st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

st.title("Crypto Dashboard")


#cache function
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/Joint_features.csv", parse_dates=["date"])
    df = df.set_index("date")
    return df


#button to reload data
st.sidebar.header("Controles")

if st.sidebar.button("Recargar datos"):
    st.cache_data.clear()   # clean cache
    st.rerun()              # reload the page with new data


#load data
df = load_data()


#sidebar controls
all_symbols = sorted({col.split("_")[0] for col in df.columns if col.endswith("_return")})

selected_symbols = st.sidebar.multiselect(
    "Activos",
    all_symbols,
    default=[all_symbols[0]]   # at least one by default
)

if not selected_symbols:
    st.warning("Select at least one crypto.")
    st.stop()

min_date = df.index.min().date()
max_date = df.index.max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date = date_range
    end_date = date_range

chart_type = st.sidebar.selectbox(
    "Graphic",
    [
        "Normalized prices",
        "Daily returns",
        "Rolling volatility",
        "Drawdown"
    ]
)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

#main area
if chart_type == "Normalized prices":
    st.subheader("Normalized prices (base = 1)")
    fig = plot_normalized_prices(
        df,
        symbols=selected_symbols,
        start_date=start_date,
        end_date=end_date
    )
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