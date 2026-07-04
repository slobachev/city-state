<script setup lang="ts">
import type { DistrictDaily, DistrictGeo } from '~/types/analytics'
import KyivScene from '~/components/scene3d/KyivScene.vue'
import TimeSlider from '~/components/scene3d/TimeSlider.vue'

const { data: geo } = await useFetch<{ districts: DistrictGeo[] }>('/api/stations')
const { data: daily } = await useFetch<DistrictDaily[]>('/api/districts')

const dates = computed(() =>
  [...new Set((daily.value ?? []).map((r) => r.date.slice(0, 10)))].sort(),
)

const selectedDate = ref('')
watch(dates, (value) => {
  if (value.length && !selectedDate.value) {
    selectedDate.value = value.at(-1)!
  }
}, { immediate: true })

const hasDataForDate = computed(() => {
  if (!daily.value || !selectedDate.value) return false
  const target = selectedDate.value.slice(0, 10)
  return daily.value.some((row) => row.date.slice(0, 10) === target)
})
</script>

<template>
  <div class="space-y-6">
    <section class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <h2 class="text-2xl font-semibold">
          3D District Map
        </h2>
        <p class="mt-1 text-slate-400">
          Extruded district blocks show PM2.5 levels over time. Drag to orbit, scroll to zoom.
        </p>
      </div>
      <NuxtLink to="/explore" class="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800">
        Switch to 2D
      </NuxtLink>
    </section>

    <TimeSlider
      v-if="dates.length"
      v-model="selectedDate"
      :min-date="dates[0]"
      :max-date="dates.at(-1)!"
    />

    <KyivScene
      v-if="geo && daily && selectedDate && hasDataForDate"
      :districts="geo.districts"
      :daily-data="daily"
      :selected-date="selectedDate"
    />

    <div
      v-else-if="geo && daily && selectedDate && !hasDataForDate"
      class="card flex h-[480px] items-center justify-center text-sm text-slate-400"
    >
      No district data available for {{ selectedDate.slice(0, 10) }}.
    </div>
  </div>
</template>
