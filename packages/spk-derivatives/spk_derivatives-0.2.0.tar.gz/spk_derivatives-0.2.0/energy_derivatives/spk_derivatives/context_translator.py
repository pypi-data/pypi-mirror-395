"""
Context Translator - Sophisticated UX Layer
============================================

Translates technical pricing outputs into real-world context that users understand.

This isn't dumbing down - it's adding sophistication by doing the extra math that
grounds abstract financial metrics in practical, relatable terms.

Examples of translations:
- Technical: "Volatility 200%"
  Grounded: "Your daily revenue could vary by ±$450 on a 10kW system"

- Technical: "$0.035645 per kWh/m²/day"
  Grounded: "$127/month hedge cost for your 50kW commercial rooftop"

- Technical: "GHI 5.2 kWh/m²/day"
  Grounded: "Your panels would produce 38 kWh/day (15% efficiency, 5kW system)"

Philosophy: Meet users where they are. Give them numbers that connect to their reality.
"""

from typing import Dict, Optional, Tuple
import numpy as np


class SolarSystemContext:
    """
    Translates solar irradiance to actual system output accounting for:
    - Panel efficiency (typical: 15-22%)
    - System losses (inverter, wiring, temperature: ~15%)
    - Panel degradation (typical: 0.5%/year)
    - Installation factors (tilt, orientation)
    """

    # Industry standard values
    PANEL_EFFICIENCY_TYPICAL = 0.20  # Modern panels: 20%
    PANEL_EFFICIENCY_PREMIUM = 0.22  # High-end panels: 22%
    PANEL_EFFICIENCY_BUDGET = 0.15   # Budget panels: 15%

    SYSTEM_LOSSES = 0.15  # Inverter, wiring, temperature: 15%
    DEGRADATION_PER_YEAR = 0.005  # 0.5% per year

    def __init__(
        self,
        system_size_kw: float,
        panel_efficiency: float = PANEL_EFFICIENCY_TYPICAL,
        system_age_years: float = 0,
        include_losses: bool = True
    ):
        """
        Initialize solar system context.

        Parameters
        ----------
        system_size_kw : float
            System size in kW (e.g., 5.0 for residential, 50.0 for commercial)
        panel_efficiency : float
            Panel efficiency (0.15-0.22 typical), default 0.20 (20%)
        system_age_years : float
            Age of system for degradation calculation
        include_losses : bool
            Whether to include system losses (inverter, wiring, etc.)
        """
        self.system_size_kw = system_size_kw
        self.panel_efficiency = panel_efficiency
        self.system_age_years = system_age_years
        self.include_losses = include_losses

        # Calculate effective efficiency
        degradation_factor = (1 - self.DEGRADATION_PER_YEAR) ** system_age_years
        self.effective_efficiency = panel_efficiency * degradation_factor

        if include_losses:
            self.effective_efficiency *= (1 - self.SYSTEM_LOSSES)

    def ghi_to_ac_output(self, ghi_kwh_m2_day: float) -> float:
        """
        Convert Global Horizontal Irradiance to actual AC output.

        Parameters
        ----------
        ghi_kwh_m2_day : float
            Solar irradiance in kWh/m²/day

        Returns
        -------
        float
            Actual AC electricity output in kWh/day
        """
        # GHI × System Size (kW) × Efficiency = AC Output (kWh/day)
        # Note: kW rating assumes 1 kW/m² standard test conditions
        ac_output = ghi_kwh_m2_day * self.system_size_kw * self.effective_efficiency
        return ac_output

    def ghi_to_monthly_output(self, ghi_kwh_m2_day: float) -> float:
        """Convert GHI to monthly AC output."""
        daily = self.ghi_to_ac_output(ghi_kwh_m2_day)
        return daily * 30  # Approximate month

    def ghi_to_annual_output(self, ghi_kwh_m2_day: float) -> float:
        """Convert GHI to annual AC output."""
        daily = self.ghi_to_ac_output(ghi_kwh_m2_day)
        return daily * 365

    def get_system_info(self) -> Dict:
        """Get human-readable system information."""
        if self.system_size_kw < 10:
            system_type = "Residential"
        elif self.system_size_kw < 100:
            system_type = "Commercial Rooftop"
        elif self.system_size_kw < 1000:
            system_type = "Small Solar Farm"
        else:
            system_type = "Utility-Scale Solar Farm"

        return {
            'system_type': system_type,
            'size_kw': self.system_size_kw,
            'panel_efficiency_pct': self.panel_efficiency * 100,
            'effective_efficiency_pct': self.effective_efficiency * 100,
            'age_years': self.system_age_years,
            'includes_losses': self.include_losses
        }


