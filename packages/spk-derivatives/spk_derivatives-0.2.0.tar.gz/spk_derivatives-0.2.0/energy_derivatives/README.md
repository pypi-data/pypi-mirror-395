# Energy-Backed Derivatives Pricing Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research Software](https://img.shields.io/badge/status-research--ready-green.svg)](RESEARCH_USE_NOTICE.md)

A rigorous quantitative framework for pricing renewable energy-backed digital assets using modern derivative pricing theory.

## ⚠️ Research Software Notice

**Version:** 0.2.0-research | **Status:** Research-Grade Software

This is research-grade software for academic use. See [RESEARCH_USE_NOTICE.md](RESEARCH_USE_NOTICE.md) for full details.

**✅ Validated for:** Academic research, education, methodology validation, proof-of-concept
**❌ Not validated for:** Production financial systems, real money trading

## Installation

### Quick Start (Research Release)

```bash
# Install the stable research release
pip install git+https://github.com/YOUR_USERNAME/solarpunk-bitcoin.git@v0.2.0-research
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/solarpunk-bitcoin.git
cd solarpunk-bitcoin

# Install with optional dependencies
pip install -e ".[viz,dev]"    # Visualization + development tools
pip install -e ".[all]"         # All optional dependencies
```

### Basic Usage

```python
from data_loader_nasa import load_solar_parameters
from binomial import BinomialTree

# Load solar parameters (Taiwan by default)
params = load_solar_parameters()

# Price a call option
tree = BinomialTree(**params, N=1000, payoff_type='call')
price = tree.price()
print(f"Option price: ${price:.6f}")
```

## Overview

This project develops and implements a comprehensive framework for pricing **energy-backed digital assets** (such as SolarPunkCoin tokens) using:

- **Binomial Option Pricing Model (BOPM)** for exact pricing
- **Monte-Carlo Simulation** for stress testing and confidence intervals
- **Greeks Calculation** for risk management and hedging
- **Dual Data Sources**: Bitcoin CEIR + NASA Solar Data for calibration

### Data Sources

**Two parallel calibration paths**:

1. **Bitcoin CEIR Data** (`data_loader.py`)
   - Historical Bitcoin price and energy consumption (2018-2025)
   - Demonstrates energy costs as fundamental value anchors
   - Lower volatility (~70%), suitable for crypto derivatives

2. **NASA Solar Data** (`data_loader_nasa.py`) **⭐ NEW**
   - Real satellite-derived solar irradiance (2020-2024)
   - Location: Taoyuan, Taiwan (24.99°N, 121.30°E)
   - Source: NASA POWER API (Global Horizontal Irradiance)
   - Higher volatility (200% deseasoned), captures weather risk
   - Direct application to renewable energy derivatives

### Connection to CEIR

The **Cumulative Energy Investment Ratio (CEIR)** framework establishes that:
- Energy costs create fundamental value anchors for cryptocurrencies
- Mining produces cumulative security that can be valued financially
- Renewable energy output has intrinsic economic value

This project extends CEIR theory by:
1. Deriving energy-backed asset prices from CEIR
2. Applying rigorous no-arbitrage derivative pricing
3. Computing comprehensive risk metrics (Greeks)
4. Enabling portfolio hedging and risk management
5. **NEW**: Calibrating with real NASA satellite data for solar energy

## Project Structure

