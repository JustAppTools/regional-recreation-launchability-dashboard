from config import DATA_PROCESSED, DATA_RAW, DOCS, DOCS_DATA, OUTPUTS_FIGURES, OUTPUTS_MAPS, OUTPUTS_REPORT
import fetch_lake_elevation
import fetch_launch_thresholds
import make_chart
import process_data


def ensure_directories() -> None:
    for path in [DATA_RAW, DATA_PROCESSED, DOCS, DOCS_DATA, OUTPUTS_FIGURES, OUTPUTS_MAPS, OUTPUTS_REPORT]:
        path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ensure_directories()
    thresholds = fetch_launch_thresholds.main()
    elevation = fetch_lake_elevation.main()
    rows = process_data.main()
    chart = make_chart.main()
    print(f"Fetched {len(thresholds)} launch thresholds.")
    print(f"Fetched lake elevation {float(elevation['lake_elevation_ft']):.1f} ft observed at {elevation['observed_at']}.")
    print(f"Wrote {len(rows)} records to data/processed/launch_status.csv.")
    print("Wrote docs/data/launch_status.geojson.")
    print(f"Wrote {chart}.")


if __name__ == "__main__":
    main()

