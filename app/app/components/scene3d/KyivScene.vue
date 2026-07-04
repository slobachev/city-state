<script setup lang="ts">
import { OrbitControls } from '@tresjs/cientos'
import type { DistrictDaily, DistrictGeo } from '~/types/analytics'
import DistrictExtrusion from '~/components/scene3d/DistrictExtrusion.vue'
import { useGeoProjection } from '~/composables/useGeoProjection'

const props = defineProps<{
  districts: DistrictGeo[]
  dailyData: DistrictDaily[]
  selectedDate: string
}>()

const { sceneCenter } = useGeoProjection()
const center = computed(() => sceneCenter(props.districts))
const sceneOffset = computed(() => [-center.value[0], 0, -center.value[2]] as [number, number, number])
</script>

<template>
  <div class="card overflow-hidden p-0">
    <div class="border-b border-slate-800 px-5 py-3">
      <h3 class="text-sm font-medium text-slate-200">
        3D District PM2.5 — {{ selectedDate.slice(0, 10) }}
      </h3>
      <p class="text-xs text-slate-500">
        Bar height = average PM2.5 (µg/m³). Color follows concentration scale.
      </p>
    </div>

    <ClientOnly>
      <div class="relative h-[480px] w-full bg-slate-950">
        <TresCanvas
          clear-color="#0f172a"
          class="h-full w-full"
        >
          <TresPerspectiveCamera
            make-default
            :position="[0, 14, 18]"
            :fov="50"
            :near="0.1"
            :far="500"
          />
          <OrbitControls
            :target="[0, 2, 0]"
            :enable-damping="true"
            :damping-factor="0.08"
          />
          <TresAmbientLight :intensity="0.7" />
          <TresDirectionalLight :position="[8, 16, 10]" :intensity="1.4" />
          <TresDirectionalLight :position="[-6, 8, -4]" :intensity="0.4" />

          <TresGroup :position="sceneOffset">
            <DistrictExtrusion
              :districts="districts"
              :daily-data="dailyData"
              :selected-date="selectedDate"
            />
          </TresGroup>
        </TresCanvas>
      </div>

      <template #fallback>
        <div class="flex h-[480px] items-center justify-center bg-slate-950 text-sm text-slate-400">
          Loading 3D scene…
        </div>
      </template>
    </ClientOnly>
  </div>
</template>

<style scoped>
:deep(canvas) {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>
