from pathlib import Path
import pandas as pd


def get_last_timestamp_from_csv(file_path: str) -> int:
    file = Path(file_path)

    if not file.is_file():
        return None
    
    try:
        # Optimization: Read only the 'date' column to avoid loading the full dataset into RAM
        df = pd.read_csv(file, usecols=['date'], parse_dates=['date'])

        if df.empty:
            return None
        
        last_date = df['date'].iloc[-1]

        # CRITICAL: Convert Pandas Timestamp (nanoseconds) to Unix Timestamp (milliseconds)
        # The Binance API expects an integer in milliseconds
        return int(last_date.value // 10**6)
    
    except Exception as e:
        print(f'Error reading local file: {e}')
        return None
    
def load_data_buffer(file_path: str, tail_size: int = 60)-> pd.DataFrame:
    file = Path(file_path)
    

    if not file.is_file():
        return None
    
    try:
        # First pass: Count total rows to identify the slicing point
        # Using a generator expression avoids loading file content into memory
        with open(file, 'r') as f:
            total_rows = sum(1 for row in f)
        
        if total_rows > tail_size:
            # Logic to keep the header but skip old data:
            # range(1, X) keeps row 0 (header) and skips rows 1 to X
            rows_to_skip = range(1, total_rows - tail_size)
            df = pd.read_csv(file, skiprows=rows_to_skip, parse_dates=['date'])
        else:
            # Fallback: If the file is smaller than the requested buffer, load everything
            df = pd.read_csv(file, parse_dates = ['date'])

        return df

    except Exception as e:
        print(f'An error has ocured: {e}')
        return None