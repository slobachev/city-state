"""Utility helpers for the data pipeline."""

import json
import re
import subprocess
from pathlib import Path

import duckdb
import requests

from config import DB_PATH, DATA_RAW, DATA_WAREHOUSE, DATA_PROCESSED


def ensure_dirs() -> None:
    """Create required data directories."""
    for path in (DATA_RAW, DATA_WAREHOUSE, DATA_PROCESSED):
        path.mkdir(parents=True, exist_ok=True)


def get_connection() -> duckdb.DuckDBPyConnection:
    """Open DuckDB connection, creating warehouse dir if needed."""
    ensure_dirs()
    return duckdb.connect(str(DB_PATH))


def fetch_json(url: str, timeout: int = 60, cache_name: str | None = None) -> dict:
    """Fetch JSON using curl (Cloudflare-safe) with optional local cache."""
    ensure_dirs()
    if cache_name:
        cache_path = DATA_RAW / cache_name
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))

    result = subprocess.run(
        [
            "curl",
            "-sL",
            "-H",
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "-H",
            "Accept: application/json, text/plain, */*",
            "-H",
            "Referer: https://www.saveecobot.com/en/maps/kyiv",
            url,
        ],
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0 or not result.stdout:
        raise RuntimeError(f"Failed to fetch {url}: {result.stderr}")

    text = result.stdout.decode("utf-8", errors="replace")
    payload = json.loads(text)
    if cache_name:
        (DATA_RAW / cache_name).write_text(text, encoding="utf-8")
    return payload


def scrape_entity_id(slug: str, parent: str = "kyiv") -> int:
    """Scrape SaveEcoBot entity ID from district page HTML."""
    url = f"https://www.saveecobot.com/en/maps/{parent}/{slug}"
    result = subprocess.run(
        [
            "curl",
            "-sL",
            "-H",
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch {url}")
    match = re.search(r'x-data="\{ id: (\d+) \}"', result.stdout)
    if not match:
        raise ValueError(f"Could not find entity ID for {slug}")
    return int(match.group(1))


def aqi_to_pm25(aqi: float) -> float:
    """Convert US EPA AQI PM2.5 to approximate concentration (µg/m³)."""
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    for c_low, c_high, aqi_low, aqi_high in breakpoints:
        if aqi_low <= aqi <= aqi_high:
            return (c_high - c_low) / (aqi_high - aqi_low) * (aqi - aqi_low) + c_low
    return 500.4


def run_sql_files(conn: duckdb.DuckDBPyConnection, directory: Path) -> None:
    """Execute all SQL files in a directory in sorted order."""
    for sql_file in sorted(directory.glob("*.sql")):
        print(f"  Running {sql_file.name}...")
        sql = sql_file.read_text(encoding="utf-8")
        conn.execute(sql)
        table_name = _extract_table_name(sql)
        if table_name:
            count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"    -> {table_name}: {count:,} rows")


def _extract_table_name(sql: str) -> str | None:
    """Extract target table name from CREATE statement."""
    match = re.search(
        r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW)\s+(\w+)",
        sql,
        re.IGNORECASE,
    )
    return match.group(1) if match else None
