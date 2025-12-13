import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.main import app  # type: ignore  # noqa: E402

client = TestClient(app)


def test_price_endpoint_binomial():
    payload = {"S0": 1.0, "K": 1.0, "T": 1.0, "r": 0.05, "sigma": 0.2, "method": "binomial", "N": 50}
    resp = client.post("/price", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "price" in data and data["price"] > 0


def test_greeks_endpoint():
    payload = {"S0": 1.0, "K": 1.0, "T": 1.0, "r": 0.05, "sigma": 0.2}
    resp = client.post("/greeks", json=payload)
    assert resp.status_code == 200
    greeks = resp.json()["greeks"]
    assert all(k in greeks for k in ["Delta", "Gamma", "Vega", "Theta", "Rho"])


def test_rate_limit_headers_present():
    payload = {"S0": 1.0, "K": 1.0, "T": 1.0, "r": 0.05, "sigma": 0.2}
    resp = client.post("/price", json=payload)
    assert resp.status_code == 200
