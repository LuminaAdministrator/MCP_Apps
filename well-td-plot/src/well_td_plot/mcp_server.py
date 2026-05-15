from __future__ import annotations

from fastmcp import FastMCP

from .config import get_settings
from .data import fetch_td_data
from .envelope import build_envelope, build_vega_lite_spec
from .ui import build_ui_html

mcp = FastMCP(
    "well-td-plot",
    instructions=(
        "Renders a Time-Depth function plot for a well. "
        "Provide a uniquedataid and receive a JIO-compatible app instance envelope "
        "containing a Vega-Lite chart and an embedded HTML UI resource."
    ),
)


@mcp.tool()
def render_td_plot(uniquedataid: str) -> dict:
    """Render a Time-Depth function plot for a well.

    Args:
        uniquedataid: The unique data identifier for the TD function in Jio.

    Returns:
        JIO app_instance envelope with a Vega-Lite chart_spec artifact
        and an embedded HTML UI resource (ui://well.TD.plot/main.html).
    """
    settings = get_settings()
    td_data = fetch_td_data(uniquedataid, settings)
    spec = build_vega_lite_spec(td_data)
    html = build_ui_html(spec, td_data.get("dataname", uniquedataid))
    return build_envelope(uniquedataid, td_data, spec, settings, html_text=html)


if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=False)
