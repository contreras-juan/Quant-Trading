from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from tvDatafeed import TvDatafeed, Interval
from dict import *

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

#timeframe_dropdown = html.Div([
#    html.P('Timeframe:'),
#    dcc.Dropdown(
#        id='timeframe-dropdown',
#        options=[{'label': timeframe, 'value': timeframe} for timeframe in TIMEFRAMES],
#        value='D1'
#    )
#])

num_bars_input = html.Div([
    html.P('Number of Candles'),
    dbc.Input(id='num-bar-input', type='number', value='1000')
])

# creates the layout of the App
app.layout = html.Div([
    html.H1('Real Time Charts'),

    dbc.Row([
        dbc.Col(symbol_dropdown),
 #       dbc.Col(timeframe_dropdown),
        dbc.Col(num_bars_input)
    ]),

    html.Hr(),

    dcc.Interval(id='update', interval=20000),

    html.Div(id='page-content')

], style={'margin-left': '5%', 'margin-right': '5%', 'margin-top': '20px'})


@app.callback(
    Output('page-content', 'children'),
    Input('update', 'n_intervals'),
    State('symbol-dropdown', 'value'), 
    #State('timeframe-dropdown', 'value'), 
    State('num-bar-input', 'value')
)


def update_ohlc_chart(interval, symbol, num_bars):
#    timeframe_str = timeframe
#    timeframe = TIMEFRAME_DICT[timeframe]

    exchange = exchange_dict[symbol]
    num_bars = int(num_bars)

    print(symbol, num_bars)

    tv = TvDatafeed()
    bars = tv.get_hist(symbol=symbol,exchange=exchange,interval=Interval.in_1_hour,n_bars=num_bars)
    df = bars.copy()
#    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = df.index

    fig = go.Figure(data=go.Candlestick(x=df['time'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']))

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(yaxis={'side': 'right'})
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    return [
        html.H2(id='chart-details', children=f'{symbol}'),
        dcc.Graph(figure=fig, config={'displayModeBar': False})
        ]


if __name__ == '__main__':
    # starts the server
    app.run_server()