-- description: Mobility infrastructure proxy metrics per district

CREATE OR REPLACE TABLE mart_mobility_proxy AS
WITH stop_stats AS (
    SELECT
        district_slug,
        COUNT(DISTINCT stop_id) AS stop_count,
        COUNT(DISTINCT route_id) AS route_count,
        SUM(trip_count) AS total_trips
    FROM raw_mobility_trips
    GROUP BY district_slug
),
district_area AS (
    SELECT district_slug, 25.0 AS area_km2
    FROM stg_mobility_stops
    GROUP BY district_slug
)
SELECT
    s.district_slug,
    s.stop_count,
    s.route_count,
    s.total_trips,
    ROUND(s.stop_count / d.area_km2, 2) AS mobility_stop_density,
    ROUND(s.total_trips / 365.0 / 18.0, 2) AS trips_per_hour_proxy
FROM stop_stats s
JOIN district_area d ON s.district_slug = d.district_slug;
