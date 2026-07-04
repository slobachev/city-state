import type { DistrictDaily } from '~/types/analytics'

export default defineEventHandler((event): DistrictDaily[] => {
  const query = getQuery(event)
  const rows = readDataFile<DistrictDaily[]>('districts_daily.json')

  const district = query.district as string | undefined
  const from = query.from as string | undefined
  const to = query.to as string | undefined

  return rows.filter((row) => {
    if (district && row.district_slug !== district) return false
    if (from && row.date < from) return false
    if (to && row.date > to) return false
    return true
  })
})
