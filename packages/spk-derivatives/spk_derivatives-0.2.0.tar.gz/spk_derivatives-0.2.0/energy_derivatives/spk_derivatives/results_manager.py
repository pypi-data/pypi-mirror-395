"""
Results Manager - Professional Result Handling
===============================================

Save, load, compare, validate, and export pricing results.

This is what users reasonably expect from a professional library.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np


class PricingResult:
    """
    Container for pricing results with save/load/export capabilities.

    This is what users expect: not just getting a price, but being able to
    save it, compare it, export it, and validate it.
    """

    def __init__(
        self,
        option_price: float,
        greeks: Dict,
        params: Dict,
        metadata: Optional[Dict] = None
    ):
        """
        Initialize pricing result.

        Parameters
        ----------
        option_price : float
            Calculated option price
        greeks : dict
            Greeks (delta, gamma, theta, vega, rho)
        params : dict
            Pricing parameters used
        metadata : dict, optional
            Additional context (system size, location, etc.)
        """
        self.option_price = option_price
        self.greeks = greeks
        self.params = params
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()

        # Add computed fields
        self._add_computed_fields()

    def _add_computed_fields(self):
        """Add useful computed fields"""
        self.computed = {
            'premium_pct': self.option_price / self.params['S0'] * 100 if self.params['S0'] > 0 else 0,
            'moneyness': self.params['S0'] / self.params['K'] if self.params['K'] > 0 else 1.0,
            'time_to_maturity_days': self.params['T'] * 365,
        }

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'option_price': self.option_price,
            'greeks': self.greeks,
            'params': self.params,
            'metadata': self.metadata,
            'computed': self.computed,
            'timestamp': self.timestamp
        }

    def save(self, filepath: str):
        """
        Save results to JSON file.

        Parameters
        ----------
        filepath : str
            Path to save file

        Examples
        --------
        >>> result.save('taiwan_10kw_pricing.json')
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

        return filepath

    @classmethod
    def load(cls, filepath: str) -> 'PricingResult':
        """
        Load results from JSON file.

        Parameters
        ----------
        filepath : str
            Path to load from

        Returns
        -------
        PricingResult
            Loaded result object

        Examples
        --------
        >>> result = PricingResult.load('taiwan_10kw_pricing.json')
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        result = cls(
            option_price=data['option_price'],
            greeks=data['greeks'],
            params=data['params'],
            metadata=data.get('metadata', {})
        )
        result.timestamp = data.get('timestamp', result.timestamp)

        return result

    def to_csv(self, filepath: str):
        """
        Export flattened results to CSV.

        Parameters
        ----------
        filepath : str
            Path to CSV file

        Examples
        --------
        >>> result.to_csv('pricing_results.csv')
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Flatten all data
        flat = {
            'timestamp': self.timestamp,
            'option_price': self.option_price,
            **{f'greek_{k}': v for k, v in self.greeks.items()},
            **{f'param_{k}': v for k, v in self.params.items()},
            **{f'computed_{k}': v for k, v in self.computed.items()},
            **{f'meta_{k}': v for k, v in self.metadata.items()}
        }

        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=flat.keys())
            writer.writeheader()
            writer.writerow(flat)

        return filepath

    def summary(self) -> str:
        """Generate human-readable summary"""
        return f"""
Pricing Result Summary
{'='*50}
Timestamp: {self.timestamp}

Option Price: ${self.option_price:.6f}
Premium:      {self.computed['premium_pct']:.2f}% of spot

Greeks:
  Delta:  {self.greeks['delta']:.4f}
  Gamma:  {self.greeks['gamma']:.4f}
  Theta:  {self.greeks['theta']:.8f}
  Vega:   {self.greeks['vega']:.6f}
  Rho:    {self.greeks['rho']:.6f}

Parameters:
  Spot (S₀):     ${self.params['S0']:.4f}
  Strike (K):    ${self.params['K']:.4f}
  Maturity (T):  {self.params['T']:.2f} years
  Rate (r):      {self.params['r']:.2%}
  Volatility:    {self.params['sigma']:.2%}

Moneyness: {self.computed['moneyness']:.3f}
{'='*50}
"""


