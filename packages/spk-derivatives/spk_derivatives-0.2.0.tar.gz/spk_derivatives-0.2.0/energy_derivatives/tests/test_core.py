import sys
from pathlib import Path
import numpy as np
from scipy.stats import norm

repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from spk_derivatives.binomial import BinomialTree  # noqa: E402
from spk_derivatives.monte_carlo import MonteCarloSimulator  # noqa: E402
from spk_derivatives.sensitivities import GreeksCalculator  # noqa: E402
from spk_derivatives.data_loader import load_parameters  # noqa: E402


def _black_scholes_call(S0: float, K: float, T: float, r: float, sigma: float) -> float:
    """Closed-form Black-Scholes call for sanity checks."""
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def test_binomial_matches_black_scholes_with_many_steps():
    S0 = K = 100.0
    sigma = 0.20
    T = 1.0
    r = 0.05
    expected = _black_scholes_call(S0, K, T, r, sigma)

    tree = BinomialTree(S0, K, T, r, sigma, N=500)
    price = tree.price()

    assert abs(price - expected) < 0.35  # within a few dimes of BS price


def test_monte_carlo_is_seed_reproducible():
    params = dict(S0=100.0, K=100.0, T=1.0, r=0.05, sigma=0.25, num_simulations=5000)
    sim1 = MonteCarloSimulator(seed=123, payoff_type='call', **params)
    sim2 = MonteCarloSimulator(seed=123, payoff_type='call', **params)

    price1 = sim1.price()
    price2 = sim2.price()
    assert np.isclose(price1, price2)


def test_data_loader_synthetic_path_when_disabled_fallback():
    params = load_parameters(data_dir="__no_such_dir__", use_repo_fallback=False)
    assert params['energy_prices'].size > 10
    assert params['sigma'] > 0
    assert params['S0'] > 0


def test_greeks_theta_negative_and_rho_positive():
    calc = GreeksCalculator(
        S0=100.0, K=100.0, T=1.0, r=0.05, sigma=0.20,
        pricing_method='binomial', N=200
    )
    theta = calc.theta()
    rho = calc.rho()

    assert theta < 0  # time decay should be negative for long call
    assert rho > 0    # call value rises with rates
