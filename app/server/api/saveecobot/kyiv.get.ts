import type { SaveEcoBotKyiv } from '~/types/saveecobot'

export default defineEventHandler(async () => {
  return await $fetch<SaveEcoBotKyiv>('https://www.saveecobot.com/en/maps/kyiv.json')
})