```
energy_derivatives/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── binomial.py              # Binomial Tree pricing engine
│   ├── monte_carlo.py           # Monte-Carlo simulation
│   ├── sensitivities.py         # Greeks calculation
│   ├── plots.py                 # Visualization utilities
│   └── data_loader.py           # CEIR data loading and processing
├── notebooks/
│   └── main.ipynb               # Complete demonstration notebook
├── data/                        # Data storage
├── results/                     # Generated results and plots
├── docs/                        # Documentation
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Reproducibility & Data
- Monte-Carlo uses a per-instance RNG; pass `seed=` for deterministic paths.
- `load_parameters(data_dir=..., use_repo_fallback=True)` will fall back to the repo `empirical/` folder; set `use_repo_fallback=False` to force synthetic data for demos/tests.
- Theta is returned as per-day time decay (negative for long calls); Rho is quoted per 1% rate change.
- Optional live fetch: `load_parameters(..., use_live_if_missing=True)` will pull recent BTC data from CoinGecko with synthetic energy estimates if local data is missing.
- Services: FastAPI (`energy_derivatives.api.main`) and Streamlit dashboard (`energy_derivatives/frontend/app.py`) ship as ready-to-run surfaces.

## Key Modules

### 1. `binomial.py` - Binomial Tree Pricing

Implements the Binomial Option Pricing Model for European derivatives.

**Key Classes:**
- `BinomialTree`: Main pricing engine
- `PayoffFunction`: Payoff structure definitions

**Example:**
```python
from src.binomial import BinomialTree

# Create binomial tree
tree = BinomialTree(
    S0=100,           # Initial price
    K=100,            # Strike price
    T=1.0,            # Time to maturity (years)
    r=0.05,           # Risk-free rate
    sigma=0.20,       # Volatility
    N=100,            # Number of steps
    payoff_type='call'  # 'call' or 'redeemable'
)

# Price the option
price = tree.price()
print(f"Option price: ${price:.2f}")
```

### 2. `monte_carlo.py` - Monte-Carlo Simulation

Simulates price paths using Geometric Brownian Motion under risk-neutral measure.

**Key Classes:**
- `MonteCarloSimulator`: Main simulation engine
- Generates terminal price distributions
- Computes confidence intervals
- Enables stress testing

**Example:**
```python
from src.monte_carlo import MonteCarloSimulator

sim = MonteCarloSimulator(
    S0=100,
    K=100,
    T=1.0,
    r=0.05,
    sigma=0.20,
    num_simulations=10000
)

# Get price with confidence interval
price, lower, upper = sim.confidence_interval()
print(f"Price: ${price:.2f}, 95% CI: [${lower:.2f}, ${upper:.2f}]")
```

### 3. `sensitivities.py` - Greeks Calculation

Computes option Greeks (Delta, Gamma, Vega, Theta, Rho) via finite differences.

**Key Classes:**
- `GreeksCalculator`: Computes all Greeks

**Example:**
```python
from src.sensitivities import GreeksCalculator

calc = GreeksCalculator(
    S0=100, K=100, T=1.0, r=0.05, sigma=0.20,
    pricing_method='binomial'
)

# Compute all Greeks
greeks = calc.compute_all_greeks()
print(f"Delta: {greeks['Delta']:.4f}")
print(f"Vega: {greeks['Vega']:.4f}")

# Display as table
print(calc.to_dataframe())
```

### 4. `plots.py` - Visualization

Comprehensive plotting utilities for analysis and results.

**Key Functions:**
- `plot_binomial_convergence()`: Show price convergence
- `plot_monte_carlo_distribution()`: Terminal payoff distribution
- `plot_greeks_curves()`: Greeks vs underlying price
- `plot_stress_test_volatility()`: Price under different volatilities
- `plot_stress_test_rate()`: Price under different rates

**Example:**
```python
from src.plots import EnergyDerivativesPlotter

EnergyDerivativesPlotter.plot_greeks_curves(
    S0=100, K=100, T=1.0, r=0.05, sigma=0.20,
    save_path='results/greeks.png'
)
```

### 5. `data_loader.py` - Data Integration

Loads empirical CEIR data from Bitcoin to calibrate models.

**Key Functions:**
- `load_ceir_data()`: Load CEIR dataset
- `compute_energy_price()`: Derive energy prices from CEIR
- `estimate_volatility()`: Estimate from historical prices
- `load_parameters()`: Load all parameters for pricing

**Example:**
```python
from src.data_loader import load_parameters

# Load empirical data and calibrate
params = load_parameters(
    data_dir='../empirical',
    T=1.0,
    r=0.05
)

S0 = params['S0']          # Initial energy price
sigma = params['sigma']    # Volatility
```

## Usage Guide

### Installation

```bash
# Clone or navigate to project
cd energy_derivatives

