"""HTTP entrypoint tests — validates the FastAPI app boundary."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from well_td_plot.http_app import create_app


@pytest.fixture()
def client(fixture_settings):
    return TestClient(create_app(fixture_settings))


# ── health ───────────────────────────────────────────────────────────────────

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ── plot HTML ────────────────────────────────────────────────────────────────

def test_plot_returns_html(client):
    resp = client.get("/td/example-well-001/plot")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_plot_contains_vega_embed(client):
    resp = client.get("/td/example-well-001/plot")
    assert "vegaEmbed" in resp.text


def test_plot_config_injected(client):
    resp = client.get("/td/example-well-001/plot")
    assert "__APP_CONFIG_JSON__" not in resp.text, "Placeholder was not replaced"
    assert "vegaLiteSpec" in resp.text


def test_plot_uses_dataname_as_title(client):
    resp = client.get("/td/example-well-001/plot")
    assert "Example Well 1" in resp.text


def test_plot_404_for_unknown_id(client):
    resp = client.get("/td/no-such-id-9999/plot")
    assert resp.status_code == 404


# ── envelope JSON ────────────────────────────────────────────────────────────

def test_envelope_result_kind(client):
    resp = client.get("/td/example-well-001/envelope")
    assert resp.status_code == 200
    assert resp.json()["result_kind"] == "app_instance"


def test_envelope_app_id(client):
    resp = client.get("/td/example-well-001/envelope")
    assert resp.json()["app_id"] == "well.TD.plot"


def test_envelope_has_ui_resource(client):
    resp = client.get("/td/example-well-001/envelope")
    data = resp.json()
    assert "ui_resource" in data["meta"]
    assert data["meta"]["ui_resource"]["uri"] == "ui://well.TD.plot/main.html"


def test_envelope_html_text_embedded(client):
    resp = client.get("/td/example-well-001/envelope")
    ui_text = resp.json()["meta"]["ui_resource"].get("text", "")
    assert "<!DOCTYPE html>" in ui_text or "<html" in ui_text


def test_envelope_state_carries_refs(client):
    resp = client.get("/td/example-well-001/envelope")
    state = resp.json()["state"]
    assert state["time_ref"] == "TWT"
    assert state["depth_ref"] == "MD"


def test_envelope_404_for_unknown_id(client):
    resp = client.get("/td/no-such-id-9999/envelope")
    assert resp.status_code == 404


def test_envelope_validates_against_schema(client, envelope_schema, schema_registry):
    import jsonschema

    resp = client.get("/td/example-well-001/envelope")
    assert resp.status_code == 200
    validator = jsonschema.Draft202012Validator(envelope_schema, registry=schema_registry)
    errors = list(validator.iter_errors(resp.json()))
    assert not errors, "HTTP envelope errors:\n" + "\n".join(str(e) for e in errors)
