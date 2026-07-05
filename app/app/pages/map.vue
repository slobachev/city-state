<script setup lang="ts">
import type { SaveEcoBotKyiv } from '~/types/saveecobot'
import { aqiColor, aqiLabel, formatDate } from '~/composables/useAirMetrics'

const MAP_EMBED_URL = 'https://www.saveecobot.com/en/maps#12/50.4501/30.5234'

const { data: kyiv, refresh, status } = await useFetch<SaveEcoBotKyiv>('/api/saveecobot/kyiv')

const aqiUpdated = computed(() => {
  const raw = kyiv.value?.aqi_updated_at
  if (!raw) return null
  return formatDate(raw)
})

function openFullMap() {
  window.open(kyiv.value?.link_maps_aqi ?? MAP_EMBED_URL, '_blank', 'noopener,noreferrer')
}
</script>

<template>
  <div class="space-y-6">
    <section class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <h2 class="text-2xl font-semibold">
          Kyiv Air Quality Map
        </h2>
        <p class="mt-1 max-w-2xl text-slate-400">
          Live monitoring map powered by
          <a
            href="https://www.saveecobot.com/"
            target="_blank"
            rel="noopener"
            class="text-emerald-400 hover:underline"
          >SaveEcoBot</a>.
          Data from 400+ citizen and official sensors across the city.
        </p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          type="button"
          class="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800"
          :disabled="status === 'pending'"
          @click="refresh()"
        >
          Refresh
        </button>
        <NuxtLink
          to="/explore"
          class="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800"
        >
          Switch to Charts
        </NuxtLink>
      </div>
    </section>

    <section
      v-if="kyiv"
      class="grid gap-4 sm:grid-cols-2 lg:grid-cols-5"
    >
      <div class="card">
        <p class="text-xs uppercase text-slate-400">
          AQI PM2.5
        </p>
        <p
          class="kpi-value"
          :style="{ color: aqiColor(kyiv.aqi) }"
        >
          {{ kyiv.aqi }}
        </p>
        <p class="text-xs text-slate-500">
          {{ aqiLabel(kyiv.aqi) }}
          <span v-if="kyiv.aqi_is_old" class="text-amber-400"> · stale</span>
        </p>
      </div>
      <div class="card">
        <p class="text-xs uppercase text-slate-400">
          Temperature
        </p>
        <p class="kpi-value">
          {{ kyiv.meteo.temperature.value }}°C
        </p>
      </div>
      <div class="card">
        <p class="text-xs uppercase text-slate-400">
          Humidity
        </p>
        <p class="kpi-value">
          {{ kyiv.meteo.humidity.value }}%
        </p>
      </div>
      <div class="card">
        <p class="text-xs uppercase text-slate-400">
          Wind
        </p>
        <p class="kpi-value">
          {{ kyiv.meteo.wind_power.value }} m/s
        </p>
        <p class="text-xs text-slate-500">
          {{ kyiv.meteo.wind_direction.value }}
        </p>
      </div>
      <div class="card">
        <p class="text-xs uppercase text-slate-400">
          Updated
        </p>
        <p class="text-sm font-medium text-slate-200">
          {{ aqiUpdated ?? '—' }}
        </p>
        <p class="mt-1 text-xs text-slate-500">
          NowCast (US EPA)
        </p>
      </div>
    </section>

    <div
      v-else-if="status === 'pending'"
      class="card flex h-24 items-center justify-center text-sm text-slate-400"
    >
      Loading SaveEcoBot data…
    </div>

    <div
      v-else
      class="card flex h-24 items-center justify-center text-sm text-red-400"
    >
      Could not load SaveEcoBot data. Try refreshing.
    </div>

    <div class="card overflow-hidden p-0">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 px-4 py-3">
        <p class="text-sm text-slate-400">
          City-wide average AQI PM2.5 (NowCast, US EPA)
        </p>
        <button
          type="button"
          class="text-sm text-emerald-400 hover:underline"
          @click="openFullMap"
        >
          Open full map ↗
        </button>
      </div>
      <iframe
        :src="MAP_EMBED_URL"
        title="SaveEcoBot Kyiv air quality map"
        class="block h-[min(70vh,720px)] w-full border-0 bg-slate-900"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        allow="geolocation"
      />
      <p class="border-t border-slate-800 px-4 py-2 text-xs text-slate-500">
        Map data ©
        <a
          href="https://www.saveecobot.com/"
          target="_blank"
          rel="noopener"
          class="text-emerald-400 hover:underline"
        >SaveEcoBot</a>
        ·
        <a
          :href="kyiv?.link ?? 'https://www.saveecobot.com/en/maps/kyiv'"
          target="_blank"
          rel="noopener"
          class="text-emerald-400 hover:underline"
        >Kyiv city page</a>
        · CC BY 4.0
      </p>
    </div>
  </div>
</template>
