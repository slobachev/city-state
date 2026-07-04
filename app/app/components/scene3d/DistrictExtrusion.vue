<script setup lang="ts">
import type { DistrictDaily, DistrictGeo } from '~/types/analytics'
import { pm25Color } from '~/composables/useAirMetrics'
import { useGeoProjection } from '~/composables/useGeoProjection'

const props = defineProps<{
  districts: DistrictGeo[]
  dailyData: DistrictDaily[]
  selectedDate: string
}>()

const { bboxSize } = useGeoProjection()

const districtMetrics = computed(() => {
  const map = new Map<string, DistrictDaily>()
  for (const row of props.dailyData) {
    if (row.date === props.selectedDate) {
      map.set(row.district_slug, row)
    }
  }
  return map
})

function barHeight(pm25: number): number {
  return Math.max(0.3, pm25 / 4)
}
</script>

<template>
  <TresGroup>
    <TresMesh :rotation="[-Math.PI / 2, 0, 0]" :position="[0, -0.05, 0]">
      <TresPlaneGeometry :args="[12, 12]" />
      <TresMeshStandardMaterial color="#1e293b" />
    </TresMesh>

    <TresGroup v-for="district in districts" :key="district.slug">
      <TresMesh
        v-if="districtMetrics.get(district.slug)"
        :position="[
          bboxSize(district.bbox).center[0],
          barHeight(districtMetrics.get(district.slug)!.pm25_avg) / 2,
          bboxSize(district.bbox).center[1],
        ]"
      >
        <TresBoxGeometry
          :args="[
            Math.max(0.5, bboxSize(district.bbox).width * 0.8),
            barHeight(districtMetrics.get(district.slug)!.pm25_avg),
            Math.max(0.5, bboxSize(district.bbox).depth * 0.8),
          ]"
        />
        <TresMeshStandardMaterial
          :color="pm25Color(districtMetrics.get(district.slug)!.pm25_avg)"
          :emissive="pm25Color(districtMetrics.get(district.slug)!.pm25_avg)"
          :emissive-intensity="0.25"
        />
      </TresMesh>
    </TresGroup>
  </TresGroup>
</template>
