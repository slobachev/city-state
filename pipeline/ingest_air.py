"""Ingest air quality data from SaveEcoBot and weather from Open-Meteo."""

from __future__ import annotations

import json
from datetime import datetime

import pandas as pd

from config import (
    CITY_HISTORY_URL,
    DISTRICT_DISPLAY_NAMES,
    DISTRICT_ENTITY_IDS,
    DISTRICT_HISTORY_URL,
    DISTRICT_SLUGS,
    KYIV_CENTER,
    KYIV_CITY_ID,
    OPEN_METEO_URL,
)
from utils import ensure_dirs, fetch_json, get_connection


def parse_history(payload: dict, entity_type: str, entity_id: int, entity_slug: str, entity_name: str) -> list[dict]:
    """Parse SaveEcoBot hourly history into flat records."""
    history = payload.get("hourly", {}).get("history", {})
    rows: list[dict] = []

    for timestamp_str, value in history.items():
        if value is False or value is None:
            continue
        if not isinstance(value, dict):
            continue
        aqi = value.get("a")
        if aqi is None:
            continue
        rows.append(
            {
                "timestamp": datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"),
                "entity_type": entity_type,
                "entity_id": entity_id,
                "entity_slug": entity_slug,
                "entity_name": entity_name,
                "aqi_pm25": float(aqi),
                "humidity_pct": float(value["h"]) if value.get("h") is not None else None,
                "wind_speed_ms": float(value["w"]) if value.get("w") is not None else None,
            }
        )
    return rows


def ingest_saveecobot() -> pd.DataFrame:
    """Fetch city and district air quality history."""
    print("Fetching SaveEcoBot city history...")
    city_payload = fetch_json(CITY_HISTORY_URL, cache_name="city_history.json")
    rows = parse_history(
        city_payload,
        "city",
        KYIV_CITY_ID,
        "kyiv",
        "Kyiv",
    )

    district_ids: dict[str, int] = dict(DISTRICT_ENTITY_IDS)
    for slug in DISTRICT_SLUGS:
        entity_id = district_ids[slug]
        print(f"  Fetching history for {slug} (id={entity_id})...")
        url = DISTRICT_HISTORY_URL.format(entity_id=entity_id)
        payload = fetch_json(url, cache_name=f"district_{slug}_history.json")
        rows.extend(
            parse_history(
                payload,
                "district",
                entity_id,
                slug,
                DISTRICT_DISPLAY_NAMES[slug],
            )
        )

    # Persist district ID map for reference
    ensure_dirs()
    from config import DATA_RAW

    (DATA_RAW / "district_entity_ids.json").write_text(
        json.dumps(district_ids, indent=2),
        encoding="utf-8",
    )

    df = pd.DataFrame(rows)
    print(f"  Loaded {len(df):,} hourly air quality records")
    return df


def ingest_open_meteo(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch historical weather from Open-Meteo for Kyiv center."""
    print(f"Fetching Open-Meteo weather ({start_date} to {end_date})...")
    lat, lon = KYIV_CENTER
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "precipitation",
        ],
        "timezone": "Europe/Kyiv",
    }
    payload = fetch_json(f"{OPEN_METEO_URL}?{requests_params(params)}")
    hourly = payload["hourly"]
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(hourly["time"]),
            "temperature_c": hourly["temperature_2m"],
            "humidity_pct": hourly["relative_humidity_2m"],
            "wind_speed_ms": hourly["wind_speed_10m"],
            "precipitation_mm": hourly["precipitation"],
        }
    )
    print(f"  Loaded {len(df):,} hourly weather records")
    return df


def requests_params(params: dict) -> str:
    """Build query string from params dict."""
    from urllib.parse import urlencode

    flat: dict[str, str] = {}
    for key, value in params.items():
        if isinstance(value, list):
            flat[key] = ",".join(value)
        else:
            flat[key] = str(value)
    return urlencode(flat)


def main() -> None:
    air_df = ingest_saveecobot()
    if air_df.empty:
        raise RuntimeError("No air quality data fetched")

    min_date = air_df["timestamp"].min().strftime("%Y-%m-%d")
    max_date = air_df["timestamp"].max().strftime("%Y-%m-%d")
    weather_df = ingest_open_meteo(min_date, max_date)

    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS raw_air_hourly")
    conn.execute("DROP TABLE IF EXISTS raw_weather_hourly")
    conn.register("air_df", air_df)
    conn.register("weather_df", weather_df)
    conn.execute("CREATE TABLE raw_air_hourly AS SELECT * FROM air_df")
    conn.execute("CREATE TABLE raw_weather_hourly AS SELECT * FROM weather_df")
    conn.close()

    print("Air ingest complete.")


if __name__ == "__main__":
    main()
