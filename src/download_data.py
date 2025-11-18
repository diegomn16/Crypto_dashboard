from data_fetcher import get_klines

if __name__ == '__main__':
    symbols = ['BTCUSDT', 'ETHUSDT']

    for s in symbols:
        df = get_klines(s, limit= 1000)
        df.to_csv(f'data/raw/{s}_data.csv', index=False)