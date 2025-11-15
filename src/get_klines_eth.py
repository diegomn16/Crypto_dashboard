import requests
import pandas as pd

def main():

    url = "https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&limit=100"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print('Algo ha ido mal')
    
    columnas = ['Kline open time', 'Open price','High price', 'Low price', 'Close price', 'Volume',
                'Kline close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 
                'Taker buy quote asset volume', 'Ignore']
    
    df = pd.DataFrame(data, columns=columnas)

    columnas_a_float = ['Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Quote asset volume',
                        'Taker buy base asset volume', 'Taker buy quote asset volume']
    
    df[columnas_a_float] = df[columnas_a_float].astype(float)
    df['Number of trades'] = df['Number of trades'].astype(int)
    df['Kline open time'] = pd.to_datetime(df['Kline open time'], unit = 'ms')
    df['Kline close time'] = pd.to_datetime(df['Kline close time'], unit = 'ms')

    nombre_archivo = 'data/ETH_data.csv'
    df.to_csv(nombre_archivo, index=False, encoding='utf-8')

if __name__ == '__main__':
    main()