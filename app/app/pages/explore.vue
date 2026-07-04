<script setup lang="ts">
import type { DistrictDaily, MobilityProxy } from '~/types/analytics'
import ChartPanel from '~/components/charts/ChartPanel.vue'
import FilterBar from '~/components/filters/FilterBar.vue'
import { pm25Color } from '~/composables/useAirMetrics'

const { data: geo } = await useFetch<{ districts: { slug: string; name: string }[] }>('/api/stations')
const { data: mobility } = await useFetch<MobilityProxy[]>('/api/mobility')

const selectedDistrict = ref('')
const dateFrom = ref('2026-04-05')
const dateTo = ref('2026-07-04')

const query = computed(() => ({
  district: selectedDistrict.value || undefined,
  from: dateFrom.value || undefined,
  to: dateTo.value || undefined,
}))

const { data: daily, refresh } = await useFetch<DistrictDaily[]>('/api/districts', {
  query,
  watch: [query],
})

watch(query, () => refresh())

const lineOption = computed(() => {
  const rows = daily.value ?? []
  const dates = [...new Set(rows.map((r) => r.date))].sort()
  const districts = [...new Set(rows.map((r) => r.district_name))]

  return {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    legend: { textStyle: { color: '#94a3b8' }, type: 'scroll' },
    grid: { left: 40, right: 20, top: 40, bottom: 30 },
    xAxis: { type: 'category', data: dates, axisLabel: { color: '#94a3b8' } },
    yAxis: { type: 'value', name: 'PM2.5 µg/m³', axisLabel: { color: '#94a3b8' } },
    series: districts.map((name) => ({
      name,
      type: 'line',
      smooth: true,
      showSymbol: false,
      data: dates.map((date) => {
        const row = rows.find((r) => r.date === date && r.district_name === name)
        return row?.pm25_avg ?? null
      }),
    })),
  }
})

const barOption = computed(() => {
  const rows = daily.value ?? []
  const latestDate = rows.at(-1)?.date
  const latest = rows.filter((r) => r.date === latestDate)
  return {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 20, top: 20, bottom: 60 },
    xAxis: {
      type: 'category',
      data: latest.map((r) => r.district_name),
      axisLabel: { color: '#94a3b8', rotate: 30 },
    },
    yAxis: { type: 'value', axisLabel: { color: '#94a3b8' } },
    series: [
      {
        type: 'bar',
        data: latest.map((r) => ({
          value: r.pm25_avg,
          itemStyle: { color: pm25Color(r.pm25_avg) },
        })),
      },
    ],
  }
})

const scatterOption = computed(() => {
  const mob = mobility.value ?? []
  const rows = daily.value ?? []
  const avgByDistrict = new Map<string, number>()
  for (const row of rows) {
    const current = avgByDistrict.get(row.district_slug) ?? 0
    avgByDistrict.set(row.district_slug, current + row.pm25_avg)
  }
  for (const [slug, total] of avgByDistrict) {
    const count = rows.filter((r) => r.district_slug === slug).length || 1
    avgByDistrict.set(slug, total / count)
  }

  return {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item' },
    xAxis: { name: 'Stop density', axisLabel: { color: '#94a3b8' } },
    yAxis: { name: 'Avg PM2.5', axisLabel: { color: '#94a3b8' } },
    series: [
      {
        type: 'scatter',
        symbolSize: 14,
        data: mob.map((m) => [
          m.mobility_stop_density,
          avgByDistrict.get(m.district_slug) ?? 0,
          m.district_slug,
        ]),
        itemStyle: { color: '#34d399' },
      },
    ],
  }
})
</script>

<template>
  <div class="space-y-6">
    <section>
      <h2 class="text-2xl font-semibold">
        Explore
      </h2>
      <p class="mt-1 text-slate-400">
        Filter districts and date ranges to drill into PM2.5 trends and mobility proxy relationships.
      </p>
    </section>

    <FilterBar
      v-if="geo"
      :districts="geo.districts"
      :selected-district="selectedDistrict"
      :date-from="dateFrom"
      :date-to="dateTo"
      @update:selected-district="selectedDistrict = $event"
      @update:date-from="dateFrom = $event"
      @update:date-to="dateTo = $event"
    />

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="card">
        <h3 class="mb-3 font-medium">
          PM2.5 Time Series
        </h3>
        <ChartPanel :option="lineOption" />
      </div>
      <div class="card">
        <h3 class="mb-3 font-medium">
          Latest District Comparison
        </h3>
        <ChartPanel :option="barOption" />
      </div>
    </div>

    <div class="card">
      <h3 class="mb-1 font-medium">
        Mobility Proxy vs PM2.5
      </h3>
      <p class="mb-3 text-xs text-slate-500">
        Stop density (stops/km²) vs average PM2.5 — infrastructure proxy, not causation.
      </p>
      <ChartPanel :option="scatterOption" height="360px" />
    </div>

    <div class="flex gap-3">
      <NuxtLink to="/map-3d" class="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800">
        Switch to 3D Map
      </NuxtLink>
      <NuxtLink to="/insights" class="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium hover:bg-emerald-500">
        Generate AI Summary
      </NuxtLink>
    </div>
  </div>
</template>
