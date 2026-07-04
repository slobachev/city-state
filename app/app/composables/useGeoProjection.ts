const KYIV_CENTER = { lat: 50.4501, lon: 30.5234 }
const SCALE = 8000

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

  return { project, bboxSize, scale: SCALE }
}
