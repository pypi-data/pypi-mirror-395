import pytest
import pandas as pd
import numpy as np
from finlearner.technical import TechnicalIndicators

@pytest.fixture
def sample_data():
    """Creates a dummy dataframe with 100 days of random stock data."""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=100)
    data = pd.DataFrame({
        'Open': np.random.uniform(100, 200, 100),
        'High': np.random.uniform(200, 210, 100),
        'Low': np.random.uniform(90, 100, 100),
        'Close': np.random.uniform(100, 200, 100),
        'Volume': np.random.randint(1000, 10000, 100)
    }, index=dates)
    return data

def test_add_all_indicators(sample_data):
    ti = TechnicalIndicators(sample_data)
    df = ti.add_all()
    
    # Check if new columns exist
    expected_cols = ['ATR', 'Stoch_K', 'CCI', 'OBV', 'Ichimoku_SpanA']
    for col in expected_cols:
        assert col in df.columns, f"Column {col} was not created."
        
    # Check for non-NaN values (after the warm-up period)
    # Ichimoku uses 52 period shift, so we check the end of the dataframe
    assert not pd.isna(df['ATR'].iloc[-1])
    assert not pd.isna(df['OBV'].iloc[-1])

def test_atr_calculation(sample_data):
    ti = TechnicalIndicators(sample_data)
    df = ti.atr(window=14)
    assert df['ATR'].min() > 0 # Volatility should be positive