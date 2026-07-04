"""Export aggregated data from DuckDB to JSON for the Nuxt app."""

from __future__ import annotations

import json
from datetime import date, datetime

from config import DATA_PROCESSED, DISTRICT_BBOX, DISTRICT_DISPLAY_NAMES
from utils import ensure_dirs, get_connection


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def export_overview(conn) -> None:
    """Export KPI overview and key findings context."""
    city = conn.execute(
        """
        SELECT
            AVG(pm25_ug_m3) AS pm25_avg,
            AVG(aqi_pm25) AS aqi_avg,
            100.0 * AVG(CASE WHEN pm25_ug_m3 > 15.0 THEN 1.0 ELSE 0.0 END) AS exceedance_rate,
            MIN(timestamp) AS period_start,
            MAX(timestamp) AS period_end
        FROM stg_air_hourly
        WHERE entity_type = 'city'
        """
    ).fetchdf().iloc[0].to_dict()

    worst = conn.execute(
        """
        SELECT district_slug, district_name, pm25_avg, exceedance_rate
        FROM mart_district_summary
        ORDER BY pm25_avg DESC
        LIMIT 3
        """
    ).fetchdf().to_dict(orient="records")

    best = conn.execute(
        """
        SELECT district_slug, district_name, pm25_avg, exceedance_rate
        FROM mart_district_summary
        ORDER BY pm25_avg ASC
        LIMIT 3
        """
    ).fetchdf().to_dict(orient="records")

    corr = conn.execute("SELECT * FROM mart_weather_correlation").fetchdf().iloc[0].to_dict()

    seasonal = conn.execute(
        """
        SELECT
            CASE
                WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 'winter'
                WHEN EXTRACT(MONTH FROM date) IN (3, 4, 5) THEN 'spring'
                WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 'summer'
                ELSE 'autumn'
            END AS season,
            AVG(pm25_avg) AS pm25_avg
        FROM mart_district_daily
        GROUP BY 1
        ORDER BY pm25_avg DESC
        """
    ).fetchdf().to_dict(orient="records")

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "city": "Kyiv",
        "kpis": {
            "pm25_avg": round(city["pm25_avg"], 2),
            "aqi_avg": round(city["aqi_avg"], 1),
            "exceedance_rate": round(city["exceedance_rate"], 1),
            "period_start": city["period_start"],
            "period_end": city["period_end"],
        },
        "worst_districts": worst,
        "best_districts": best,
        "seasonal": seasonal,
        "correlations": {
            "pm25_wind": round(corr["corr_pm25_wind"], 3),
            "pm25_humidity": round(corr["corr_pm25_humidity"], 3),
            "pm25_temperature": round(corr["corr_pm25_temperature"], 3),
            "sample_size": int(corr["sample_size"]),
        },
        "findings": _generate_findings(worst, best, seasonal, corr),
    }
    _write("overview.json", payload)


def _generate_findings(worst, best, seasonal, corr) -> list[str]:
    """Generate template findings from aggregated stats."""
    findings = []
    if worst:
        findings.append(
            f"{worst[0]['district_name']} has the highest average PM2.5 "
            f"({worst[0]['pm25_avg']:.1f} µg/m³) across the observation period."
        )
    if seasonal:
        high = seasonal[0]
        low = seasonal[-1]
        findings.append(
            f"Seasonal pattern: {high['season']} averages {high['pm25_avg']:.1f} µg/m³ "
            f"vs {low['season']} at {low['pm25_avg']:.1f} µg/m³."
        )
    if corr.get("corr_pm25_wind") is not None:
        direction = "negative" if corr["corr_pm25_wind"] < 0 else "positive"
        findings.append(
            f"PM2.5 shows a {direction} correlation with wind speed "
            f"(r = {corr['corr_pm25_wind']:.2f}), suggesting dispersion effects."
        )
    if best:
        findings.append(
            f"{best[0]['district_name']} consistently reports the lowest PM2.5 levels "
            f"({best[0]['pm25_avg']:.1f} µg/m³ average)."
        )
    return findings


