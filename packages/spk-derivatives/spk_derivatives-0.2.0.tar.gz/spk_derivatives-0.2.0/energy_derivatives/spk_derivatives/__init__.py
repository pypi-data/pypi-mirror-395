"""
SPK Derivatives: Energy Derivatives Pricing Framework
======================================================

A quantitative framework for pricing solar energy derivatives using
binomial trees, Monte-Carlo simulation, and risk-neutral valuation.

Features:
---------
- Binomial Option Pricing Model (BOPM)
- Monte-Carlo simulation for derivative pricing
- Greeks calculation (Delta, Vega, Theta, Rho, Gamma)
- NASA POWER API integration for solar irradiance data
- Professional workflow tools (validation, comparison, batch pricing)
- Context translation (GHI → kWh → dollar values)

Author: SPK Derivatives Team
Year: 2025
"""

__version__ = "0.2.0"
__author__ = "SPK Derivatives Team"

# Import modules
from . import binomial
from . import monte_carlo
from . import sensitivities
from . import data_loader
from . import data_loader_nasa
from . import live_data
from . import context_translator
from . import results_manager

# Optional: plots (requires matplotlib)
try:
    from . import plots
except ImportError:
    plots = None  # matplotlib not installed

# Import commonly used functions for convenience
from .data_loader_nasa import load_solar_parameters, fetch_nasa_data
from .data_loader import load_parameters
from .binomial import BinomialTree
from .monte_carlo import MonteCarloSimulator, price_energy_derivative_mc
from .sensitivities import GreeksCalculator, compute_energy_derivatives_greeks as calculate_greeks

# Import context translator (sophistication layer)
from .context_translator import (
    SolarSystemContext,
    PriceTranslator,
    VolatilityTranslator,
    GreeksTranslator,
    create_contextual_summary
)

# Import results manager (professional workflow)
from .results_manager import (
    PricingResult,
    ResultsComparator,
    PricingValidator,
    batch_price,
    comparative_context,
    break_even_analysis
)

__all__ = [
    # Modules
    'binomial',
    'monte_carlo',
    'sensitivities',
    'plots',
    'data_loader',
    'data_loader_nasa',
    'live_data',
    'context_translator',
    'results_manager',

    # Convenience functions
    'load_solar_parameters',
    'fetch_nasa_data',
    'load_parameters',
    'BinomialTree',
    'MonteCarloSimulator',
    'price_energy_derivative_mc',
    'GreeksCalculator',
    'calculate_greeks',

    # Context translation (sophistication layer)
    'SolarSystemContext',
    'PriceTranslator',
    'VolatilityTranslator',
    'GreeksTranslator',
    'create_contextual_summary',

    # Results management (professional workflow)
    'PricingResult',
    'ResultsComparator',
    'PricingValidator',
    'batch_price',
    'comparative_context',
    'break_even_analysis',
]
