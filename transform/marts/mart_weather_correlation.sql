-- description: Pearson correlation between PM2.5 and weather variables (city level)

CREATE OR REPLACE TABLE mart_weather_correlation AS
SELECT
    corr(s.pm25_ug_m3, COALESCE(s.wind_speed_ms, w.wind_speed_ms)) AS corr_pm25_wind,
    corr(s.pm25_ug_m3, COALESCE(s.humidity_pct, w.humidity_pct)) AS corr_pm25_humidity,
    corr(s.pm25_ug_m3, w.temperature_c) AS corr_pm25_temperature,
    COUNT(*) AS sample_size
FROM stg_air_hourly s
JOIN stg_weather_hourly w ON s.timestamp = w.timestamp
WHERE s.entity_type = 'city';
