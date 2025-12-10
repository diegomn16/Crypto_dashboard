import requests
import pandas as pd

def fetch_klines(symbol, interval = '1d', limit = 1000, start_time = None):
    """
    Fetches raw candlestick data from Binance API.
    Supports both fixed-limit queries (initial load) and time-based queries (incremental updates).
    """
    url = f'https://api.binance.com/api/v3/klines'

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    # Incremental Loading Logic:
    if start_time:
        params['startTime'] = start_time
        del params['limit']

    # Set a timeout to prevent the script from hanging indefinitely on network issues
    response = requests.get(url, params=params, timeout=10)
        
    # Raise an HTTPError if the HTTP request returned an unsuccessful status code (4xx or 5xx)
    response.raise_for_status()
        
    data = response.json()
    return data
    
    

def klines_to_dataframe(raw):
    """
    Converts raw API response (list of lists) into a structured Pandas DataFrame
    with correct data types and datetime parsing.
    """
    # Mapping Binance API response structure to column names
    columns = ['open_time', 'open_price','high_price', 'low_price', 'close_price', 'volume',
                'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 
                'taker_buy_quote_asset_volume', 'ignore']
    
    df = pd.DataFrame(raw, columns=columns)

    # Type Casting: APIs often return numeric data as strings to preserve precision.
    # We must convert them to float/int for mathematical operations.
    columns_to_float = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'quote_asset_volume',
                        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    
    df[columns_to_float] = df[columns_to_float].astype(float)
    df['num_trades'] = df['num_trades'].astype(int)
    
    # Timestamp Conversion: Binance uses Unix timestamps in milliseconds (unit='ms')
    df['open_time'] = pd.to_datetime(df['open_time'], unit = 'ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit = 'ms')

    return df

def get_klines(symbol, interval="1d", limit=1000):
    """
    Wrapper function for simple, non-incremental fetching.
    Useful for initial backfills or ad-hoc analysis.
    """
    raw = fetch_klines(symbol, interval=interval, limit=limit)
    df = klines_to_dataframe(raw)
    return df