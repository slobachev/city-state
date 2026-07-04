import type { DistrictGeo } from '~/types/analytics'

export default defineEventHandler((): { districts: DistrictGeo[] } => {
  return readDataFile('districts_geo.json')
})
