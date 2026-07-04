<script setup lang="ts">
import type { DistrictDaily, DistrictGeo } from '~/types/analytics'
import KyivScene from '~/components/scene3d/KyivScene.vue'
import TimeSlider from '~/components/scene3d/TimeSlider.vue'

const { data: geo } = await useFetch<{ districts: DistrictGeo[] }>('/api/stations')
const { data: daily } = await useFetch<DistrictDaily[]>('/api/districts')

const dates = computed(() =>
  [...new Set((daily.value ?? []).map((r) => r.date))].sort(),
)

const selectedDate = ref('')
watch(dates, (value) => {
  if (value.length && !selectedDate.value) {
    selectedDate.value = value.at(-1)!
  }
}, { immediate: true })
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
      v-if="geo && daily && selectedDate"
      :districts="geo.districts"
      :daily-data="daily"
      :selected-date="selectedDate"
    />
  </div>
</template>
