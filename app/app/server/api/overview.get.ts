import type { OverviewData } from '~/types/analytics'

export default defineEventHandler((): OverviewData => {
  return readDataFile<OverviewData>('overview.json')
})
