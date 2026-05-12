import csv
import json
import re
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    DATA_RAW,
    GENERATED_AT_TIMEZONE,
    USBR_LAKE_LEVEL_URL,
    USGS_DAILY_VALUES_URL,
    USGS_SITE_URL,
)


USER_AGENT = "LakeRooseveltLaunchabilityDashboard/0.1 personal public data project"


def fetch_url(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_usbr_lake_level(page_html: str) -> dict:
    text = re.sub(r"<[^>]+>", " ", page_html)
    text = re.sub(r"\s+", " ", text)
    observed = re.search(
        r"elevation of Lake Roosevelt was ([0-9,.]+) feet above sea level at midnight on ([A-Za-z]+ \d{1,2}, \d{4})",
        text,
        flags=re.IGNORECASE,
    )
    if not observed:
        raise RuntimeError("Could not parse observed USBR lake elevation.")

    return {
        "lake_elevation_ft": float(observed.group(1).replace(",", "")),
        "observed_at": observed.group(2),
        "lake_elevation_source": "Bureau of Reclamation Grand Coulee Dam Lake Roosevelt Lake Levels",
        "lake_elevation_source_url": USBR_LAKE_LEVEL_URL,
        "is_forecast": "false",
    }


def latest_usgs_value(raw_json: str) -> dict | None:
    payload = json.loads(raw_json)
    series = payload.get("value", {}).get("timeSeries", [])
    values = []
    for item in series:
        for value_block in item.get("values", []):
            values.extend(value_block.get("value", []))
    if not values:
        return None
    latest = sorted(values, key=lambda row: row.get("dateTime", ""))[-1]
    return {
        "lake_elevation_ft": float(latest["value"]),
        "observed_at": latest["dateTime"],
        "lake_elevation_source": "USGS 12436000 Franklin Roosevelt Lake at Grand Coulee Dam",
        "lake_elevation_source_url": USGS_DAILY_VALUES_URL,
        "is_forecast": "false",
    }


def main() -> dict:
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    try:
        usbr_html = fetch_url(USBR_LAKE_LEVEL_URL)
        (DATA_RAW / "usbr_lake_level.html").write_text(usbr_html, encoding="utf-8")
        result = parse_usbr_lake_level(usbr_html)
    except Exception as exc:
        usgs_json = fetch_url(USGS_DAILY_VALUES_URL)
        (DATA_RAW / "usgs_12436000_daily.json").write_text(usgs_json, encoding="utf-8")
        result = latest_usgs_value(usgs_json)
        if result is None:
            raise RuntimeError(
                "USBR elevation parse failed and USGS 12436000 returned no recent values."
            ) from exc

    try:
        site_catalog = fetch_url(USGS_SITE_URL)
        (DATA_RAW / "usgs_12436000_site_catalog.rdb").write_text(site_catalog, encoding="utf-8")
    except Exception:
        pass

    result["retrieved_at"] = datetime.now(ZoneInfo(GENERATED_AT_TIMEZONE)).isoformat(timespec="seconds")
    path = DATA_RAW / "lake_elevation.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)

    return result


if __name__ == "__main__":
    elevation = main()
    print(
        f"Fetched lake elevation {elevation['lake_elevation_ft']:.1f} ft "
        f"from {elevation['lake_elevation_source']}."
    )

