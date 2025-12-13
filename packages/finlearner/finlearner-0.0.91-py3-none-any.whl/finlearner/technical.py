import pandas as pd
import numpy as np

class TechnicalIndicators:
    """
    Advanced Technical Analysis suite.
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def add_all(self):
        """Adds all available indicators to the dataframe."""
        self.bollinger_bands()
        self.rsi()
        self.macd()
        self.atr()
        self.stochastic()
        self.cci()
        self.obv()
        self.ichimoku()
        return self.data

    def bollinger_bands(self, window: int = 20, num_std: int = 2):
        self.data['MA20'] = self.data['Close'].rolling(window=window).mean()
        std = self.data['Close'].rolling(window=window).std()
        self.data['BB_Upper'] = self.data['MA20'] + (std * num_std)
        self.data['BB_Lower'] = self.data['MA20'] - (std * num_std)
        return self.data

    def rsi(self, window: int = 14):
        delta = self.data['Close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        return self.data

    def macd(self, fast: int = 12, slow: int = 26, signal: int = 9):
        ema_fast = self.data['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.data['Close'].ewm(span=slow, adjust=False).mean()
        self.data['MACD'] = ema_fast - ema_slow
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=signal, adjust=False).mean()
        return self.data
    
    
    def atr(self, window: int = 14):
        """Average True Range (Volatility)"""
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        self.data['ATR'] = true_range.rolling(window=window).mean()
        return self.data

    def stochastic(self, k_window: int = 14, d_window: int = 3):
        """Stochastic Oscillator"""
        low_min = self.data['Low'].rolling(window=k_window).min()
        high_max = self.data['High'].rolling(window=k_window).max()
        
        self.data['Stoch_K'] = 100 * ((self.data['Close'] - low_min) / (high_max - low_min))
        self.data['Stoch_D'] = self.data['Stoch_K'].rolling(window=d_window).mean()
        return self.data

    def cci(self, window: int = 20):
        """Commodity Channel Index"""
        tp = (self.data['High'] + self.data['Low'] + self.data['Close']) / 3
        sma = tp.rolling(window=window).mean()
        mad = tp.rolling(window=window).apply(lambda x: np.abs(x - x.mean()).mean())
        self.data['CCI'] = (tp - sma) / (0.015 * mad)
        return self.data

    def obv(self):
        """On-Balance Volume"""
        self.data['OBV'] = (np.sign(self.data['Close'].diff()) * self.data['Volume']).fillna(0).cumsum()
        return self.data

    def ichimoku(self):
        """Ichimoku Cloud"""
        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
        nine_period_high = self.data['High'].rolling(window=9).max()
        nine_period_low = self.data['Low'].rolling(window=9).min()
        self.data['Ichimoku_Tenkan'] = (nine_period_high + nine_period_low) / 2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2
        period26_high = self.data['High'].rolling(window=26).max()
        period26_low = self.data['Low'].rolling(window=26).min()
        self.data['Ichimoku_Kijun'] = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A): (Conversion + Base)/2
        self.data['Ichimoku_SpanA'] = ((self.data['Ichimoku_Tenkan'] + self.data['Ichimoku_Kijun']) / 2).shift(26)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2
        period52_high = self.data['High'].rolling(window=52).max()
        period52_low = self.data['Low'].rolling(window=52).min()
        self.data['Ichimoku_SpanB'] = ((period52_high + period52_low) / 2).shift(26)

        # Chikou Span (Lagging Span): Close shifted back 26 periods
        self.data['Ichimoku_Chikou'] = self.data['Close'].shift(-26)
        return self.data