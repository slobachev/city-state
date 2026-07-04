// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@tresjs/nuxt'],
  css: ['~/assets/css/main.css'],
  tres: {
    devtools: true,
  },
  runtimeConfig: {
    aiApiKey: process.env.NUXT_AI_API_KEY || '',
    aiModel: process.env.NUXT_AI_MODEL || 'gpt-4o-mini',
    public: {
      appName: 'Kyiv Air & Mobility Explorer',
    },
  },
  app: {
    head: {
      title: 'Kyiv Air & Mobility Explorer',
      meta: [
        {
          name: 'description',
          content:
            'Urban air quality and mobility analytics dashboard for Kyiv, Ukraine.',
        },
      ],
    },
  },
})
