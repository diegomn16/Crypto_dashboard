import requests

def main():
    
    url = "https://api.binance.com/api/v3/time"
    response = requests.get(url)

    print('Status code:', response.status_code)

    if response.status_code == 200:
        data = response.json()
        print('Contenido JSON:', data)
    else:
        print('Algo ha ido mal con la petición')

if __name__ == '__main__':
    main()