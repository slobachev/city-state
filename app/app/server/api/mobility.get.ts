import type { MobilityProxy } from '~/types/analytics'

export default defineEventHandler((): MobilityProxy[] => {
  return readDataFile<MobilityProxy[]>('mobility_proxy.json')
})
