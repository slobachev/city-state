/** AQI PM2.5 color scale (US EPA categories). */
export function aqiColor(aqi: number): string {
  if (aqi <= 50) return '#22c55e'
  if (aqi <= 100) return '#eab308'
  if (aqi <= 150) return '#f97316'
  if (aqi <= 200) return '#ef4444'
  return '#a855f7'
}

export function aqiLabel(aqi: number): string {
  if (aqi <= 50) return 'Good'
  if (aqi <= 100) return 'Moderate'
  if (aqi <= 150) return 'Unhealthy for sensitive groups'
  if (aqi <= 200) return 'Unhealthy'
  if (aqi <= 300) return 'Very unhealthy'
  return 'Hazardous'
}

export function pm25Color(pm25: number): string {
  if (pm25 <= 12) return '#22c55e'
  if (pm25 <= 35.4) return '#eab308'
  if (pm25 <= 55.4) return '#f97316'
  if (pm25 <= 150.4) return '#ef4444'
  return '#a855f7'
}

export function formatDate(value: string): string {
  return new Date(value).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export function formatNumber(value: number, digits = 1): string {
  return value.toFixed(digits)
}
