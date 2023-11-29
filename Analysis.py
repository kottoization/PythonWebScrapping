import Functions #tu mozna dac pozniej from Functions import nazwa_funkcji , wtedy mozna odwolywac sie bezposrednio do tej nazwy, albo mozna zostawic tak i robic Functions.nazw_funkcji, jest to obojetne ale spoko zeby bylo wszzedzie tak samo 
import pandas as pd
import matplotlib.pyplot as plt


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#przykladowe pobranie danych do data table dla bitcoina

#stworzenie url
btcUrl = Functions.construct_download_url('BTC', '2022-11-27', '2023-11-27','daily')

#pobranie danych
btcYear = Functions.scrape_yahoo_finance_data(btcUrl, headers)

#przykladowe pobranie danych do data table dla ethereum

#stworzenie url
ethUrl = Functions.construct_download_url('ETH', '2022-11-27', '2023-11-27','daily')

#pobranie danych 
ethYear = Functions.scrape_yahoo_finance_data(ethUrl, headers)

def endoftheday_data_weekly(df, title):
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
    df[numeric_columns] = df[numeric_columns].apply(lambda x: x.str.replace(',', ''))
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    plt.figure(figsize=(10, 6))  # Rozmiar wykresu (opcjonalne)
    plt.bar(df["Date"], df["AdjClose"])
    plt.title(title)
    plt.xlabel("Data")
    plt.ylabel("Koniec dnia")
    plt.show()

def mean_profit (list, nazwy):
    mean = list()
    for i in list:
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
        i[numeric_columns] = i[numeric_columns].apply(lambda x: x.str.replace(',', ''))
        i[numeric_columns] = i[numeric_columns].apply(pd.to_numeric, errors='coerce')





# po takim pobraniu danych nasze zmienne btcYear oraz ethYear to sa dataframe z pythona czyli ramki danych (tabele)
