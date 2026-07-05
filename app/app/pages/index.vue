<script setup lang="ts">
import type { OverviewData } from '~/types/analytics';
import {
    aqiColor,
    aqiLabel,
    formatDate,
    formatDateTime,
    formatNumber,
    pm25Color,
} from '~/composables/useAirMetrics';

const { data: overview } = await useFetch<OverviewData>('/api/overview');
const { data: city, refresh: refreshLive, status: liveStatus } = await useLiveCityAir({ city: 'kyiv' });

const liveUpdated = computed(() => {
    const raw = city.value?.aqi_updated_at;
    return raw ? formatDateTime(raw) : null;
});
</script>

<template>
    <div v-if="overview" class="space-y-8">
        <section>
            <h2 class="text-2xl font-semibold">Kyiv Air Quality Overview</h2>
            <p class="mt-2 max-w-3xl text-slate-400">
                Which districts have the worst air quality, and how do weather and mobility infrastructure
                relate to pollution patterns?
            </p>
        </section>

        <!-- Live layer -->
        <section class="space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-3">
                <div>
                    <h3 class="text-sm font-medium uppercase tracking-wide text-emerald-400">Live Now</h3>
                    <p class="text-xs text-slate-500">City-wide average from SaveEcoBot sensor network</p>
                </div>
                <button
                    type="button"
                    class="rounded-lg border border-slate-700 px-3 py-1.5 text-xs hover:bg-slate-800"
                    :disabled="liveStatus === 'pending'"
                    @click="refreshLive()"
                >
                    Refresh
                </button>
            </div>

            <div v-if="city" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div class="card border-emerald-900/40">
                    <p class="text-xs uppercase text-slate-400">AQI PM2.5</p>
                    <p class="kpi-value" :style="{ color: aqiColor(city.aqi) }">
                        {{ city.aqi }}
                    </p>
                    <p class="text-xs text-slate-500">
                        {{ aqiLabel(city.aqi) }}
                        <span v-if="city.aqi_is_old" class="text-amber-400"> · stale</span>
                    </p>
                </div>
                <div class="card border-emerald-900/40">
                    <p class="text-xs uppercase text-slate-400">Temperature</p>
                    <p class="kpi-value">{{ city.meteo.temperature.value }}°C</p>
                </div>
                <div class="card border-emerald-900/40">
                    <p class="text-xs uppercase text-slate-400">Humidity</p>
                    <p class="kpi-value">{{ city.meteo.humidity.value }}%</p>
                </div>
                <div class="card border-emerald-900/40">
                    <p class="text-xs uppercase text-slate-400">Updated</p>
                    <p class="mt-2 text-sm text-slate-200">{{ liveUpdated ?? '—' }}</p>
                    <p class="text-xs text-slate-500">NowCast (US EPA)</p>
                </div>
            </div>

            <div
                v-else-if="liveStatus === 'pending'"
                class="card flex h-20 items-center justify-center text-sm text-slate-400"
            >
                Loading live data…
            </div>
        </section>

        <!-- Batch analytics layer -->
        <section class="space-y-3">
            <div>
                <h3 class="text-sm font-medium uppercase tracking-wide text-slate-400">
                    Historical Analytics
                </h3>
                <p class="text-xs text-slate-500">
                    Charts and rankings updated daily
                    <span v-if="overview.generated_at">
                        · last batch {{ formatDateTime(overview.generated_at) }}
                    </span>
                </p>
            </div>

            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <div class="card">
                    <p class="text-xs uppercase text-slate-400">Avg PM2.5</p>
                    <p class="kpi-value">
                        {{ formatNumber(overview.kpis.pm25_avg) }}
                    </p>
                    <p class="text-xs text-slate-500">µg/m³ over period</p>
                </div>
                <div class="card">
                    <p class="text-xs uppercase text-slate-400">Avg AQI PM2.5</p>
                    <p class="kpi-value">
                        {{ formatNumber(overview.kpis.aqi_avg, 0) }}
                    </p>
                </div>
                <div class="card">
                    <p class="text-xs uppercase text-slate-400">WHO Exceedance</p>
                    <p class="kpi-value">{{ formatNumber(overview.kpis.exceedance_rate) }}%</p>
                    <p class="text-xs text-slate-500">hours &gt; 15 µg/m³</p>
                </div>
                <div class="card">
                    <p class="text-xs uppercase text-slate-400">Period</p>
                    <p class="mt-2 text-sm text-slate-200">
                        {{ formatDate(overview.kpis.period_start) }}
                        —
                        {{ formatDate(overview.kpis.period_end) }}
                    </p>
                </div>
            </div>
        </section>

        <section class="grid gap-6 lg:grid-cols-2">
            <div class="card">
                <h3 class="mb-4 font-medium text-red-400">Highest PM2.5 Districts</h3>
                <ul class="space-y-3">
                    <li
                        v-for="d in overview.worst_districts"
                        :key="d.district_slug"
                        class="flex items-center justify-between text-sm"
                    >
                        <span>{{ d.district_name }}</span>
                        <span :style="{ color: pm25Color(d.pm25_avg) }">
                            {{ formatNumber(d.pm25_avg) }} µg/m³
                        </span>
                    </li>
                </ul>
            </div>
            <div class="card">
                <h3 class="mb-4 font-medium text-emerald-400">Key Findings</h3>
                <ul class="space-y-2 text-sm text-slate-300">
                    <li v-for="(finding, i) in overview.findings" :key="i" class="flex gap-2">
                        <span class="text-emerald-500">•</span>
                        <span>{{ finding }}</span>
                    </li>
                </ul>
            </div>
        </section>

        <section class="card">
            <h3 class="mb-4 font-medium">Weather Correlations (City Level)</h3>
            <div class="grid gap-4 sm:grid-cols-3 text-sm">
                <div>
                    <p class="text-slate-400">PM2.5 vs Wind</p>
                    <p class="text-xl font-semibold">r = {{ overview.correlations.pm25_wind }}</p>
                </div>
                <div>
                    <p class="text-slate-400">PM2.5 vs Humidity</p>
                    <p class="text-xl font-semibold">r = {{ overview.correlations.pm25_humidity }}</p>
                </div>
                <div>
                    <p class="text-slate-400">Sample Size</p>
                    <p class="text-xl font-semibold">
                        {{ overview.correlations.sample_size.toLocaleString() }} hrs
                    </p>
                </div>
            </div>
        </section>

        <section class="flex flex-wrap gap-3">
            <NuxtLink
                to="/explore"
                class="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium hover:bg-emerald-500"
            >
                Explore Data
            </NuxtLink>
            <NuxtLink
                to="/map"
                class="rounded-lg border border-slate-700 px-4 py-2 text-sm hover:bg-slate-800"
            >
                Open Live Map
            </NuxtLink>
        </section>
    </div>
</template>
