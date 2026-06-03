# Regional Recreation Launchability Dashboard

Independent public-data dashboard estimating regional boat launch usability from the latest available reservoir elevation and published minimum launch elevations.

This is an independent personal portfolio project and is not official guidance from the Bureau of Reclamation, National Park Service, Bureau of Land Management, tribal governments, state agencies, local governments, or any other land manager. Results should be read as "likely usable based on published elevation thresholds" and are subject to official alerts, maintenance, weather, debris, and on-the-ground conditions.

## Overview

The dashboard combines public reservoir-elevation data with published boat-launch minimum elevation thresholds to produce a reproducible, map-based snapshot of likely launchability. It is designed as a compact geospatial data project: source data is fetched with Python, transformed into tabular and GeoJSON outputs, visualized in a static web dashboard, and refreshed automatically through GitHub Actions.

The public dashboard includes:

- Latest available lake elevation and observation date
- Daily data retrieval timestamp
- Interactive Leaflet map of launch locations
- Launch table with minimum elevation, elevation margin, and status label
- Source attribution and non-official-use disclaimer

Live site: https://justapptools.github.io/regional-recreation-launchability-dashboard/

## Run

```bash
python scripts/run_all.py
```

The pipeline writes:

- `data/processed/launch_status.csv`
- `docs/data/launch_status.geojson`
- `outputs/figures/launch_status_chart.png`

Open `docs/index.html` in a browser after running the pipeline.

## Refresh Data

On Windows, use the local virtual environment Python directly:

```powershell
& .\.venv\Scripts\python.exe scripts\run_all.py
```

GitHub Actions refreshes the generated dashboard data once per day at `13:00 UTC` using the workflow in `.github/workflows/refresh-dashboard.yml`. The workflow can also be run manually from the repository's GitHub Actions tab by selecting **Refresh dashboard data** and choosing **Run workflow**.

When the workflow commits refreshed generated data, GitHub Pages updates from the committed `docs/` files.

## Data Sources

- NPS Lake Roosevelt boating page: public boat launch minimum lake elevations.
- Bureau of Reclamation Grand Coulee Dam Lake Roosevelt lake levels page: latest available observed elevation.
- [USGS Water Services site 12436000](https://waterdata.usgs.gov/monitoring-location/12436000/) catalog/daily endpoint: official site metadata and fallback data check for Franklin Roosevelt Lake at Grand Coulee Dam.
- OpenStreetMap and NPS structured data: launch point coordinate seeds for mapping.

## Status Rules

- `Likely usable`: `margin_ft >= 5`
- `Marginal`: `0 <= margin_ft < 5`
- `Below threshold`: `margin_ft < 0`

`margin_ft = current_lake_elevation_ft - minimum_launch_elevation_ft`
