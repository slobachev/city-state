-- description: Clean hourly air quality readings with PM2.5 estimation from AQI

CREATE OR REPLACE TABLE stg_air_hourly AS
SELECT
    timestamp,
    entity_type,
    entity_id,
    entity_slug,
    entity_name,
    aqi_pm25,
    humidity_pct,
    wind_speed_ms,
    CASE
        WHEN aqi_pm25 <= 50 THEN aqi_pm25 * 12.0 / 50.0
        WHEN aqi_pm25 <= 100 THEN (aqi_pm25 - 51) * (35.4 - 12.1) / 49.0 + 12.1
        WHEN aqi_pm25 <= 150 THEN (aqi_pm25 - 101) * (55.4 - 35.5) / 49.0 + 35.5
        WHEN aqi_pm25 <= 200 THEN (aqi_pm25 - 151) * (150.4 - 55.5) / 49.0 + 55.5
        WHEN aqi_pm25 <= 300 THEN (aqi_pm25 - 201) * (250.4 - 150.5) / 99.0 + 150.5
        ELSE (aqi_pm25 - 301) * (350.4 - 250.5) / 99.0 + 250.5
    END AS pm25_ug_m3,
    CAST(timestamp AS DATE) AS date
FROM raw_air_hourly
WHERE aqi_pm25 IS NOT NULL;
