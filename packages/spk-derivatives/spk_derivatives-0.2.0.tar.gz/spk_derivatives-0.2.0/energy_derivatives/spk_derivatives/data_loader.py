"""
Data Loader for Energy Derivatives
===================================

Loads and processes empirical CEIR data to derive realistic underlying prices
for derivative pricing models.

Key Functions:
-----------
load_ceir_data(): Load Bitcoin CEIR from empirical folder
compute_energy_price(): Derive energy unit prices from CEIR
estimate_volatility(): Estimate volatility from historical prices
load_parameters(): Load all parameters for derivative pricing
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
import warnings
from pathlib import Path

REQUIRED_COLUMNS = ["Date", "Price", "Market_Cap"]


def validate_ceir_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure CEIR dataframe has required columns and datatypes.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Coerce numeric fields
    df = df.copy()
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Market_Cap"] = pd.to_numeric(df["Market_Cap"], errors="coerce")

    # Ensure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def _resolve_data_directory(data_dir: str, use_repo_fallback: bool = True) -> Optional[Path]:
    """
    Resolve the data directory with sensible fallbacks.

    Returns
    -------
    Optional[Path]
        Path object if the directory exists, otherwise None.
    """
    candidate = Path(data_dir)
    if candidate.exists():
        return candidate

    if use_repo_fallback:
        # Fallback: look for empirical folder at repo root
        repo_root_candidate = Path(__file__).resolve().parents[2] / "empirical"
        if repo_root_candidate.exists():
            warnings.warn(f"Data directory {data_dir} not found, using {repo_root_candidate}")
            return repo_root_candidate

    warnings.warn(f"Data directory {data_dir} not found and no fallback available")
    return None


def load_ceir_data(data_dir: str = '../empirical',
                   use_repo_fallback: bool = True,
                   use_live_if_missing: bool = False) -> pd.DataFrame:
    """
    Load CEIR data from empirical folder.
    
    Parameters
    ----------
    data_dir : str
        Path to empirical data directory
    use_repo_fallback : bool
        If True, fall back to repo-level empirical folder when not found
    use_live_if_missing : bool
        If True, fetch live data when local data is missing
        
    Returns
    -------
    pd.DataFrame
        DataFrame with Date, Price, Energy_TWh_Annual, Market_Cap, CEIR
    """

    resolved_dir = _resolve_data_directory(data_dir, use_repo_fallback=use_repo_fallback)
    if resolved_dir is None:
        if use_live_if_missing:
            try:
                from .live_data import load_or_fetch_live_ceir
                live_df = load_or_fetch_live_ceir()
                if not live_df.empty:
                    return validate_ceir_schema(live_df)
            except Exception as exc:
                warnings.warn(f"Live data fetch failed: {exc}")
        return _generate_synthetic_ceir_data()

    try:
        # Load Bitcoin price data
        btc_data_candidates = [
            'bitcoin_ceir_final.csv',
            'bitcoin_ceir_complete.csv',
            'btc_ds_parsed.csv'
        ]

        btc_file = None
        for candidate in btc_data_candidates:
            path = resolved_dir / candidate
            if path.exists():
                btc_file = path
                break
        
        if btc_file is None:
            warnings.warn("No Bitcoin price file found, using synthetic data")
            return _generate_synthetic_ceir_data()
        
        df = pd.read_csv(btc_file)
        
        # Ensure Date column
        if 'Date' not in df.columns:
            if 'Exchange Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Exchange Date'])
            else:
                df['Date'] = pd.date_range(start='2018-01-01', periods=len(df))
        else:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Ensure Price column
        if 'Price' not in df.columns:
            if 'Open' in df.columns:
                df['Price'] = df['Open']
            elif 'Close' in df.columns:
                df['Price'] = df['Close']
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        # Load energy data if available
        energy_file = resolved_dir / 'btc_con.csv'
        if energy_file.exists():
            energy_df = pd.read_csv(energy_file)
            energy_df['DateTime'] = pd.to_datetime(energy_df['DateTime'])
            energy_df['Date'] = energy_df['DateTime'].dt.date
            energy_df = energy_df.rename(columns={'Estimated TWh per Year': 'Energy_TWh_Annual'})
            
            df['Date_only'] = df['Date'].dt.date
            df = df.merge(
                energy_df[['Date', 'Energy_TWh_Annual']].drop_duplicates('Date', keep='first'),
                left_on='Date_only',
                right_on='Date',
                how='left',
                suffixes=('', '_energy')
            )
            df = df.drop('Date_only', axis=1)
            if 'Date_energy' in df.columns:
                df = df.drop('Date_energy', axis=1)
        
        # Compute market cap if not present
        if 'Market_Cap' not in df.columns:
            # Approximate Bitcoin supply curve
            days_since_start = (df['Date'] - df['Date'].min()).dt.days
            df['Supply'] = 21e6 - (21e6 - 17e6) * np.exp(-0.693 * days_since_start / (4 * 365))
            df['Market_Cap'] = df['Price'] * df['Supply']
        df['Market_Cap'] = pd.to_numeric(df['Market_Cap'], errors='coerce')
        
        # Compute CEIR if not present
        if 'CEIR' not in df.columns and 'Energy_TWh_Annual' in df.columns:
            df = compute_ceir_column(df)
        
        df = validate_ceir_schema(df)
        return df.sort_values('Date').reset_index(drop=True)
    
    except Exception as e:
        warnings.warn(f"Error loading CEIR data: {e}, using synthetic data")
        return _generate_synthetic_ceir_data()


def compute_ceir_column(df: pd.DataFrame, electricity_price: float = 0.05) -> pd.DataFrame:
    """
    Compute CEIR column from price and energy data.
    
    CEIR = Market Cap / Cumulative Energy Cost
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with Market_Cap and Energy_TWh_Annual
    electricity_price : float
        Electricity price ($/kWh) for energy cost calculation
        
    Returns
    -------
    pd.DataFrame
        DataFrame with CEIR column added
    """
    
    # Daily energy cost
    df['Daily_Energy_TWh'] = df['Energy_TWh_Annual'] / 365
    df['Daily_Energy_Cost_USD'] = df['Daily_Energy_TWh'] * electricity_price * 1e9  # Convert TWh to kWh
    
    # Cumulative energy cost
    df['Cumulative_Energy_Cost'] = df['Daily_Energy_Cost_USD'].cumsum()
    
    # CEIR
    df['CEIR'] = df['Market_Cap'] / df['Cumulative_Energy_Cost']
    df['CEIR'] = df['CEIR'].replace([np.inf, -np.inf], np.nan).fillna(method='ffill')
    
    return df


def _generate_synthetic_ceir_data(n_days: int = 2000) -> pd.DataFrame:
    """
    Generate synthetic CEIR data for testing.
    
    Parameters
    ----------
    n_days : int
        Number of days of data
        
    Returns
    -------
    pd.DataFrame
        Synthetic CEIR dataset
    """
    
    dates = pd.date_range(start='2018-01-01', periods=n_days, freq='D')
    
    # Geometric Brownian motion for price
    returns = np.random.normal(0.0005, 0.03, n_days)
    prices = 1000 * np.exp(np.cumsum(returns))
    
    # Supply curve
    days_idx = np.arange(n_days)
    supply = 21e6 - (21e6 - 17e6) * np.exp(-0.693 * days_idx / (4 * 365))
    market_caps = prices * supply
    
    # Energy consumption (increasing)
    energy_twh = 30 + 100 * (days_idx / n_days) + 10 * np.random.normal(0, 1, n_days)
    energy_twh = np.maximum(energy_twh, 20)  # Ensure positive
    
    # CEIR
    daily_energy_cost = energy_twh / 365 * 0.05 * 1e9
    cumulative_energy_cost = np.cumsum(daily_energy_cost)
    ceir = market_caps / cumulative_energy_cost
    
    df = pd.DataFrame({
        'Date': dates,
        'Price': prices,
        'Supply': supply,
        'Market_Cap': market_caps,
        'Energy_TWh_Annual': energy_twh,
        'CEIR': ceir
    })
    
    return df


def compute_energy_price(ceir_df: pd.DataFrame, 
                        normalization_date: Optional[str] = None) -> np.ndarray:
    """
    Derive energy unit prices from CEIR.
    
    Energy price represents the present value of 1 unit of energy
    backed by the CEIR framework.
    
    Parameters
    ----------
    ceir_df : pd.DataFrame
        DataFrame with CEIR column
    normalization_date : str, optional
        Date to normalize prices to (YYYY-MM-DD format)
        
    Returns
    -------
    np.ndarray
        Energy unit prices
    """
    ceir_series = pd.to_numeric(ceir_df['CEIR'], errors='coerce')
    ceir_series = ceir_series.replace([np.inf, -np.inf], np.nan).ffill().bfill()
    
    positive_ceir = ceir_series[ceir_series > 0]
    if positive_ceir.empty:
        warnings.warn("CEIR series is empty or non-positive; using flat energy price of 1.0")
        return np.ones(len(ceir_series))
    
    baseline = positive_ceir.iloc[0]
    energy_prices = ceir_series / baseline
    
    # If normalization date specified, rescale
    if normalization_date:
        norm_date = pd.Timestamp(normalization_date)
        norm_idx = (ceir_df['Date'] - norm_date).abs().argmin()
        if energy_prices.iloc[norm_idx] != 0:
            energy_prices = energy_prices / energy_prices.iloc[norm_idx]
    
    return energy_prices.to_numpy()


def estimate_volatility(price_series: np.ndarray, 
                       periods: int = 252) -> float:
    """
    Estimate annualized volatility from price series.
    
    Parameters
    ----------
    price_series : np.ndarray
        Price array
    periods : int
        Trading periods per year (default: 252)
        
    Returns
    -------
    float
        Annualized volatility
    """
    prices = np.asarray(price_series, dtype=float)
    prices = prices[np.isfinite(prices) & (prices > 0)]
    if len(prices) < 2:
        warnings.warn("Not enough valid price points to estimate volatility; defaulting to 20%")
        return 0.20

    returns = np.diff(np.log(prices))
    returns = returns[np.isfinite(returns)]
    if len(returns) == 0:
        warnings.warn("No finite returns found; defaulting to 20% volatility")
        return 0.20

    daily_vol = np.std(returns)
    annualized_vol = daily_vol * np.sqrt(periods)
    
    return float(annualized_vol)


def load_parameters(data_dir: str = '../empirical',
                   T: float = 1.0,
                   r: float = 0.05,
                   use_repo_fallback: bool = True,
                   use_live_if_missing: bool = False) -> Dict:
    """
    Load all parameters for derivative pricing from empirical data.
    
    Parameters
    ----------
    data_dir : str
        Path to empirical data directory
    T : float
        Time to maturity (years)
    r : float
        Risk-free rate
    use_repo_fallback : bool
        If True, fall back to repo-level empirical folder when not found
    use_live_if_missing : bool
        If True, attempt to fetch live data if local data is missing
        
    Returns
    -------
    Dict
        Dictionary with pricing parameters:
        - S0: Initial energy price
        - sigma: Estimated volatility
        - T: Time to maturity
        - r: Risk-free rate
        - K: Strike price (set to current price)
        - ceir_df: Full CEIR DataFrame
    """
    
    # Load CEIR data
    ceir_df = load_ceir_data(data_dir, use_repo_fallback=use_repo_fallback,
                             use_live_if_missing=use_live_if_missing)
    
    # Compute energy price
    energy_prices = compute_energy_price(ceir_df)
    
    # Estimate volatility
    sigma = estimate_volatility(energy_prices)
    if not np.isfinite(sigma) or sigma <= 0:
        warnings.warn("Estimated volatility is non-positive; defaulting to 20%")
        sigma = 0.20
    
    # Get current price (latest)
    S0 = energy_prices[-1]
    if not np.isfinite(S0) or S0 <= 0:
        warnings.warn("Invalid S0 derived from CEIR data; defaulting to 1.0")
        S0 = 1.0
    
    # Strike price (at-the-money)
    K = S0
    
    params = {
        'S0': S0,
        'sigma': sigma if np.isfinite(sigma) and sigma > 0 else 0.20,
        'T': T,
        'r': r,
        'K': K,
        'ceir_df': ceir_df,
        'energy_prices': energy_prices,
        'data_dir': data_dir
    }
    
    return params


def get_ceir_summary(ceir_df: pd.DataFrame) -> Dict:
    """
    Get summary statistics from CEIR data.
    
    Parameters
    ----------
    ceir_df : pd.DataFrame
        CEIR DataFrame
        
    Returns
    -------
    Dict
        Summary statistics
    """
    
    summary = {
        'start_date': ceir_df['Date'].min(),
        'end_date': ceir_df['Date'].max(),
        'n_days': len(ceir_df),
        'price_min': ceir_df['Price'].min(),
        'price_max': ceir_df['Price'].max(),
        'price_current': ceir_df['Price'].iloc[-1],
        'market_cap_current': ceir_df['Market_Cap'].iloc[-1],
        'ceir_mean': ceir_df['CEIR'].mean(),
        'ceir_std': ceir_df['CEIR'].std(),
        'energy_twh_mean': ceir_df['Energy_TWh_Annual'].mean() if 'Energy_TWh_Annual' in ceir_df else np.nan
    }
    
    return summary
