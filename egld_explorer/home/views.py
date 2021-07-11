from django.shortcuts import render

from binance.client import Client
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter



# Create your views here.

def home(request):
    # keys from second account, don't worry
    client = Client(api_key = 'zG4HPT1D1xdOm05jmJLDPpAbyMuHHZBB7h25PUHP5iw18acsdbKMqLQkn1O68XSi', 
                    api_secret = 'QoaEinp64OAvs60Lf1cwhTb7jWg8hqj7v1ANPE1p3rcjcbuRM8ubC0oSkSnHC8Bi',
                    testnet = True,
                    tld = 'us')

    price = client.get_symbol_ticker(symbol="BTCUSDT")

    # get timestamp of earliest date data is available
    timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1h')

    # request historical candle (or klines) data
    bars = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=100)
    useful_bars = [price[:5] for price in bars]

    # option 4 - create a Pandas DataFrame and export to CSV
    df = pd.DataFrame(useful_bars, columns=['date', 'open', 'high', 'low', 'close'])
    df.set_index('date', inplace=True)

    fig1 = [Scatter(x=df.index, y=df['close'],
                        mode='lines', name='Principal Chart',
                        opacity=0.8, marker_color='blue')]

    plot(fig1, filename="home/templates/home/principal_chart.html" , auto_open=False)

    return render(request, 'home/home.html', {
        "price": price['price'],
        "symbol": price['symbol'],
        "nb_prix": len(df.index)
    })