def export_districts_daily(conn) -> None:
    """Export daily time series per district."""
    df = conn.execute(
        """
        SELECT
            date,
            district_slug,
            district_name,
            ROUND(pm25_avg, 2) AS pm25_avg,
            ROUND(aqi_avg, 1) AS aqi_avg,
            ROUND(exceedance_rate, 1) AS exceedance_rate,
            ROUND(humidity_avg, 1) AS humidity_avg,
            ROUND(wind_avg, 1) AS wind_avg
        FROM mart_district_daily
        ORDER BY date, district_slug
        """
    ).fetchdf()
    _write("districts_daily.json", df.to_dict(orient="records"))


def export_timeseries(conn) -> None:
    """Export city-level hourly time series (sampled for UI performance)."""
    df = conn.execute(
        """
        SELECT
            timestamp,
            ROUND(pm25_ug_m3, 2) AS pm25_ug_m3,
            aqi_pm25,
            humidity_pct,
            wind_speed_ms
        FROM stg_air_hourly
        WHERE entity_type = 'city'
        ORDER BY timestamp
        """
    ).fetchdf()
    # Sample every 3 hours if dataset is large
    if len(df) > 1500:
        df = df.iloc[::3]
    _write("timeseries_hourly.json", df.to_dict(orient="records"))


def export_districts_geo() -> None:
    """Export district centroids and bounding boxes for maps."""
    districts = []
    for slug, bbox in DISTRICT_BBOX.items():
        districts.append(
            {
                "slug": slug,
                "name": DISTRICT_DISPLAY_NAMES[slug],
                "centroid": {"lat": bbox["lat"], "lon": bbox["lon"]},
                "bbox": {
                    "min_lat": bbox["min_lat"],
                    "max_lat": bbox["max_lat"],
                    "min_lon": bbox["min_lon"],
                    "max_lon": bbox["max_lon"],
                },
            }
        )
    _write("districts_geo.json", {"districts": districts})


def export_mobility(conn) -> None:
    """Export mobility proxy metrics."""
    df = conn.execute("SELECT * FROM mart_mobility_proxy ORDER BY district_slug").fetchdf()
    _write("mobility_proxy.json", df.to_dict(orient="records"))


def export_insights_context(conn) -> None:
    """Export pre-aggregated context for AI insights endpoint."""
    overview_path = DATA_PROCESSED / "overview.json"
    overview = json.loads(overview_path.read_text(encoding="utf-8"))
    mobility = json.loads((DATA_PROCESSED / "mobility_proxy.json").read_text(encoding="utf-8"))

    joined = conn.execute(
        """
        SELECT
            d.district_slug,
            d.district_name,
            ROUND(d.pm25_avg, 2) AS pm25_avg,
            ROUND(d.exceedance_rate, 1) AS exceedance_rate,
            m.stop_count,
            m.mobility_stop_density
        FROM mart_district_summary d
        LEFT JOIN mart_mobility_proxy m ON d.district_slug = m.district_slug
        ORDER BY d.pm25_avg DESC
        """
    ).fetchdf().to_dict(orient="records")

    _write(
        "insights_context.json",
        {
            "overview": overview,
            "districts": joined,
            "mobility": mobility,
        },
    )


def _write(filename: str, payload) -> None:
    path = DATA_PROCESSED / filename
    path.write_text(json.dumps(payload, cls=Encoder, indent=2), encoding="utf-8")
    print(f"  Exported {filename}")


def main() -> None:
    ensure_dirs()
    conn = get_connection()
    print("Exporting JSON files...")
    export_overview(conn)
    export_districts_daily(conn)
    export_timeseries(conn)
    export_districts_geo()
    export_mobility(conn)
    export_insights_context(conn)
    conn.close()
    print("Export complete.")


if __name__ == "__main__":
    main()
