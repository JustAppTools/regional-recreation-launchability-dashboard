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

## Data Sources

- NPS Lake Roosevelt boating page: public boat launch minimum lake elevations.
- Bureau of Reclamation Grand Coulee Dam Lake Roosevelt lake levels page: current/recent observed elevation.
- USGS site 12436000 catalog/daily endpoint: official site metadata and fallback data check for Franklin Roosevelt Lake at Grand Coulee Dam.
- OpenStreetMap and NPS structured data: V1 launch point coordinate seeds for mapping.

## Status Rules

- `Likely usable`: `margin_ft >= 5`
- `Marginal`: `0 <= margin_ft < 5`
- `Below threshold`: `margin_ft < 0`

`margin_ft = current_lake_elevation_ft - minimum_launch_elevation_ft`

