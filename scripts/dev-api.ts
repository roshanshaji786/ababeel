// Local stand-in for Vercel Functions: runs api/*.ts on :3001 with a .localdb folder as storage.
import http from 'node:http'
import { promises as fs } from 'node:fs'
import path from 'node:path'

const routes: Record<string, () => Promise<{ default: (req: any, res: any) => unknown }>> = {
  products: () => import('../api/products.js'),
  orders: () => import('../api/orders.js'),
  login: () => import('../api/login.js'),
  upload: () => import('../api/upload.js'),
}

http.createServer(async (req, res) => {
  const url = new URL(req.url || '/', 'http://localhost')
  if (url.pathname.startsWith('/local-images/')) {
    try {
      const file = path.join(process.cwd(), '.localdb/images', path.basename(url.pathname))
      res.writeHead(200, { 'Content-Type': 'image/' + path.extname(file).slice(1).replace('jpg', 'jpeg') })
      return res.end(await fs.readFile(file))
    } catch { res.writeHead(404); return res.end() }
  }
  const name = url.pathname.replace(/^\/api\//, '')
  const load = routes[name]
  if (!load) { res.writeHead(404); return res.end('{}') }
  let raw = ''
  for await (const chunk of req) raw += chunk
  const vreq = Object.assign(req, {
    query: Object.fromEntries(url.searchParams),
    body: raw ? JSON.parse(raw) : undefined,
  })
  const vres = Object.assign(res, {
    status(code: number) { res.statusCode = code; return vres },
    json(data: unknown) { res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(data)); return vres },
  })
  await (await load()).default(vreq, vres)
}).listen(3001, () => console.log('API on http://localhost:3001'))
