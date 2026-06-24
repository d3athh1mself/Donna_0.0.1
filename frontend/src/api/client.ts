export class ApiError extends Error {
  readonly status?: number

  constructor(message: string, status?: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function getJson<T>(path: string): Promise<T> {
  if (!path.startsWith('/api/')) {
    throw new ApiError('Public API requests must use the /api/ path')
  }

  const response = await fetch(path, {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    throw new ApiError(`Request failed with status ${response.status}`, response.status)
  }

  return (await response.json()) as T
}
