# TD Plot — JIO-Compatible MCP App

A standalone MCP app that renders **Time-Depth (TD) function plots** for well data.

This app wraps [Vega-Lite](https://vega.github.io/vega-lite/) to produce a JIO-compatible
`app_instance` envelope containing an interactive HTML chart.

---

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Run the HTTP app (standalone browser mode)
python -m well_td_plot.http_app

# Run the MCP server (stdio)
python -m well_td_plot.mcp_server

# Run tests
pytest -v
```

## Configuration

All settings are env-var driven (`TD_PLOT_*`). Copy `.env.example` to `.env` and adjust.

| Variable | Default | Description |
|---|---|---|
| `TD_PLOT_DATA_SOURCE_MODE` | `fixture` | `fixture` or `external_http` |
| `TD_PLOT_DATA_SERVICE_URL` | `http://localhost:8001` | Base URL for external TD data service |
| `TD_PLOT_HOST` | `0.0.0.0` | HTTP server bind address |
| `TD_PLOT_PORT` | `8080` | HTTP server port |

### Data source modes

- **`fixture`** — loads from `sample_data/{well_uuid}.json`. Use for local development and tests.
- **`external_http`** — fetches `GET {DATA_SERVICE_URL}/wells/{uuid}/td_function`. Expected response shape matches `sample_data/example-well-001.json`.

## HTTP Endpoints

| Path | Description |
|---|---|
| `GET /health` | Health check |
| `GET /healthz` | Health check (alias) |
| `GET /wells/{uuid}/plot` | Standalone HTML TD plot page |
| `GET /wells/{uuid}/envelope` | JIO app instance envelope (JSON) |

## MCP Tool

**`render_td_plot(well_uuid: str)`**

Returns a JIO `app_instance` envelope with:
- `emitted_artifacts`: one `chart_spec` artifact (primary role)
- `selectable_runtime_values`: `selected_well_uuid`
- `state`: includes `vega_lite_spec` and `source_tool: "Vega Lite Chart"`
- `meta.ui_resource`: `ui://well.TD.plot/main.html` with embedded HTML `text`

## Lifecycle Model

| Field | Value |
|---|---|
| `result_kind` | `app_instance` |
| `state_kind` | `resolved` |
| `state_schema_version` | `1` |

This app is **read-only** (no durable session state). Each call with the same UUID produces
the same resolved envelope. The state schema is defined in `schemas/state.resolved.v1.schema.json`.

## Validation

Validate the bundled fixture against the public JIO schema:

```bash
cd C:\Claude_Projects\third_party_reference
python scripts/validate_public_bundle_examples.py \
  --schema schemas/app_instance_envelope.public.schema.json \
  C:\Claude_Projects\MCP_Plot_TD\fixtures\envelope.example.json
```

Or using the project-local schemas:

```bash
python -c "
import json, jsonschema
from pathlib import Path
from referencing import Registry, Resource

schemas_dir = Path('schemas')
registry = Registry()
for p in schemas_dir.glob('*.json'):
    c = json.loads(p.read_text())
    if '\$id' in c:
        registry = registry.with_resource(c['\$id'], Resource.from_contents(c))

schema = json.loads((schemas_dir / 'app_instance_envelope.public.schema.json').read_text())
instance = json.loads(Path('fixtures/envelope.example.json').read_text())
v = jsonschema.Draft202012Validator(schema, registry=registry)
errors = list(v.iter_errors(instance))
print('OK' if not errors else errors)
"
```

## Docker

```bash
docker build -t well-td-plot .
docker run -p 8080:8080 well-td-plot
```

## Wrapper Notes

This app wraps Vega-Lite Chart as an upstream provider. Provider-native Vega-Lite fields
are kept inside `state.vega_lite_spec` and never appear at the top level of the JIO envelope.
The host-facing result is indistinguishable from a native JIO app result.

## Repository Layout

```
src/well_td_plot/
  config.py       env-driven settings
  data.py         TD data access (fixture / external_http)
  envelope.py     canonical JIO app result builder
  http_app.py     standalone HTTP surface (FastAPI)
  mcp_server.py   MCP stdio entrypoint (FastMCP)
  ui.py           UI resource construction and config injection
ui/main.html      hosted Vega-Lite UI template
schemas/
  state.resolved.v1.schema.json      app state schema
  app_instance_envelope.public.*     bundled public JIO schemas
sample_data/      example TD function JSON files
fixtures/         pre-built envelope examples for validation
tests/            envelope, HTTP, and MCP transport tests
Dockerfile
.github/workflows/ci.yml
```
