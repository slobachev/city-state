# Data Dictionary

## Raw Tables (DuckDB)

### `raw_air_hourly`
Hourly air quality readings at city and district level.

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | TIMESTAMP | Hour bucket (local Kyiv time) |
| `entity_type` | VARCHAR | `city` or `district` |
| `entity_id` | INTEGER | SaveEcoBot entity ID |
| `entity_slug` | VARCHAR | URL slug (e.g. `holosiivskyi`) |
| `entity_name` | VARCHAR | Human-readable name |
| `aqi_pm25` | DOUBLE | AQI PM2.5 NowCast |
| `humidity_pct` | DOUBLE | Relative humidity (nullable) |
| `wind_speed_ms` | DOUBLE | Wind speed (nullable) |

### `raw_weather_hourly`
Open-Meteo historical weather for Kyiv center.

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | TIMESTAMP | Hour |
| `temperature_c` | DOUBLE | °C |
| `humidity_pct` | DOUBLE | % |
| `wind_speed_ms` | DOUBLE | m/s |
| `precipitation_mm` | DOUBLE | mm |

### `raw_mobility_stops`
GTFS stops with district assignment.

| Column | Type | Description |
|--------|------|-------------|
| `stop_id` | VARCHAR | GTFS stop ID |
| `stop_name` | VARCHAR | Stop name |
| `latitude` | DOUBLE | WGS84 |
| `longitude` | DOUBLE | WGS84 |
| `district_slug` | VARCHAR | Assigned Kyiv district |

## Processed JSON (Nuxt API)

| File | Description |
|------|-------------|
| `overview.json` | KPI cards, top districts, correlations |
| `districts_daily.json` | Daily time series per district |
| `districts_geo.json` | District centroids and bbox for maps |
| `timeseries_hourly.json` | City-level hourly series (sampled) |
| `mobility_proxy.json` | Mobility metrics per district |
| `insights_context.json` | Pre-aggregated stats for AI endpoint |
