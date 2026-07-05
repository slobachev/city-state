import type { InsightsResponse } from '~/types/analytics'

interface InsightsBody {
  district?: string
  dateFrom?: string
  dateTo?: string
}

export default defineEventHandler(async (event): Promise<InsightsResponse> => {
  const body = await readBody<InsightsBody>(event)
  const config = useRuntimeConfig()
  const context = readDataFile<{
    overview: {
      kpis: Record<string, unknown>
      findings: string[]
      correlations: Record<string, number>
      worst_districts: { district_name: string; pm25_avg: number }[]
    }
    districts: {
      district_slug: string
      district_name: string
      pm25_avg: number
      exceedance_rate: number
      mobility_stop_density: number | null
    }[]
  }>('insights_context.json')

  const filteredDistricts = body.district
    ? context.districts.filter((d) => d.district_slug === body.district)
    : context.districts

  const promptContext = {
    city: 'Kyiv',
    period: context.overview.kpis,
    filter: {
      district: body.district ?? 'all',
      dateFrom: body.dateFrom,
      dateTo: body.dateTo,
    },
    kpis: context.overview.kpis,
    correlations: context.overview.correlations,
    topDistricts: filteredDistricts.slice(0, 5),
    existingFindings: context.overview.findings,
  }

  if (config.aiApiKey) {
    try {
      const response = await $fetch<{
        choices: { message: { content: string } }[]
      }>('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${config.aiApiKey}`,
          'Content-Type': 'application/json',
        },
        body: {
          model: config.aiModel,
          temperature: 0.3,
          response_format: { type: 'json_object' },
          messages: [
            {
              role: 'system',
              content:
                'You are a data analyst assistant. Respond ONLY with valid JSON: {"summary":"...","findings":["..."],"limitations":["..."],"confidence":"high|medium|low"}. Use only the provided aggregates. Note correlation is not causation.',
            },
            {
              role: 'user',
              content: `Analyze this Kyiv air quality data snapshot:\n${JSON.stringify(promptContext, null, 2)}`,
            },
          ],
        },
      })

      const parsed = JSON.parse(response.choices[0].message.content)
      return {
        summary: parsed.summary,
        findings: parsed.findings ?? [],
        limitations: parsed.limitations ?? [],
        confidence: parsed.confidence ?? 'medium',
        source: 'llm',
      }
    } catch {
      // Fall through to template insights
    }
  }

  return buildTemplateInsights(context, body.district)
})

function buildTemplateInsights(
  context: {
    overview: {
      kpis: { pm25_avg: number; exceedance_rate: number; period_start: string; period_end: string }
      findings: string[]
      correlations: { pm25_wind: number; pm25_humidity: number }
    }
    districts: { district_name: string; pm25_avg: number; mobility_stop_density: number | null }[]
  },
  district?: string,
): InsightsResponse {
  const top = context.districts[0]
  const wind = context.overview.correlations.pm25_wind

  return {
    summary: district
      ? `Analysis for filtered district snapshot shows average PM2.5 of ${context.overview.kpis.pm25_avg.toFixed(1)} µg/m³ across Kyiv with localized patterns in ${top?.district_name ?? 'selected area'}.`
      : `Kyiv air quality from ${context.overview.kpis.period_start.slice(0, 10)} to ${context.overview.kpis.period_end.slice(0, 10)} averages ${context.overview.kpis.pm25_avg.toFixed(1)} µg/m³ PM2.5 with ${context.overview.kpis.exceedance_rate.toFixed(1)}% hours above WHO guideline.`,
    findings: context.overview.findings.slice(0, 4),
    limitations: [
      'Mobility metrics reflect scheduled public transport infrastructure, not real-time traffic.',
      'PM2.5 is estimated from AQI where raw concentration is unavailable.',
      'Correlation does not imply causation.',
      'Historical charts and rankings are refreshed once per day via automated pipeline.',
    ],
    confidence: 'medium',
    source: 'template',
  }
}
