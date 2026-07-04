-- description: Clean GTFS stops assigned to Kyiv districts

CREATE OR REPLACE TABLE stg_mobility_stops AS
SELECT
    stop_id,
    stop_name,
    latitude,
    longitude,
    district_slug
FROM raw_mobility_stops
WHERE district_slug IS NOT NULL;
