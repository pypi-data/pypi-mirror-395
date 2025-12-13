"""
Utility script to export current CEIR-derived snapshot (S0, K, sigma, r, Greeks)
into a JSON file usable by the blockchain oracle updater.
"""

import json
from pathlib import Path
import sys

from data_loader import load_parameters
from sensitivities import GreeksCalculator


def export_snapshot(
    output: Path = Path("energy_derivatives/results/snapshot.json"),
    data_dir: str = "empirical",
    use_repo_fallback: bool = True,
    use_live_if_missing: bool = False,
):
    params = load_parameters(
        data_dir=data_dir,
        use_repo_fallback=use_repo_fallback,
        use_live_if_missing=use_live_if_missing,
    )
    calc = GreeksCalculator(
        params["S0"], params["K"], params["T"], params["r"], params["sigma"],
        pricing_method="binomial", N=200
    )
    greeks = calc.compute_all_greeks()

    snapshot = {
        "S0": float(params["S0"]),
        "K": float(params["K"]),
        "sigma": int(params["sigma"] * 1_000_000),  # scale for solidity
        "r": int(params["r"] * 1_000_000),
        "greeks": {k.lower(): float(v) for k, v in greeks.items() if k != "Price"},
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        json.dump(snapshot, f, indent=2)
    return output


if __name__ == "__main__":
    out = export_snapshot()
    print(f"Wrote snapshot to {out}")
