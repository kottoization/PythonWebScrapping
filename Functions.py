from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

#https://finance.yahoo.com/crypto/  <- link do ogolnej stornki z ktorej mamy liste krypto do requesta
#poradnik https://www.youtube.com/watch?v=tBiygN2Cif4

def construct_download_url(
        currency, #np BTC dla bitcoina, ze stronki https://finance.yahoo.com/crypto/ latwo to pobrac z linkow kolejnych walut
        period1, #data od w formacie rok-miesiac-dzien
        period2, #data do w formacie rok-miesiac-dzien
        interval='daily' #daily lub weekly lub monthly zaleznie jaki przedzial czasu chcemy miec
):
    """
    :period1 & period2: 'yyyy-mm-dd'
    :interval: {daily,weekly,monthly}

    """
    def convert_to_seconds(period):
        datetime_value = datetime.strptime(period, '%Y-%m-%d')
        total_seconds = int(time.mktime(datetime_value.timetuple())) 
        return total_seconds 
    try:
        interval_reference = {'daily':'1d', 'weekly':'1wk', 'monthly':'1mo'}
        _interval = interval_reference.get(interval)
        if(_interval is None):
            print('Nie podano interwału.')            
        p1 = convert_to_seconds(period1)
        p2 = convert_to_seconds(period2)
        url = f'https://finance.yahoo.com/quote/{currency}-USD/history?period1={p1}&period2={p2}&interval={_interval}&filter=history&frequency=1d&includeAdjustedClose=true'
        return url
    except Exception as e:
        print(e)
        return


def scrape_yahoo_finance_data(Url, headers):
    response = requests.get(Url, headers=headers)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'data-test': 'historical-prices'})

        if table:
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    row_data = [cell.text.strip() for cell in cells]
                    data.append(row_data)

            # Tworzenie DataFrame Pandas z pobranych danych
            df = pd.DataFrame(data[1:-1], columns=data[0])
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
            
            # Konwersja kolumny Date do formatu daty
            df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

            return df
        else:
            print('Nie znaleziono tabeli z danymi.')
    else:
        print('Nie udało się pobrać strony. Status:', response.status_code)


