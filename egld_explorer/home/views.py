from django.shortcuts import render

from binance.client import Client
from binance import BinanceSocketManager
import pandas as pd
from pandas.io.sql import read_sql
from plotly.offline import plot
from plotly.graph_objs import Figure, Scatter
from plotly.io import to_html
from datetime import datetime

import asyncio
import sqlalchemy




# Create your views here.

def home(request):
    # keys from second account, don't worry
    client = Client(api_key = 'zG4HPT1D1xdOm05jmJLDPpAbyMuHHZBB7h25PUHP5iw18acsdbKMqLQkn1O68XSi', 
                    api_secret = 'QoaEinp64OAvs60Lf1cwhTb7jWg8hqj7v1ANPE1p3rcjcbuRM8ubC0oSkSnHC8Bi')

    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket('BTCUSDT')

    engine = sqlalchemy.create_engine('sqlite://BTCUSDTstream.db')

    def createframe(msg):
        df = pd.DataFrame([msg])
        df = df.loc[:,['s','E','p']]
        df.columns = ['symbol', 'Time', 'Price']
        df.Price = df.Price.astype(float)
        df.Time = pd.to_datetime(df.Time, unit='ms')
        return df

    async def main():
        i=0
        while i<10:
            await socket.__aenter__()
            msg = await socket.recv()
            df = createframe(msg)
            df.to_sql('BTCUSDT', engine, if_exists='append', index=False)
            i+=1
    
    asyncio.run(main())

    df = read_sql('BTCUSDT', engine)

    price = client.get_symbol_ticker(symbol="BTCUSDT")

    # get timestamp of earliest date data is available
    #timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1h')

    # request historical candle (or klines) data
    #bars = client.get_historical_klines('BTCUSDT', '1h', timestamp, limit=100)
    #useful_bars = [price[:5] for price in bars]

    # option 4 - create a Pandas DataFrame and export to CSV
    #df = pd.DataFrame(useful_bars, columns=['date', 'open', 'high', 'low', 'close'])
    #df["date"] = [datetime.fromtimestamp(int(i) / 1000 )for i in df["date"]]
    #f.set_index('date', inplace=True)

    fig1 = Figure()
    fig1 = [Scatter(x=df.index, y=df['close'], name='Principal Chart')]

    plot_div = plot(fig1, output_type='div', include_plotlyjs=False)
    #graph = fig1.to_html(full_html=False, default_height=500, default_width=700)
    #plot(fig1, filename="home/templates/home/principal_chart.html" , auto_open=False)

    return render(request, 'home/home.html', {
        "price": price['price'],
        "symbol": price['symbol'],
        "nb_prix": len(df.index),
        "graph": plot_div
    })