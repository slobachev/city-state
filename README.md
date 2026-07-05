# Cities Urban Mobility & Air Quality Explorer

Data analytics project: interactive dashboard for cities air quality,
weather correlations, and public transport mobility proxy metrics.

**Business question:** Which city (currently Kyiv) districts have the worst air quality, and how
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
- [City GTFS](https://data.gov.ua/) — public transport schedules (mobility proxy)

## Data Freshness

| Layer              | Source                                  | Update frequency                 |
| ------------------ | --------------------------------------- | -------------------------------- |
| Live AQI & weather | SaveEcoBot API (`/api/saveecobot/kyiv`) | On page load / manual refresh    |
| Charts & rankings  | Python pipeline → `data/processed/`     | Daily (GitHub Actions cron)      |
| Mobility proxy     | City GTFS                               | Weekly or on manual pipeline run |

## Quick Start

### 1. Data Pipeline

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r pipeline/requirements.txt
python pipeline/run_all.py          # use cached SaveEcoBot data if available
python pipeline/run_all.py --refresh  # fetch fresh data from APIs
```

Charts and rankings in `data/processed/` are refreshed automatically once per day via GitHub Actions (`.github/workflows/refresh-data.yml`). Live AQI on the Overview and Map pages comes directly from SaveEcoBot at request time.

### 2. Dashboard

```bash
cd app
npm install
npm run dev
```

Open http://localhost:3000

### 3. AI Insights

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
