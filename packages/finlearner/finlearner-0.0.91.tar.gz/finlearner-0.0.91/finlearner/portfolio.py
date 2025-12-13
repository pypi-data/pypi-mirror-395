import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PortfolioOptimizer:
    """
    Optimizes asset allocation using Mean-Variance Optimization (Markowitz).
    """
    def __init__(self, tickers: list, start: str, end: str):
        import yfinance as yf
        self.data = yf.download(tickers, start=start, end=end)['Adj Close']
        self.returns = self.data.pct_change()
        
    def optimize(self, num_portfolios: int = 5000):
        """
        Simulates random portfolios to find the Efficient Frontier.
        """
        results = np.zeros((3, num_portfolios))
        weights_record = []
        
        mean_daily_returns = self.returns.mean()
        cov_matrix = self.returns.cov()
        
        for i in range(num_portfolios):
            weights = np.random.random(len(self.data.columns))
            weights /= np.sum(weights)
            weights_record.append(weights)
            
            # Portfolio return and volatility
            portfolio_return = np.sum(mean_daily_returns * weights) * 252
            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
            
            results[0,i] = portfolio_std_dev
            results[1,i] = portfolio_return
            results[2,i] = results[1,i] / results[0,i] # Sharpe Ratio

        # Find max Sharpe ratio
        max_sharpe_idx = np.argmax(results[2])
        sdp, rp = results[0,max_sharpe_idx], results[1,max_sharpe_idx]
        max_sharpe_allocation = pd.DataFrame(weights_record[max_sharpe_idx], index=self.data.columns, columns=['allocation'])
        
        return results, max_sharpe_allocation, (sdp, rp)