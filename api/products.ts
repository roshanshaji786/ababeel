import type { VercelRequest, VercelResponse } from '@vercel/node'
import type { Product } from '../shared/types.js'
import { CATEGORIES } from '../shared/types.js'
import { isAdmin } from './_lib/auth.js'
import { loadProducts, saveProducts } from './_lib/products.js'

const slugify = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60)
const strList = (v: unknown) => (Array.isArray(v) ? v.map((x) => String(x).trim()).filter(Boolean).slice(0, 20) : [])

function clean(input: Partial<Product>, existing: Product[]): Product | string {
  const name = String(input.name ?? '').trim().slice(0, 120)
  if (!name) return 'Please add a product name.'
  const price = Math.round(Number(input.price))
  if (!Number.isFinite(price) || price <= 0) return 'Please add a price above 0.'
  const mrp = input.mrp ? Math.round(Number(input.mrp)) : undefined
  const category = CATEGORIES.some((c) => c.id === input.category) ? input.category! : 'women'
  const id = input.id && existing.some((p) => p.id === input.id) ? input.id : `p-${Date.now().toString(36)}`
  let slug = slugify(String(input.slug || name)) || id
  if (existing.some((p) => p.slug === slug && p.id !== id)) slug = `${slug}-${id.slice(-4)}`
  const prev = existing.find((p) => p.id === id)
  return {
    id, slug, name, category, price,
    mrp: mrp && mrp > price ? mrp : undefined,
    sizes: strList(input.sizes),
    soldOutSizes: strList(input.soldOutSizes),
    images: strList(input.images).filter((u) => u.startsWith('/') || u.startsWith('https://')).slice(0, 8),
    description: String(input.description ?? '').slice(0, 3000),
    fabric: String(input.fabric ?? '').slice(0, 200) || undefined,
    care: String(input.care ?? '').slice(0, 200) || undefined,
    featured: !!input.featured,
    active: input.active !== false,
    createdAt: prev?.createdAt ?? new Date().toISOString(),
  }
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  try {
    if (req.method === 'GET') {
      const all = await loadProducts()
      if (req.query.all && isAdmin(req)) {
        res.setHeader('Cache-Control', 'no-store')
        return res.json(all)
      }
      res.setHeader('Cache-Control', 'public, max-age=0, s-maxage=30, stale-while-revalidate=300')
      return res.json(all.filter((p) => p.active))
    }
    if (!isAdmin(req)) return res.status(401).json({ error: 'Please sign in again.' })
    const items = await loadProducts()
    if (req.method === 'POST') {
      const p = clean(req.body ?? {}, items)
      if (typeof p === 'string') return res.status(400).json({ error: p })
      const i = items.findIndex((x) => x.id === p.id)
      if (i >= 0) items[i] = p
      else items.unshift(p)
      await saveProducts(items)
      return res.json(items)
    }
    if (req.method === 'DELETE') {
      const next = items.filter((p) => p.id !== req.query.id)
      await saveProducts(next)
      return res.json(next)
    }
    res.status(405).json({ error: 'Not allowed' })
  } catch (e) {
    console.error(e)
    res.status(500).json({ error: 'Something went wrong on our side. Please try again.' })
  }
}