class PriceTranslator:
    """
    Translates option prices into real-world costs/revenues for specific system sizes.
    """

    def __init__(
        self,
        solar_system: SolarSystemContext,
        electricity_rate: float = 0.12,  # $/kWh (typical US residential)
        buyback_rate: Optional[float] = None  # $/kWh (net metering rate)
    ):
        """
        Initialize price translator.

        Parameters
        ----------
        solar_system : SolarSystemContext
            Solar system specification
        electricity_rate : float
            Utility electricity rate ($/kWh)
        buyback_rate : float, optional
            Solar buyback/net metering rate ($/kWh)
            If None, assumes same as electricity_rate
        """
        self.solar_system = solar_system
        self.electricity_rate = electricity_rate
        self.buyback_rate = buyback_rate or electricity_rate

    def option_price_to_monthly_cost(
        self,
        option_price_per_ghi: float,
        ghi_kwh_m2_day: float
    ) -> float:
        """
        Convert option price ($/kWh/m²/day) to monthly hedge cost.

        Parameters
        ----------
        option_price_per_ghi : float
            Option price in dollars per (kWh/m²/day)
        ghi_kwh_m2_day : float
            Current solar irradiance

        Returns
        -------
        float
            Monthly cost in dollars
        """
        # Option is priced per unit of GHI
        # For a system, cost scales with system size and time
        daily_cost = option_price_per_ghi * self.solar_system.system_size_kw
        monthly_cost = daily_cost * 30
        return monthly_cost

    def option_price_to_annual_cost(
        self,
        option_price_per_ghi: float,
        ghi_kwh_m2_day: float
    ) -> float:
        """Convert option price to annual hedge cost."""
        daily_cost = option_price_per_ghi * self.solar_system.system_size_kw
        annual_cost = daily_cost * 365
        return annual_cost

    def revenue_at_ghi(self, ghi_kwh_m2_day: float) -> Tuple[float, float, float]:
        """
        Calculate revenue at given irradiance level.

        Returns
        -------
        tuple
            (daily_revenue, monthly_revenue, annual_revenue)
        """
        daily_kwh = self.solar_system.ghi_to_ac_output(ghi_kwh_m2_day)
        daily_revenue = daily_kwh * self.buyback_rate

        monthly_revenue = daily_revenue * 30
        annual_revenue = daily_revenue * 365

        return daily_revenue, monthly_revenue, annual_revenue


class VolatilityTranslator:
    """
    Translates volatility percentages into dollar revenue swings.
    """

    def __init__(
        self,
        price_translator: PriceTranslator,
        spot_ghi: float
    ):
        """
        Initialize volatility translator.

        Parameters
        ----------
        price_translator : PriceTranslator
            Price translator instance
        spot_ghi : float
            Current spot GHI (kWh/m²/day)
        """
        self.price_translator = price_translator
        self.spot_ghi = spot_ghi

    def volatility_to_revenue_range(
        self,
        volatility: float,
        confidence: float = 0.68  # 1 standard deviation
    ) -> Tuple[float, float, float]:
        """
        Convert volatility to daily revenue range.

        Parameters
        ----------
        volatility : float
            Annualized volatility (e.g., 2.0 for 200%)
        confidence : float
            Confidence level (0.68 = 1σ, 0.95 = 2σ)

        Returns
        -------
        tuple
            (daily_low, daily_expected, daily_high) revenue in dollars
        """
        # Daily volatility = annual volatility / sqrt(365)
        daily_vol = volatility / np.sqrt(365)

        # For confidence interval, use appropriate z-score
        if confidence == 0.68:
            z = 1.0  # 1 standard deviation
        elif confidence == 0.95:
            z = 2.0  # 2 standard deviations
        else:
            z = 1.0

        # GHI range at confidence interval
        ghi_low = self.spot_ghi * np.exp(-z * daily_vol)
        ghi_high = self.spot_ghi * np.exp(z * daily_vol)

        # Convert to revenue
        daily_low, _, _ = self.price_translator.revenue_at_ghi(ghi_low)
        daily_expected, _, _ = self.price_translator.revenue_at_ghi(self.spot_ghi)
        daily_high, _, _ = self.price_translator.revenue_at_ghi(ghi_high)

        return daily_low, daily_expected, daily_high

    def volatility_to_monthly_range(
        self,
        volatility: float,
        confidence: float = 0.68
    ) -> Tuple[float, float, float]:
        """
        Convert volatility to monthly revenue range.

        Monthly volatility = daily volatility × sqrt(30)
        """
        daily_low, daily_expected, daily_high = self.volatility_to_revenue_range(
            volatility, confidence
        )

        return daily_low * 30, daily_expected * 30, daily_high * 30


