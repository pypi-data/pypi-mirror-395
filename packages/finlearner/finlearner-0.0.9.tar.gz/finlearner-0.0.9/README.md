[![CI/CD](https://github.com/ankitdutta428/finlearn/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/ankitdutta428/finlearn/actions)
[![PyPI version](https://badge.fury.io/py/finlearn.svg)](https://badge.fury.io/py/finlearn)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

**FinLearner** is a comprehensive Python library for financial analysis, algorithmic trading research, and deep learning-based market prediction. It combines advanced technical analysis, modern portfolio theory, and state-of-the-art LSTM models into a single, production-ready API.

Whether you are a researcher, a quant developer, or a data scientist, FinLearn provides the robust tools needed to analyze markets and build predictive models.

## Key Features

* **Deep Learning Models:** Pre-configured LSTM and GRU architectures optimized for time-series forecasting.
* **Portfolio Optimization:** Implementation of Markowitz Mean-Variance Optimization to find the Efficient Frontier and maximize Sharpe Ratios.
* **Technical Analysis:** A suite of 20+ technical indicators (RSI, MACD, Bollinger Bands, etc.) optimized for Pandas.
* **Interactive Visualization:** Beautiful, interactive financial charts powered by Plotly.
* **Data Pipeline:** Unified data fetching wrapper for Yahoo Finance.

---

## Installation

You can install `finlearn` directly from PyPI:

```bash
pip install finlearn
Or build from source:Bashgit clone [https://github.com/ankitdutta428/finlearn.git](https://github.com/ankitdutta428/finlearn.git)
cd finlearn
pip install -e .
```
⚡ Quick Start1. Market Prediction (Deep Learning)Train an LSTM model to predict future stock prices with just a few lines of code.
```Python
from finlearn import DataLoader, TimeSeriesPredictor, Plotter

# 1. Fetch Data
# Automatically handles cleaning and preprocessing
df = DataLoader.download_data('AAPL', start='2020-01-01', end='2024-01-01')

# 2. Train Model
# Initialize the predictor with a 60-day lookback window
predictor = TimeSeriesPredictor(lookback_days=60)
predictor.fit(df, epochs=25, batch_size=32)

# 3. Predict
predictions = predictor.predict(df)

# 4. Visualize Results
# Plot actual vs predicted prices
Plotter.plot_prediction(df, predictions, title="Apple Stock Prediction")
2. Portfolio OptimizationUse Modern Portfolio Theory to allocate assets efficiently.Pythonfrom finlearn import PortfolioOptimizer

# Define your portfolio assets
tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']

# Initialize Optimizer
opt = PortfolioOptimizer(tickers=tickers, start='2023-01-01', end='2024-01-01')

# Run Monte Carlo Simulation to find the optimal allocation
results, allocation, metrics = opt.optimize(num_portfolios=5000)

print("Optimal Asset Allocation (Max Sharpe Ratio):")
print(allocation)
3. Technical Analysis & PlottingAnalyze trends using standard indicators.Pythonfrom finlearn import TechnicalIndicators, Plotter

# Load Data
df = DataLoader.download_data('NVDA', start='2023-01-01', end='2024-01-01')

# Add Indicators
ti = TechnicalIndicators(df)
df_tech = ti.add_all() # Adds RSI, MACD, Bollinger Bands, etc.

# Interactive Candlestick Chart
Plotter.candlestick(df_tech, title="NVIDIA Technical Analysis")
```

## Modules Overview

| Module | Description |
| :--- | :--- |
| **`finlearn.models`** | Contains Deep Learning classes (`TimeSeriesPredictor`) using TensorFlow/Keras. |
| **`finlearn.portfolio`** | Tools for asset allocation and portfolio optimization (`PortfolioOptimizer`). |
| **`finlearn.technical`** | Library of technical indicators (RSI, MACD, Bollinger Bands). |
| **`finlearn.data`** | Data ingestion layer wrapping `yfinance`. |
| **`finlearn.plotting`** | Visualization tools based on `plotly` for interactive charts. |

 ## Contributing

We welcome contributions! Please see the guidelines below:

* Fork the repository.
* Create a feature branch (`git checkout -b feature/AmazingFeature`).
* Commit your changes (`git commit -m 'Add some AmazingFeature'`).
* Push to the branch (`git push origin feature/AmazingFeature`).
* Open a Pull Request.
* Please ensure all new modules include unit tests in the `tests/` directory.

## License

* Distributed under the Apache 2.0 License. See `LICENSE` for more information.
* Built with ❤️ by Ankit Dutta