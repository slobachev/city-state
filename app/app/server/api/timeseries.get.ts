import type { TimeseriesPoint } from '~/types/analytics'

export default defineEventHandler((): TimeseriesPoint[] => {
  return readDataFile<TimeseriesPoint[]>('timeseries_hourly.json')
})
