"""Ingest Kyiv public transport GTFS data for mobility proxy metrics."""

from __future__ import annotations

import io
import zipfile
from pathlib import Path

import gtfs_kit as gk
import pandas as pd
import requests

from config import DATA_RAW, DISTRICT_BBOX, DISTRICT_SLUGS, GTFS_URL
from utils import ensure_dirs, get_connection


def assign_district(lat: float, lon: float) -> str | None:
    """Assign a stop to a district using bounding box."""
    for slug in DISTRICT_SLUGS:
        bbox = DISTRICT_BBOX[slug]
        if (
            bbox["min_lat"] <= lat <= bbox["max_lat"]
            and bbox["min_lon"] <= lon <= bbox["max_lon"]
        ):
            return slug
    return None


def download_gtfs() -> Path:
    """Download GTFS static feed to data/raw."""
    ensure_dirs()
    zip_path = DATA_RAW / "gtfs_kyiv.zip"
    print(f"Downloading GTFS from {GTFS_URL}...")
    response = requests.get(
        GTFS_URL,
        timeout=120,
        headers={"User-Agent": "KyivAirExplorer/1.0 (portfolio project)"},
    )
    response.raise_for_status()
    zip_path.write_bytes(response.content)
    print(f"  Saved {len(response.content):,} bytes")
    return zip_path


def ingest_gtfs(zip_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse GTFS zip into stops and trip frequency tables."""
    extract_dir = DATA_RAW / "gtfs"
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)

    feed = gk.read_feed(str(extract_dir), dist_units="km")

    stops = feed.stops.copy()
    stops = stops.dropna(subset=["stop_lat", "stop_lon"])
    stops["district_slug"] = stops.apply(
        lambda row: assign_district(row["stop_lat"], row["stop_lon"]),
        axis=1,
    )
    stops = stops.dropna(subset=["district_slug"])

    stop_times = feed.stop_times.merge(
        feed.trips[["trip_id", "route_id"]],
        on="trip_id",
        how="left",
    )
    stop_times = stop_times.merge(
        stops[["stop_id", "district_slug"]],
        on="stop_id",
        how="inner",
    )

    # Count trips per stop (proxy for service frequency)
    trip_counts = (
        stop_times.groupby(["district_slug", "stop_id", "route_id"])
        .size()
        .reset_index(name="trip_count")
    )

    print(f"  Parsed {len(stops):,} stops in Kyiv districts")
    print(f"  Parsed {len(trip_counts):,} stop-route trip records")
    return stops, trip_counts


def main() -> None:
    try:
        zip_path = download_gtfs()
        stops_df, trips_df = ingest_gtfs(zip_path)
    except Exception as exc:
        print(f"GTFS download failed ({exc}), using fallback sample data...")
        stops_df, trips_df = _fallback_mobility_data()

    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS raw_mobility_stops")
    conn.execute("DROP TABLE IF EXISTS raw_mobility_trips")
    conn.register("stops_df", stops_df)
    conn.register("trips_df", trips_df)
    conn.execute(
        """
        CREATE TABLE raw_mobility_stops AS
        SELECT
            stop_id,
            stop_name,
            CAST(stop_lat AS DOUBLE) AS latitude,
            CAST(stop_lon AS DOUBLE) AS longitude,
            district_slug
        FROM stops_df
        """
    )
    conn.execute(
        """
        CREATE TABLE raw_mobility_trips AS
        SELECT
            district_slug,
            stop_id,
            route_id,
            trip_count
        FROM trips_df
        """
    )
    conn.close()
    print("Mobility ingest complete.")


def _fallback_mobility_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate synthetic mobility proxy when GTFS is unavailable."""
    from config import DISTRICT_BBOX, DISTRICT_DISPLAY_NAMES

    stops_rows = []
    trip_rows = []
    for i, slug in enumerate(DISTRICT_SLUGS):
        bbox = DISTRICT_BBOX[slug]
        for j in range(5 + i * 2):
            stops_rows.append(
                {
                    "stop_id": f"{slug}_{j}",
                    "stop_name": f"Stop {j} ({DISTRICT_DISPLAY_NAMES[slug]})",
                    "stop_lat": bbox["lat"] + (j - 2) * 0.005,
                    "stop_lon": bbox["lon"] + (j - 2) * 0.005,
                    "district_slug": slug,
                }
            )
            trip_rows.append(
                {
                    "district_slug": slug,
                    "stop_id": f"{slug}_{j}",
                    "route_id": f"route_{j % 4}",
                    "trip_count": 20 + j * 3,
                }
            )

    return pd.DataFrame(stops_rows), pd.DataFrame(trip_rows)


if __name__ == "__main__":
    main()
