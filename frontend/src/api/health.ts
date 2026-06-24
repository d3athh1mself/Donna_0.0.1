import { getJson } from './client'

export type HealthStatus = 'ok'

export interface HealthResponse {
  status: HealthStatus
}

export async function getHealthStatus(): Promise<HealthResponse> {
  const health = await getJson<Partial<HealthResponse>>('/api/health')

  if (health.status !== 'ok') {
    throw new Error('Backend health response was not ok')
  }

  return { status: health.status }
}
