"""
Live data helpers for CEIR-derived parameters.
Provides lightweight Bitcoin market fetch and synthetic energy estimates
with optional caching for reproducibility.
"""

import warnings
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests

CACHE_DIR = Path(__file__).resolve().parents[1] / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_DIR / "live_ceir_cache.csv"


def fetch_live_bitcoin_market(days: int = 365) -> pd.DataFrame:
    """
    Fetch recent Bitcoin price and market cap data from CoinGecko.

    Parameters
    ----------
    days : int
        Lookback window in days
    """
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    resp = requests.get(url, params={"vs_currency": "usd", "days": days})
    resp.raise_for_status()
    data = resp.json()
    prices = data.get("prices", [])
    market_caps = data.get("market_caps", [])

    df = pd.DataFrame({
        "Date": pd.to_datetime([p[0] for p in prices], unit="ms"),
        "Price": [p[1] for p in prices],
        "Market_Cap": [m[1] for m in market_caps] if market_caps else [np.nan] * len(prices),
    })

    # Synthetic energy estimates (placeholder rising trend)
    days_idx = np.arange(len(df))
    df["Energy_TWh_Annual"] = 80 + 40 * (days_idx / len(df)) + 5 * np.random.normal(0, 1, len(df))
    df["Energy_TWh_Annual"] = df["Energy_TWh_Annual"].clip(lower=50)

    return _compute_ceir(df)


def _compute_ceir(df: pd.DataFrame, electricity_price: float = 0.05) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("Date")
    df["Daily_Energy_TWh"] = df["Energy_TWh_Annual"] / 365
    df["Daily_Energy_Cost_USD"] = df["Daily_Energy_TWh"] * electricity_price * 1e9
    df["Cumulative_Energy_Cost"] = df["Daily_Energy_Cost_USD"].cumsum()
    df["CEIR"] = df["Market_Cap"] / df["Cumulative_Energy_Cost"]
    df["CEIR"] = df["CEIR"].replace([np.inf, -np.inf], np.nan).ffill()
    return df


def cache_live_ceir(df: pd.DataFrame, path: Path = CACHE_FILE) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def load_cached_live_ceir(path: Path = CACHE_FILE) -> Optional[pd.DataFrame]:
    if path.exists():
        return pd.read_csv(path, parse_dates=["Date"])
    return None


def load_or_fetch_live_ceir(days: int = 365, use_cache: bool = True) -> pd.DataFrame:
    if use_cache:
        cached = load_cached_live_ceir()
        if cached is not None:
            return cached
    try:
        df = fetch_live_bitcoin_market(days=days)
        cache_live_ceir(df)
        return df
    except Exception as exc:
        warnings.warn(f"Live fetch failed ({exc}); returning empty DataFrame")
        return pd.DataFrame()
