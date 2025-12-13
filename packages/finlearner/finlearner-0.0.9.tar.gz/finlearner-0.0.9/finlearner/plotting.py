import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class Plotter:
    @staticmethod
    def candlestick(df: pd.DataFrame, title: str = "Stock Price"):
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                            row_width=[0.2, 0.7])

        # Candlestick
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                     low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

        # Volume
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=2, col=1)

        fig.update_layout(title=title, yaxis_title='Price', xaxis_rangeslider_visible=False)
        fig.show()