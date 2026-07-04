<script setup lang="ts">
import type { InsightsResponse } from '~/types/analytics'

const district = ref('')
const loading = ref(false)
const result = ref<InsightsResponse | null>(null)
const error = ref('')

async function generateInsights() {
  loading.value = true
  error.value = ''
  try {
    result.value = await $fetch<InsightsResponse>('/api/insights', {
      method: 'POST',
      body: { district: district.value || undefined },
    })
  } catch (e) {
    error.value = 'Failed to generate insights.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <section>
      <h2 class="text-2xl font-semibold">
        AI-Assisted Insights
      </h2>
      <p class="mt-1 max-w-2xl text-slate-400">
        Generates a narrative summary from pre-aggregated metrics. Set
        <code class="text-emerald-400">NUXT_AI_API_KEY</code> for LLM-powered insights;
        otherwise template-based fallback is used.
      </p>
    </section>

    <div class="card flex flex-wrap items-end gap-4">
      <div class="min-w-[200px]">
        <label class="mb-1 block text-xs uppercase text-slate-400">Optional district filter</label>
        <input
          v-model="district"
          type="text"
          placeholder="e.g. podilskyi"
          class="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm"
        >
      </div>
      <button
        class="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium hover:bg-emerald-500 disabled:opacity-50"
        :disabled="loading"
        @click="generateInsights"
      >
        {{ loading ? 'Generating…' : 'Generate Summary' }}
      </button>
    </div>

    <p v-if="error" class="text-sm text-red-400">
      {{ error }}
    </p>

    <div v-if="result" class="space-y-4">
      <div class="card">
        <div class="mb-2 flex items-center gap-2">
          <span
            class="rounded-full px-2 py-0.5 text-xs"
            :class="result.source === 'llm' ? 'bg-emerald-900 text-emerald-300' : 'bg-slate-800 text-slate-400'"
          >
            {{ result.source === 'llm' ? 'LLM' : 'Template' }}
          </span>
          <span class="text-xs text-slate-500">Confidence: {{ result.confidence }}</span>
        </div>
        <p class="text-slate-200">
          {{ result.summary }}
        </p>
      </div>

      <div class="card">
        <h3 class="mb-3 font-medium">
          Findings
        </h3>
        <ul class="space-y-2 text-sm text-slate-300">
          <li v-for="(item, i) in result.findings" :key="i">
            • {{ item }}
          </li>
        </ul>
      </div>

      <div class="card">
        <h3 class="mb-3 font-medium text-amber-400">
          Limitations
        </h3>
        <ul class="space-y-2 text-sm text-slate-400">
          <li v-for="(item, i) in result.limitations" :key="i">
            • {{ item }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
