I built V1 of a small public-data dashboard for Lake Roosevelt NRA boat launches.

The idea is simple: combine the current/recent Lake Roosevelt reservoir elevation with NPS-published minimum launch elevations, then calculate how much margin each launch has above or below its threshold.

V1 includes:

- A reproducible Python pipeline
- NPS threshold scraping
- Bureau of Reclamation lake-level fetching
- CSV and GeoJSON outputs
- A static Leaflet dashboard
- A chart for quick portfolio/storytelling use

Important caveat: this is not official NPS guidance. It estimates whether a launch is likely usable based on published elevation thresholds only. Actual access can change because of official alerts, maintenance, weather, debris, and on-the-ground conditions.

Next steps after V1 could include cleaner GIS source validation, alert integration, or publishing through GitHub Pages, but I intentionally kept this first version focused and reproducible.