# Install dependencies
pip install -r requirements.txt
```

### Testing (optional)
```bash
pytest energy_derivatives/tests
```

### API Server (FastAPI)
```bash
uvicorn energy_derivatives.api.main:app --reload
# Then POST to /price, /greeks, /stress
# Optional: set API_KEY env and pass header x-api-key
```

### Streamlit Dashboard
```bash
streamlit run energy_derivatives/frontend/app.py
```

### Export Snapshot for Oracle
```bash
python energy_derivatives/src/export_snapshot.py
# writes energy_derivatives/results/snapshot.json
```

### Generate Report (Markdown + optional PDF)
```bash
python energy_derivatives/src/report.py
# or: make report
```

### Docker Builds
```bash
make docker-api         # builds API image (Dockerfile.api)
make docker-dashboard   # builds Streamlit image (Dockerfile.dashboard)
docker-compose up --build  # run API + dashboard together
```

### Makefile shortcuts
- `make api` / `make dashboard`
- `make tests-python` / `make tests-solidity`
- `make export-snapshot`
- `make tests-security` (dockerized Slither)
- `make report`

### Lockfiles
- `energy_derivatives/requirements-lock.txt` pins Python deps
- `blockchain/package-lock.json` pins JS deps

### Quick Start

**Run the complete demonstration notebook:**

```bash
jupyter notebook notebooks/main.ipynb
```

This will:
1. Load empirical CEIR data
2. Price energy derivatives using both methods
3. Compute all Greeks
4. Generate stress tests
5. Create publication-quality visualizations
6. Summarize results and applications

### Basic Pricing Example

```python
import sys
sys.path.insert(0, 'src')

from binomial import BinomialTree
from monte_carlo import MonteCarloSimulator
from data_loader import load_parameters

# Load empirical data
params = load_parameters(data_dir='empirical', T=1.0, r=0.05)

# Binomial pricing
tree = BinomialTree(
    params['S0'], params['K'], params['T'], 
    params['r'], params['sigma'], N=100, 
    payoff_type='call'
)
binomial_price = tree.price()

# Monte-Carlo pricing
sim = MonteCarloSimulator(
    params['S0'], params['K'], params['T'], 
    params['r'], params['sigma'], 
    num_simulations=10000
)
mc_price, lower, upper = sim.confidence_interval()

print(f"Binomial:  ${binomial_price:.4f}")
print(f"MC:        ${mc_price:.4f} [${lower:.4f}, ${upper:.4f}]")
```

## Mathematical Framework

### 1. Geometric Brownian Motion

Under the risk-neutral measure:

$$dS_t = r S_t dt + \sigma S_t dW_t$$

Terminal price:
$$S_T = S_0 \exp\left(\left(r - \frac{\sigma^2}{2}\right)T + \sigma\sqrt{T}Z\right)$$

### 2. Binomial Model

Up/down factors:
$$u = e^{\sigma\sqrt{\Delta t}}, \quad d = \frac{1}{u}$$

Risk-neutral probability:
$$q = \frac{e^{r\Delta t} - d}{u - d}$$

Backward induction:
$$V_i^{(j)} = e^{-r\Delta t}\left(q V_i^{(j+1)} + (1-q)V_{i+1}^{(j+1)}\right)$$

### 3. Option Price

$$V = e^{-rT} \mathbb{E}^Q[\text{Payoff}(S_T)]$$

### 4. Greeks (Finite Differences)

**Delta:**
$$\Delta = \frac{V(S_0 + h) - V(S_0 - h)}{2h}$$

**Vega:**
$$\nu = \frac{V(\sigma + h) - V(\sigma - h)}{2h}$$

**Theta:**
$$\Theta = -\frac{V(T - \Delta t) - V(T)}{\Delta t}$$

**Rho:**
$$\rho = \frac{V(r + h) - V(r - h)}{2h}$$

## Payoff Structures

### 1. European Call Option

Redeem energy only if price exceeds strike:

$$\text{Payoff} = \max(S_T - K, 0)$$

**Use case:** Energy producers hedge against price drops

### 2. Direct Redeemable Claim

Direct 1-unit claim on energy:

$$\text{Payoff} = S_T$$

**Use case:** SPK token backed by renewable energy

## Results and Interpretation

### Example Output

```
Binomial Tree Price (N=100):      $23.4567
Monte-Carlo Price (10,000 paths):  $23.4823 [$23.1234, $23.8412]

