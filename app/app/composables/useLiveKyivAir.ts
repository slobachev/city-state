import type { SaveEcoBotCity } from '~/types/saveecobot';

/** Live SaveEcoBot city snapshot (AQI, meteo). Refreshed on each fetch / manual refresh. */
export function useLiveCityAir({ city = 'kyiv' }: { city?: string }) {
    return useFetch<SaveEcoBotCity>(`/api/saveecobot/${city}`);
}
