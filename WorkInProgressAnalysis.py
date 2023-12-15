import Functions 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go


def changing_format(df):
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.str.replace(',', ''))
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df

def endoftheday_data_weekly(df, title):
    data = {
        "x": df["Date"],
        "y": df["AdjClose"],
        "title": title,
        "x_label": "Date",
        "y_label": "Close Price at EOD"
    }
    return data

def endoftheday_vs_beginningoftheday_data_weekly(df, title):
    data = {
        "x1": df["Date"],
        "y1": df["Open"],
        "label1": 'Open',
        "marker1": 'o',
        "x2": df["Date"],
        "y2": df["Close"],
        "label2": 'Close',
        "marker2": 'x',
        "title": title,
        "x_label": "Date",
        "y_label": "Value"
    }
    return data

def profit(data_list, currencies):
    mean = []
    for data in data_list:
        last_index = data.index[-1]
        first_price = data["AdjClose"].iloc[0]
        last_price = data["AdjClose"].iloc[last_index]
        new_element = ((last_price - first_price) / first_price) * 100
        mean.append(new_element)
    
    data = {
        "x": currencies,
        "y": mean,
        "title": "Increase in value (%)",
        "x_label": "Crypto currency",
        "y_label": "%"
    }
    return data

def calculate_greed_fear_index(df):
    df1 = df.copy()
    if 'Close' not in df1.columns:
        raise ValueError("The 'Close' column is missing in the DataFrame.")
    
    close_prices = df1['Close']
    close_prices = df1['Close'].str.replace(',', '').astype(float)
    percentage_changes = []

    for i in range(1, len(close_prices)):
        percentage_change = ((close_prices.iloc[i] - close_prices.iloc[i - 1]) / close_prices.iloc[i - 1]) * 100
        percentage_changes.append(percentage_change)
    
    df1['PriceChanges'] = [0] + percentage_changes

    conditions = [
        (df1['PriceChanges'] > 0),
        (df1['PriceChanges'] < 0),
    ]
    choices = [1, -1]

    df1['GreedFearIndex'] = pd.cut(df1['PriceChanges'], bins=[float('-inf'), 0, float('inf')], labels=choices)
    
    data = {
        "x": df1['Date'],
        "y": df1['GreedFearIndex'],
        "title": 'Fear/Greed Index',
        "x_label": 'Date',
        "y_label": 'Index'
    }
    return data

def plot_candlestick_chart(df, crypto):
    candlestick = go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        close=df['Close'],
        low=df['Low'],
        high=df['High'],
        name=crypto + '/USD Candlestick'
    )

    fig = go.Figure(data=[candlestick])

    fig.update_layout(
        width=900,
        height=450,
        title=dict(text=crypto + '<b>/USD Chart</b>', font=dict(size=30)),
        yaxis_title=dict(text='Price (USD)', font=dict(size=15)),
        margin=dict(l=10, r=20, t=80, b=20),
        xaxis_rangeslider_visible=False,
    )

    return fig.to_dict()

def train_linear_regression_model(df, crypto):
    features = df[['Open', 'High', 'Low', 'Volume']]
    target = df['AdjClose'].str.replace(',', '').astype(float)

    numeric_columns2 = ['Open', 'High', 'Low', 'Volume']
    features[numeric_columns2] = features[numeric_columns2].apply(lambda x: x.str.replace(',', ''))
    features[numeric_columns2] = features[numeric_columns2].apply(pd.to_numeric, errors='coerce')

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    
    data = {
        "x": X_test['Open'],
        "y1": y_test,
        "y2": predictions,
        "title": crypto,
        "x_label": 'Open Price',
        "y_label": 'AdjClose Price',
        "mse": mse
    }
    return data

def profit4Crypto():
    btcUrl = Functions.construct_download_url('BTC', '2022-11-27', '2023-11-27','weekly')
    btcYear = Functions.scrape_yahoo_finance_data(btcUrl, headers)

    ethUrl = Functions.construct_download_url('ETH', '2022-11-27', '2023-11-27','weekly')
    ethYear = Functions.scrape_yahoo_finance_data(ethUrl, headers)

    bnbUrl = Functions.construct_download_url('BNB', '2022-11-27', '2023-11-27','weekly')
    bnbYear = Functions.scrape_yahoo_finance_data(bnbUrl, headers)

    solUrl = Functions.construct_download_url('SOL', '2022-11-27', '2023-11-27','weekly')
    solYear = Functions.scrape_yahoo_finance_data(solUrl, headers)

    #changing_format(btcYear)
    #changing_format(ethYear)
    #changing_format(bnbYear)
    #changing_format(solYear)
    #TODO: sprawdzic czy to powinno byc, chyba wychodzi na to ze ta funkcja powinna sie lacznie tylko raz wywoalc
   
    lista = [btcYear, ethYear, bnbYear, solYear]
    nazwy = ["Bitcoin", "Ethernum", "Binance", "Solana"]
    
    data = {
        "lista": lista,
        "nazwy": nazwy
    }
    return data
