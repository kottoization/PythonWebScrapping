import Functions #tu mozna dac pozniej from Functions import nazwa_funkcji , wtedy mozna odwolywac sie bezposrednio do tej nazwy, albo mozna zostawic tak i robic Functions.nazw_funkcji, jest to obojetne ale spoko zeby bylo wszzedzie tak samo 
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go
import Functions


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def changing_format(df):
     numeric_columns = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
     df[numeric_columns] = df[numeric_columns].apply(lambda x: x.str.replace(',', ''))
     df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

def endoftheday_data_weekly(df, title):
    plt.figure(figsize=(10, 6))
    plt.bar(df["Date"], df["AdjClose"])
    plt.title(title)
    plt.xlabel("Data")
    plt.ylabel("Koniec dnia")
    plt.show()

def endoftheday_vs_beginningoftheday_data_weekly(df, title):
    plt.figure(figsize=(10, 6))
    plt.plot(df["Date"], df["Open"], label='Otwarcie', marker='o')
    plt.plot(df["Date"], df["Close"], label='Zamknięcie', marker='o')
    plt.title(title)
    plt.xlabel("Data")
    plt.ylabel("Wartość")
    plt.legend()
    plt.show()

def profit(list, nazwy):
    mean = []
    for i in list:
        new_element = (i["AdjClose"].iloc[0] - i["AdjClose"].iloc[51])/i["AdjClose"].iloc[51]*100
        mean.append(new_element)
    plt.figure(figsize=(10, 6))
    plt.bar(nazwy, mean)
    plt.title("Procentowy wzrost wartości kryptowaluty")
    plt.xlabel("Kryptowaluta")
    plt.ylabel("%")
    plt.show()


def calculate_greed_fear_index(df):
    #df= changing_format(df)
     # Ensure 'Close' is present in the DataFrame
    df1= df.copy()
    if 'Close' not in df1.columns:
        raise ValueError("The 'Close' column is missing in the DataFrame.")
    
    # Extract 'Close' prices
    close_prices = df1['Close']
    close_prices= df1['Close'].str.replace(',', '').astype(float)
   # close_prices= pd.to_numeric(close_prices)
    # Initialize an empty list to store percentage changes
    percentage_changes = []
    
    # Calculate the percentage change in close prices for each index
    for i in range(1, len(close_prices)):
        percentage_change = ((close_prices.iloc[i] - close_prices.iloc[i - 1]) / close_prices.iloc[i - 1]) * 100
        percentage_changes.append(percentage_change)
    
    # Create a new column 'PriceChanges' in the DataFrame
    df1['PriceChanges'] = [0] + percentage_changes
    
    # Classify as Greed (1), Fear (-1), or Neutral (0) based on the percentage change
    conditions = [
        (df1['PriceChanges'] > 0),
        (df1['PriceChanges'] < 0),
    ]
    choices = [1, -1]
    
    df1['GreedFearIndex'] = pd.cut(df1['PriceChanges'], bins=[float('-inf'), 0, float('inf')], labels=choices)
    print(df1)
    
    return df1

def plot_candlestick_chart(df,crypto):
    # Tworzenie obiektu Candlestick
    candlestick = go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        close=df['Close'],
        low=df['Low'],
        high=df['High'],
        name= crypto+ '/USD Candlestick'
    )

    # Tworzenie obiektu Figure
    fig = go.Figure(data=[candlestick])

    # Konfiguracja układu
    fig.update_layout(
        width=900,
        height=450,
        title=dict(text=crypto+'<b>/USD Chart</b>', font=dict(size=30)),
        yaxis_title=dict(text='Price (USD)', font=dict(size=15)),
        margin=dict(l=10, r=20, t=80, b=20),
        xaxis_rangeslider_visible=False,
    )

    # Wyświetlanie wykresu
    fig.show()


def train_linear_regression_model(df,crypto):
 
    # Wybór zmiennych objaśniających
    features = df[['Open', 'High', 'Low', 'Volume']]
    #features= changing_format(features)
    # Zmienna objaśniana
    target = df['AdjClose'].str.replace(',', '').astype(float)

    numeric_columns2 = ['Open', 'High', 'Low', 'Volume']
    features[numeric_columns2] = features[numeric_columns2].apply(lambda x: x.str.replace(',', ''))
    features[numeric_columns2] = features[numeric_columns2].apply(pd.to_numeric, errors='coerce')
    # Podział danych na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    # Uczenie modelu regresji liniowej
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Przewidywanie na zbiorze testowym
    predictions = model.predict(X_test)
    
    # Ocena modelu
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    
    # Wykres porównujący rzeczywiste wartości z przewidywanymi
    plt.scatter(X_test['Open'], y_test, color='black', label='Actual')
    plt.scatter(X_test['Open'], predictions, color='blue', label='Predicted')
    plt.xlabel('Open Price')
    plt.ylabel('AdjClose Price')
    plt.title(crypto)
    plt.legend()
    plt.show()

def profit4Crypto():
    btcUrl = Functions.construct_download_url('BTC', '2022-11-27', '2023-11-27','weekly')

    #pobranie danych
    btcYear = Functions.scrape_yahoo_finance_data(btcUrl, headers)

    #przykladowe pobranie danych do data table dla ethereum

    #stworzenie url
    ethUrl = Functions.construct_download_url('ETH', '2022-11-27', '2023-11-27','weekly')

    #pobranie danych
    ethYear = Functions.scrape_yahoo_finance_data(ethUrl, headers)

    #przykladowe pobranie danych do data table dla binance

    #stworzenie url
    bnbUrl = Functions.construct_download_url('BNB', '2022-11-27', '2023-11-27','weekly')

    #pobranie danych
    bnbYear = Functions.scrape_yahoo_finance_data(bnbUrl, headers)

    #przykladowe pobranie danych do data table dla solany

    #stworzenie url
    solUrl = Functions.construct_download_url('SOL', '2022-11-27', '2023-11-27','weekly')

    #pobranie danych
    solYear = Functions.scrape_yahoo_finance_data(solUrl, headers)

    changing_format(btcYear)
    changing_format(ethYear)
    changing_format(bnbYear)
    changing_format(solYear)

    #Funkcja poiera listę tabel  danymi dotycącymi krypotwaluty oraz listę nazw. Podaje o jaki procent wzrosły/zmalały krptowaluty
    lista = [btcYear, ethYear, bnbYear, solYear]
    nazwy = ["Bitcoin", "Ethernum", "Binance", "Solana"]
    profit(lista, nazwy)

