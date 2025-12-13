"""
Greeks Calculation for Energy Derivatives
==========================================

Computes option Greeks (Delta, Vega, Theta, Rho) via finite differences.

Greeks measure sensitivity to various market parameters and are essential
for risk management and hedging strategies.

Key Functions:
-----------
compute_greeks(): Compute all Greeks at once
delta(): Price sensitivity to underlying
vega(): Price sensitivity to volatility
theta(): Time decay
rho(): Interest rate sensitivity
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
from .binomial import BinomialTree
from .monte_carlo import MonteCarloSimulator
import warnings


class GreeksCalculator:
    """
    Compute Greeks (option sensitivities) via finite differences.
    
    Greeks tell us how the option price changes with market parameters:
    - Delta: ∂V/∂S (exposure to underlying)
    - Vega: ∂V/∂σ (exposure to volatility)
    - Theta: ∂V/∂T (time decay)
    - Rho: ∂V/∂r (interest rate exposure)
    
    Parameters
    ----------
    S0 : float
        Initial price
    K : float
        Strike price
    T : float
        Time to maturity
    r : float
        Risk-free rate
    sigma : float
        Volatility
    pricing_method : str
        'binomial' or 'monte_carlo'
    N : int (for binomial)
        Number of steps
    num_simulations : int (for MC)
        Number of paths
    payoff_type : str
        'call' or 'redeemable'
    seed : int, optional
        Random seed for Monte-Carlo based Greeks
    """
    
    def __init__(self,
                 S0: float,
                 K: float,
                 T: float,
                 r: float,
                 sigma: float,
                 pricing_method: str = 'binomial',
                 N: int = 100,
                 num_simulations: int = 5000,
                 payoff_type: str = 'call',
                 seed: Optional[int] = None):
        """Initialize Greeks calculator."""
        
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.pricing_method = pricing_method
        self.N = N
        self.num_simulations = num_simulations
        self.payoff_type = payoff_type
        self.seed = seed
        
        self._base_price = None
    
    def _price_function(self, **kwargs) -> float:
        """
        Internal pricing function that uses specified method.
        Allows parameter overrides for finite difference calculations.
        """
        # Get parameters, with overrides
        S0 = kwargs.get('S0', self.S0)
        K = kwargs.get('K', self.K)
        T = kwargs.get('T', self.T)
        r = kwargs.get('r', self.r)
        sigma = kwargs.get('sigma', self.sigma)
        
        if self.pricing_method == 'binomial':
            tree = BinomialTree(S0, K, T, r, sigma, self.N, self.payoff_type)
            return tree.price()
        elif self.pricing_method == 'monte_carlo':
            sim = MonteCarloSimulator(S0, K, T, r, sigma, 
                                     self.num_simulations, seed=self.seed,
                                     payoff_type=self.payoff_type)
            return sim.price()
        else:
            raise ValueError(f"Unknown pricing method: {self.pricing_method}")
    
    def base_price(self) -> float:
        """
        Compute base option price.
        
        Returns
        -------
        float
            Option price at current parameters
        """
        if self._base_price is None:
            self._base_price = self._price_function()
        return self._base_price
    
    def delta(self, bump_size: Optional[float] = None) -> float:
        """
        Compute Delta: ∂V/∂S
        
        Sensitivity to 1 unit change in underlying price.
        Central difference: Delta = (V(S+h) - V(S-h)) / (2h)
        
        Parameters
        ----------
        bump_size : float, optional
            Size of price bump (default: 1% of S0)
            
        Returns
        -------
        float
            Delta
        """
        if bump_size is None:
            bump_size = 0.01 * self.S0
        
        v_up = self._price_function(S0=self.S0 + bump_size)
        v_down = self._price_function(S0=self.S0 - bump_size)
        
        delta = (v_up - v_down) / (2 * bump_size)
        return delta
    
    def gamma(self, bump_size: Optional[float] = None) -> float:
        """
        Compute Gamma: ∂²V/∂S²
        
        Second derivative - rate of change of Delta.
        Gamma = (V(S+h) - 2*V(S) + V(S-h)) / h²
        
        Parameters
        ----------
        bump_size : float, optional
            Size of price bump (default: 1% of S0)
            
        Returns
        -------
        float
            Gamma
        """
        if bump_size is None:
            bump_size = 0.01 * self.S0
        
        v_center = self.base_price()
        v_up = self._price_function(S0=self.S0 + bump_size)
        v_down = self._price_function(S0=self.S0 - bump_size)
        
        gamma = (v_up - 2 * v_center + v_down) / (bump_size ** 2)
        return gamma
    
    def vega(self, bump_size: float = 0.01) -> float:
        """
        Compute Vega: ∂V/∂σ
        
        Sensitivity to 1% change in volatility.
        Vega = (V(σ+h) - V(σ-h)) / (2h)
        
        Note: Vega is typically reported per 1% volatility change,
        so we multiply by 0.01 for convention.
        
        Parameters
        ----------
        bump_size : float
            Volatility bump in decimal (default: 0.01 = 1%)
            
        Returns
        -------
        float
            Vega (per 1% volatility change)
        """
        if self.sigma - bump_size <= 0:
            warnings.warn("Volatility bump would make sigma non-positive, using smaller bump")
            bump_size = self.sigma / 4
        
        v_up = self._price_function(sigma=self.sigma + bump_size)
        v_down = self._price_function(sigma=self.sigma - bump_size)
        
        vega = (v_up - v_down) / (2 * bump_size)
        # Normalize to per 1% change
        vega_per_1pct = vega * 0.01
        return vega_per_1pct
    
    def theta(self, bump_size: float = 1/252, trading_days: int = 252) -> float:
        """
        Compute Theta: -∂V/∂T
        
        Time decay per day (negative of time derivative).
        Theta = -(V(T-h) - V(T)) / h, where h = 1 day
        
        Positive Theta means value decreases with time (time decay works for you).
        
        Parameters
        ----------
        bump_size : float
            Time bump (default: 1/252 = 1 trading day)
        trading_days : int
            Number of trading days in a year (used to convert bump_size to days)
            
        Returns
        -------
        float
            Theta per day (negative value = time decay)
        """
        if self.T - bump_size <= 0:
            warnings.warn("Time bump would make T non-positive, using smaller bump")
            bump_size = self.T / 2
        
        v_center = self.base_price()
        v_future = self._price_function(T=self.T - bump_size)
        
        # Convert to per-day decay regardless of bump size
        effective_days = bump_size * trading_days
        theta_per_day = (v_future - v_center) / effective_days
        
        return theta_per_day
    
    def rho(self, bump_size: float = 0.01) -> float:
        """
        Compute Rho: ∂V/∂r
        
        Sensitivity to 1% change in interest rate.
        Rho = (V(r+h) - V(r-h)) / (2h)
        
        Note: Rho is typically reported per 1% interest rate change.
        
        Parameters
        ----------
        bump_size : float
            Rate bump in decimal (default: 0.01 = 1%)
            
        Returns
        -------
        float
            Rho (per 1% interest rate change)
        """
        v_up = self._price_function(r=self.r + bump_size)
        v_down = self._price_function(r=self.r - bump_size)
        
        rho = (v_up - v_down) / (2 * bump_size)
        # Report per 1% rate move
        return rho * 0.01
    
    def compute_all_greeks(self) -> Dict[str, float]:
        """
        Compute all Greeks at once.
        
        Returns
        -------
        Dict[str, float]
            Dictionary containing all Greeks
        """
        greeks = {
            'Price': self.base_price(),
            'Delta': self.delta(),
            'Gamma': self.gamma(),
            'Vega': self.vega(),
            'Theta': self.theta(),
            'Rho': self.rho()
        }
        return greeks
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Return Greeks as a DataFrame for display.
        
        Returns
        -------
        pd.DataFrame
            Greeks with interpretations
        """
        greeks = self.compute_all_greeks()
        
        interpretations = {
            'Price': 'Current option price',
            'Delta': 'Price change per $1 underlying move (0-1 range)',
            'Gamma': 'Delta change per $1 underlying move (convexity)',
            'Vega': 'Price change per 1% volatility increase',
            'Theta': 'Daily time decay (negative = loses value each day)',
            'Rho': 'Price change per 1% interest rate increase'
        }
        
        data = {
            'Greek': list(greeks.keys()),
            'Value': list(greeks.values()),
            'Interpretation': [interpretations.get(g, '') for g in greeks.keys()]
        }
        
        return pd.DataFrame(data)
    
    def get_parameters_summary(self) -> Dict:
        """
        Return summary of parameters.
        
        Returns
        -------
        Dict
            Parameter dictionary
        """
        return {
            'S0': self.S0,
            'K': self.K,
            'T': self.T,
            'r': self.r,
            'sigma': self.sigma,
            'pricing_method': self.pricing_method,
            'N': self.N,
            'num_simulations': self.num_simulations,
            'payoff_type': self.payoff_type
        }


# Convenience function
def compute_energy_derivatives_greeks(S0: float, K: float, T: float, r: float, 
                                     sigma: float,
                                     pricing_method: str = 'binomial',
                                     N: int = 100,
                                     num_simulations: int = 5000,
                                     payoff_type: str = 'call',
                                     seed: Optional[int] = None) -> pd.DataFrame:
    """
    Quick Greeks computation for energy derivatives.
    
    Parameters
    ----------
    S0 : float
        Initial price
    K : float
        Strike price
    T : float
        Time to maturity
    r : float
        Risk-free rate
    sigma : float
        Volatility
    pricing_method : str
        'binomial' or 'monte_carlo'
    N : int
        Binomial steps
    num_simulations : int
        Number of Monte-Carlo paths if using MC method
    payoff_type : str
        'call' or 'redeemable'
    seed : int, optional
        Random seed for Monte-Carlo method
        
    Returns
    -------
    pd.DataFrame
        Greeks table
    """
    calc = GreeksCalculator(
        S0, K, T, r, sigma,
        pricing_method=pricing_method,
        N=N,
        num_simulations=num_simulations,
        payoff_type=payoff_type,
        seed=seed
    )
    return calc.to_dataframe()
