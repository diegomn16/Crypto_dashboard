import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Import custom modules
# Ensure features.py and utils.py are updated with the logic we discussed
from data_fetcher import fetch_klines, klines_to_dataframe
from transform_data import transform_df, merge_assets
from features import calc_norm_prices, calc_daily_returns, calc_vol_roll, calc_drawdown, calc_cum_return
from utils import get_last_timestamp_from_csv, load_data_buffer

CSV_PATH = 'data/processed/Joint_features.csv'

if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT']
    
    # STATE PREPARATION (Context Loading)
    # Retrieve the last timestamp to avoid re-downloading existing data
    last_ts = get_last_timestamp_from_csv(CSV_PATH)
    
    start_time = None
    initial_prices = {}
    prev_peaks = {}
    df_buffer = pd.DataFrame()

    if last_ts:
        print(f"Updating data since: {pd.to_datetime(last_ts, unit='ms')}")
        
        # Request data starting from the next millisecond to avoid duplicates
        start_time = last_ts + 1 
        
        # Load the last 60 rows to act as a buffer for rolling calculations (e.g., volatility)
        df_buffer = load_data_buffer(CSV_PATH, tail_size=60)
        
        # STATE RECOVERY: Reconstruct mathematical context to prevent graph discontinuities
        if not df_buffer.empty:
            last_row = df_buffer.iloc[-1]
            for s in symbols:
                col = s.lower()
            # 1. Recuperamos el contexto matemático (P0 y Picos)
                if f'{col}_norm' in last_row:
                    initial_prices[col] = last_row[col] / last_row[f'{col}_norm']
                    prev_peaks[f'{col}_norm'] = last_row[f'{col}_norm'] / (last_row[f'{col}_drawdown'] + 1)
            
            cols_to_keep = [s.lower() for s in symbols]
            valid_cols = [c for c in cols_to_keep if c in df_buffer.columns]
            df_buffer = df_buffer[valid_cols]

    # FETCH & TRANSFORM (Delta Load)
    dfs_new = []
    for s in symbols:
        # Pass dynamic start_time. If None, it defaults to initial load behavior.
        raw_data = fetch_klines(s, start_time=start_time)
        
        if raw_data:
            df = klines_to_dataframe(raw_data)

            if not df.empty:
                df = transform_df(df, s)
                dfs_new.append(df)
            else:
                print(f'Binance returned an empty structure for {s}')
    
    # If no new data is retrieved for any symbol, exit gracefully
    if not dfs_new:
        print("System is up to date. No new data found.")
        sys.exit()

    # Merge only the newly fetched data
    df_new_merged = merge_assets(dfs_new)

    # BUFFER MERGE (Context Injection)    
    if not df_buffer.empty:
        # Concatenate: Recent History (Buffer) + New Data
        # This provides the necessary window for rolling metrics
        df_calc = pd.concat([df_buffer, df_new_merged])
    else:
        # Initial load scenario: No buffer available
        df_calc = df_new_merged

    # FEATURE CALCULATION (With State Injection)    
    # Pass recovered initial_prices and prev_peaks to maintain historical consistency
    df_norm = calc_norm_prices(df_calc, initial_prices)
    df_daily_return = calc_daily_returns(df_calc)
    df_cum_return = calc_cum_return(df_norm)
    df_vol_roll = calc_vol_roll(df_calc)
    df_drawdown = calc_drawdown(df_norm, prev_peaks)

    # Join all calculated features
    df_features_full = df_calc.join([df_norm, df_daily_return, df_cum_return, df_vol_roll, df_drawdown])

    #SMART SAVE (Slicing & Appending)
    if last_ts:
        # Slice: Remove buffer rows, keep ONLY the new rows
        # We identify new rows by checking indices not present in the buffer
        new_indices = df_features_full.index.difference(df_buffer.index)
        df_to_save = df_features_full.loc[new_indices]
        
        if not df_to_save.empty:
            # Mode 'a' (append) and header=False to write at the end of the file
            df_to_save.to_csv(CSV_PATH, mode='a', header=False)
            print(f"Success: Appended {len(df_to_save)} new rows to {CSV_PATH}.")
        else:
            print("Processing complete, but no new unique rows to save.")
    else:
        # Initial load: Write mode with header
        df_features_full.to_csv(CSV_PATH, mode='w', header=True)
        print("Initial full load completed successfully.")