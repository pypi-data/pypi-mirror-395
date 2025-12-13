"""
Monte-Carlo Simulation for Energy Derivatives
==============================================

Implements Monte-Carlo methods for pricing energy-backed derivatives and 
generating confidence intervals and stress test scenarios.

Key Classes:
-----------
MonteCarloSimulator: Main simulation engine
PayoffSimulator: Payoff computation for paths

Key Methods:
-----------
simulate_paths(): Generate GBM price paths
compute_price(): Price via path averaging
confidence_interval(): Compute confidence bounds
stress_test(): Evaluate performance under different volatilities
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, List, Optional
from scipy import stats
import warnings


class MonteCarloSimulator:
    """
    Monte-Carlo simulation engine for energy-backed derivatives.
    
    Uses Geometric Brownian Motion (GBM) under risk-neutral measure:
    dS_t = r*S_t*dt + sigma*S_t*dW_t
    
    Solution: S_T = S_0 * exp((r - sigma²/2)*T + sigma*sqrt(T)*Z)
    where Z ~ N(0,1)
    
    Parameters
    ----------
    S0 : float
        Initial price
    K : float
        Strike/threshold price
    T : float
        Time to maturity (years)
    r : float
        Risk-free rate (annualized)
    sigma : float
        Volatility (annualized)
    num_simulations : int
        Number of Monte-Carlo paths (default: 10000)
    seed : int, optional
        Random seed for reproducibility
    payoff_type : str
        'call' for European call, 'redeemable' for direct claim
    """
    
    def __init__(self,
                 S0: float,
                 K: float,
                 T: float,
                 r: float,
                 sigma: float,
                 num_simulations: int = 10000,
                 seed: Optional[int] = None,
                 payoff_type: str = 'call'):
        """Initialize Monte-Carlo simulator."""
        
        if S0 <= 0:
            raise ValueError("S0 must be positive")
        if T <= 0:
            raise ValueError("T must be positive")
        if sigma <= 0:
            raise ValueError("sigma must be positive")
        if num_simulations < 1:
            raise ValueError("num_simulations must be at least 1")
        
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.num_simulations = num_simulations
        self.payoff_type = payoff_type
        self.rng = np.random.default_rng(seed)
        
        self.terminal_prices = None
        self.payoffs = None
        self._price_cache = None
    
    def simulate_paths(self, num_steps: int = 252, 
                      return_paths: bool = False) -> Optional[np.ndarray]:
        """
        Simulate GBM price paths.
        
        Parameters
        ----------
        num_steps : int
            Number of time steps per path (default: 252 for trading days)
        return_paths : bool
            If True, return full paths; if False, compute terminal prices
            
        Returns
        -------
        Optional[np.ndarray]
            If return_paths=True: array of shape (num_simulations, num_steps+1)
            If return_paths=False: None (stores terminal_prices internally)
        """
        dt = self.T / num_steps
        
        if return_paths:
            # Return full paths
            paths = np.zeros((self.num_simulations, num_steps + 1))
            paths[:, 0] = self.S0
            
            for step in range(1, num_steps + 1):
                Z = self.rng.normal(0, 1, self.num_simulations)
                paths[:, step] = paths[:, step-1] * np.exp(
                    (self.r - 0.5 * self.sigma ** 2) * dt + 
                    self.sigma * np.sqrt(dt) * Z
                )
            
            self.terminal_prices = paths[:, -1]
            return paths
        else:
            # Compute terminal prices only (more efficient)
            Z = self.rng.normal(0, 1, self.num_simulations)
            self.terminal_prices = self.S0 * np.exp(
                (self.r - 0.5 * self.sigma ** 2) * self.T + 
                self.sigma * np.sqrt(self.T) * Z
            )
            return None
    
    def _compute_payoffs(self) -> np.ndarray:
        """
        Compute payoff at maturity for all simulated paths.
        
        Returns
        -------
        np.ndarray
            Payoff values
        """
        if self.terminal_prices is None:
            raise RuntimeError("Must call simulate_paths() first")
        
        if self.payoff_type == 'call':
            payoffs = np.maximum(self.terminal_prices - self.K, 0)
        elif self.payoff_type == 'redeemable':
            payoffs = self.terminal_prices.copy()
        else:
            raise ValueError(f"Unknown payoff_type: {self.payoff_type}")
        
        self.payoffs = payoffs
        return payoffs
    
    def price(self, num_steps: int = 252) -> float:
        """
        Compute option price via Monte-Carlo.
        
        Price = exp(-rT) * E[Payoff]
        
        Parameters
        ----------
        num_steps : int
            Time steps per path
            
        Returns
        -------
        float
            Monte-Carlo price estimate
        """
        if self.terminal_prices is None:
            self.simulate_paths(num_steps)
        
        if self.payoffs is None:
            self._compute_payoffs()
        
        price = np.exp(-self.r * self.T) * np.mean(self.payoffs)
        self._price_cache = price
        return price
    
    def confidence_interval(self, num_steps: int = 252, 
                           confidence: float = 0.95) -> Tuple[float, float, float]:
        """
        Compute Monte-Carlo price with confidence interval.
        
        Parameters
        ----------
        num_steps : int
            Time steps per path
        confidence : float
            Confidence level (default: 0.95 for 95% CI)
            
        Returns
        -------
        Tuple[float, float, float]
            (price_estimate, lower_bound, upper_bound)
        """
        if self.terminal_prices is None:
            self.simulate_paths(num_steps)
        
        if self.payoffs is None:
            self._compute_payoffs()
        
        # Discount payoffs
        pv_payoffs = np.exp(-self.r * self.T) * self.payoffs
        
        mean_price = np.mean(pv_payoffs)
        std_price = np.std(pv_payoffs)
        se = std_price / np.sqrt(self.num_simulations)
        
        # Critical value
        alpha = 1 - confidence
        z_critical = stats.norm.ppf(1 - alpha / 2)
        
        ci_width = z_critical * se
        lower = mean_price - ci_width
        upper = mean_price + ci_width
        
        return mean_price, lower, upper
    
    def price_distribution(self) -> pd.DataFrame:
        """
        Get distribution statistics of terminal payoffs.
        
        Returns
        -------
        pd.DataFrame
            Statistics (mean, std, percentiles, etc.)
        """
        if self.payoffs is None:
            self.simulate_paths()
            self._compute_payoffs()
        
        pv_payoffs = np.exp(-self.r * self.T) * self.payoffs
        
        stats_dict = {
            'Mean': np.mean(pv_payoffs),
            'Std Dev': np.std(pv_payoffs),
            'Min': np.min(pv_payoffs),
            'Q1 (25%)': np.percentile(pv_payoffs, 25),
            'Median': np.median(pv_payoffs),
            'Q3 (75%)': np.percentile(pv_payoffs, 75),
            'Max': np.max(pv_payoffs),
            'Skewness': stats.skew(pv_payoffs),
            'Kurtosis': stats.kurtosis(pv_payoffs)
        }
        
        return pd.DataFrame(stats_dict, index=['Value']).T
    
    def stress_test(self, volatilities: Optional[List[float]] = None,
                   num_steps: int = 252) -> pd.DataFrame:
        """
        Price the derivative under different volatility scenarios.
        
        Parameters
        ----------
        volatilities : List[float], optional
            Volatilities to test (default: 0.05 to 1.00 in 0.05 steps)
        num_steps : int
            Time steps per path
            
        Returns
        -------
        pd.DataFrame
            Price under each volatility scenario
        """
        if volatilities is None:
            volatilities = np.arange(0.05, 1.05, 0.05)
        
        base_price = self._price_cache if self._price_cache is not None else self.price(num_steps)
        results = []
        for vol in volatilities:
            sim = MonteCarloSimulator(self.S0, self.K, self.T, self.r, vol,
                                     self.num_simulations, payoff_type=self.payoff_type)
            price = sim.price(num_steps)
            results.append({
                'Volatility': f"{vol:.1%}",
                'Price': price,
                'Change': price - base_price
            })
        
        return pd.DataFrame(results)
    
    def rate_sensitivity(self, rates: Optional[List[float]] = None,
                        num_steps: int = 252) -> pd.DataFrame:
        """
        Price the derivative under different interest rates.
        
        Parameters
        ----------
        rates : List[float], optional
            Rates to test
        num_steps : int
            Time steps per path
            
        Returns
        -------
        pd.DataFrame
            Price under each rate scenario
        """
        if rates is None:
            rates = np.arange(-0.02, 0.11, 0.01)
        
        results = []
        for rate in rates:
            sim = MonteCarloSimulator(self.S0, self.K, self.T, rate, self.sigma,
                                     self.num_simulations, payoff_type=self.payoff_type)
            price = sim.price(num_steps)
            results.append({
                'Rate': f"{rate:.1%}",
                'Price': price
            })
        
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
            'num_simulations': self.num_simulations,
            'payoff_type': self.payoff_type
        }


# Convenience functions
def price_energy_derivative_mc(S0: float, K: float, T: float, r: float, sigma: float,
                              num_simulations: int = 10000,
                              payoff_type: str = 'call') -> Tuple[float, float, float]:
    """
    Quick Monte-Carlo pricing with confidence interval.
    
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
    num_simulations : int
        Number of paths
    payoff_type : str
        Payoff type ('call' or 'redeemable')
        
    Returns
    -------
    Tuple[float, float, float]
        (price, lower_ci, upper_ci)
    """
    sim = MonteCarloSimulator(S0, K, T, r, sigma, num_simulations, payoff_type=payoff_type)
    return sim.confidence_interval()
