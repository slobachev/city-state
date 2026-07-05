import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const geo = JSON.parse(
  fs.readFileSync(path.join(ROOT, 'data/raw/kyiv_districts.geojson'), 'utf8'),
)

const NAME_TO_SLUG = {
  '\u0413\u043e\u043b\u043e\u0441\u0456\u0457\u0432\u0441\u044c\u043a\u0438\u0439': 'holosiivskyi',
  '\u0414\u0430\u0440\u043d\u0438\u0446\u044c\u043a\u0438\u0439': 'darnytskyi',
  '\u0414\u0435\u0441\u043d\u044f\u043d\u0441\u044c\u043a\u0438\u0439': 'desnianskyi',
  '\u0414\u043d\u0456\u043f\u0440\u043e\u0432\u0441\u044c\u043a\u0438\u0439': 'dniprovskyi',
  '\u041e\u0431\u043e\u043b\u043e\u043d\u0441\u044c\u043a\u0438\u0439': 'obolonskyi',
  '\u041f\u0435\u0447\u0435\u0440\u0441\u044c\u043a\u0438\u0439': 'pecherskyi',
  '\u041f\u043e\u0434\u0456\u043b\u044c\u0441\u044c\u043a\u0438\u0439': 'podilskyi',
  '\u0421\u0432\u044f\u0442\u043e\u0448\u0438\u043d\u0441\u044c\u043a\u0438\u0439': 'sviatoshynskyi',
  "\u0421\u043e\u043b\u043e\u043c'\u044f\u043d\u0441\u044c\u043a\u0438\u0439": 'solomianskyi',
  '\u0428\u0435\u0432\u0447\u0435\u043d\u043a\u0456\u0432\u0441\u044c\u043a\u0438\u0439': 'shevchenkivskyi',
}

const DISPLAY = {
  holosiivskyi: 'Holosiivskyi',
  darnytskyi: 'Darnytskyi',
  desnianskyi: 'Desnianskyi',
  dniprovskyi: 'Dniprovskyi',
  obolonskyi: 'Obolonskyi',
  pecherskyi: 'Pecherskyi',
  podilskyi: 'Podilskyi',
  sviatoshynskyi: 'Sviatoshynskyi',
  solomianskyi: 'Solomianskyi',
  shevchenkivskyi: 'Shevchenkivskyi',
}

const BBOX = {
  holosiivskyi: { lat: 50.395, lon: 30.505, min_lat: 50.34, max_lat: 50.43, min_lon: 30.45, max_lon: 30.56 },
  darnytskyi: { lat: 50.405, lon: 30.645, min_lat: 50.36, max_lat: 50.45, min_lon: 30.58, max_lon: 30.72 },
  desnianskyi: { lat: 50.515, lon: 30.615, min_lat: 50.48, max_lat: 50.55, min_lon: 30.55, max_lon: 30.68 },
  dniprovskyi: { lat: 50.455, lon: 30.605, min_lat: 50.42, max_lat: 50.49, min_lon: 30.55, max_lon: 30.66 },
  obolonskyi: { lat: 50.515, lon: 30.495, min_lat: 50.48, max_lat: 50.55, min_lon: 30.42, max_lon: 30.56 },
  pecherskyi: { lat: 50.425, lon: 30.545, min_lat: 50.40, max_lat: 50.45, min_lon: 30.50, max_lon: 30.60 },
  podilskyi: { lat: 50.475, lon: 30.485, min_lat: 50.44, max_lat: 50.51, min_lon: 30.42, max_lon: 30.55 },
  sviatoshynskyi: { lat: 50.455, lon: 30.395, min_lat: 50.42, max_lat: 50.49, min_lon: 30.34, max_lon: 30.45 },
  solomianskyi: { lat: 50.435, lon: 30.475, min_lat: 50.40, max_lat: 50.47, min_lon: 30.42, max_lon: 30.53 },
  shevchenkivskyi: { lat: 50.455, lon: 30.515, min_lat: 50.43, max_lat: 50.48, min_lon: 30.48, max_lon: 30.55 },
}

const districts = geo.features.map((feature) => {
  const slug = NAME_TO_SLUG[feature.properties.name_2]
  const bbox = BBOX[slug]
  return {
    slug,
    name: DISPLAY[slug],
    centroid: { lat: bbox.lat, lon: bbox.lon },
    bbox: {
      min_lat: bbox.min_lat,
      max_lat: bbox.max_lat,
      min_lon: bbox.min_lon,
      max_lon: bbox.max_lon,
    },
    polygon: feature.geometry.coordinates[0].map(([lon, lat]) => [lon, lat]),
  }
}).sort((a, b) => a.slug.localeCompare(b.slug))

fs.writeFileSync(
  path.join(ROOT, 'data/processed/districts_geo.json'),
  JSON.stringify({ districts }, null, 2),
)
console.log(`Wrote ${districts.length} districts with polygons`)
