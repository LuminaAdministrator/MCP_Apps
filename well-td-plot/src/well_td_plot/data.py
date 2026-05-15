from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from .config import Settings

SAMPLE_DATA_DIR = Path(__file__).resolve().parents[2] / "sample_data"


def _load_fixture(uniquedataid: str) -> dict[str, Any]:
    path = SAMPLE_DATA_DIR / f"{uniquedataid}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"No fixture file found for uniquedataid '{uniquedataid}'. "
            f"Expected: {path}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _fetch_external(uniquedataid: str, settings: Settings) -> dict[str, Any]:
    url = f"{settings.data_service_url}/api/td/{uniquedataid}"
    response = httpx.get(url, timeout=30.0)
    response.raise_for_status()
    return response.json()


def fetch_td_data(uniquedataid: str, settings: Settings) -> dict[str, Any]:
    """Fetch TD function data for a given uniquedataid.

    Modes (TD_PLOT_DATA_SOURCE_MODE):
      fixture       — load from sample_data/{uniquedataid}.json
      external_http — GET {DATA_SERVICE_URL}/api/td/{uniquedataid}

    Expected response shape:
      {
        "uniquedataid": str,
        "dataname":     str,
        "time_unit":    str,   e.g. "ms"
        "depth_unit":   str,   e.g. "m"
        "time_ref":     str,   e.g. "TWT" | "OWT"
        "depth_ref":    str,   e.g. "MD" | "TVD"
        "td_pairs": [
          { "time": float, "depth": float },
          ...
        ]
      }
    """
    if settings.data_source_mode == "fixture":
        return _load_fixture(uniquedataid)
    if settings.data_source_mode == "external_http":
        return _fetch_external(uniquedataid, settings)
    raise ValueError(f"Unknown data source mode: {settings.data_source_mode!r}")
