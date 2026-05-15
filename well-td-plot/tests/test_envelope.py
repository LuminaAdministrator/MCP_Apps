"""Validate the envelope builder and fixture against the public JIO schema."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from well_td_plot.data import fetch_td_data
from well_td_plot.envelope import build_envelope, build_vega_lite_spec

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


# ── builder tests ────────────────────────────────────────────────────────────

def test_envelope_validates_against_public_schema(
    fixture_settings, envelope_schema, schema_registry
):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)

    validator = jsonschema.Draft202012Validator(envelope_schema, registry=schema_registry)
    errors = list(validator.iter_errors(envelope))
    assert not errors, "Envelope validation errors:\n" + "\n".join(str(e) for e in errors)


def test_result_kind_is_app_instance(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    assert envelope["result_kind"] == "app_instance"


def test_state_kind_is_resolved(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    assert envelope["state_kind"] == "resolved"


def test_state_schema_version(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    assert envelope["state_schema_version"] == "1"


def test_emits_chart_spec_artifact(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    types = [a["artifact_type"] for a in envelope["emitted_artifacts"]]
    assert "chart_spec" in types


def test_primary_artifact_role(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    primary = [a for a in envelope["emitted_artifacts"] if a.get("role") == "primary"]
    assert primary
    assert primary[0]["artifact_type"] == "chart_spec"


def test_state_contains_vega_spec(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    assert "vega_lite_spec" in envelope["state"]
    assert isinstance(envelope["state"]["vega_lite_spec"], dict)


def test_state_source_tool_is_vega_lite(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    assert envelope["state"]["source_tool"] == "Vega Lite Chart"


def test_state_carries_measurement_refs(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    state = envelope["state"]
    assert state["time_ref"] == "TWT"
    assert state["depth_ref"] == "MD"
    assert state["time_unit"] == "ms"
    assert state["depth_unit"] == "m"


def test_ui_resource_published(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    assert envelope["meta"]["ui_resource"]["uri"] == "ui://well.TD.plot/main.html"


def test_html_text_embedded_in_ui_resource(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope(
        "example-well-001", td_data, spec, fixture_settings, html_text="<html/>"
    )
    assert envelope["meta"]["ui_resource"].get("text") == "<html/>"


def test_selectable_runtime_value_key(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    keys = [v["key"] for v in envelope["selectable_runtime_values"]]
    assert "selected_uniquedataid" in keys


def test_no_provider_fields_at_top_level(fixture_settings):
    """Vega-Lite fields must not appear at the top level of the JIO envelope."""
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-001", td_data, spec, fixture_settings)
    vega_fields = {"$schema", "mark", "encoding", "data", "layer", "hconcat", "vconcat"}
    leaked = set(envelope.keys()) & vega_fields
    assert not leaked, f"Provider-native Vega-Lite fields leaked to top level: {leaked}"


def test_vega_spec_uses_real_axis_labels(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    assert "TWT" in spec["encoding"]["x"]["title"]
    assert "MD" in spec["encoding"]["y"]["title"]


def test_vega_spec_depth_axis_reversed(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    assert spec["encoding"]["y"]["scale"]["reverse"] is True


def test_vega_spec_line_only_no_point(fixture_settings):
    td_data = fetch_td_data("example-well-001", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    mark = spec["mark"]
    assert mark["type"] == "line"
    assert "point" not in mark


def test_second_well_validates(fixture_settings, envelope_schema, schema_registry):
    td_data = fetch_td_data("example-well-002", fixture_settings)
    spec = build_vega_lite_spec(td_data)
    envelope = build_envelope("example-well-002", td_data, spec, fixture_settings)
    validator = jsonschema.Draft202012Validator(envelope_schema, registry=schema_registry)
    errors = list(validator.iter_errors(envelope))
    assert not errors


# ── pre-built fixture test ───────────────────────────────────────────────────

def test_bundled_fixture_validates(envelope_schema, schema_registry):
    """The committed fixtures/envelope.example.json must pass schema validation."""
    instance = json.loads(
        (FIXTURES_DIR / "envelope.example.json").read_text(encoding="utf-8")
    )
    validator = jsonschema.Draft202012Validator(envelope_schema, registry=schema_registry)
    errors = list(validator.iter_errors(instance))
    assert not errors, "Fixture validation errors:\n" + "\n".join(str(e) for e in errors)
