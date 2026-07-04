"""Shared configuration for the Kyiv air quality data pipeline."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_WAREHOUSE = ROOT / "data" / "warehouse"
DATA_PROCESSED = ROOT / "data" / "processed"
TRANSFORM = ROOT / "transform"

DB_PATH = DATA_WAREHOUSE / "kyiv.duckdb"

KYIV_CITY_ID = 2
KYIV_CENTER = (50.4501, 30.5234)

SAVEECOBOT_BASE = "https://www.saveecobot.com/en/maps"
CITY_HISTORY_URL = f"{SAVEECOBOT_BASE}/city-history-v1/city/{KYIV_CITY_ID}.json"
DISTRICT_HISTORY_URL = f"{SAVEECOBOT_BASE}/city-history-v1/district/{{entity_id}}.json"

OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

GTFS_URL = "http://193.23.225.211:8002/export-gtfs-static"

DISTRICT_ENTITY_IDS = {
    "holosiivskyi": 95,
    "darnytskyi": 96,
    "desnianskyi": 97,
    "dniprovskyi": 98,
    "obolonskyi": 99,
    "pecherskyi": 100,
    "podilskyi": 101,
    "sviatoshynskyi": 102,
    "solomianskyi": 103,
    "shevchenkivskyi": 104,
}

DISTRICT_SLUGS = list(DISTRICT_ENTITY_IDS.keys())

DISTRICT_DISPLAY_NAMES = {
    "holosiivskyi": "Holosiivskyi",
    "darnytskyi": "Darnytskyi",
    "desnianskyi": "Desnianskyi",
    "dniprovskyi": "Dniprovskyi",
    "obolonskyi": "Obolonskyi",
    "pecherskyi": "Pecherskyi",
    "podilskyi": "Podilskyi",
    "sviatoshynskyi": "Sviatoshynskyi",
    "solomianskyi": "Solomianskyi",
    "shevchenkivskyi": "Shevchenkivskyi",
}

# Approximate district centroids and bbox (WGS84) for GTFS stop assignment
DISTRICT_BBOX = {
    "holosiivskyi": {"lat": 50.395, "lon": 30.505, "min_lat": 50.34, "max_lat": 50.43, "min_lon": 30.45, "max_lon": 30.56},
    "darnytskyi": {"lat": 50.405, "lon": 30.645, "min_lat": 50.36, "max_lat": 50.45, "min_lon": 30.58, "max_lon": 30.72},
    "desnianskyi": {"lat": 50.515, "lon": 30.615, "min_lat": 50.48, "max_lat": 50.55, "min_lon": 30.55, "max_lon": 30.68},
    "dniprovskyi": {"lat": 50.455, "lon": 30.605, "min_lat": 50.42, "max_lat": 50.49, "min_lon": 30.55, "max_lon": 30.66},
    "obolonskyi": {"lat": 50.515, "lon": 30.495, "min_lat": 50.48, "max_lat": 50.55, "min_lon": 30.42, "max_lon": 30.56},
    "pecherskyi": {"lat": 50.425, "lon": 30.545, "min_lat": 50.40, "max_lat": 50.45, "min_lon": 30.50, "max_lon": 30.60},
    "podilskyi": {"lat": 50.475, "lon": 30.485, "min_lat": 50.44, "max_lat": 50.51, "min_lon": 30.42, "max_lon": 30.55},
    "sviatoshynskyi": {"lat": 50.455, "lon": 30.395, "min_lat": 50.42, "max_lat": 50.49, "min_lon": 30.34, "max_lon": 30.45},
    "solomianskyi": {"lat": 50.435, "lon": 30.475, "min_lat": 50.40, "max_lat": 50.47, "min_lon": 30.42, "max_lon": 30.53},
    "shevchenkivskyi": {"lat": 50.455, "lon": 30.515, "min_lat": 50.43, "max_lat": 50.48, "min_lon": 30.48, "max_lon": 30.55},
}

WHO_PM25_THRESHOLD = 15.0
