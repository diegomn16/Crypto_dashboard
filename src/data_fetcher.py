import requests
import pandas as pd

def fetch_klines(symbol, interval = '1d', limit = 1000):

    url = f'https://api.binance.com/api/v3/klines'

    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    
    except Exception as e:
        print(f'An error has occurred: {e}')
        raise

def klines_to_dataframe(raw):
    columns = ['open_time', 'open_price','high_price', 'low_price', 'close_price', 'volume',
                'close_time', 'quote_asset_volume', 'num_trades', 'taker_buy_base_asset_volume', 
                'taker_buy_quote_asset_volume', 'ignore']
    
    df = pd.DataFrame(raw, columns=columns)

    columns_to_float = ['open_price', 'high_price', 'low_price', 'close_price', 'volume', 'quote_asset_volume',
                        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    
    df[columns_to_float] = df[columns_to_float].astype(float)
    df['num_trades'] = df['num_trades'].astype(int)
    df['open_time'] = pd.to_datetime(df['open_time'], unit = 'ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit = 'ms')

    return df

def get_klines(symbol, interval="1d", limit=1000):
    raw = fetch_klines(symbol, interval=interval, limit=limit)
    df = klines_to_dataframe(raw)
    return df