class GreeksTranslator:
    """
    Translates Greeks into actionable risk management metrics.
    """

    @staticmethod
    def delta_to_hedge_amount(
        delta: float,
        system_size_kw: float,
        ghi_kwh_m2_day: float,
        solar_system: SolarSystemContext
    ) -> Dict:
        """
        Translate Delta to actual amount of production to hedge.

        Parameters
        ----------
        delta : float
            Option delta (0-1)
        system_size_kw : float
            System size in kW
        ghi_kwh_m2_day : float
            Current GHI
        solar_system : SolarSystemContext
            Solar system for output calculation

        Returns
        -------
        dict
            Hedge amounts in various units
        """
        daily_output_kwh = solar_system.ghi_to_ac_output(ghi_kwh_m2_day)
        hedge_kwh_daily = daily_output_kwh * delta
        hedge_kwh_monthly = hedge_kwh_daily * 30

        return {
            'delta': delta,
            'hedge_ratio_pct': delta * 100,
            'daily_output_kwh': daily_output_kwh,
            'hedge_kwh_daily': hedge_kwh_daily,
            'hedge_kwh_monthly': hedge_kwh_monthly,
            'interpretation': f"Hedge {delta:.1%} of your production"
        }

    @staticmethod
    def theta_to_time_decay(
        theta: float,
        system_size_kw: float
    ) -> Dict:
        """
        Translate Theta to actual dollar decay.

        Parameters
        ----------
        theta : float
            Theta (per day)
        system_size_kw : float
            System size for scaling

        Returns
        -------
        dict
            Time decay in various periods
        """
        # Theta is per unit per day, scale by system size
        daily_decay = abs(theta) * system_size_kw
        weekly_decay = daily_decay * 7
        monthly_decay = daily_decay * 30
        annual_decay = daily_decay * 365

        return {
            'theta_per_day': theta,
            'daily_decay_dollars': daily_decay,
            'weekly_decay_dollars': weekly_decay,
            'monthly_decay_dollars': monthly_decay,
            'annual_decay_dollars': annual_decay,
            'interpretation': f"Option loses ${daily_decay:.2f}/day to time decay"
        }

    @staticmethod
    def vega_to_volatility_impact(
        vega: float,
        system_size_kw: float,
        current_volatility: float
    ) -> Dict:
        """
        Translate Vega to dollar impact of volatility changes.

        Parameters
        ----------
        vega : float
            Vega (price change per 1% volatility change)
        system_size_kw : float
            System size for scaling
        current_volatility : float
            Current volatility level

        Returns
        -------
        dict
            Volatility impact scenarios
        """
        # Scale vega by system size
        vega_scaled = vega * system_size_kw

        # Show impact of ±10% volatility change
        impact_10pct_increase = vega_scaled * 10
        impact_10pct_decrease = -vega_scaled * 10

        # Show impact of ±20% volatility change
        impact_20pct_increase = vega_scaled * 20
        impact_20pct_decrease = -vega_scaled * 20

        return {
            'vega': vega,
            'current_volatility_pct': current_volatility * 100,
            'impact_10pct_increase': impact_10pct_increase,
            'impact_10pct_decrease': impact_10pct_decrease,
            'impact_20pct_increase': impact_20pct_increase,
            'impact_20pct_decrease': impact_20pct_decrease,
            'interpretation': f"±10% volatility change = ±${abs(impact_10pct_increase):.2f} option value"
        }


