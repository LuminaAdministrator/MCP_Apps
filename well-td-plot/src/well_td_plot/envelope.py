from __future__ import annotations

from typing import Any

from .config import Settings


def build_vega_lite_spec(td_data: dict[str, Any]) -> dict[str, Any]:
    """Build a Vega-Lite line chart spec from TD function data."""
    td_pairs = td_data.get("td_pairs", [])
    time_label = f"{td_data.get('time_ref', 'Time')} ({td_data.get('time_unit', '')})"
    depth_label = f"{td_data.get('depth_ref', 'Depth')} ({td_data.get('depth_unit', '')})"

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Time-Depth function plot",
        "width": 350,
        "height": 550,
        "data": {"values": td_pairs},
        "mark": {"type": "line", "color": "#1f77b4", "strokeWidth": 2},
        "encoding": {
            "x": {
                "field": "time",
                "type": "quantitative",
                "title": time_label,
                "axis": {"orient": "top", "tickCount": 6},
            },
            "y": {
                "field": "depth",
                "type": "quantitative",
                "title": depth_label,
                "scale": {"reverse": True},
                "axis": {"tickCount": 8},
            },
            "tooltip": [
                {"field": "time",  "type": "quantitative", "title": time_label},
                {"field": "depth", "type": "quantitative", "title": depth_label},
            ],
        },
        "title": td_data.get("dataname", "Time-Depth Function"),
    }


def build_envelope(
    uniquedataid: str,
    td_data: dict[str, Any],
    vega_lite_spec: dict[str, Any],
    settings: Settings,
    *,
    html_text: str | None = None,
) -> dict[str, Any]:
    """Build the canonical JIO app instance envelope for a TD plot result."""
    dataname = td_data.get("dataname", uniquedataid)
    instance_id = f"well.TD.plot.{uniquedataid}"

    ui_resource: dict[str, Any] = {
        "uri": settings.ui_resource_uri,
        "mimeType": "text/html;profile=mcp-app",
    }
    if html_text is not None:
        ui_resource["text"] = html_text

    return {
        "instance_id": instance_id,
        "result_kind": "app_instance",
        "app_id": settings.app_id,
        "app_version": settings.app_version,
        "source_tool": "well.TD.plot.render",
        "title": f"TD Plot: {dataname}",
        "artifact_refs": [],
        "emitted_artifacts": [
            {
                "artifact_id": f"artifact:well.TD.plot:{uniquedataid}:chart_spec",
                "artifact_type": "chart_spec",
                "role": "primary",
                "title": f"TD chart — {dataname}",
                "source_tool": "well.TD.plot.render",
                "instance_id": instance_id,
            }
        ],
        "selectable_runtime_values": [
            {
                "key": "selected_uniquedataid",
                "value_type": "string",
                "label": "Selected TD function",
                "description": "The uniquedataid of the TD function that was plotted.",
                "value_schema": {"type": "string"},
            }
        ],
        "state_kind": "resolved",
        "state_schema_version": "1",
        "state": {
            "uniquedataid": uniquedataid,
            "dataname": dataname,
            "source_tool": "Vega Lite Chart",
            "time_ref": td_data.get("time_ref"),
            "time_unit": td_data.get("time_unit"),
            "depth_ref": td_data.get("depth_ref"),
            "depth_unit": td_data.get("depth_unit"),
            "vega_lite_spec": vega_lite_spec,
            "data_point_count": len(td_data.get("td_pairs", [])),
        },
        "summary": (
            f"Resolved TD plot for '{dataname}' ({uniquedataid}), "
            f"{len(td_data.get('td_pairs', []))} data points."
        ),
        "meta": {
            "app_name": "TD Plot",
            "description": "Time-Depth function plot using Vega-Lite.",
            "ui_resource": ui_resource,
        },
    }
