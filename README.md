# Lake Roosevelt Launchability Dashboard

V1 public-data dashboard estimating Lake Roosevelt NRA boat launch usability from current/recent reservoir elevation and NPS-published minimum launch elevations.

This is a personal portfolio project and is not official NPS guidance. Results should be read as "likely usable based on published elevation thresholds" and are subject to official NPS alerts, maintenance, weather, debris, and on-the-ground conditions.

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
- Bureau of Reclamation Grand Coulee Dam Lake Roosevelt lake levels page: current/recent observed elevation.
- [USGS Water Services site 12436000](https://waterdata.usgs.gov/monitoring-location/12436000/) catalog/daily endpoint: official site metadata and fallback data check for Franklin Roosevelt Lake at Grand Coulee Dam.
- OpenStreetMap and NPS structured data: V1 launch point coordinate seeds for mapping.

## Status Rules

- `Likely usable`: `margin_ft >= 5`
- `Marginal`: `0 <= margin_ft < 5`
- `Below threshold`: `margin_ft < 0`

`margin_ft = current_lake_elevation_ft - minimum_launch_elevation_ft`
