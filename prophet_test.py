import pandas as pd
from data import get_data
from prophet import Prophet
import matplotlib.pyplot as plt
import time

while True:
    data = get_data()

    configs = {
        '1m': (1000, 3, 'h'),
        '5m': (500, 6, 'h'),
        '1h': (100, 12, 'h'),
    }

    for k, v in configs.items():
        df = data['BTC/USDT'][k]
        df = df.tail(v[0])

        df = df.reset_index() # Make sure that the timestamp is not an index anymore
        df.columns = ['ds', 'y1', 'y2', 'y3', 'y', 'y4'] # Renaming columns as required by Prophet
        df = df[['ds', 'y']] # Select only required columns
        df['ds'] = pd.to_datetime(df['ds'] / 1000, unit='s')

        m = Prophet()
        m.fit(df)

        future = m.make_future_dataframe(periods=v[1], freq=v[2])
        forecast = m.predict(future)
        fig1 = m.plot(forecast)

        plt.savefig(f'forecast_{k}.png')
    time.sleep(60)