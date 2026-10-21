import { createHmac, scryptSync, timingSafeEqual } from 'node:crypto'
import type { VercelRequest } from '@vercel/node'

const SESSION_DAYS = 30
const isLocal = !process.env.BLOB_READ_WRITE_TOKEN

function secret(): string {
  const s = process.env.SESSION_SECRET
  if (s) return s
  if (isLocal) return 'local-dev-secret'
  throw new Error('SESSION_SECRET is not set')
}


export function checkPin(pin: string): boolean {
  const stored = process.env.ADMIN_PIN_HASH
  if (!stored) return isLocal && pin === '1234'
  const [salt, hash] = stored.split(':')
  const got = scryptSync(pin, salt, 32)
  const want = Buffer.from(hash, 'hex')
  return got.length === want.length && timingSafeEqual(got, want)
}

const sign = (data: string) => createHmac('sha256', secret()).update(data).digest('base64url')

export function makeToken(): string {
  const payload = Buffer.from(JSON.stringify({ role: 'admin', exp: Date.now() + SESSION_DAYS * 864e5 })).toString('base64url')
  return `${payload}.${sign(payload)}`
}

export function isAdmin(req: VercelRequest): boolean {
  const h = req.headers.authorization || ''
  const token = h.startsWith('Bearer ') ? h.slice(7) : ''
  const [payload, sig] = token.split('.')
  if (!payload || !sig) return false
  const want = Buffer.from(sign(payload))
  const got = Buffer.from(sig)
  if (want.length !== got.length || !timingSafeEqual(want, got)) return false
  try {
    const { exp } = JSON.parse(Buffer.from(payload, 'base64url').toString())
    return typeof exp === 'number' && exp > Date.now()
  } catch { return false }
}

// Best-effort limit on wrong PINs (per server instance): 5 tries per 15 minutes per IP.
const tries = new Map<string, { n: number; until: number }>()
export function clientIp(req: VercelRequest): string {
  return String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown'
}
export function tooManyTries(ip: string): boolean {
  const t = tries.get(ip)
  return !!t && t.n >= 5 && t.until > Date.now()
}
export function noteFailure(ip: string) {
  const t = tries.get(ip)
  if (!t || t.until < Date.now()) tries.set(ip, { n: 1, until: Date.now() + 15 * 60e3 })
  else t.n++
}
