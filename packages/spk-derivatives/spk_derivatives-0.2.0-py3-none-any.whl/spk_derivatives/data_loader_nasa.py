"""
NASA POWER API Data Loader for Solar Energy Derivatives
=========================================================

Fetches real-world Global Horizontal Irradiance (GHI) data from NASA POWER API
to calibrate volatility parameters for solar energy derivatives pricing.

Location: Taoyuan, Taiwan (24.99°N, 121.30°E)
Data Source: NASA POWER (Prediction Of Worldwide Energy Resources)
Parameter: ALLSKY_SFC_SW_DWN (Solar Irradiance in kW-hr/m²/day)

Key Functions:
-----------
fetch_nasa_data(): Fetch historical GHI data from NASA API
get_volatility_params(): Calculate annualized volatility from solar data
load_solar_parameters(): Load complete parameters for solar derivative pricing
"""

import requests
import pandas as pd
import numpy as np
import warnings
from typing import Dict, Tuple, Optional
from pathlib import Path

# --- CONFIGURATION ---
# Coordinates for Taoyuan, Taiwan
LAT = 24.99
LON = 121.30
START_YEAR = 2020
END_YEAR = 2024


def fetch_nasa_data(
    lat: float = LAT,
    lon: float = LON,
    start: int = START_YEAR,
    end: int = END_YEAR,
    cache: bool = True
) -> pd.DataFrame:
    """
    Fetches Daily Global Horizontal Irradiance (GHI) from NASA POWER API.

    Parameters
    ----------
    lat : float
        Latitude (default: 24.99 for Taoyuan)
    lon : float
        Longitude (default: 121.30 for Taoyuan)
    start : int
        Start year (default: 2020)
    end : int
        End year (default: 2024)
    cache : bool
        If True, cache data locally to avoid repeated API calls

    Returns
    -------
    pd.DataFrame
        DataFrame with Date index and GHI column (kW-hr/m²/day)
    """

    # Check cache first
    cache_dir = Path(__file__).parent.parent / 'data'
    cache_file = cache_dir / f'nasa_ghi_{lat}_{lon}_{start}_{end}.csv'

    if cache and cache_file.exists():
        print(f"📁 Loading cached NASA data from {cache_file}")
        df = pd.read_csv(cache_file, parse_dates=['Date'], index_col='Date')
        print(f"✅ Loaded {len(df)} days of cached data")
        return df

    # Fetch from NASA API
    base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",  # Solar Irradiance (kW-hr/m²/day)
        "community": "RE",                   # Renewable Energy
        "longitude": lon,
        "latitude": lat,
        "start": f"{start}0101",
        "end": f"{end}1231",
        "format": "JSON"
    }

    print(f"📡 Connecting to NASA Satellite Database for Taoyuan ({lat}, {lon})...")
    print(f"   Date Range: {start}-01-01 to {end}-12-31")

    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"NASA API Failed: {e}")

    data = response.json()

    # Parse JSON into DataFrame
    try:
        solar_dict = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        df = pd.DataFrame.from_dict(solar_dict, orient='index', columns=['GHI'])
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        df.index.name = 'Date'
    except (KeyError, ValueError) as e:
        raise ValueError(f"Failed to parse NASA API response: {e}")

    # Filter missing data (NASA uses -999 for missing)
    original_len = len(df)
    df = df[df['GHI'] > -900].copy()
    removed = original_len - len(df)

    if removed > 0:
        warnings.warn(f"Removed {removed} days with missing data")

    print(f"✅ Success! Loaded {len(df)} days of historical solar data")

    # Cache for future use
    if cache:
        cache_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache_file)
        print(f"💾 Cached data to {cache_file}")

    return df


