# Solarpunk Bitcoin: Energy-Backed Cryptocurrency Research & Development

Academic research on renewable energy as a fundamental anchor for cryptocurrency value, with practical derivatives pricing framework for energy-backed assets.

## 📚 Research Papers

- **CEIR-Trifecta.md** – Core empirical work: "When Does Energy Cost Anchor Cryptocurrency Value?" Triple natural experiment design (China mining ban 2021, Ethereum merge 2022, Russia sanctions 2025)
- **Quasi-SD-CEIR.md** – Framework extension: Supply-demand dynamics with sentiment analysis and hidden Markov regimes
- **Final-Iteration.md** – SolarPunkCoin concept: Renewable-energy-backed stablecoin addressing 10 cryptocurrency failure modes
- **Empirical-Milestone.md** – Spring 2025 research proposal for Yuan Ze University

## 🔧 Energy Derivatives Framework

Production-ready Python package for pricing European-style options on renewable energy-backed assets.

**Quick start:**
```bash
cd energy_derivatives
pip install -r requirements.txt
jupyter notebook notebooks/main.ipynb
```

**Core modules:**
- `binomial.py` – Binomial tree pricing with convergence analysis
- `monte_carlo.py` – Monte Carlo simulation with confidence intervals
- `sensitivities.py` – Greeks computation (delta, gamma, vega, theta, rho)
- `plots.py` – Publication-quality visualizations
- `data_loader.py` – Energy data calibration

**Details:** ~2,300 lines of production code, full documentation, Jupyter notebook with 10-section walkthrough.

## �� Empirical Data & Analysis

`empirical/` contains CEIR computation pipeline:
- Bitcoin/Ethereum energy consumption (TWh/year from Digiconomist)
- Mining distribution (geographic concentration)
- Electricity prices (regional, time-varying)
- Macro controls (S&P 500, VIX, gold)
- Analysis scripts (`gecko.py`, `CEIR.py`, `Regression.py`)

## 📖 Project Structure

```
solarpunk-coin/
├── README.md                     # This file
├── CEIR-Trifecta.md              # Main research paper
├── Quasi-SD-CEIR.md              # Supply-demand extension
├── Final-Iteration.md            # SolarPunkCoin vision
├── Empirical-Milestone.md        # Research roadmap
│
├── energy_derivatives/           # Derivatives pricing package
│   ├── src/                      # Core modules
│   │   ├── binomial.py
│   │   ├── monte_carlo.py
│   │   ├── sensitivities.py
│   │   ├── plots.py
│   │   └── data_loader.py
│   ├── notebooks/
│   │   └── main.ipynb            # Full demonstration
│   └── requirements.txt
│
├── empirical/                    # CEIR data & scripts
│   ├── gecko.py                  # Data collection
│   ├── CEIR.py                   # CEIR calculations
│   ├── Regression.py             # Analysis
│   └── data/                     # CSV files
│
└── examples/
    └── presentation_colab.ipynb  # Solar energy demo
```

## 🎯 Key Features

✅ **Rigorous Theory:** Risk-neutral valuation, geometric Brownian motion, arbitrage-free pricing  
✅ **Two Methods:** Binomial tree (exact) + Monte Carlo (distribution analysis)  
✅ **Complete Greeks:** All 5 sensitivities via finite differences  
✅ **Real Data:** Calibrated to Bitcoin CEIR (2018–2025)  
✅ **Multi-Location:** Taiwan, Arizona, Spain solar data comparison  
✅ **Production Code:** Type hints, comprehensive docstrings, error handling  

## 🚀 Usage

**Python API:**
```python
from energy_derivatives.binomial import BinomialTree
from energy_derivatives.data_loader import load_parameters

params = load_parameters(data_dir='empirical')
price = BinomialTree(**params, N=400).price()
```

**Jupyter Notebook:**
```bash
cd energy_derivatives
jupyter notebook notebooks/main.ipynb
```

See `notebooks/main.ipynb` for complete 10-section demo with explanations.

## 📝 Author

Spectating101 (s1133958@mail.yzu.edu.tw)  
Yuan Ze University

## 📄 License

MIT

---

**Status:** Research papers completed (peer review in progress). Derivatives framework complete and submission-ready.
