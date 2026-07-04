<script setup lang="ts">
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, ScatterChart } from 'echarts/charts'
import {
  GridComponent,
  LegendComponent,
  TooltipComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer,
  LineChart,
  BarChart,
  ScatterChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
])

defineProps<{
  option: Record<string, unknown>
  height?: string
}>()
</script>

<template>
  <ClientOnly>
    <VChart
      :option="option"
      autoresize
      :style="{ height: height || '320px', width: '100%' }"
    />
  </ClientOnly>
</template>
