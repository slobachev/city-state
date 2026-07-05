<script setup lang="ts">
const route = useRoute();
const config = useRuntimeConfig();

const links = [
    { to: '/', label: 'Overview' },
    { to: '/explore', label: 'Explore' },
    { to: '/map', label: 'Map' },
    { to: '/insights', label: 'AI Insights' },
    { to: '/methodology', label: 'Methodology' },
];

function isActive(path: string): boolean {
    return route.path === path;
}
</script>

<template>
    <div class="min-h-screen">
        <header class="border-b border-slate-800 bg-slate-950/90 backdrop-blur">
            <div class="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-4">
                <div>
                    <p class="text-xs uppercase tracking-widest text-emerald-500">Data Analytics Portfolio</p>
                    <h1 class="text-lg font-semibold">
                        {{ config.public.appName }}
                    </h1>
                </div>
                <nav class="flex flex-wrap gap-1">
                    <NuxtLink
                        v-for="link in links"
                        :key="link.to"
                        :to="link.to"
                        class="nav-link"
                        :class="{ 'nav-link-active': isActive(link.to) }"
                    >
                        {{ link.label }}
                    </NuxtLink>
                </nav>
            </div>
        </header>
        <main class="mx-auto max-w-7xl px-4 py-8">
            <NuxtPage />
        </main>
        <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
            Air quality data from
            <a
                href="https://www.saveecobot.com/"
                target="_blank"
                rel="noopener"
                class="text-emerald-400 hover:underline"
                >SaveEcoBot</a
            >. Built with Nuxt and DuckDB.
        </footer>
    </div>
</template>
