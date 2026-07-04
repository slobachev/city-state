const KYIV_CENTER = { lat: 50.4501, lon: 30.5234 }
// Scale factor: ~0.1° lat/lon ≈ 1 scene unit per district edge
const SCALE = 100

/** Project WGS84 coordinates to local 3D scene coordinates. */
export function useGeoProjection() {
  function project(lat: number, lon: number): [number, number] {
    const x = (lon - KYIV_CENTER.lon) * SCALE
    const z = -(lat - KYIV_CENTER.lat) * SCALE
    return [x, z]
  }

  function bboxSize(bbox: {
    min_lat: number
    max_lat: number
    min_lon: number
    max_lon: number
  }): { width: number; depth: number; center: [number, number] } {
    const [x1, z1] = project(bbox.min_lat, bbox.min_lon)
    const [x2, z2] = project(bbox.max_lat, bbox.max_lon)
    const width = Math.abs(x2 - x1)
    const depth = Math.abs(z2 - z1)
    const centerLat = (bbox.min_lat + bbox.max_lat) / 2
    const centerLon = (bbox.min_lon + bbox.max_lon) / 2
    const center = project(centerLat, centerLon)
    return { width, depth, center }
  }

  /** Compute orbit target at the centroid of all district bboxes. */
  function sceneCenter(
    districts: { bbox: { min_lat: number; max_lat: number; min_lon: number; max_lon: number } }[],
  ): [number, number, number] {
    if (!districts.length) return [0, 0, 0]
    let minX = Infinity
    let maxX = -Infinity
    let minZ = Infinity
    let maxZ = -Infinity
    for (const d of districts) {
      const { center, width, depth } = bboxSize(d.bbox)
      minX = Math.min(minX, center[0] - width / 2)
      maxX = Math.max(maxX, center[0] + width / 2)
      minZ = Math.min(minZ, center[1] - depth / 2)
      maxZ = Math.max(maxZ, center[1] + depth / 2)
    }
    return [(minX + maxX) / 2, 0, (minZ + maxZ) / 2]
  }

  return { project, bboxSize, sceneCenter, scale: SCALE }
}
