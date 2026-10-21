import type { Order, Product } from '../../shared/types'
import { load } from './storage'

async function call<T>(path: string, init: RequestInit & { auth?: boolean } = {}): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (init.auth) headers.Authorization = `Bearer ${load<string>('ab-admin', '')}`
  let res: Response
  try {
    res = await fetch(path, { ...init, headers })
  } catch {
    throw new Error('No connection. Check your internet and try again.')
  }
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    const err = new Error(data.error || 'Something went wrong. Please try again.') as Error & { status?: number }
    err.status = res.status
    throw err
  }
  return data as T
}

export const api = {
  products: () => call<Product[]>('/api/products'),
  allProducts: () => call<Product[]>('/api/products?all=1', { auth: true }),
  saveProduct: (p: Partial<Product>) => call<Product[]>('/api/products', { method: 'POST', body: JSON.stringify(p), auth: true }),
  deleteProduct: (id: string) => call<Product[]>(`/api/products?id=${encodeURIComponent(id)}`, { method: 'DELETE', auth: true }),
  placeOrder: (body: unknown) => call<Order>('/api/orders', { method: 'POST', body: JSON.stringify(body) }),
  orders: () => call<Order[]>('/api/orders', { auth: true }),
  setOrderStatus: (key: string, status: string) => call<Order>('/api/orders', { method: 'PATCH', body: JSON.stringify({ key, status }), auth: true }),
  login: (pin: string) => call<{ token: string }>('/api/login', { method: 'POST', body: JSON.stringify({ pin }) }),
  upload: (data: string, type: string) => call<{ url: string }>('/api/upload', { method: 'POST', body: JSON.stringify({ data, type }), auth: true }),
}
