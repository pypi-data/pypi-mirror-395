import numpy as np
from scipy.stats import norm

class BlackScholesMerton:
    """
    Black-Scholes-Merton Model for European Option Pricing.
    Supports continuous dividend yield.
    """
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0):
        """
        Args:
            S: Spot price
            K: Strike price
            T: Time to maturity (years)
            r: Risk-free rate
            sigma: Volatility
            q: Continuous dividend yield (0 for non-dividend paying)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q

    def _d1_d2(self):
        d1 = (np.log(self.S / self.K) + (self.r - self.q + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2

    def price(self, option_type: str = 'call') -> float:
        d1, d2 = self._d1_d2()
        if option_type == 'call':
            price = (self.S * np.exp(-self.q * self.T) * norm.cdf(d1)) - \
                    (self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        else:
            price = (self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) - \
                    (self.S * np.exp(-self.q * self.T) * norm.cdf(-d1))
        return price

    def greeks(self, option_type: str = 'call') -> dict:
        """Calculates Delta, Gamma, Vega, Theta, Rho"""
        d1, d2 = self._d1_d2()
        
        # Common terms
        pdf_d1 = norm.pdf(d1)
        cdf_d1 = norm.cdf(d1) if option_type == 'call' else norm.cdf(-d1)
        
        # Delta
        if option_type == 'call':
            delta = np.exp(-self.q * self.T) * norm.cdf(d1)
        else:
            delta = np.exp(-self.q * self.T) * (norm.cdf(d1) - 1)
            
        # Gamma (Same for Call and Put)
        gamma = (np.exp(-self.q * self.T) * pdf_d1) / (self.S * self.sigma * np.sqrt(self.T))
        
        # Vega (Same for Call and Put)
        vega = self.S * np.exp(-self.q * self.T) * pdf_d1 * np.sqrt(self.T) / 100 # Scaled
        
        return {'delta': delta, 'gamma': gamma, 'vega': vega}