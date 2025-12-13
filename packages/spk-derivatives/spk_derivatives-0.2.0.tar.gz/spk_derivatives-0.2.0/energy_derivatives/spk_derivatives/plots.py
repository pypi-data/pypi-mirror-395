"""
Visualization and Plotting for Energy Derivatives
=================================================

Comprehensive plotting utilities for results visualization including:
- Convergence analysis
- Price distributions
- Greeks surfaces and curves
- Stress test comparisons

Key Functions:
-----------
plot_binomial_convergence(): Show how price converges with steps
plot_monte_carlo_distribution(): Terminal payoff distribution
plot_greeks_curves(): Sensitivity curves for each Greek
plot_stress_test(): Volatility/rate stress test results
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, List, Tuple
from .binomial import BinomialTree
from .monte_carlo import MonteCarloSimulator
from .sensitivities import GreeksCalculator
import warnings


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class EnergyDerivativesPlotter:
    """
    Comprehensive plotting for energy derivatives analysis.
    """
    
    @staticmethod
    def plot_binomial_convergence(S0: float, K: float, T: float, r: float, 
                                 sigma: float, payoff_type: str = 'call',
                                 step_range: Optional[List[int]] = None,
                                 figsize: Tuple[int, int] = (10, 6),
                                 save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot convergence of binomial price as steps increase.
        
        Parameters
        ----------
        S0, K, T, r, sigma : float
            Model parameters
        payoff_type : str
            'call' or 'redeemable'
        step_range : List[int], optional
            Steps to test (default: [10, 25, 50, 100, 200, 500])
        figsize : Tuple[int, int]
            Figure size
        save_path : str, optional
            Path to save figure
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        if step_range is None:
            step_range = [10, 25, 50, 100, 200, 500]
        
        tree_ref = BinomialTree(S0, K, T, r, sigma, step_range[-1], payoff_type)
        prices = []
        
        for N in step_range:
            tree = BinomialTree(S0, K, T, r, sigma, N, payoff_type)
            price = tree.price()
            prices.append(price)
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(step_range, prices, 'o-', linewidth=2, markersize=8, color='steelblue')
        
        # Add convergence indicator
        if len(prices) >= 2:
            final_price = prices[-1]
            ax.axhline(y=final_price, color='red', linestyle='--', alpha=0.7, 
                      label=f'Converged price: ${final_price:.2f}')
        
        ax.set_xlabel('Number of Steps (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Option Price ($)', fontsize=12, fontweight='bold')
        ax.set_title(f'Binomial Tree Convergence\n({payoff_type.capitalize()} | ' + 
                    f'S₀=${S0:.2f}, K=${K:.2f}, σ={sigma:.1%})',
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    @staticmethod
    def plot_monte_carlo_distribution(S0: float, K: float, T: float, r: float,
                                     sigma: float, payoff_type: str = 'call',
                                     num_simulations: int = 10000,
                                     figsize: Tuple[int, int] = (12, 5),
                                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot terminal value distribution from Monte-Carlo simulation.
        
        Parameters
        ----------
        S0, K, T, r, sigma : float
            Model parameters
        payoff_type : str
            'call' or 'redeemable'
        num_simulations : int
            Number of paths
        figsize : Tuple[int, int]
            Figure size
        save_path : str, optional
            Path to save figure
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        sim = MonteCarloSimulator(S0, K, T, r, sigma, num_simulations, payoff_type=payoff_type)
        sim.simulate_paths()
        payoffs = sim._compute_payoffs()
        pv_payoffs = np.exp(-r * T) * payoffs
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Terminal prices histogram
        ax = axes[0]
        ax.hist(sim.terminal_prices, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
        ax.axvline(S0, color='red', linestyle='--', linewidth=2, label=f'S₀ = ${S0:.2f}')
        ax.axvline(np.mean(sim.terminal_prices), color='green', linestyle='--', 
                  linewidth=2, label=f'Mean = ${np.mean(sim.terminal_prices):.2f}')
        ax.set_xlabel('Terminal Price ($)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title('Terminal Stock Price Distribution', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Payoff distribution
        ax = axes[1]
        ax.hist(pv_payoffs, bins=50, alpha=0.7, color='coral', edgecolor='black')
        ax.axvline(np.mean(pv_payoffs), color='darkred', linestyle='--', linewidth=2,
                  label=f'Mean Payoff = ${np.mean(pv_payoffs):.2f}')
        ax.set_xlabel('Present Value of Payoff ($)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
        ax.set_title(f'Payoff Distribution ({payoff_type.capitalize()})', 
                    fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.suptitle(f'Monte-Carlo Simulation Results ({num_simulations:,} paths)\n' + 
                    f'S₀=${S0:.2f}, K=${K:.2f}, T={T:.2f}yr, σ={sigma:.1%}, r={r:.1%}',
                    fontsize=13, fontweight='bold', y=1.00)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    @staticmethod
    def plot_greeks_curves(S0: float, K: float, T: float, r: float, sigma: float,
                          payoff_type: str = 'call',
                          figsize: Tuple[int, int] = (14, 10),
                          save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot how Greeks change with underlying price.
        
        Parameters
        ----------
        S0, K, T, r, sigma : float
            Model parameters
        payoff_type : str
            'call' or 'redeemable'
        figsize : Tuple[int, int]
            Figure size
        save_path : str, optional
            Path to save figure
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        # Range of underlying prices
        price_range = np.linspace(S0 * 0.5, S0 * 1.5, 20)
        
        greeks_data = {
            'Price': [],
            'Delta': [],
            'Gamma': [],
            'Vega': [],
            'Theta': [],
            'Rho': []
        }
        
        for price in price_range:
            calc = GreeksCalculator(price, K, T, r, sigma, 'binomial', 50, payoff_type=payoff_type)
            greeks = calc.compute_all_greeks()
            
            for greek_name in ['Price', 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho']:
                greeks_data[greek_name].append(greeks[greek_name])
        
        fig, axes = plt.subplots(2, 3, figsize=figsize)
        
        # Plot each Greek
        greek_list = ['Price', 'Delta', 'Gamma', 'Vega', 'Theta', 'Rho']
        colors = ['steelblue', 'orange', 'green', 'red', 'purple', 'brown']
        
        for idx, (greek, color) in enumerate(zip(greek_list, colors)):
            ax = axes[idx // 3, idx % 3]
            ax.plot(price_range, greeks_data[greek], 'o-', linewidth=2, 
                   markersize=6, color=color, label=greek)
            
            ax.axvline(S0, color='gray', linestyle='--', alpha=0.5, linewidth=1)
            ax.set_xlabel('Underlying Price ($)', fontsize=10, fontweight='bold')
            ax.set_ylabel(f'{greek} Value', fontsize=10, fontweight='bold')
            ax.set_title(f'{greek} vs Underlying Price', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
        
        fig.suptitle(f'Greeks Analysis\n(S₀=${S0:.2f}, K=${K:.2f}, T={T:.2f}yr, ' + 
                    f'σ={sigma:.1%}, r={r:.1%})',
                    fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    @staticmethod
    def plot_stress_test_volatility(S0: float, K: float, T: float, r: float,
                                   payoff_type: str = 'call',
                                   num_simulations: int = 5000,
                                   figsize: Tuple[int, int] = (10, 6),
                                   save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot price under different volatility scenarios.
        
        Parameters
        ----------
        S0, K, T, r : float
            Model parameters (sigma varies)
        payoff_type : str
            'call' or 'redeemable'
        num_simulations : int
            MC paths
        figsize : Tuple[int, int]
            Figure size
        save_path : str, optional
            Path to save figure
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        volatilities = np.arange(0.05, 1.05, 0.05)
        prices = []
        
        for vol in volatilities:
            sim = MonteCarloSimulator(S0, K, T, r, vol, num_simulations, payoff_type=payoff_type)
            price = sim.price()
            prices.append(price)
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(volatilities * 100, prices, 'o-', linewidth=2, markersize=8, 
               color='steelblue', label='Option Price')
        
        ax.fill_between(volatilities * 100, prices, alpha=0.2, color='steelblue')
        ax.set_xlabel('Volatility (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Option Price ($)', fontsize=12, fontweight='bold')
        ax.set_title(f'Stress Test: Price vs Volatility\n({payoff_type.capitalize()} | ' + 
                    f'S₀=${S0:.2f}, K=${K:.2f}, T={T:.2f}yr, r={r:.1%})',
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    @staticmethod
    def plot_stress_test_rate(S0: float, K: float, T: float, sigma: float,
                             payoff_type: str = 'call',
                             num_simulations: int = 5000,
                             figsize: Tuple[int, int] = (10, 6),
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot price under different interest rate scenarios.
        
        Parameters
        ----------
        S0, K, T, sigma : float
            Model parameters (rate varies)
        payoff_type : str
            'call' or 'redeemable'
        num_simulations : int
            MC paths
        figsize : Tuple[int, int]
            Figure size
        save_path : str, optional
            Path to save figure
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        rates = np.arange(-0.02, 0.11, 0.01)
        prices = []
        
        for rate in rates:
            sim = MonteCarloSimulator(S0, K, T, rate, sigma, num_simulations, payoff_type=payoff_type)
            price = sim.price()
            prices.append(price)
        
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(rates * 100, prices, 's-', linewidth=2, markersize=8,
               color='coral', label='Option Price')
        
        ax.fill_between(rates * 100, prices, alpha=0.2, color='coral')
        ax.set_xlabel('Interest Rate (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Option Price ($)', fontsize=12, fontweight='bold')
        ax.set_title(f'Stress Test: Price vs Interest Rate\n({payoff_type.capitalize()} | ' + 
                    f'S₀=${S0:.2f}, K=${K:.2f}, T={T:.2f}yr, σ={sigma:.1%})',
                    fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
    
    @staticmethod
    def plot_price_comparison(S0: float, K: float, T: float, r: float, sigma: float,
                             payoff_type: str = 'call',
                             N: int = 100,
                             figsize: Tuple[int, int] = (10, 6),
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Compare binomial vs Monte-Carlo pricing.
        
        Parameters
        ----------
        S0, K, T, r, sigma : float
            Model parameters
        payoff_type : str
            'call' or 'redeemable'
        N : int
            Binomial steps
        figsize : Tuple[int, int]
            Figure size
        save_path : str, optional
            Path to save figure
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        # Binomial
        tree = BinomialTree(S0, K, T, r, sigma, N, payoff_type)
        binomial_price = tree.price()
        
        # Monte-Carlo
        sim = MonteCarloSimulator(S0, K, T, r, sigma, 10000, payoff_type=payoff_type)
        mc_price, mc_low, mc_high = sim.confidence_interval()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        methods = ['Binomial\n(N=100)', 'Monte-Carlo\n(N=10,000)']
        prices = [binomial_price, mc_price]
        colors = ['steelblue', 'coral']
        
        bars = ax.bar(methods, prices, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        
        # Add error bars for MC
        ax.errorbar(1, mc_price, yerr=[[mc_price - mc_low], [mc_high - mc_price]], 
                   fmt='none', ecolor='black', capsize=10, capthick=2, linewidth=2)
        
        # Add value labels
        for bar, price in zip(bars, prices):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${price:.2f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.set_ylabel('Option Price ($)', fontsize=12, fontweight='bold')
        ax.set_title(f'Pricing Method Comparison\n({payoff_type.capitalize()} | ' + 
                    f'S₀=${S0:.2f}, K=${K:.2f}, T={T:.2f}yr, σ={sigma:.1%}, r={r:.1%})',
                    fontsize=13, fontweight='bold')
        ax.set_ylim(0, max(prices) * 1.3)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        return fig
