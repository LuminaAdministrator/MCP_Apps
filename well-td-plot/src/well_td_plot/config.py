from __future__ import annotations

import os


class Settings:
    def __init__(
        self,
        *,
        data_source_mode: str | None = None,
        data_service_url: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ) -> None:
        self.data_source_mode = (
            data_source_mode
            if data_source_mode is not None
            else os.environ.get("TD_PLOT_DATA_SOURCE_MODE", "fixture")
        )
        self.data_service_url = (
            data_service_url
            if data_service_url is not None
            else os.environ.get("TD_PLOT_DATA_SERVICE_URL", "http://localhost:8001")
        )
        self.host = host if host is not None else os.environ.get("TD_PLOT_HOST", "0.0.0.0")
        self.port = port if port is not None else int(os.environ.get("TD_PLOT_PORT", "8080"))
        self.app_id = "well.TD.plot"
        self.app_version = "1"
        self.ui_resource_uri = "ui://well.TD.plot/main.html"


def get_settings() -> Settings:
    return Settings()
