# import ccxt
# import yfinance as yf
# import pandas as pd

# # 암호화폐 거래소와 연결
# exchange = ccxt.binance()

# # Bitcoin/USDT의 5분봉 데이터 가져오기
# btc_data = exchange.fetch_ohlcv("BTC/USDT", timeframe='5m', limit=1000)
# btc_df = pd.DataFrame(btc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# # 나스닥과 금의 5분봉 데이터 가져오기
# nasdaq_data = yf.download("NQ=F", interval="5m", period="5d")
# gold_data = yf.download("GC=F", interval="5m", period="5d")

import os
import ccxt
import pandas as pd 
from datetime import datetime
import numpy as np
from collections import defaultdict

def fetch_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    num_retries = 0
    try:
        num_retries += 1
        data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        return data
    except Exception:
        if num_retries > max_retries:
            raise Exception('Failed to fetch', timeframe, 'data after', max_retries, 'attempts')


def get_data():
    exchange = ccxt.binance()
    timeframes = ['5m', '1h', '1d']
    symbols = ['BTC/USDT']
    history_data = {}

    for symbol in symbols:
        if symbol not in history_data.keys():
            history_data[symbol] = {}
        for timeframe in timeframes:
            filename = f'{symbol.replace("/", "")}-{timeframe}.csv'
            file_exists = os.path.isfile(filename)
            since = exchange.parse8601('2023-06-01T00:00:00Z')
            if file_exists:
                existing_data = pd.read_csv(filename, index_col=0)
                since = existing_data.index[-1]
            data = []
            while True:
                print(datetime.fromtimestamp(since / 1000.0))
                fetched_data = fetch_ohlcv(exchange, 3, symbol, timeframe, since, 1000)
                if not fetched_data:
                    break
                if since == fetched_data[-1][0]:
                    break
                data += fetched_data
                since = fetched_data[-1][0]
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']).dropna()
            df.set_index('timestamp', inplace=True)
            if file_exists:
                frames = [existing_data, df]

                # Exclude any empty frames
                frames = [f for f in frames if not f.empty]

                # Then perform concat
                df = pd.concat(frames)
                df.to_csv(filename)
            else:
                df.to_csv(filename)
            
            history_data[symbol][timeframe] = df
    return history_data

if __name__ == '__main__':
    print(get_data())