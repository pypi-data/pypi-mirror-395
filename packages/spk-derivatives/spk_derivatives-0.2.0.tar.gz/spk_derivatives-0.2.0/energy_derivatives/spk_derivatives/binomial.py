"""
Binomial Option Pricing Model (BOPM)
====================================

Implements the Binomial Tree model for pricing energy-backed derivative claims.

Key Classes:
-----------
BinomialTree: Main pricing engine
PayoffFunction: Payoff structure definitions

Key Methods:
-----------
price_call_option(): Price call-style redeemable claims
price_european_claim(): Price direct redeemable claims
compute_convergence(): Show convergence as steps increase
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List
import warnings


class PayoffFunction:
    """
    Defines payoff structures for energy-backed claims.
    """
    
    @staticmethod
    def european_call(S_T: float, K: float) -> float:
        """
        European call payoff: max(S_T - K, 0)
        
        Parameters
        ----------
        S_T : float
            Terminal stock price
        K : float
            Strike price (threshold)
            
        Returns
        -------
        float
            Payoff at maturity
        """
        return max(S_T - K, 0)
    
    @staticmethod
    def redeemable_claim(S_T: float, K: float = 0) -> float:
        """
        Direct redeemable claim payoff: S_T
        (Ignores K, present for interface consistency)
        
        Parameters
        ----------
        S_T : float
            Terminal stock price
        K : float
            Unused (present for interface consistency)
            
        Returns
        -------
        float
            Terminal value (1-unit claim on energy)
        """
        return S_T


class BinomialTree:
    """
    Binomial Option Pricing Model for energy-backed derivatives.
    
    Uses risk-neutral valuation to compute arbitrage-free prices.
    
    Parameters
    ----------
    S0 : float
        Initial underlying price (energy price or CEIR-derived value)
    K : float
        Strike price (redemption threshold)
    T : float
        Time to maturity (years)
    r : float
        Risk-free rate (annualized)
    sigma : float
        Volatility of underlying (annualized)
    N : int
        Number of steps in the tree
    payoff_type : str
        'call' for European call, 'redeemable' for direct claim
        
    Attributes
    ----------
    dt : float
        Time step
    u : float
        Up factor
    d : float
        Down factor
    q : float
        Risk-neutral probability of up movement
    """
    
    def __init__(self, 
                 S0: float, 
                 K: float, 
                 T: float, 
                 r: float, 
                 sigma: float, 
                 N: int = 100,
                 payoff_type: str = 'call'):
        """Initialize the binomial tree."""
        
        if S0 <= 0:
            raise ValueError("S0 must be positive")
        if T <= 0:
            raise ValueError("T must be positive")
        if sigma <= 0:
            raise ValueError("sigma must be positive")
        if N < 1:
            raise ValueError("N must be at least 1")
        if r < -0.5:  # Allow negative rates but warn
            warnings.warn("Negative risk-free rates detected")
            
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.N = N
        self.payoff_type = payoff_type
        
        # Compute tree parameters
        self.dt = T / N
        self.u = np.exp(sigma * np.sqrt(self.dt))
        self.d = 1 / self.u
        
        # Risk-neutral probability
        exp_rdt = np.exp(r * self.dt)
        try:
            self.q = (exp_rdt - self.d) / (self.u - self.d)
        except ZeroDivisionError:
            raise ValueError("Invalid u, d parameters - cannot compute risk-neutral probability")
        
        # Validation
        if not (0 <= self.q <= 1):
            raise ValueError(
                f"Invalid parameters: risk-neutral probability q={self.q:.4f} not in [0,1]. "
                f"Consider adjusting sigma (current: {sigma}) or r (current: {r})"
            )
    
    def _generate_terminal_prices(self) -> np.ndarray:
        """
        Generate all possible terminal prices S_T(i) = S0 * u^(N-i) * d^i
        
        Returns
        -------
        np.ndarray
            Array of terminal prices (length N+1)
        """
        terminal_prices = np.zeros(self.N + 1)
        for i in range(self.N + 1):
            terminal_prices[i] = self.S0 * (self.u ** (self.N - i)) * (self.d ** i)
        return terminal_prices
    
    def _compute_payoffs(self, terminal_prices: np.ndarray) -> np.ndarray:
        """
        Compute payoff at maturity for each terminal price.
        
        Parameters
        ----------
        terminal_prices : np.ndarray
            Array of terminal prices
            
        Returns
        -------
        np.ndarray
            Payoff values at maturity
        """
        payoffs = np.zeros(len(terminal_prices))
        
        if self.payoff_type == 'call':
            for i, price in enumerate(terminal_prices):
                payoffs[i] = PayoffFunction.european_call(price, self.K)
        elif self.payoff_type == 'redeemable':
            for i, price in enumerate(terminal_prices):
                payoffs[i] = PayoffFunction.redeemable_claim(price, self.K)
        else:
            raise ValueError(f"Unknown payoff_type: {self.payoff_type}")
        
        return payoffs
    
    def _backward_induction(self, payoffs: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Backward induction through the tree to compute option price.
        
        Parameters
        ----------
        payoffs : np.ndarray
            Payoffs at maturity
            
        Returns
        -------
        Tuple[np.ndarray, float]
            (price at each node at t=0, option price at root)
        """
        # Initialize value array for current time step
        values = payoffs.copy()
        discount = np.exp(-self.r * self.dt)
        
        # Backward iterate through time steps
        for step in range(self.N - 1, -1, -1):
            # Number of nodes at this step
            nodes = step + 1
            new_values = np.zeros(nodes)
            
            for i in range(nodes):
                # Value is discounted expected value under risk-neutral measure
                new_values[i] = discount * (self.q * values[i] + (1 - self.q) * values[i + 1])
            
            values = new_values
        
        option_price = values[0]
        return values, option_price
    
    def price(self) -> float:
        """
        Compute the option price using binomial model.
        
        Returns
        -------
        float
            Arbitrage-free option price
        """
        terminal_prices = self._generate_terminal_prices()
        payoffs = self._compute_payoffs(terminal_prices)
        _, option_price = self._backward_induction(payoffs)
        return option_price
    
    def price_with_tree(self) -> Tuple[float, Dict]:
        """
        Compute option price and return full tree information.
        
        Returns
        -------
        Tuple[float, Dict]
            (option_price, tree_info)
        """
        terminal_prices = self._generate_terminal_prices()
        payoffs = self._compute_payoffs(terminal_prices)
        values, option_price = self._backward_induction(payoffs)
        
        tree_info = {
            'terminal_prices': terminal_prices,
            'payoffs': payoffs,
            'root_values': values,
            'q': self.q,
            'u': self.u,
            'd': self.d,
            'dt': self.dt
        }
        
        return option_price, tree_info
    
    def sensitivity_analysis_convergence(self, 
                                        step_range: List[int] = None) -> pd.DataFrame:
        """
        Show how price converges as number of steps increases.
        
        Parameters
        ----------
        step_range : List[int], optional
            Steps to test (default: [10, 25, 50, 100, 200, 500])
            
        Returns
        -------
        pd.DataFrame
            Convergence table with steps and prices
        """
        if step_range is None:
            step_range = [10, 25, 50, 100, 200, 500]
        
        results = []
        for N in step_range:
            tree = BinomialTree(self.S0, self.K, self.T, self.r, self.sigma, 
                               N, self.payoff_type)
            price = tree.price()
            results.append({'Steps': N, 'Price': price})
        
        return pd.DataFrame(results)
    
    def get_parameters_summary(self) -> Dict:
        """
        Return summary of model parameters.
        
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
            'N': self.N,
            'payoff_type': self.payoff_type,
            'u': self.u,
            'd': self.d,
            'q': self.q,
            'dt': self.dt
        }


# Convenience functions
def price_energy_call(S0: float, K: float, T: float, r: float, sigma: float, 
                     N: int = 100) -> float:
    """
    Price an energy-backed call option (European style).
    
    Parameters
    ----------
    S0 : float
        Initial energy price or CEIR value
    K : float
        Strike/redemption threshold
    T : float
        Time to maturity (years)
    r : float
        Risk-free rate
    sigma : float
        Volatility
    N : int
        Tree steps
        
    Returns
    -------
    float
        Call option price
    """
    tree = BinomialTree(S0, K, T, r, sigma, N, 'call')
    return tree.price()


def price_energy_claim(S0: float, T: float, r: float, sigma: float, 
                      N: int = 100) -> float:
    """
    Price a direct energy-backed redeemable claim.
    
    Parameters
    ----------
    S0 : float
        Initial energy price
    T : float
        Time to maturity (years)
    r : float
        Risk-free rate
    sigma : float
        Volatility
    N : int
        Tree steps
        
    Returns
    -------
    float
        Claim price
    """
    tree = BinomialTree(S0, K=0, T=T, r=r, sigma=sigma, N=N, payoff_type='redeemable')
    return tree.price()
