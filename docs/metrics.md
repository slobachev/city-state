# Metrics Definitions

All metrics are computed in DuckDB (`transform/marts/`) and exported to `data/processed/`.

## Air Quality

| Metric            | Definition                                                                  | Source                       |
| ----------------- | --------------------------------------------------------------------------- | ---------------------------- |
| `aqi_pm25`        | PM2.5 Air Quality Index (US EPA NowCast)                                    | SaveEcoBot history field `a` |
| `pm25_ug_m3`      | Estimated PM2.5 concentration (µg/m³), derived from AQI via EPA breakpoints | Computed in `stg_air_hourly` |
| `pm25_avg`        | Mean `pm25_ug_m3` over the selected period                                  | `mart_district_daily`        |
| `aqi_avg`         | Mean `aqi_pm25` over the selected period                                    | `mart_district_daily`        |
| `exceedance_rate` | Share of hourly readings where `pm25_ug_m3` > 15 µg/m³ (WHO guideline)      | `mart_district_daily`        |
| `worst_district`  | District with highest `pm25_avg` in the selected period                     | `overview.json`              |

## Weather

| Metric                       | Definition                                    | Source                                       |
| ---------------------------- | --------------------------------------------- | -------------------------------------------- |
| `temperature_c`              | Air temperature at 2 m (°C)                   | Open-Meteo + SaveEcoBot `h`/`w` proxy fields |
| `humidity_pct`               | Relative humidity (%)                         | SaveEcoBot history field `h`                 |
| `wind_speed_ms`              | Wind speed (m/s)                              | SaveEcoBot history field `w`                 |
| `weather_corr_pm25_wind`     | Pearson r between hourly PM2.5 and wind speed | `mart_weather_correlation`                   |
| `weather_corr_pm25_humidity` | Pearson r between hourly PM2.5 and humidity   | `mart_weather_correlation`                   |

## Mobility (Infrastructure Proxy)

| Metric                  | Definition                                                | Source                    |
| ----------------------- | --------------------------------------------------------- | ------------------------- |
| `stop_count`            | Number of public transport stops in district bounding box | Kyiv GTFS + district bbox |
| `route_count`           | Distinct routes serving stops in the district             | Kyiv GTFS                 |
| `trips_per_hour_proxy`  | Average scheduled trips per hour through district stops   | GTFS `stop_times`         |
| `mobility_stop_density` | `stop_count` / district area (km²)                        | `mart_mobility_proxy`     |

## Limitations

- Mobility metrics describe **scheduled public transport infrastructure**, not real-time traffic volume.
- PM2.5 is **estimated from AQI** when raw concentration is unavailable in the API snapshot.
