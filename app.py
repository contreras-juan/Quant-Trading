from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from tvDatafeed import TvDatafeed, Interval
from dict import *
from datetime import datetime, timedelta


# creates the Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

symbol_dropdown = html.Div([
    html.P('Symbol:'),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=['QQQ', 'SPY', 'IWM'],
        value='QQQ'
    )
])

timeframe_dropdown = html.Div([
    html.P('Timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=['Daily', 'Weekly', 'Monthly'],
        value='Daily'
    )
])

num_bars_input = html.Div([
    html.P('Number of Candles'),
    dbc.Input(id='num-bar-input', type='number', value='100')
])

# creates the layout of the App
app.layout = html.Div([
    html.H1('Real Time Charts'),

    dbc.Row([
        dbc.Col(symbol_dropdown),
        dbc.Col(timeframe_dropdown),
        dbc.Col(num_bars_input)
    ]),

    html.Hr(),

    dcc.Interval(id='update', interval=5000),

    html.Div(id='page-content')

], style={'margin-left': '5%', 'margin-right': '5%', 'margin-top': '20px'})


@app.callback(
    Output('page-content', 'children'),
    Input('update', 'n_intervals'),
    State('symbol-dropdown', 'value'), 
    State('timeframe-dropdown', 'value'), 
    State('num-bar-input', 'value')
)

def update_ohlc_chart(interval, symbol, timeframe, num_bars):

#    timeframe_str = timeframe
    freq = freq_dict[timeframe]
    exchange = exchange_dict[symbol]
    num_bars = int(num_bars)

    delta_t = timedelta_dict[timeframe]

#    print(symbol, num_bars)

    tv = TvDatafeed()
    bars = tv.get_hist(symbol=symbol, exchange=exchange, interval=freq , n_bars=num_bars)
    df = bars.copy()
#    df['time'] = pd.to_datetime(df['time'], unit='s')

    df['time'] = df.index
    df['ma'] = df['close'].rolling(window=21).mean()

    df['buy'] = 'Nothing'
    df['buy'] = np.where(
        (df['close'] > df['open']) & (df['close'] < df['ma']) & (df['open']/df['close'] >=0.995),
        'Buy Call',
        df['buy']
    )

    df['buy'] = np.where(
        (df['open'] > df['close']) & (df['open'] > df['ma']) & (df['close']/df['open'] >=0.995),
        'Buy Put',
        df['buy']
    )

    df['close_op'] = 'Nothing'
    df['close_op'] = np.where(
        (df['close'] > df['open']) & (df['close'] < df['ma']) & (df['open']/df['close'] >=0.995),
        'Close Call',
        df['close_op']
    )

    df['close_op'] = np.where(
        (df['open'] > df['close']) & (df['open'] > df['ma']) & (df['close']/df['open'] >=0.995),
        'Close Put',
        df['close_op']
    )


    fig = go.Figure(data=go.Candlestick(x=df['time'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']))

    period = freq_name_dict[timeframe]

    fig.add_trace(
        go.Scatter(
            x=df['time'],
            y=df['ma'],
            line=dict(color = '#e0e0e0'),
            name = f'21-{period} moving average'
        )
    )

    buy_call = df[df['buy']=='Buy Call']
    buy_put = df[df['buy']=='Buy Put']

    close_call = df[df['close_op']=='Close Call']
    close_put = df[df['close_op']=='Close Put']
    
    


    fig.add_trace(
        go.Scatter(
            x=buy_call['time'],
            y=buy_call['close']-2,
            mode='markers',
            name = 'Buy Call',
            marker=dict(
                size=8,
                color='#3276E6'
        )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=buy_call['time'],
            y=buy_call['close']+2,
            mode='markers',
            name = 'Close put',
            marker=dict(
                size=8,
                color='#E60580'
        )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=buy_put['time'],
            y=buy_put['close']-2,
            mode='markers',
            name = 'Buy Put',
            marker=dict(
                size=8,
                color='#E6A010'
        )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=buy_put['time'],
            y=buy_put['close']+2,
            mode='markers',
            name = 'Close call',
            marker=dict(
                size=8,
                color='#0CE605'
        )
        )
    )


    fig.update_layout(template='plotly_dark', title=f"Historical price of: {symbol} ", yaxis_title=f'{symbol} price (USD)', xaxis_title='Date', xaxis_rangeslider_visible=False)



    return [
        dcc.Graph(figure=fig, config={'displayModeBar': False})
        ]


if __name__ == '__main__':
    # starts the server
    app.run_server(host='0.0.0.0', port=8050, debug=True)