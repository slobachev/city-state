# Kyiv Urban Mobility & Air Quality Explorer

Portfolio data analytics project: interactive dashboard for Kyiv air quality,
weather correlations, and public transport mobility proxy metrics.

**Business question:** Which Kyiv districts have the worst air quality, and how
does it relate to weather conditions and urban mobility infrastructure?

## Stack

| Layer       | Technology                     |
| ----------- | ------------------------------ |
| Frontend    | Nuxt 4, Vue 3, Tailwind CSS    |
| Live Map    | SaveEcoBot embed               |
| Charts      | ECharts (vue-echarts)          |
| Analytics   | Python, DuckDB, SQL (dbt-lite) |
| AI Insights | OpenAI API (optional fallback) |

## Data Sources

- [SaveEcoBot](https://www.saveecobot.com/en/maps/kyiv) — air quality (CC BY 4.0)
- [Open-Meteo](https://open-meteo.com/) — historical weather
- [Kyiv GTFS](https://data.gov.ua/) — public transport schedules (mobility proxy)

## Quick Start

### 1. Data Pipeline

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r pipeline/requirements.txt
python pipeline/run_all.py
```

### 2. Dashboard

```bash
cd app
npm install
npm run dev
```

Open http://localhost:3000

### 3. AI Insights (optional)

```bash
# app/.env
NUXT_AI_API_KEY=sk-...
```

## Project Structure

```
├── pipeline/          # Python ETL + DuckDB export
├── transform/         # dbt-lite SQL models
├── data/processed/    # JSON aggregates for API
├── app/               # Nuxt dashboard
├── notebooks/         # EDA notebooks
└── docs/              # Metrics & data dictionary
```

## Key Findings (Apr–Jul 2026 snapshot)

1. **Sviatoshynskyi** has the highest average PM2.5 (~8.4 µg/m³)
2. **Holosiivskyi** reports the lowest levels (~4.5 µg/m³)
3. **Summer** averages higher PM2.5 than spring (7.4 vs 5.9 µg/m³)
4. **Negative correlation** with wind speed (r ≈ -0.23) suggests dispersion effects

## Pages

| Route          | Description                     |
| -------------- | ------------------------------- |
| `/`            | KPI overview and key findings   |
| `/explore`     | 2D charts with filters          |
| `/map`         | SaveEcoBot live air quality map |
| `/insights`    | AI-assisted summary             |
| `/methodology` | Data sources and limitations    |

## License

Code: MIT. SaveEcoBot data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
