# Methodology

This V1 estimates launch usability using a simple elevation-threshold method.

1. Scrape the NPS Lake Roosevelt boating page for the published minimum lake elevation for each boat launch.
2. Fetch the Bureau of Reclamation Grand Coulee Dam Lake Roosevelt lake-level page and parse the most recent observed midnight elevation shown there.
3. Keep a [USGS Water Services site 12436000](https://waterdata.usgs.gov/monitoring-location/12436000/) catalog snapshot as official station metadata and use the USGS daily values endpoint as a fallback if Reclamation parsing fails.
4. Join each launch threshold to V1 coordinate seeds compiled from NPS structured data, NPS place pages, and OpenStreetMap slipway features.
5. Calculate `margin_ft = current_lake_elevation_ft - minimum_launch_elevation_ft`.
6. Assign status:
   - `Likely usable` when `margin_ft >= 5`
   - `Marginal` when `0 <= margin_ft < 5`
   - `Below threshold` when `margin_ft < 0`

The dashboard does not determine whether a launch is officially open or closed. It only estimates likely usability based on reservoir elevation and published thresholds. Users should check official NPS alerts and local conditions.
