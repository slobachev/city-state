import type { DistrictDaily } from '~/types/analytics'

export default defineEventHandler((event): DistrictDaily[] => {
  const query = getQuery(event)
  const rows = readDataFile<DistrictDaily[]>('districts_daily.json')

  const district = query.district as string | undefined
  const from = query.from as string | undefined
  const to = query.to as string | undefined

  return rows.filter((row) => {
    const rowDate = row.date.slice(0, 10)
    if (district && row.district_slug !== district) return false
    if (from && rowDate < from) return false
    if (to && rowDate > to) return false
    return true
  })
})
