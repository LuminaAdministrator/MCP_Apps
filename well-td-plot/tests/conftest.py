from __future__ import annotations

import json
from pathlib import Path

import pytest

from well_td_plot.config import Settings

SCHEMAS_DIR = Path(__file__).resolve().parents[1] / "schemas"
FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture()
def fixture_settings() -> Settings:
    return Settings(data_source_mode="fixture")


@pytest.fixture()
def schema_registry():
    """Build a jsonschema Registry from the project schemas dir."""
    from referencing import Registry, Resource

    registry = Registry()
    for schema_path in SCHEMAS_DIR.glob("*.json"):
        contents = json.loads(schema_path.read_text(encoding="utf-8"))
        if isinstance(contents, dict) and "$id" in contents:
            registry = registry.with_resource(
                contents["$id"], Resource.from_contents(contents)
            )
    return registry


@pytest.fixture()
def envelope_schema() -> dict:
    path = SCHEMAS_DIR / "app_instance_envelope.public.schema.json"
    return json.loads(path.read_text(encoding="utf-8"))
