FROM python:3.12-slim

WORKDIR /app

# src/ must be present when pip builds the package
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir .

# Runtime assets
COPY ui/          ./ui/
COPY schemas/     ./schemas/
COPY sample_data/ ./sample_data/
COPY fixtures/    ./fixtures/

ENV TD_PLOT_HOST=0.0.0.0
ENV TD_PLOT_PORT=8080
ENV TD_PLOT_DATA_SOURCE_MODE=fixture

EXPOSE 8080

CMD ["python", "-m", "well_td_plot.http_app"]
