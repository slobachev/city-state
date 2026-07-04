import { join } from 'node:path'
import { readFileSync, existsSync } from 'node:fs'

const DATA_DIR = join(process.cwd(), '..', 'data', 'processed')

export function readDataFile<T>(filename: string): T {
  const filePath = join(DATA_DIR, filename)
  if (!existsSync(filePath)) {
    throw createError({
      statusCode: 404,
      statusMessage: `Data file not found: ${filename}`,
    })
  }
  const raw = readFileSync(filePath, 'utf-8')
  // Pandas exports NaN/Infinity literals that are invalid in strict JSON.
  const sanitized = raw
    .replace(/:\s*NaN\b/g, ': null')
    .replace(/:\s*-?Infinity\b/g, ': null')
  return JSON.parse(sanitized) as T
}