Greeks:
  Delta:   0.6234  (60% exposure to underlying)
  Gamma:   0.0156  (convexity positive)
  Vega:    8.3421  (vulnerable to volatility drops)
  Theta:  -0.0234  (daily time decay)
  Rho:     0.5421  (benefits from rate increases)
```

### Interpretation

- **Delta = 0.62**: Hedge 62% of energy output
- **Gamma = 0.016**: Delta stable (not too convex)
- **Vega = 8.34**: Gains $8.34 per 1% volatility increase
- **Theta = -0.023**: Loses $0.023 per day
- **Rho = 0.54**: Gains $0.54 per 1% rate increase

## Applications

### 1. SolarPunkCoin (SPK) Issuance

Fair value of SPK token backed by 1 kWh renewable energy.

### 2. Producer Hedging

Energy producers use call options to hedge against price drops.

### 3. Grid Stabilization

Stability mechanisms via theta decay collection.

### 4. Central Bank Integration

Energy-backed CBDC with formal pricing and policy integration.

### 5. International Energy Markets

Multi-region pricing enables decentralized energy finance.

## References

### Derivative Pricing Theory

- Hull, J. C. (2021). *Options, Futures, and Other Derivatives* (11th ed.)
- Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities
- Cox, J. C., Ross, S. A., & Rubinstein, M. (1979). Option pricing: A simplified approach

### Energy Economics & Cryptocurrency

- Hayes, A. S. (2017). Production costs and cryptocurrency valuation
- Pagnotta, E., & Buraschi, A. (2018). An equilibrium model of the market for Bitcoin
- Sockin, M., & Xiong, W. (2021). Informational frictions and commodity prices

### CEIR Framework

- See: `CEIR-Trifecta.md` and `Quasi-SD-CEIR.md` in parent directory

## Validation

All code includes:
- ✓ Parameter validation
- ✓ Bounds checking
- ✓ Binomial-MC convergence
- ✓ Greeks consistency tests
- ✓ No-arbitrage verification

## Performance Notes

Typical runtimes:
- Binomial (N=100): ~100ms
- Monte-Carlo (10k paths): ~500ms
- Greeks calculation: ~1-2 seconds
- Full visualization suite: ~10-15 seconds

## Extension Points

The framework is designed for extension:

### Add New Payoff Types
```python
# In sensitivities.py
class PayoffFunction:
    @staticmethod
    def custom_payoff(S_T, K):
        # Your payoff logic
        return result
```

### Add New Stochastic Models
```python
# Create new simulator classes inheriting from MonteCarloSimulator
class JumpDiffusionSimulator(MonteCarloSimulator):
    # Jump-diffusion process
    pass
```

### Multi-Factor Models
```python
# Extend to include grid utilization, storage, etc.
class MultiFactorSimulator:
    # Energy price + grid state + storage
    pass
```

## Troubleshooting

### Issue: Import errors for seaborn/matplotlib

```bash
pip install matplotlib seaborn
```

### Issue: CEIR data not found

- Ensure `empirical/` folder is in parent directory
- Check filenames match expectations
- Falls back to synthetic data if files missing

### Issue: Memory errors with large simulations

- Reduce `num_simulations` (default: 10,000)
- Use Binomial tree instead for deterministic pricing
- Run on machine with more RAM

## License

[Specify your license]

## Contact & Support

For questions about:
- **Derivatives pricing**: See `notebooks/main.ipynb` for examples
- **CEIR framework**: See `../CEIR-Trifecta.md`
- **SolarPunk vision**: See `../Final-Iteration.md`

---

**Framework developed**: November 2025  
**Last updated**: November 6, 2025  
**Version**: 1.0.0
