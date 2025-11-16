import pandas as pd

def main():
    df_BTC = pd.read_csv('data/BTC_data.csv')
    df_ETH = pd.read_csv('data/ETH_data.csv')

    df_BTC = df_BTC.rename(columns = {'Close price': 'BTC close', 'Kline open time': 'Date'})
    df_ETH = df_ETH.rename(columns = {'Close price': 'ETH close', 'Kline open time': 'Date'})

    columnas_relevantesBTC = ['Date', 'BTC close']
    columnas_relevantesETH = ['Date', 'ETH close']

    df_BTC = df_BTC[columnas_relevantesBTC]
    df_ETH = df_ETH[columnas_relevantesETH]

    df_conjunto = pd.merge(df_BTC, df_ETH, on = 'Date')
    df_conjunto['Date'] = pd.to_datetime(df_conjunto['Date'])
    df_conjunto = df_conjunto.set_index('Date')
    df_conjunto.to_csv('data/Joint_data.csv')

    print(df_conjunto.index.dtype)
if __name__ == '__main__':
    main()