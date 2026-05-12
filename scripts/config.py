from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DOCS = PROJECT_ROOT / "docs"
DOCS_DATA = DOCS / "data"
OUTPUTS_FIGURES = PROJECT_ROOT / "outputs" / "figures"
OUTPUTS_MAPS = PROJECT_ROOT / "outputs" / "maps"
OUTPUTS_REPORT = PROJECT_ROOT / "outputs" / "report"

NPS_BOATING_URL = "https://www.nps.gov/laro/planyourvisit/boating.htm"
NPS_STRUCTURED_DATA_URL = "https://www.nps.gov/laro/structured_data_laro.json"
USBR_LAKE_LEVEL_URL = "https://www.usbr.gov/pn/grandcoulee/lakelevel/index.html"
USGS_SITE_URL = (
    "https://waterservices.usgs.gov/nwis/site/?format=rdb&sites=12436000"
    "&seriesCatalogOutput=true&siteStatus=all"
)
USGS_DAILY_VALUES_URL = (
    "https://waterservices.usgs.gov/nwis/dv/?format=json&sites=12436000"
    "&period=P30D&parameterCd=62614&siteStatus=all"
)

GENERATED_AT_TIMEZONE = "America/Denver"

STATUS_ORDER = {
    "Below threshold": 0,
    "Marginal": 1,
    "Likely usable": 2,
}

