<template>
  <div class="prose prose-invert max-w-none space-y-8">
    <section>
      <h2 class="text-2xl font-semibold text-white">
        Methodology
      </h2>
      <p class="text-slate-400">
        This dashboard answers: <em>Which Kyiv districts have the worst air quality,
        and is it related to weather or mobility infrastructure?</em>
      </p>
    </section>

    <section class="card space-y-4">
      <h3 class="text-lg font-medium text-emerald-400">
        Data Sources
      </h3>
      <ul class="list-disc space-y-2 pl-5 text-sm text-slate-300">
        <li>
          <strong>Air quality:</strong>
          <a href="https://www.saveecobot.com/en/maps/kyiv" target="_blank" rel="noopener" class="text-emerald-400 hover:underline">SaveEcoBot</a>
          — hourly AQI PM2.5 (US EPA NowCast) for Kyiv city and 10 districts.
        </li>
        <li>
          <strong>Weather:</strong>
          <a href="https://open-meteo.com/" target="_blank" rel="noopener" class="text-emerald-400 hover:underline">Open-Meteo</a>
          — historical temperature, humidity, wind, precipitation.
        </li>
        <li>
          <strong>Mobility proxy:</strong>
          <a href="https://data.gov.ua/" target="_blank" rel="noopener" class="text-emerald-400 hover:underline">Kyiv GTFS</a>
          (Kyivpastrans) — stop counts, routes, scheduled trip frequency.
        </li>
      </ul>
      <p class="text-xs text-slate-500">
        SaveEcoBot data is used under CC BY 4.0. Active link to
        <a href="https://www.saveecobot.com/" target="_blank" rel="noopener" class="text-emerald-400 hover:underline">saveecobot.com</a>
        is required.
      </p>
    </section>

    <section class="card space-y-4">
      <h3 class="text-lg font-medium">
        Pipeline Architecture
      </h3>
      <ol class="list-decimal space-y-2 pl-5 text-sm text-slate-300">
        <li>Python ingest: SaveEcoBot JSON + Open-Meteo + GTFS → DuckDB raw tables</li>
        <li>dbt-lite SQL transforms in <code>transform/</code> (staging → marts)</li>
        <li>Export aggregated JSON to <code>data/processed/</code></li>
        <li>Nuxt server API serves static aggregates (no runtime analytics)</li>
        <li>TresJS 3D scene visualizes district-level PM2.5 extrusions</li>
      </ol>
    </section>

    <section class="card space-y-4">
      <h3 class="text-lg font-medium">
        Limitations
      </h3>
      <ul class="list-disc space-y-2 pl-5 text-sm text-slate-300">
        <li><strong>Mobility ≠ traffic:</strong> GTFS reflects scheduled public transport, not road congestion.</li>
        <li><strong>Sensor heterogeneity:</strong> citizen vs official monitors vary in quality.</li>
        <li><strong>PM2.5 estimation:</strong> concentration derived from AQI when raw µg/m³ unavailable.</li>
        <li><strong>Correlation ≠ causation:</strong> weather affects dispersion but does not explain all variance.</li>
        <li><strong>Static snapshot:</strong> run <code>python pipeline/run_all.py</code> to refresh data.</li>
      </ul>
    </section>

    <section class="card">
      <h3 class="text-lg font-medium">
        Metrics Reference
      </h3>
      <p class="text-sm text-slate-400">
        See <code>docs/metrics.md</code> in the repository for full KPI definitions.
      </p>
    </section>
  </div>
</template>
