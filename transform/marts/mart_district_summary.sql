-- description: District-level summary statistics for the full dataset period

CREATE OR REPLACE TABLE mart_district_summary AS
SELECT
    district_slug,
    district_name,
    AVG(pm25_avg) AS pm25_avg,
    AVG(aqi_avg) AS aqi_avg,
    AVG(exceedance_rate) AS exceedance_rate,
    MAX(pm25_max) AS pm25_peak,
    COUNT(DISTINCT date) AS days_observed
FROM mart_district_daily
GROUP BY district_slug, district_name;
