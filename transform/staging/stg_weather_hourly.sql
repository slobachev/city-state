-- description: Clean hourly weather readings from Open-Meteo

CREATE OR REPLACE TABLE stg_weather_hourly AS
SELECT
    timestamp,
    temperature_c,
    humidity_pct,
    wind_speed_ms,
    precipitation_mm,
    CAST(timestamp AS DATE) AS date
FROM raw_weather_hourly;
