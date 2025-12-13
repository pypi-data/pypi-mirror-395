"""
Generate a simple pricing report (markdown + optional PDF) using local modules or API.
"""

from pathlib import Path
import json
import os
from typing import Optional

from .data_loader import load_parameters
from .binomial import BinomialTree
from .monte_carlo import MonteCarloSimulator
from .sensitivities import GreeksCalculator

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def _compute_local(S0: float, K: float, T: float, r: float, sigma: float):
    tree = BinomialTree(S0, K, T, r, sigma, N=200)
    binom_price = tree.price()
    sim = MonteCarloSimulator(S0, K, T, r, sigma, num_simulations=10000)
    mc_price, mc_low, mc_high = sim.confidence_interval()
    greeks = GreeksCalculator(S0, K, T, r, sigma, pricing_method="binomial", N=200).compute_all_greeks()
    return binom_price, mc_price, mc_low, mc_high, greeks


def _write_markdown(path: Path, payload: dict):
    lines = [
        "# Energy Derivatives Report",
        "",
        f"- S0: {payload['S0']:.6f}",
        f"- K: {payload['K']:.6f}",
        f"- T: {payload['T']:.2f}",
        f"- r: {payload['r']:.4f}",
        f"- sigma: {payload['sigma']:.4f}",
        "",
        "## Prices",
        f"- Binomial: {payload['binomial']:.6f}",
        f"- Monte Carlo: {payload['mc_price']:.6f} (95% CI [{payload['mc_low']:.6f}, {payload['mc_high']:.6f}])",
        "",
        "## Greeks",
    ]
    for k, v in payload["greeks"].items():
        lines.append(f"- {k}: {v:.6f}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines))


def _write_pdf(path: Path, payload: dict):
    if not HAS_PDF:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Energy Derivatives Report")
    y -= 30
    c.setFont("Helvetica", 10)
    for line in [
        f"S0: {payload['S0']:.6f}",
        f"K: {payload['K']:.6f}",
        f"T: {payload['T']:.2f}",
        f"r: {payload['r']:.4f}",
        f"sigma: {payload['sigma']:.4f}",
    ]:
        c.drawString(50, y, line); y -= 15
    y -= 10
    c.setFont("Helvetica-Bold", 12); c.drawString(50, y, "Prices"); y -= 20; c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Binomial: {payload['binomial']:.6f}"); y -= 15
    c.drawString(50, y, f"Monte Carlo: {payload['mc_price']:.6f} (95% CI [{payload['mc_low']:.6f}, {payload['mc_high']:.6f}])"); y -= 25
    c.setFont("Helvetica-Bold", 12); c.drawString(50, y, "Greeks"); y -= 20; c.setFont("Helvetica", 10)
    for k, v in payload["greeks"].items():
        c.drawString(50, y, f"{k}: {v:.6f}"); y -= 15
    c.showPage()
    c.save()


def generate_report(
    output_dir: Path = Path("energy_derivatives/results"),
    data_dir: str = "empirical",
    use_live_if_missing: bool = False,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "report.md"
    pdf_path = output_dir / "report.pdf"

    params = load_parameters(data_dir=data_dir, use_live_if_missing=use_live_if_missing)
    payload = {
        "S0": float(params["S0"]),
        "K": float(params["K"]),
        "T": float(params["T"]),
        "r": float(params["r"]),
        "sigma": float(params["sigma"]),
    }

    if api_url and HAS_REQUESTS:
        headers = {"x-api-key": api_key} if api_key else {}
        price_resp = requests.post(f"{api_url}/price", json={"method": "binomial", **payload, "N": 200}, headers=headers, timeout=10)
        greeks_resp = requests.post(f"{api_url}/greeks", json=payload, headers=headers, timeout=10)
        price_data = price_resp.json()
        greeks_data = greeks_resp.json()["greeks"]
        payload.update({
            "binomial": price_data.get("price"),
            "mc_price": price_data.get("price"),
            "mc_low": price_data.get("ci_95", [None, None])[0] if "ci_95" in price_data else price_data.get("price"),
            "mc_high": price_data.get("ci_95", [None, None])[1] if "ci_95" in price_data else price_data.get("price"),
            "greeks": greeks_data,
        })
    else:
        binom_price, mc_price, mc_low, mc_high, greeks = _compute_local(**payload)
        payload.update({
            "binomial": binom_price,
            "mc_price": mc_price,
            "mc_low": mc_low,
            "mc_high": mc_high,
            "greeks": greeks,
        })

    _write_markdown(md_path, payload)
    if HAS_PDF:
        _write_pdf(pdf_path, payload)
    return {"markdown": md_path, "pdf": pdf_path if HAS_PDF else None}


if __name__ == "__main__":
    result = generate_report(
        api_url=os.environ.get("API_URL"),
        api_key=os.environ.get("API_KEY"),
        use_live_if_missing=False,
    )
    print(json.dumps({k: str(v) for k, v in result.items()}))
