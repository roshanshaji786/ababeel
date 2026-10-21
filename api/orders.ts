import type { VercelRequest, VercelResponse } from '@vercel/node'
import type { Order, OrderItem } from '../shared/types.js'
import { ORDER_STATUSES } from '../shared/types.js'
import { isAdmin } from './_lib/auth.js'
import { loadProducts } from './_lib/products.js'
import { createJSON, listPaths, readJSON, writeJSON } from './_lib/store.js'

const str = (v: unknown, max: number) => String(v ?? '').trim().slice(0, max)

async function create(req: VercelRequest, res: VercelResponse) {
  const body = req.body ?? {}
  if (body.website) return res.json({ ok: true }) // honeypot
  const c = body.customer ?? {}
  const customer = {
    name: str(c.name, 80), phone: str(c.phone, 20).replace(/[^\d+ ]/g, ''),
    address: str(c.address, 400), city: str(c.city, 60), pincode: str(c.pincode, 6).replace(/\D/g, ''),
  }
  if (!customer.name || customer.phone.replace(/\D/g, '').length < 10 || !customer.address || customer.pincode.length !== 6) {
    return res.status(400).json({ error: 'Please fill in your name, a 10-digit phone number, address and 6-digit pincode.' })
  }
  const products = await loadProducts()
  const raw: unknown[] = Array.isArray(body.items) ? body.items.slice(0, 20) : []
  const items: OrderItem[] = []
  for (const r of raw as { productId?: string; size?: string; qty?: number }[]) {
    const p = products.find((x) => x.id === r.productId && x.active)
    if (!p) continue
    const size = str(r.size, 20)
    if (p.sizes.length && !p.sizes.includes(size)) continue
    if (p.soldOutSizes.includes(size)) continue
    const qty = Math.min(10, Math.max(1, Math.round(Number(r.qty) || 1)))
    items.push({ productId: p.id, name: p.name, size, qty, price: p.price, image: p.images[0] })
  }
  if (!items.length) return res.status(400).json({ error: 'Your bag is empty or those items are no longer available.' })
  const now = new Date()
  const ist = new Date(now.getTime() + 5.5 * 3600e3)
  const number = `AB${ist.toISOString().slice(2, 10).replace(/-/g, '')}-${Math.floor(1000 + Math.random() * 9000)}`
  const order: Order = {
    id: number, number, createdAt: now.toISOString(), items,
    subtotal: items.reduce((s, i) => s + i.price * i.qty, 0),
    customer, note: str(body.note, 500) || undefined, status: 'new',
  }
  // Pathnames sort by time; the random suffix keeps them unguessable.
  await createJSON(`orders/${now.toISOString().replace(/[:.]/g, '-')}-${number}`, order)
  res.json(order)
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  res.setHeader('Cache-Control', 'no-store')
  try {
    if (req.method === 'POST') return await create(req, res)
    if (!isAdmin(req)) return res.status(401).json({ error: 'Please sign in again.' })
    if (req.method === 'GET') {
      const paths = (await listPaths('orders/')).sort().reverse().slice(0, 150)
      const orders = await Promise.all(paths.map(async (key) => {
        const o = await readJSON<Order>(key)
        return o ? { ...o, key } : null
      }))
      return res.json(orders.filter(Boolean))
    }
    if (req.method === 'PATCH') {
      const key = str(req.body?.key, 300)
      const status = req.body?.status
      if (!key.startsWith('orders/') || !ORDER_STATUSES.includes(status)) return res.status(400).json({ error: 'Bad request' })
      const o = await readJSON<Order>(key)
      if (!o) return res.status(404).json({ error: 'Order not found' })
      const next = { ...o, status }
      delete (next as Partial<Order>).key
      await writeJSON(key, next)
      return res.json({ ...next, key })
    }
    res.status(405).json({ error: 'Not allowed' })
  } catch (e) {
    console.error(e)
    res.status(500).json({ error: 'Something went wrong on our side. Please try again.' })
  }
}
