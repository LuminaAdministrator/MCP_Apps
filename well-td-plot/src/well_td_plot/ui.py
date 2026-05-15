from __future__ import annotations

import json
from pathlib import Path
from typing import Any

UI_DIR = Path(__file__).resolve().parents[2] / "ui"
_CONFIG_PLACEHOLDER = "__APP_CONFIG_JSON__"


def load_ui_template() -> str:
    return (UI_DIR / "main.html").read_text(encoding="utf-8")


def inject_config(template: str, config: dict[str, Any]) -> str:
    return template.replace(_CONFIG_PLACEHOLDER, json.dumps(config))


def build_ui_html(vega_lite_spec: dict[str, Any], well_name: str) -> str:
    """Return complete HTML with Vega-Lite spec and well name injected."""
    template = load_ui_template()
    config = {"vegaLiteSpec": vega_lite_spec, "wellName": well_name}
    return inject_config(template, config)