def get_volatility_params(
    df: pd.DataFrame,
    window: int = 365,
    deseason: bool = True,
    method: str = 'log',
    cap_volatility: Optional[float] = None
) -> Tuple[float, pd.DataFrame]:
    """
    Calculates the Annualized Volatility (Sigma) from solar irradiance data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with GHI column and DatetimeIndex
    window : int
        Trading periods per year for annualization (default: 365 for daily data)
    deseason : bool
        If True, remove seasonal component before calculating volatility.
        Recommended for solar data to isolate weather-driven risk.
    method : str
        Method for calculating returns:
        - 'log' (recommended): Log returns, symmetric and stable
        - 'pct_change': Simple percentage change (legacy, can create artifacts)
        - 'normalized': Normalized by mean GHI
    cap_volatility : Optional[float]
        Optional cap on volatility for numerical stability.
        If None, no capping applied. If provided, caps at this level (e.g., 2.0 for 200%).

    Returns
    -------
    Tuple[float, pd.DataFrame]
        (annualized_volatility, dataframe_with_returns)

    Notes
    -----
    The 'log' method is recommended as it:
    - Handles small denominators gracefully
    - Treats up/down moves symmetrically
    - Is standard practice in quantitative finance
    - Avoids artifacts from pct_change() on physical quantities

    Examples
    --------
    >>> df = fetch_nasa_data()
    >>> sigma, df_with_returns = get_volatility_params(df, method='log')
    >>> print(f"Volatility: {sigma:.2%}")
    """

    df = df.copy()

    # Step 1: Deseasonalization (if requested)
    if deseason:
        df['Month'] = df.index.month
        monthly_avg = df.groupby('Month')['GHI'].transform('mean')
        df['GHI_Deseason'] = df['GHI'] / monthly_avg
        source_data = df['GHI_Deseason']
        print(f"   ℹ️  Deseasoning applied: removes predictable seasonal cycles")
    else:
        source_data = df['GHI']

    # Step 2: Calculate returns using specified method
    if method == 'log':
        # Log returns: log(P_t / P_{t-1})
        # Most stable for finance applications
        df['Returns'] = np.log(source_data / source_data.shift(1))
    elif method == 'pct_change':
        # Simple returns: (P_t - P_{t-1}) / P_{t-1}
        # Can create artifacts with small denominators
        df['Returns'] = source_data.pct_change()
    elif method == 'normalized':
        # Normalized changes: (P_t - P_{t-1}) / mean(P)
        # Alternative that avoids small denominator issue
        mean_value = source_data.mean()
        df['Returns'] = (source_data - source_data.shift(1)) / mean_value
    else:
        raise ValueError(
            f"Unknown volatility method: '{method}'. "
            f"Must be one of: 'log', 'pct_change', 'normalized'"
        )

    # Step 3: Clean returns
    valid_returns = df['Returns'].replace([np.inf, -np.inf], np.nan).dropna()

    if len(valid_returns) < 2:
        warnings.warn(
            "Not enough valid returns to estimate volatility; defaulting to 20%"
        )
        return 0.20, df

    # Step 4: Calculate volatility
    daily_vol = valid_returns.std()
    annual_vol = daily_vol * np.sqrt(window)

    # Step 5: Apply cap if specified
    if cap_volatility is not None and annual_vol > cap_volatility:
        warnings.warn(
            f"Volatility {annual_vol:.2%} exceeds cap {cap_volatility:.0%}. "
            f"Capping for numerical stability. "
            f"Consider using method='log' or increasing cap if this is unexpected."
        )
        annual_vol = cap_volatility

    # Step 6: Sanity check
    if not np.isfinite(annual_vol) or annual_vol <= 0:
        warnings.warn(
            f"Invalid volatility {annual_vol}; defaulting to 20%. "
            f"Check input data for issues."
        )
        annual_vol = 0.20

    return float(annual_vol), df


def compute_solar_price(df: pd.DataFrame,
                       energy_value_per_kwh: float = 0.10,
                       panel_efficiency: float = 0.20,
                       panel_area_m2: float = 1.0) -> np.ndarray:
    """
    Compute underlying asset price from GHI data.

    Converts solar irradiance to economic value:
    Price = GHI × Panel_Efficiency × Area × Energy_Value

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with GHI column
    energy_value_per_kwh : float
        Economic value of 1 kWh of energy ($/kWh)
    panel_efficiency : float
        Solar panel conversion efficiency (0-1, default 0.20 = 20%)
    panel_area_m2 : float
        Panel area in square meters (default: 1.0)

    Returns
    -------
    np.ndarray
        Array of daily energy prices
    """

    # Energy generated (kWh) = GHI × efficiency × area
    energy_kwh = df['GHI'] * panel_efficiency * panel_area_m2

    # Economic value ($) = energy × price per kWh
    prices = energy_kwh * energy_value_per_kwh

    return prices.to_numpy()


