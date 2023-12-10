from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

# funkcja tworzaca url
def construct_download_url(
    currency,
    period1,
    period2,
    interval='daily'
):
    INTERVAL_REFERENCE = {'daily': '1d', 'weekly': '1wk', 'monthly': '1mo'}
    YAHOO_FINANCE_URL = 'https://finance.yahoo.com/quote/'

    def convert_to_seconds(period):
        datetime_value = datetime.strptime(period, '%Y-%m-%d')
        total_seconds = int(time.mktime(datetime_value.timetuple()))
        return total_seconds

    try:
        _interval = INTERVAL_REFERENCE.get(interval)
        if _interval is None:
            raise ValueError('Nie podano interwału.')

        p1 = convert_to_seconds(period1)
        p2 = convert_to_seconds(period2)
        url = f'{YAHOO_FINANCE_URL}{currency}-USD/history?period1={p1}&period2={p2}&interval={_interval}&filter=history&frequency=1d&includeAdjustedClose=true'
        return url
    except Exception as e:
        raise e


# funkcja pobierajaca dane
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