def create_contextual_summary(
    option_price: float,
    greeks: Dict,
    params: Dict,
    system_size_kw: float = 10.0,
    electricity_rate: float = 0.12,
    panel_efficiency: float = 0.20
) -> str:
    """
    Create a comprehensive, contextually grounded summary.

    This is the sophistication layer in action.

    Parameters
    ----------
    option_price : float
        Calculated option price
    greeks : dict
        Greeks dictionary
    params : dict
        Pricing parameters
    system_size_kw : float
        System size in kW
    electricity_rate : float
        $/kWh electricity rate
    panel_efficiency : float
        Panel efficiency (0.15-0.22)

    Returns
    -------
    str
        Formatted contextual summary
    """
    # Set up translators
    solar_system = SolarSystemContext(
        system_size_kw=system_size_kw,
        panel_efficiency=panel_efficiency
    )

    price_translator = PriceTranslator(
        solar_system=solar_system,
        electricity_rate=electricity_rate
    )

    vol_translator = VolatilityTranslator(
        price_translator=price_translator,
        spot_ghi=params['S0'] / 0.10  # Convert back to GHI
    )

    # Calculate contextual metrics
    spot_ghi = params['S0'] / 0.10
    system_info = solar_system.get_system_info()
    daily_output = solar_system.ghi_to_ac_output(spot_ghi)
    monthly_output = daily_output * 30

    daily_rev, monthly_rev, annual_rev = price_translator.revenue_at_ghi(spot_ghi)

    monthly_hedge_cost = price_translator.option_price_to_monthly_cost(
        option_price, spot_ghi
    )
    annual_hedge_cost = price_translator.option_price_to_annual_cost(
        option_price, spot_ghi
    )

    daily_low, daily_exp, daily_high = vol_translator.volatility_to_revenue_range(
        params['sigma'], confidence=0.68
    )
    monthly_low, monthly_exp, monthly_high = vol_translator.volatility_to_monthly_range(
        params['sigma'], confidence=0.68
    )

    delta_info = GreeksTranslator.delta_to_hedge_amount(
        greeks['delta'], system_size_kw, spot_ghi, solar_system
    )

    theta_info = GreeksTranslator.theta_to_time_decay(
        greeks['theta'], system_size_kw
    )

    vega_info = GreeksTranslator.vega_to_volatility_impact(
        greeks['vega'], system_size_kw, params['sigma']
    )

    # Build the summary
    summary = f"""
{'='*70}
SOLAR DERIVATIVES PRICING - CONTEXTUAL SUMMARY
{'='*70}

YOUR SOLAR SYSTEM
{'-'*70}
System Type:       {system_info['system_type']}
System Size:       {system_size_kw:.1f} kW
Panel Efficiency:  {system_info['panel_efficiency_pct']:.1f}%
Effective Output:  {system_info['effective_efficiency_pct']:.1f}% (after losses)

CURRENT PRODUCTION & REVENUE
{'-'*70}
Solar Irradiance:  {spot_ghi:.2f} kWh/m²/day
Your AC Output:    {daily_output:.1f} kWh/day ({monthly_output:.0f} kWh/month)
Daily Revenue:     ${daily_rev:.2f}/day
Monthly Revenue:   ${monthly_rev:.2f}/month
Annual Revenue:    ${annual_rev:,.2f}/year

(at ${electricity_rate:.2f}/kWh electricity rate)

REVENUE VOLATILITY (What "σ = {params['sigma']:.0%}" Actually Means)
{'-'*70}
Your revenue is VOLATILE. Here's what that means in dollars:

Daily Revenue Range (68% confidence):
  Low Day:         ${daily_low:.2f}  (bad weather)
  Expected:        ${daily_exp:.2f}  (average)
  High Day:        ${daily_high:.2f} (excellent sun)
  Daily Swing:     ±${(daily_high - daily_exp):.2f}

Monthly Revenue Range (68% confidence):
  Low Month:       ${monthly_low:.2f}
  Expected:        ${monthly_exp:.2f}
  High Month:      ${monthly_high:.2f}
  Monthly Swing:   ±${(monthly_high - monthly_exp):.2f}

Translation: Your monthly revenue could vary by ±${(monthly_high - monthly_exp):.0f}
due to weather unpredictability.

OPTION PRICING (What It Costs to Hedge This Risk)
{'-'*70}
Call Option Price:     ${option_price:.6f} per unit
Your Monthly Cost:     ${monthly_hedge_cost:.2f}/month
Your Annual Cost:      ${annual_hedge_cost:.2f}/year

Translation: It costs ${monthly_hedge_cost:.0f}/month to protect against
revenue drops below ${params['K']:.4f}.

Cost as % of revenue:  {(monthly_hedge_cost/monthly_rev)*100:.1f}% of expected revenue

RISK MANAGEMENT METRICS (What the Greeks Mean for YOU)
{'-'*70}

1. DELTA = {greeks['delta']:.3f} → HEDGE RATIO
   Your Daily Output:     {daily_output:.1f} kWh/day
   Amount to Hedge:       {delta_info['hedge_kwh_daily']:.1f} kWh/day ({delta_info['hedge_ratio_pct']:.1f}%)
   Monthly Hedge:         {delta_info['hedge_kwh_monthly']:.0f} kWh/month

   Translation: To properly hedge, you need to cover {delta_info['hedge_ratio_pct']:.0f}%
   of your production with this option.

2. THETA = {greeks['theta']:.6f} → TIME DECAY
   Daily Value Loss:      ${theta_info['daily_decay_dollars']:.2f}/day
   Weekly Value Loss:     ${theta_info['weekly_decay_dollars']:.2f}/week
   Monthly Value Loss:    ${theta_info['monthly_decay_dollars']:.2f}/month
   Annual Value Loss:     ${theta_info['annual_decay_dollars']:.2f}/year

   Translation: If you BUY this option, you lose ${theta_info['daily_decay_dollars']:.2f}/day
   to time decay. If you SELL it, you earn ${theta_info['daily_decay_dollars']:.2f}/day.

3. VEGA = {greeks['vega']:.6f} → VOLATILITY SENSITIVITY
   Current Volatility:    {vega_info['current_volatility_pct']:.0f}%

   If volatility increases by 10%:  Option value +${vega_info['impact_10pct_increase']:.2f}
   If volatility decreases by 10%:  Option value ${vega_info['impact_10pct_decrease']:.2f}

   Translation: If weather becomes MORE unpredictable (+10% vol), your option
   is worth ${vega_info['impact_10pct_increase']:.0f} more. If weather stabilizes, it
   loses ${abs(vega_info['impact_10pct_decrease']):.0f} in value.

PRACTICAL SCENARIOS
{'-'*70}

Scenario A: You OWN the solar farm, WANT TO HEDGE revenue risk
  → BUY this call option
  → Cost: ${monthly_hedge_cost:.2f}/month
  → Benefit: Protected if production drops below {params['K']:.4f}
  → Trade-off: Pay ${monthly_hedge_cost:.0f}/month for peace of mind

Scenario B: You're a SPECULATOR, think weather will be BETTER than expected
  → SELL this call option
  → Collect: ${monthly_hedge_cost:.2f}/month premium
  → Risk: Pay out if production exceeds {params['K']:.4f}
  → Profit: Earn ${theta_info['daily_decay_dollars']:.2f}/day from time decay

Scenario C: You think VOLATILITY WILL INCREASE (storm season)
  → BUY this option (vega = {greeks['vega']:.4f} > 0)
  → Gain: ${vega_info['impact_10pct_increase']:.0f} per +10% volatility
  → Strategy: Volatility trading (not directional)

COMPARISON TO OTHER INVESTMENTS
{'-'*70}
Your annual revenue:           ${annual_rev:,.0f}
Annual hedge cost:             ${annual_hedge_cost:,.0f} ({(annual_hedge_cost/annual_rev)*100:.1f}% of revenue)
Revenue volatility:            {params['sigma']:.0%}

For comparison:
- Stock market volatility:     ~20% (your risk is {params['sigma']/0.20:.1f}x higher)
- Insurance as % of value:     ~1-2% (you're paying {(annual_hedge_cost/annual_rev)*100:.1f}%)
- This is weather derivatives, not insurance (different product)

{'='*70}
"""

    return summary
