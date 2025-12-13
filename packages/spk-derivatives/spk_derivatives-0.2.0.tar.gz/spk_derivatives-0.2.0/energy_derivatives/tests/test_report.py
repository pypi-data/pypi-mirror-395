import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spk_derivatives.report import generate_report  # type: ignore  # noqa: E402


def test_generate_report(tmp_path: Path):
    out = tmp_path / "results"
    result = generate_report(output_dir=out, use_live_if_missing=False)
    assert result["markdown"].exists()
