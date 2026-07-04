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

function normalizeDate(value: string): string {
  return value.slice(0, 10)
}

const districtMeshes = computed(() => {
  const target = normalizeDate(props.selectedDate)
  const result: {
    slug: string
    name: string
    pm25: number
    position: [number, number, number]
    size: [number, number, number]
    color: string
  }[] = []

  for (const district of props.districts) {
    const metric = props.dailyData.find(
      (row) => row.district_slug === district.slug && normalizeDate(row.date) === target,
    )
    if (!metric) continue

    const size = bboxSize(district.bbox)
    const height = Math.max(0.5, metric.pm25_avg / 1.5)
    const color = pm25Color(metric.pm25_avg)

    result.push({
      slug: district.slug,
      name: district.name,
      pm25: metric.pm25_avg,
      position: [size.center[0], height / 2, size.center[1]],
      size: [
        Math.max(0.7, size.width * 0.85),
        height,
        Math.max(0.7, size.depth * 0.85),
      ],
      color,
    })
  }

  return result
})
</script>

<template>
  <TresGroup>
    <!-- Ground plane -->
    <TresMesh :rotation="[-Math.PI / 2, 0, 0]" :position="[0, -0.01, 0]">
      <TresPlaneGeometry :args="[16, 16]" />
      <TresMeshStandardMaterial color="#334155" />
    </TresMesh>

    <!-- District bars -->
    <TresMesh
      v-for="mesh in districtMeshes"
      :key="mesh.slug"
      :position="mesh.position"
    >
      <TresBoxGeometry :args="mesh.size" />
      <TresMeshStandardMaterial :color="mesh.color" />
    </TresMesh>
  </TresGroup>
</template>
