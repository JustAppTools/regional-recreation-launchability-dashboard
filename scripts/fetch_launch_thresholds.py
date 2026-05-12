import csv
import html
import re
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

from config import DATA_RAW, GENERATED_AT_TIMEZONE, NPS_BOATING_URL


USER_AGENT = "LakeRooseveltLaunchabilityDashboard/0.1 personal public data project"


def fetch_url(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_thresholds(page_html: str) -> list[dict]:
    heading = "Minimum Boat Launch Lake Elevations"
    start = page_html.find(heading)
    if start == -1:
        raise RuntimeError("Could not find NPS minimum boat launch elevation heading.")

    ul_match = re.search(r"<ul>(.*?)</ul>", page_html[start:], flags=re.IGNORECASE | re.DOTALL)
    if not ul_match:
        raise RuntimeError("Could not find NPS launch elevation list after heading.")

    rows = []
    for item in re.findall(r"<li[^>]*>(.*?)</li>", ul_match.group(1), flags=re.IGNORECASE | re.DOTALL):
        text = re.sub(r"<[^>]+>", " ", item)
        text = html.unescape(text).replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text).strip()
        match = re.match(r"(.+?)\s+(\d{4})\s*'?$", text)
        if not match:
            continue
        rows.append(
            {
                "launch_name": match.group(1).strip(),
                "minimum_launch_elevation_ft": float(match.group(2)),
                "threshold_source_url": NPS_BOATING_URL,
            }
        )

    if len(rows) < 20:
        raise RuntimeError(f"Expected about 22 launch thresholds; parsed {len(rows)}.")
    return rows


def write_thresholds(rows: list[dict]) -> None:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    path = DATA_RAW / "nps_launch_thresholds.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["launch_name", "minimum_launch_elevation_ft", "threshold_source_url"],
        )
        writer.writeheader()
        writer.writerows(rows)

    metadata = DATA_RAW / "nps_launch_thresholds_metadata.txt"
    generated = datetime.now(ZoneInfo(GENERATED_AT_TIMEZONE)).isoformat(timespec="seconds")
    metadata.write_text(
        "\n".join(
            [
                f"source_url={NPS_BOATING_URL}",
                f"retrieved_at={generated}",
                f"record_count={len(rows)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> list[dict]:
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    raw_html = fetch_url(NPS_BOATING_URL)
    (DATA_RAW / "nps_boating.html").write_text(raw_html, encoding="utf-8")
    rows = parse_thresholds(raw_html)
    write_thresholds(rows)
    return rows


if __name__ == "__main__":
    parsed = main()
    print(f"Fetched {len(parsed)} NPS launch thresholds.")

