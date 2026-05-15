FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY pyproject.toml ./
RUN pip install --no-cache-dir ".[dev]"

# Copy application source
COPY src/ ./src/
COPY ui/  ./ui/
COPY schemas/ ./schemas/
COPY sample_data/ ./sample_data/
COPY fixtures/ ./fixtures/

# Default: run the HTTP app
ENV TD_PLOT_HOST=0.0.0.0
ENV TD_PLOT_PORT=8080
ENV TD_PLOT_DATA_SOURCE_MODE=fixture

EXPOSE 8080

CMD ["python", "-m", "well_td_plot.http_app"]
