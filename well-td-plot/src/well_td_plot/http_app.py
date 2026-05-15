from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from .config import Settings, get_settings
from .data import fetch_td_data
from .envelope import build_envelope, build_vega_lite_spec
from .ui import build_ui_html


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title="TD Plot",
        description="JIO-compatible Time-Depth function plot app (Vega-Lite wrapper)",
        version="1.0.0",
    )

    @app.get("/health")
    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/td/{uniquedataid}/plot", response_class=HTMLResponse)
    def get_plot(uniquedataid: str) -> HTMLResponse:
        """Serve the Vega-Lite TD plot as a standalone HTML page."""
        try:
            td_data = fetch_td_data(uniquedataid, settings)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Data fetch error: {exc}") from exc

        spec = build_vega_lite_spec(td_data)
        html = build_ui_html(spec, td_data.get("dataname", uniquedataid))
        return HTMLResponse(content=html)

    @app.get("/td/{uniquedataid}/envelope")
    def get_envelope(uniquedataid: str) -> JSONResponse:
        """Return the canonical JIO app instance envelope for a TD plot."""
        try:
            td_data = fetch_td_data(uniquedataid, settings)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"Data fetch error: {exc}") from exc

        spec = build_vega_lite_spec(td_data)
        html = build_ui_html(spec, td_data.get("dataname", uniquedataid))
        envelope = build_envelope(uniquedataid, td_data, spec, settings, html_text=html)
        return JSONResponse(content=envelope)

    return app


if __name__ == "__main__":
    import uvicorn

    s = get_settings()
    uvicorn.run(create_app(s), host=s.host, port=s.port)
