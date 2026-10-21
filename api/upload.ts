import type { VercelRequest, VercelResponse } from '@vercel/node'
import { isAdmin } from './_lib/auth.js'
import { putImage } from './_lib/store.js'

const TYPES: Record<string, string> = { 'image/webp': 'webp', 'image/jpeg': 'jpg', 'image/png': 'png' }

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' })
  if (!isAdmin(req)) return res.status(401).json({ error: 'Please sign in again.' })
  const type = String(req.body?.type ?? '')
  const ext = TYPES[type]
  if (!ext) return res.status(400).json({ error: 'Please upload a JPG, PNG or WebP photo.' })
  const buf = Buffer.from(String(req.body?.data ?? ''), 'base64')
  if (!buf.length || buf.length > 3.5 * 1024 * 1024) return res.status(400).json({ error: 'That photo is too large.' })
  try {
    const url = await putImage(`p-${Date.now().toString(36)}.${ext}`, buf, type)
    res.json({ url })
  } catch (e) {
    console.error(e)
    res.status(500).json({ error: 'Upload failed. Please try again.' })
  }
}
