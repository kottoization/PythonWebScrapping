import Functions #tu mozna dac pozniej from Functions import nazwa_funkcji , wtedy mozna odwolywac sie bezposrednio do tej nazwy, albo mozna zostawic tak i robic Functions.nazw_funkcji, jest to obojetne ale spoko zeby bylo wszzedzie tak samo 
import pandas as pd
import Analysis

#trzeba dodac headers bo inaczej yahoo rzuca nam 404 nie znaleziono strony
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


#przykladowe pobranie danych do data table dla bitcoina

#stworzenie url
btcUrl = Functions.construct_download_url('BTC', '2022-11-27', '2023-11-27','weekly')

#pobranie danych
btcYear = Functions.scrape_yahoo_finance_data(btcUrl, headers)

#przykladowe pobranie danych do data table dla ethereum

#stworzenie url
ethUrl = Functions.construct_download_url('ETH', '2022-11-27', '2023-11-27','daily')

#pobranie danych
ethYear = Functions.scrape_yahoo_finance_data(ethUrl, headers)

#Analysis.endoftheday_data(btcYear,"Bitcoin")

