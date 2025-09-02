import yfinance as yf
import numpy as np
import pandas as probability_default
from scipy.stats import norm
from scipy.optimize import root

N = norm.cdf

def merton_model(E, D, equity_volatility, r, T):
    """
    E = Market value of equity
    D = default barrier (value of companies debt)
    equity_volatility: Volatility of equity
    r: Treasury bonds 1 year rate
    T: Time to maturity in years
    """
    # Defining the system of equations to solve
    def equations(x):
        V, sigma_v = x
        d1 = (np.log(V/D) + (r + 0.5 * sigma_v**2) * T) / (sigma_v * np.sqrt(T))
        d2 = d1 - sigma_v * np.sqrt(T)
        eq1 = V * N(d1) - D * np.exp(-r * T) * N(d2) - E
        eq2 = N(d1) * V * sigma_v / E - equity_volatility # Equation for equity volatility
        return [eq1, eq2]

    # Initial guess: V = E + D, sigma_v = equity_volatility * E / (E + D)
    V_guess = E + D
    sigma_v_guess = equity_volatility * E / (E + D)
    sol = root(equations, [V_guess, sigma_v_guess])
    V, sigma_v = sol.x

    distance_default = (np.log(V/D) + (r - 0.5 * sigma_v**2) * T) / (sigma_v * np.sqrt(T))
    probability_default = N(-distance_default)
    return float(V), float(sigma_v), float(distance_default), float(probability_default)

