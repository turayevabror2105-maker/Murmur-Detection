export const API_BASE = 'http://localhost:8000/api'

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`)
  const data = await res.json()
  if (!res.ok) {
    throw data
  }
  return data
}

export async function apiPost<T>(path: string, body?: any): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : undefined
  })
  const data = await res.json()
  if (!res.ok) {
    throw data
  }
  return data
}

export async function uploadFile(file: File): Promise<any> {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
  })
  const data = await res.json()
  if (!res.ok) {
    throw data
  }
  return data
}
