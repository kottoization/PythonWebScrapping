import Functions
import Analysis
import WorkInProgressAnalysis
import PlottingUtils
from datetime import datetime
import pycodestyle 

def check_style(files):
    style_checker = pycodestyle
    style_checker = pycodestyle.StyleGuide()
    result = style_checker.check_files(files)
    print(result.messages)

def compose_functions(func_list):
    def composed(*args, **kwargs):
        result = None
        for func in func_list:
            if result is None:
                result = func(*args, **kwargs)
            else:
                result = func(result)
        return result
    
    return composed

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    def downloadData(crypto):
        url = Functions.construct_download_url(crypto, '2022-01-01', datetime.today().strftime('%Y-%m-%d'), 'weekly') 
        data = Functions.scrape_yahoo_finance_data(url, headers)
        return data

    # Funkcja pobierająca dane i analizująca dla wybranej kryptowaluty
    def analyze_crypto(data,crypto):
        print(f'Analiza danych dla {crypto}:\n{data}')
        Analysis.plot_candlestick_chart(data,crypto)
        Analysis.calculate_greed_fear_index(data)
        Analysis.train_linear_regression_model(data,crypto) 
        Analysis.changing_format(data)
        Analysis.endoftheday_data_weekly(data, crypto)
        Analysis.endoftheday_vs_beginningoftheday_data_weekly(data,crypto)
       
    # analyze_crypto(downloadData('ETH'),'ETH')
    # analyze_crypto(downloadData('BTC'),'BTC')
    # analyze_crypto(downloadData('BNB'),'BNB')
    # analyze_crypto(downloadData('SOL'),'SOL')
    # Analysis.profit4Crypto()

    functions_to_compose = [
        lambda: analyze_crypto(downloadData('BTC'), 'BTC'),
    #    lambda: analyze_crypto(downloadData('ETH'), 'ETH'),
    #    lambda: analyze_crypto(downloadData('BNB'), 'BNB'),
    #   lambda: analyze_crypto(downloadData('SOL'), 'SOL'),
        lambda: Analysis.profit4Crypto()
    ]

   # composed_function = compose_functions(functions_to_compose)
   # composed_function()



   ### ---- new type of plotting - test below, over this is just a composition
    btc_data = downloadData('BTC')
    eth_data = downloadData('ETH')  #TODO: delete the duplicate if not needed
    formatted_btc_data = WorkInProgressAnalysis.changing_format(btc_data)
    formatted_eth_data = WorkInProgressAnalysis.changing_format(eth_data)

    btc_endoftheday_data = WorkInProgressAnalysis.endoftheday_data_weekly(formatted_btc_data, 'Bitcoin End of the Day')
    btc_greed_fear_index = WorkInProgressAnalysis.calculate_greed_fear_index(formatted_eth_data)

    eth_endoftheday_data = WorkInProgressAnalysis.endoftheday_data_weekly(formatted_btc_data, 'Ethereum End of the Day')
    eth_greed_fear_index = WorkInProgressAnalysis.calculate_greed_fear_index(formatted_eth_data)

    btc_profit = WorkInProgressAnalysis.profit([formatted_btc_data], ['Bitcoin'])
    eth_profit = WorkInProgressAnalysis.profit([formatted_eth_data], ['Ethereum'])

    # Tworzenie listy danych dla wykresu
    charts_data = [
        btc_endoftheday_data,
        eth_endoftheday_data,
        btc_greed_fear_index,
        eth_greed_fear_index,
        btc_profit,
        eth_profit
    ]

    # Wywołanie funkcji plot_multiple_charts
    PlottingUtils.plot_multiple_charts(charts_data)

    files_to_check = ['Main.Main.py', 'Analysis.py', 'Functions.py', 'PlottingUtils.py', 'WorkInProgressAnalysis.py']
    check_style(files_to_check)

if __name__ == "__main__":
    main()

