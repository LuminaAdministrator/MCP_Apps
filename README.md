# MCP_Apps

Standalone MCP apps for the JIO geophysical platform.

Each app lives in its own subfolder and is a self-contained repository unit
that satisfies the JIO external delivery bundle contract.

## Apps

| Folder | App ID | Description |
|---|---|---|
| `well-td-plot/` | `well.TD.plot` | Time-Depth function plot for well data (Vega-Lite) |

## Structure

Each app folder contains:

- `src/` — Python package
- `ui/` — HTML UI template
- `schemas/` — JIO public schemas + app state schema
- `sample_data/` — fixture data for local development
- `fixtures/` — pre-built envelope examples for validation
- `tests/` — envelope, HTTP, and MCP transport tests
- `docs/` — upstream API contract (SQL + endpoint shape)
- `helm/` — Helm chart for deployment
- `Dockerfile` / `.github/workflows/ci.yml`

## Running an app locally

```bash
cd well-td-plot
pip install -e ".[dev]"
python -m well_td_plot.http_app      # HTTP mode
python -m well_td_plot.mcp_server    # MCP stdio mode
pytest -v                            # tests
```
