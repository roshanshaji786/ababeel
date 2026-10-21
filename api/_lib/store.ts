// Tiny JSON "database" on Vercel Blob. Falls back to a local folder when no
// Blob token is set, so the API can run on a laptop (`npm run api`).
import { get, put, list } from '@vercel/blob'
import { promises as fs } from 'node:fs'
import path from 'node:path'

const useBlob = !!process.env.BLOB_READ_WRITE_TOKEN
const LOCAL = path.join(process.cwd(), '.localdb')

export async function readJSON<T>(pathname: string): Promise<T | null> {
  if (!useBlob) {
    try { return JSON.parse(await fs.readFile(path.join(LOCAL, pathname), 'utf8')) as T } catch { return null }
  }
  const res = await get(pathname, { access: 'public', useCache: false })
  if (!res || res.statusCode !== 200) return null
  return JSON.parse(await new Response(res.stream).text()) as T
}

/** Writes JSON at an exact pathname (overwrites). */
export async function writeJSON(pathname: string, data: unknown): Promise<void> {
  const body = JSON.stringify(data)
  if (!useBlob) {
    const file = path.join(LOCAL, pathname)
    await fs.mkdir(path.dirname(file), { recursive: true })
    await fs.writeFile(file, body)
    return
  }
  await put(pathname, body, {
    access: 'public', addRandomSuffix: false, allowOverwrite: true,
    contentType: 'application/json', cacheControlMaxAge: 60,
  })
}

/** Creates a new JSON blob under a hard-to-guess name and returns its pathname. */
export async function createJSON(prefix: string, data: unknown): Promise<string> {
  const body = JSON.stringify(data)
  if (!useBlob) {
    const name = `${prefix}-${Math.random().toString(36).slice(2, 12)}.json`
    await writeJSON(name, data)
    return name
  }
  const res = await put(`${prefix}.json`, body, {
    access: 'public', addRandomSuffix: true, contentType: 'application/json', cacheControlMaxAge: 60,
  })
  return res.pathname
}

export async function listPaths(prefix: string, limit = 300): Promise<string[]> {
  if (!useBlob) {
    try {
      const dir = path.join(LOCAL, prefix)
      return (await fs.readdir(dir)).map((f) => `${prefix}${f}`)
    } catch { return [] }
  }
  const out: string[] = []
  let cursor: string | undefined
  do {
    const page = await list({ prefix, limit: 1000, cursor })
    out.push(...page.blobs.map((b) => b.pathname))
    cursor = page.hasMore ? page.cursor : undefined
  } while (cursor && out.length < limit)
  return out
}

/** Stores an uploaded image and returns its public URL. */
export async function putImage(name: string, body: Buffer, contentType: string): Promise<string> {
  if (!useBlob) {
    const file = path.join(LOCAL, 'images', name)
    await fs.mkdir(path.dirname(file), { recursive: true })
    await fs.writeFile(file, body)
    return `/local-images/${name}`
  }
  const res = await put(`images/${name}`, body, {
    access: 'public', addRandomSuffix: true, contentType, cacheControlMaxAge: 60 * 60 * 24 * 365,
  })
  return res.url
}
