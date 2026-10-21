import type { VercelRequest, VercelResponse } from '@vercel/node'
import { checkPin, clientIp, makeToken, noteFailure, tooManyTries } from './_lib/auth.js'

export default async function handler(req: VercelRequest, res: VercelResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' })
  const ip = clientIp(req)
  if (tooManyTries(ip)) return res.status(429).json({ error: 'Too many wrong tries. Wait 15 minutes and try again.' })
  const pin = String(req.body?.pin ?? '')
  await new Promise((r) => setTimeout(r, 400))
  if (!pin || !checkPin(pin)) {
    noteFailure(ip)
    return res.status(401).json({ error: 'That PIN is not right.' })
  }
  res.json({ token: makeToken() })
}