def load_solar_parameters(
    lat: float = LAT,
    lon: float = LON,
    start: int = START_YEAR,
    end: int = END_YEAR,
    T: float = 1.0,
    r: float = 0.05,
    energy_value_per_kwh: float = 0.10,
    cache: bool = True,
    volatility_method: str = 'log',
    volatility_cap: Optional[float] = None,
    deseason: bool = True
) -> Dict:
    """
    Load all parameters for solar derivative pricing from NASA data.

    Parameters
    ----------
    lat : float
        Latitude (default: 24.99 for Taoyuan, Taiwan)
    lon : float
        Longitude (default: 121.30 for Taoyuan, Taiwan)
    start : int
        Start year for data fetching
    end : int
        End year for data fetching
    T : float
        Time to maturity in years
    r : float
        Risk-free rate (annualized)
    energy_value_per_kwh : float
        Economic value per kWh of energy
    cache : bool
        Use cached NASA data if available
    volatility_method : str
        Method for volatility calculation:
        - 'log': Log returns (recommended, default)
        - 'pct_change': Simple percentage change
        - 'normalized': Normalized by mean
    volatility_cap : Optional[float]
        Optional cap on volatility. If None, no capping.
        Example: 2.0 for 200% cap.
    deseason : bool
        Remove seasonal patterns before calculating volatility

    Returns
    -------
    Dict
        Dictionary with pricing parameters:
        - S0: Initial energy price
        - sigma: Estimated volatility (from solar data)
        - T: Time to maturity
        - r: Risk-free rate
        - K: Strike price (set to current price, ATM)
        - ghi_df: Full GHI DataFrame with returns
        - energy_prices: Array of daily energy prices
        - location: Dict with lat/lon
        - volatility_method: Method used for calculation
        - volatility_capped: Whether capping was applied

    Examples
    --------
    >>> # Default (recommended): log returns, no cap
    >>> params = load_solar_parameters()

    >>> # With capping at 200%
    >>> params = load_solar_parameters(volatility_cap=2.0)

    >>> # Different location
    >>> params = load_solar_parameters(lat=33.45, lon=-112.07)  # Phoenix, AZ
    """

    # Fetch NASA data
    ghi_df = fetch_nasa_data(lat, lon, start, end, cache)

    # Calculate volatility with specified method
    sigma, ghi_df = get_volatility_params(
        ghi_df,
        method=volatility_method,
        cap_volatility=volatility_cap,
        deseason=deseason
    )

    # Compute energy prices
    energy_prices = compute_solar_price(ghi_df, energy_value_per_kwh)

    # Get current price (latest)
    S0 = float(energy_prices[-1])

    # Strike price (at-the-money)
    K = S0

    # Check if volatility was capped
    volatility_capped = (volatility_cap is not None and
                        'exceeds cap' in str(warnings.filters))

    params = {
        'S0': S0,
        'sigma': sigma,
        'T': T,
        'r': r,
        'K': K,
        'ghi_df': ghi_df,
        'energy_prices': energy_prices,
        'location': {
            'latitude': lat,
            'longitude': lon,
            'name': 'Taoyuan, Taiwan'
        },
        'data_source': 'NASA POWER API',
        'parameter': 'ALLSKY_SFC_SW_DWN (GHI)',
        'date_range': f"{start}-{end}",
        'volatility_method': volatility_method,
        'volatility_cap': volatility_cap,
        'deseasonalized': deseason
    }

    return params


def get_solar_summary(params: Dict) -> Dict:
    """
    Get summary statistics from solar data.

    Parameters
    ----------
    params : Dict
        Parameters dictionary from load_solar_parameters()

    Returns
    -------
    Dict
        Summary statistics
    """

    ghi_df = params['ghi_df']
    energy_prices = params['energy_prices']

    summary = {
        'location': params['location']['name'],
        'latitude': params['location']['latitude'],
        'longitude': params['location']['longitude'],
        'data_source': params['data_source'],
        'date_range': params['date_range'],
        'start_date': ghi_df.index.min(),
        'end_date': ghi_df.index.max(),
        'n_days': len(ghi_df),
        'ghi_mean': ghi_df['GHI'].mean(),
        'ghi_std': ghi_df['GHI'].std(),
        'ghi_min': ghi_df['GHI'].min(),
        'ghi_max': ghi_df['GHI'].max(),
        'price_mean': np.mean(energy_prices),
        'price_std': np.std(energy_prices),
        'price_current': params['S0'],
        'volatility': params['sigma']
    }

    return summary


if __name__ == "__main__":
    """
    Demo: Fetch NASA data and calculate volatility
    """
    print("="*80)
    print("NASA POWER API Solar Data Loader - Demo".center(80))
    print("="*80)

    # Load parameters
    params = load_solar_parameters()

    # Display summary
    summary = get_solar_summary(params)

    print(f"\n📍 LOCATION:")
    print(f"   {summary['location']}")
    print(f"   Latitude: {summary['latitude']}°N")
    print(f"   Longitude: {summary['longitude']}°E")

    print(f"\n📊 DATA SUMMARY:")
    print(f"   Source: {summary['data_source']}")
    print(f"   Date Range: {summary['date_range']}")
    print(f"   Trading Days: {summary['n_days']}")

    print(f"\n☀️ SOLAR IRRADIANCE (GHI):")
    print(f"   Mean: {summary['ghi_mean']:.2f} kW-hr/m²/day")
    print(f"   Std Dev: {summary['ghi_std']:.2f} kW-hr/m²/day")
    print(f"   Range: [{summary['ghi_min']:.2f}, {summary['ghi_max']:.2f}]")

    print(f"\n💰 ENERGY PRICES:")
    print(f"   Mean: ${summary['price_mean']:.4f}")
    print(f"   Std Dev: ${summary['price_std']:.4f}")
    print(f"   Current (S₀): ${summary['price_current']:.4f}")

    print(f"\n📈 VOLATILITY:")
    print(f"   Annualized (σ): {summary['volatility']:.2%}")

    print(f"\n💡 DERIVATIVES PARAMETERS:")
    print(f"   S₀ = ${params['S0']:.4f}")
    print(f"   K = ${params['K']:.4f} (at-the-money)")
    print(f"   σ = {params['sigma']:.2%}")
    print(f"   T = {params['T']} year")
    print(f"   r = {params['r']:.2%}")

    print("\n" + "="*80)
    print("✅ NASA data integration successful!")
    print("="*80)
