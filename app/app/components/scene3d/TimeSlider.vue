<script setup lang="ts">
const props = defineProps<{
  modelValue: string
  minDate: string
  maxDate: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const dates = computed(() => {
  const result: string[] = []
  const start = new Date(props.minDate)
  const end = new Date(props.maxDate)
  for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
    result.push(d.toISOString().slice(0, 10))
  }
  return result
})

const index = computed({
  get: () => dates.value.indexOf(props.modelValue.slice(0, 10)),
  set: (value: number) => {
    emit('update:modelValue', dates.value[value] ?? props.modelValue.slice(0, 10))
  },
})
</script>

<template>
  <div class="card">
    <div class="mb-2 flex items-center justify-between text-sm">
      <span class="text-slate-400">Timeline</span>
      <span class="font-medium text-emerald-400">{{ modelValue.slice(0, 10) }}</span>
    </div>
    <input
      v-model.number="index"
      type="range"
      min="0"
      :max="Math.max(0, dates.length - 1)"
      class="w-full accent-emerald-500"
    >
  </div>
</template>
