<script setup lang="ts">
const props = defineProps<{
  districts: { slug: string; name: string }[]
  selectedDistrict: string
  dateFrom: string
  dateTo: string
}>()

const emit = defineEmits<{
  'update:selectedDistrict': [value: string]
  'update:dateFrom': [value: string]
  'update:dateTo': [value: string]
}>()
</script>

<template>
  <div class="card flex flex-wrap items-end gap-4">
    <div class="min-w-[180px] flex-1">
      <label class="mb-1 block text-xs uppercase tracking-wide text-slate-400">
        District
      </label>
      <select
        class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm"
        :value="selectedDistrict"
        @change="emit('update:selectedDistrict', ($event.target as HTMLSelectElement).value)"
      >
        <option value="">All districts</option>
        <option v-for="d in districts" :key="d.slug" :value="d.slug">
          {{ d.name }}
        </option>
      </select>
    </div>
    <div class="min-w-[160px] flex-1">
      <label class="mb-1 block text-xs uppercase tracking-wide text-slate-400">
        From
      </label>
      <input
        type="date"
        class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm"
        :value="dateFrom"
        @input="emit('update:dateFrom', ($event.target as HTMLInputElement).value)"
      >
    </div>
    <div class="min-w-[160px] flex-1">
      <label class="mb-1 block text-xs uppercase tracking-wide text-slate-400">
        To
      </label>
      <input
        type="date"
        class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm"
        :value="dateTo"
        @input="emit('update:dateTo', ($event.target as HTMLInputElement).value)"
      >
    </div>
  </div>
</template>
