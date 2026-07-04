<script setup lang="ts">
import { OrbitControls } from '@tresjs/cientos'
import type { DistrictDaily, DistrictGeo } from '~/types/analytics'
import DistrictExtrusion from '~/components/scene3d/DistrictExtrusion.vue'

const props = defineProps<{
  districts: DistrictGeo[]
  dailyData: DistrictDaily[]
  selectedDate: string
}>()
</script>

<template>
  <div class="card overflow-hidden p-0">
    <div class="border-b border-slate-800 px-5 py-3">
      <h3 class="text-sm font-medium text-slate-200">
        3D District PM2.5 — {{ selectedDate }}
      </h3>
      <p class="text-xs text-slate-500">
        Bar height = average PM2.5 (µg/m³). Color follows concentration scale.
      </p>
    </div>
    <div class="h-[480px] w-full">
      <TresCanvas clear-color="#0f172a">
        <TresPerspectiveCamera :position="[8, 10, 12]" :look-at="[0, 0, 0]" />
        <OrbitControls make-default />
        <TresAmbientLight :intensity="0.6" />
        <TresDirectionalLight :position="[5, 10, 5]" :intensity="1.2" />
        <Suspense>
          <DistrictExtrusion
            :districts="districts"
            :daily-data="dailyData"
            :selected-date="selectedDate"
          />
        </Suspense>
      </TresCanvas>
    </div>
  </div>
</template>
