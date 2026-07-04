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
  return JSON.parse(readFileSync(filePath, 'utf-8')) as T
}
