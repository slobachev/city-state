-- description: Daily air quality metrics aggregated by district

CREATE OR REPLACE TABLE mart_district_daily AS
SELECT
    date,
    entity_slug AS district_slug,
    entity_name AS district_name,
    AVG(pm25_ug_m3) AS pm25_avg,
    AVG(aqi_pm25) AS aqi_avg,
    MAX(pm25_ug_m3) AS pm25_max,
    MIN(pm25_ug_m3) AS pm25_min,
    AVG(humidity_pct) AS humidity_avg,
    AVG(wind_speed_ms) AS wind_avg,
    100.0 * AVG(CASE WHEN pm25_ug_m3 > 15.0 THEN 1.0 ELSE 0.0 END) AS exceedance_rate,
    COUNT(*) AS reading_count
FROM stg_air_hourly
WHERE entity_type = 'district'
GROUP BY date, entity_slug, entity_name;
