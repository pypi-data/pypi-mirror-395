import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple

class TimeSeriesPredictor:
    """
    LSTM-based Time Series Predictor for Financial Data.
    """
    def __init__(self, lookback_days: int = 60):
        self.lookback_days = lookback_days
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def _prepare_data(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        X, y = [], []
        for i in range(self.lookback_days, len(data)):
            X.append(data[i-self.lookback_days:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    def fit(self, df: pd.DataFrame, epochs: int = 25, batch_size: int = 32):
        """
        Trains the LSTM model.
        """
        dataset = df[['Close']].values
        scaled_data = self.scaler.fit_transform(dataset)
        
        X_train, y_train = self._prepare_data(scaled_data)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

        # Build World-Class Architecture
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(units=50, return_sequences=False))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(units=25))
        self.model.add(Dense(units=1))

        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predicts future prices based on the trained model.
        """
        dataset = df[['Close']].values
        inputs = dataset[len(dataset) - len(dataset) - self.lookback_days:]
        inputs = inputs.reshape(-1, 1)
        inputs = self.scaler.transform(inputs)

        X_test = []
        for i in range(self.lookback_days, len(inputs)):
            X_test.append(inputs[i-self.lookback_days:i, 0])
        
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        
        predicted_prices = self.model.predict(X_test)
        predicted_prices = self.scaler.inverse_transform(predicted_prices)
        return predicted_prices