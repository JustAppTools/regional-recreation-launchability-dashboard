import csv
import json
from pathlib import Path

from config import DATA_PROCESSED, DATA_RAW, DOCS_DATA, STATUS_ORDER
from launch_coordinates import LAUNCH_COORDINATES


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def status_for_margin(margin: float) -> str:
    if margin >= 5:
        return "Likely usable"
    if margin >= 0:
        return "Marginal"
    return "Below threshold"


def build_status_rows() -> tuple[list[dict], dict]:
    thresholds = read_csv(DATA_RAW / "nps_launch_thresholds.csv")
    elevation = read_csv(DATA_RAW / "lake_elevation.csv")[0]
    lake_level = float(elevation["lake_elevation_ft"])

    rows = []
    for row in thresholds:
        name = row["launch_name"]
        minimum = float(row["minimum_launch_elevation_ft"])
        margin = lake_level - minimum
        coords = LAUNCH_COORDINATES.get(name)
        if not coords:
            raise RuntimeError(f"No coordinate seed found for launch: {name}")
        rows.append(
            {
                "launch_name": name,
                "minimum_launch_elevation_ft": f"{minimum:.1f}",
                "current_lake_elevation_ft": f"{lake_level:.1f}",
                "margin_ft": f"{margin:.1f}",
                "status": status_for_margin(margin),
                "latitude": f"{coords['latitude']:.6f}",
                "longitude": f"{coords['longitude']:.6f}",
                "coordinate_source": coords["source"],
                "threshold_source_url": row["threshold_source_url"],
                "lake_elevation_source": elevation["lake_elevation_source"],
                "lake_elevation_source_url": elevation["lake_elevation_source_url"],
                "observed_at": elevation["observed_at"],
                "data_retrieved_at": elevation["retrieved_at"],
            }
        )

    rows.sort(key=lambda item: (STATUS_ORDER[item["status"]], float(item["margin_ft"]), item["launch_name"]))
    return rows, elevation


def write_csv(rows: list[dict]) -> None:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    path = DATA_PROCESSED / "launch_status.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_geojson(rows: list[dict], elevation: dict) -> None:
    DOCS_DATA.mkdir(parents=True, exist_ok=True)
    features = []
    for row in rows:
        props = dict(row)
        lon = float(props.pop("longitude"))
        lat = float(props.pop("latitude"))
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": props,
            }
        )
    payload = {
        "type": "FeatureCollection",
        "metadata": {
            "current_lake_elevation_ft": float(elevation["lake_elevation_ft"]),
            "observed_at": elevation["observed_at"],
            "retrieved_at": elevation["retrieved_at"],
            "lake_elevation_source": elevation["lake_elevation_source"],
            "lake_elevation_source_url": elevation["lake_elevation_source_url"],
            "status_rules": {
                "Likely usable": "margin_ft >= 5",
                "Marginal": "0 <= margin_ft < 5",
                "Below threshold": "margin_ft < 0",
            },
            "disclaimer": (
                "Personal public-data portfolio project; not official NPS guidance. "
                "Launch usability is subject to official NPS alerts, maintenance, weather, "
                "debris, and on-the-ground conditions."
            ),
        },
        "features": features,
    }
    serialized = json.dumps(payload, indent=2)
    (DOCS_DATA / "launch_status.geojson").write_text(serialized, encoding="utf-8")
    (DOCS_DATA / "launch_status.js").write_text(
        "window.LAUNCH_STATUS_DATA = " + serialized + ";\n",
        encoding="utf-8",
    )


def main() -> list[dict]:
    rows, elevation = build_status_rows()
    write_csv(rows)
    write_geojson(rows, elevation)
    return rows


if __name__ == "__main__":
    processed = main()
    print(f"Processed {len(processed)} launch status records.")
