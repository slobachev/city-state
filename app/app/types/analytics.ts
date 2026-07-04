export interface OverviewData {
  generated_at: string
  city: string
  kpis: {
    pm25_avg: number
    aqi_avg: number
    exceedance_rate: number
    period_start: string
    period_end: string
  }
  worst_districts: DistrictRank[]
  best_districts: DistrictRank[]
  seasonal: { season: string; pm25_avg: number }[]
  correlations: {
    pm25_wind: number
    pm25_humidity: number
    pm25_temperature: number
    sample_size: number
  }
  findings: string[]
}

export interface DistrictRank {
  district_slug: string
  district_name: string
  pm25_avg: number
  exceedance_rate: number
}

export interface DistrictDaily {
  date: string
  district_slug: string
  district_name: string
  pm25_avg: number
  aqi_avg: number
  exceedance_rate: number
  humidity_avg: number | null
  wind_avg: number | null
}

export interface DistrictGeo {
  slug: string
  name: string
  centroid: { lat: number; lon: number }
  bbox: {
    min_lat: number
    max_lat: number
    min_lon: number
    max_lon: number
  }
}

export interface TimeseriesPoint {
  timestamp: string
  pm25_ug_m3: number
  aqi_pm25: number
  humidity_pct: number | null
  wind_speed_ms: number | null
}

export interface MobilityProxy {
  district_slug: string
  stop_count: number
  route_count: number
  total_trips: number
  mobility_stop_density: number
  trips_per_hour_proxy: number
}

export interface InsightsResponse {
  summary: string
  findings: string[]
  limitations: string[]
  confidence: 'high' | 'medium' | 'low'
  source: 'llm' | 'template'
}