class ResultsComparator:
    """
    Compare multiple pricing results.

    Users expect to compare scenarios side-by-side.
    """

    def __init__(self, results: List[PricingResult], labels: Optional[List[str]] = None):
        """
        Initialize comparator.

        Parameters
        ----------
        results : list of PricingResult
            Results to compare
        labels : list of str, optional
            Labels for each result (default: Result 1, Result 2, ...)
        """
        self.results = results
        self.labels = labels or [f"Result {i+1}" for i in range(len(results))]

    def comparison_table(self) -> str:
        """Generate comparison table"""
        # Header
        table = f"\n{'='*80}\n"
        table += f"PRICING COMPARISON ({len(self.results)} scenarios)\n"
        table += f"{'='*80}\n\n"

        # Column headers
        col_width = 20
        table += f"{'Metric':<{col_width}}"
        for label in self.labels:
            table += f"{label:<{col_width}}"
        table += "\n" + "-"*80 + "\n"

        # Option price
        table += f"{'Option Price':<{col_width}}"
        for r in self.results:
            table += f"${r.option_price:<{col_width-1}.6f}"
        table += "\n"

        # Premium %
        table += f"{'Premium %':<{col_width}}"
        for r in self.results:
            table += f"{r.computed['premium_pct']:<{col_width}.2f}%"
        table += "\n\n"

        # Greeks
        table += "GREEKS\n" + "-"*80 + "\n"
        for greek in ['delta', 'gamma', 'theta', 'vega', 'rho']:
            table += f"{greek.capitalize():<{col_width}}"
            for r in self.results:
                table += f"{r.greeks[greek]:<{col_width}.6f}"
            table += "\n"

        table += "\n" + "PARAMETERS\n" + "-"*80 + "\n"

        # Parameters
        for param in ['S0', 'K', 'T', 'r', 'sigma']:
            table += f"{param:<{col_width}}"
            for r in self.results:
                val = r.params[param]
                if param in ['r', 'sigma']:
                    table += f"{val*100:<{col_width}.2f}%"
                else:
                    table += f"{val:<{col_width}.4f}"
            table += "\n"

        table += "\n" + "="*80 + "\n"

        return table

    def best_value(self) -> tuple:
        """
        Find best value option (lowest price).

        Returns
        -------
        tuple
            (index, label, result)
        """
        prices = [r.option_price for r in self.results]
        idx = np.argmin(prices)
        return idx, self.labels[idx], self.results[idx]

    def highest_delta(self) -> tuple:
        """Find option with highest delta"""
        deltas = [r.greeks['delta'] for r in self.results]
        idx = np.argmax(deltas)
        return idx, self.labels[idx], self.results[idx]

    def export_comparison(self, filepath: str):
        """
        Export comparison to CSV.

        Parameters
        ----------
        filepath : str
            Output CSV path
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        rows = []
        for label, result in zip(self.labels, self.results):
            row = {
                'scenario': label,
                'option_price': result.option_price,
                'premium_pct': result.computed['premium_pct'],
                **{f'greek_{k}': v for k, v in result.greeks.items()},
                **{f'param_{k}': v for k, v in result.params.items()}
            }
            rows.append(row)

        if rows:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return filepath


class PricingValidator:
    """
    Validate pricing results for sanity.

    Users expect: "Is this price reasonable or did something go wrong?"
    """

    # Typical ranges for validation
    VOLATILITY_NORMAL_MAX = 1.0  # 100% is already high
    VOLATILITY_EXTREME_MAX = 3.0  # 300% is extreme
    PREMIUM_TYPICAL_MAX = 0.5  # 50% premium is high
    PREMIUM_EXTREME_MAX = 1.0  # 100% premium is extreme

    @staticmethod
    def validate(result: PricingResult) -> Dict[str, Any]:
        """
        Validate pricing result and return warnings/info.

        Parameters
        ----------
        result : PricingResult
            Result to validate

        Returns
        -------
        dict
            Validation report with warnings and info
        """
        warnings = []
        info = []
        errors = []

        # Check option price
        if result.option_price <= 0:
            errors.append("Option price is zero or negative - calculation error")
        elif result.option_price > result.params['S0']:
            warnings.append(f"Option price (${result.option_price:.4f}) exceeds spot price (${result.params['S0']:.4f})")

        # Check volatility
        vol = result.params['sigma']
        if vol > PricingValidator.VOLATILITY_EXTREME_MAX:
            warnings.append(f"EXTREME volatility: {vol:.0%} (typical max: {PricingValidator.VOLATILITY_EXTREME_MAX:.0%})")
        elif vol > PricingValidator.VOLATILITY_NORMAL_MAX:
            info.append(f"High volatility: {vol:.0%} (normal max: {PricingValidator.VOLATILITY_NORMAL_MAX:.0%})")

        # Check premium
        premium_pct = result.computed['premium_pct'] / 100
        if premium_pct > PricingValidator.PREMIUM_EXTREME_MAX:
            warnings.append(f"EXTREME premium: {premium_pct:.0%} of spot (typical max: {PricingValidator.PREMIUM_EXTREME_MAX:.0%})")
        elif premium_pct > PricingValidator.PREMIUM_TYPICAL_MAX:
            info.append(f"High premium: {premium_pct:.0%} (normal max: {PricingValidator.PREMIUM_TYPICAL_MAX:.0%})")

        # Check delta
        delta = result.greeks['delta']
        if not (0 <= delta <= 1):
            warnings.append(f"Delta ({delta:.3f}) outside valid range [0, 1]")

        # Check moneyness
        moneyness = result.computed['moneyness']
        if moneyness < 0.5 or moneyness > 2.0:
            info.append(f"Deep {'out' if moneyness < 1 else 'in'}-the-money (moneyness: {moneyness:.2f})")

        # Generate summary
        status = 'ERROR' if errors else 'WARNING' if warnings else 'OK'

        return {
            'status': status,
            'errors': errors,
            'warnings': warnings,
            'info': info,
            'is_valid': len(errors) == 0
        }

    @staticmethod
    def validation_report(result: PricingResult) -> str:
        """Generate human-readable validation report"""
        validation = PricingValidator.validate(result)

        report = f"\n{'='*60}\n"
        report += f"VALIDATION REPORT\n"
        report += f"{'='*60}\n"
        report += f"Status: {validation['status']}\n"
        report += f"{'='*60}\n\n"

        if validation['errors']:
            report += "❌ ERRORS:\n"
            for err in validation['errors']:
                report += f"  - {err}\n"
            report += "\n"

        if validation['warnings']:
            report += "⚠️  WARNINGS:\n"
            for warn in validation['warnings']:
                report += f"  - {warn}\n"
            report += "\n"

        if validation['info']:
            report += "ℹ️  INFO:\n"
            for inf in validation['info']:
                report += f"  - {inf}\n"
            report += "\n"

        if not (validation['errors'] or validation['warnings'] or validation['info']):
            report += "✅ All checks passed - result looks reasonable\n\n"

        report += f"{'='*60}\n"

        return report


def batch_price(
    scenarios: List[Dict],
    pricing_func,
    labels: Optional[List[str]] = None
) -> ResultsComparator:
    """
    Price multiple scenarios in batch.

    Users expect: "I have 5 solar farms, price them all."

    Parameters
    ----------
    scenarios : list of dict
        List of parameter dictionaries
    pricing_func : callable
        Function that takes params and returns (price, greeks)
    labels : list of str, optional
        Labels for each scenario

    Returns
    -------
    ResultsComparator
        Comparator with all results

    Examples
    --------
    >>> scenarios = [
    ...     {'lat': 24.99, 'lon': 121.30},  # Taiwan
    ...     {'lat': 33.45, 'lon': -112.07},  # Arizona
    ... ]
    >>> comparator = batch_price(scenarios, my_pricing_func, ['Taiwan', 'Arizona'])
    >>> print(comparator.comparison_table())
    """
    results = []

    for scenario in scenarios:
        price, greeks, params = pricing_func(scenario)
        result = PricingResult(
            option_price=price,
            greeks=greeks,
            params=params,
            metadata=scenario
        )
        results.append(result)

    return ResultsComparator(results, labels)


def comparative_context(result: PricingResult) -> Dict[str, str]:
    """
    Add comparative context: "Is this a good deal?"

    Users expect to understand if their pricing is reasonable.

    Parameters
    ----------
    result : PricingResult
        Pricing result to contextualize

    Returns
    -------
    dict
        Contextual comparisons
    """
    context = {}

    # Volatility comparison
    vol = result.params['sigma']
    stock_market_vol = 0.20  # Typical S&P 500
    vol_multiple = vol / stock_market_vol

    context['volatility_vs_stocks'] = (
        f"Your volatility ({vol:.0%}) is {vol_multiple:.1f}x higher than "
        f"stock market ({stock_market_vol:.0%})"
    )

    # Premium comparison
    premium_pct = result.computed['premium_pct']
    insurance_typical = 1.5  # Typical insurance ~1-2% of value

    if premium_pct > 10:
        context['premium_vs_insurance'] = (
            f"Your option premium ({premium_pct:.1f}% of spot) is {premium_pct/insurance_typical:.1f}x "
            f"higher than typical insurance ({insurance_typical:.1f}%). "
            f"This is weather derivatives, not insurance - high volatility = high premium."
        )
    else:
        context['premium_vs_insurance'] = (
            f"Your option premium ({premium_pct:.1f}% of spot) is comparable to "
            f"insurance costs ({insurance_typical:.1f}%)."
        )

    # Time value
    days_to_expiry = result.computed['time_to_maturity_days']
    if days_to_expiry < 30:
        context['time_context'] = (
            f"Only {days_to_expiry:.0f} days to expiry - time decay accelerating rapidly"
        )
    elif days_to_expiry < 90:
        context['time_context'] = (
            f"{days_to_expiry:.0f} days to expiry - moderate time decay"
        )
    else:
        context['time_context'] = (
            f"{days_to_expiry:.0f} days to expiry - slow time decay"
        )

    return context


def break_even_analysis(result: PricingResult, system_size_kw: float = 10.0) -> Dict[str, Any]:
    """
    Calculate break-even scenarios: "When does this pay off?"

    Users expect to understand when the hedge is worthwhile.

    Parameters
    ----------
    result : PricingResult
        Pricing result
    system_size_kw : float
        System size in kW for scaling

    Returns
    -------
    dict
        Break-even calculations
    """
    # Simplified break-even calculation
    # For a call option: pays off when S_T > K + premium

    premium = result.option_price
    strike = result.params['K']
    spot = result.params['S0']

    # Break-even spot price at expiry
    breakeven_price = strike + premium
    breakeven_change_pct = ((breakeven_price / spot) - 1) * 100

    # Probability estimate (simplified using normal approximation)
    vol = result.params['sigma']
    T = result.params['T']

    # For ATM option, roughly 50% probability
    # For ITM/OTM, adjust based on moneyness
    moneyness = result.computed['moneyness']

    return {
        'breakeven_price': breakeven_price,
        'breakeven_change_pct': breakeven_change_pct,
        'current_spot': spot,
        'strike': strike,
        'premium_paid': premium,
        'interpretation': (
            f"Option breaks even if price reaches ${breakeven_price:.4f} "
            f"({breakeven_change_pct:+.1f}% from current spot)"
        )
    }
