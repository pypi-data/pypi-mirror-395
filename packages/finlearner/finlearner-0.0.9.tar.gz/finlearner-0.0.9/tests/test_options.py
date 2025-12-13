import pytest
import numpy as np
from finlearner.options import BlackScholesMerton

def test_call_price():
    # S=100, K=100, T=1, r=5%, sigma=20% -> Call Price should be ~10.45
    bs = BlackScholesMerton(S=100, K=100, T=1, r=0.05, sigma=0.2)
    price = bs.price('call')
    assert 10.40 <= price <= 10.50

def test_put_call_parity():
    # C - P = S - K * e^(-rT)
    bs = BlackScholesMerton(S=100, K=100, T=1, r=0.05, sigma=0.2)
    call_price = bs.price('call')
    put_price = bs.price('put')
    
    lhs = call_price - put_price
    rhs = 100 - 100 * np.exp(-0.05 * 1)
    
    assert np.isclose(lhs, rhs, atol=0.01)

def test_greeks():
    bs = BlackScholesMerton(S=100, K=100, T=1, r=0.05, sigma=0.2)
    greeks = bs.greeks('call')
    
    assert 'delta' in greeks
    assert 'gamma' in greeks
    assert 'vega' in greeks
    # Delta of ATM call should be approx 0.5-0.6
    assert 0.5 <= greeks['delta'] <= 0.7