import { useCallback, useEffect, useState, type FormEvent } from 'react'
import { ImagePlus, LogOut, MessageCircle, Phone, Plus, RefreshCw, Trash2, X } from 'lucide-react'
import { CATEGORIES, ORDER_STATUSES, type Order, type Product } from '../../shared/types'
import { api } from '../lib/api'
import { money, thumb, when } from '../lib/format'
import { load, remove, save } from '../lib/storage'
import { useStore } from '../lib/store'
import { waLink } from '../lib/whatsapp'
import { Sheet } from '../components/ui'

function Login({ onDone }: { onDone: () => void }) {
  const [pin, setPin] = useState('')
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true); setErr('')
    try {
      const { token } = await api.login(pin)
      save('ab-admin', token)
      onDone()
    } catch (ex) { setErr((ex as Error).message) } finally { setBusy(false) }
  }
  return (
    <form className="wrap form" style={{ maxWidth: 420, paddingTop: 40 }} onSubmit={submit}>
      <span className="eyebrow">Store admin</span>
      <h1 style={{ fontSize: 40 }}>Sign in</h1>
      <div className="field">
        <label htmlFor="pin">Admin PIN</label>
        <input id="pin" className="input" type="password" inputMode="numeric" autoComplete="current-password" value={pin} onChange={(e) => setPin(e.target.value)} required autoFocus />
      </div>
      {err && <p className="err" role="alert">{err}</p>}
      <button className="btn btn-primary btn-block" disabled={busy}>{busy ? 'Checking…' : 'Sign in'}</button>
    </form>
  )
}

const blank: Partial<Product> = { name: '', category: 'women', price: undefined, sizes: ['S', 'M', 'L', 'XL', 'XXL'], soldOutSizes: [], images: [], description: '', featured: false, active: true }

async function toWebp(file: File): Promise<string> {
  const bmp = await createImageBitmap(file)
  const scale = Math.min(1, 1400 / Math.max(bmp.width, bmp.height))
  const c = document.createElement('canvas')
  c.width = Math.round(bmp.width * scale); c.height = Math.round(bmp.height * scale)
  c.getContext('2d')!.drawImage(bmp, 0, 0, c.width, c.height)
  const url = c.toDataURL('image/webp', 0.82)
  return url.split(',')[1]
}

function ProductForm({ initial, onClose, onSaved }: { initial: Partial<Product>; onClose: () => void; onSaved: (all: Product[]) => void }) {
  const [p, setP] = useState<Partial<Product>>(initial)
  const [sizesText, setSizesText] = useState((initial.sizes ?? []).join(', '))
  const [busy, setBusy] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [err, setErr] = useState('')
  const sizes = sizesText.split(',').map((s) => s.trim()).filter(Boolean)
  const toast = useStore((s) => s.toast)

  const upload = async (files: FileList | null) => {
    if (!files?.length) return
    setUploading(true); setErr('')
    try {
      const urls: string[] = []
      for (const f of Array.from(files).slice(0, 6)) urls.push((await api.upload(await toWebp(f), 'image/webp')).url)
      setP((cur) => ({ ...cur, images: [...(cur.images ?? []), ...urls] }))
    } catch (ex) { setErr((ex as Error).message) } finally { setUploading(false) }
  }

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true); setErr('')
    try {
      const all = await api.saveProduct({ ...p, sizes, soldOutSizes: (p.soldOutSizes ?? []).filter((s) => sizes.includes(s)) })
      onSaved(all); toast('Saved'); onClose()
    } catch (ex) { setErr((ex as Error).message) } finally { setBusy(false) }
  }

  const del = async () => {
    if (!p.id || !confirm(`Delete "${p.name}"? This cannot be undone.`)) return
    setBusy(true)
    try { onSaved(await api.deleteProduct(p.id)); toast('Deleted'); onClose() } catch (ex) { setErr((ex as Error).message) } finally { setBusy(false) }
  }

  const toggleOut = (s: string) => setP({ ...p, soldOutSizes: p.soldOutSizes?.includes(s) ? p.soldOutSizes.filter((x) => x !== s) : [...(p.soldOutSizes ?? []), s] })

  return (
    <Sheet title={p.id ? 'Edit product' : 'Add product'} onClose={onClose}>
      <form className="form" onSubmit={submit}>
        <div className="field">
          <label>Photos</label>
          <div className="thumbs">
            {(p.images ?? []).map((src) => (
              <div className="t" key={src}>
                <img src={thumb(src)} alt="" />
                <button type="button" aria-label="Remove photo" onClick={() => setP({ ...p, images: p.images!.filter((x) => x !== src) })}><X size={16} /></button>
              </div>
            ))}
            <label className="upload" aria-label="Add photos">
              {uploading ? <RefreshCw size={22} className="spin" /> : <ImagePlus size={24} />}
              <input type="file" accept="image/*" multiple hidden onChange={(e) => upload(e.target.files)} />
            </label>
          </div>
          <span className="hint">First photo is the cover. Portrait (3:4) photos look best.</span>
        </div>
        <div className="field"><label htmlFor="pn">Name</label><input id="pn" className="input" required value={p.name ?? ''} onChange={(e) => setP({ ...p, name: e.target.value })} /></div>
        <div className="field">
          <label htmlFor="pc">Category</label>
          <select id="pc" className="input" value={p.category} onChange={(e) => setP({ ...p, category: e.target.value as Product['category'] })}>
            {CATEGORIES.map((c) => <option key={c.id} value={c.id}>{c.label}</option>)}
          </select>
        </div>
        <div className="row2">
          <div className="field"><label htmlFor="pp">Price (₹)</label><input id="pp" className="input" required inputMode="numeric" value={p.price ?? ''} onChange={(e) => setP({ ...p, price: Number(e.target.value.replace(/\D/g, '')) || undefined })} /></div>
          <div className="field"><label htmlFor="pm">Old price (₹)</label><input id="pm" className="input" inputMode="numeric" placeholder="Optional" value={p.mrp ?? ''} onChange={(e) => setP({ ...p, mrp: Number(e.target.value.replace(/\D/g, '')) || undefined })} /></div>
        </div>
        <div className="field">
          <label htmlFor="ps">Sizes</label>
          <input id="ps" className="input" value={sizesText} onChange={(e) => setSizesText(e.target.value)} placeholder="S, M, L, XL or Free size" />
          <span className="hint">Separate with commas. Tap a size below to mark it sold out.</span>
          <div className="sizes">{sizes.map((s) => <button type="button" key={s} className={`size ${p.soldOutSizes?.includes(s) ? 'out' : ''}`} style={{ opacity: 1 }} onClick={() => toggleOut(s)}>{s}</button>)}</div>
        </div>
        <div className="field"><label htmlFor="pd">Description</label><textarea id="pd" className="input" value={p.description ?? ''} onChange={(e) => setP({ ...p, description: e.target.value })} /></div>
        <div className="row2">
          <div className="field"><label htmlFor="pf">Fabric</label><input id="pf" className="input" value={p.fabric ?? ''} onChange={(e) => setP({ ...p, fabric: e.target.value })} /></div>
          <div className="field"><label htmlFor="pca">Care</label><input id="pca" className="input" value={p.care ?? ''} onChange={(e) => setP({ ...p, care: e.target.value })} /></div>
        </div>
        <label className="check"><input type="checkbox" checked={p.active !== false} onChange={(e) => setP({ ...p, active: e.target.checked })} />Show in shop</label>
        <label className="check"><input type="checkbox" checked={!!p.featured} onChange={(e) => setP({ ...p, featured: e.target.checked })} />Feature on home page</label>
        {err && <p className="err" role="alert">{err}</p>}
        <button className="btn btn-primary btn-block" disabled={busy || uploading}>{busy ? 'Saving…' : 'Save product'}</button>
        {p.id && <button type="button" className="btn btn-ghost btn-block" onClick={del} disabled={busy}><Trash2 size={18} />Delete product</button>}
      </form>
    </Sheet>
  )
}

function OrderCard({ o, onStatus }: { o: Order; onStatus: (o: Order, s: string) => void }) {
  const phone = o.customer.phone.replace(/\D/g, '').replace(/^(\d{10})$/, '91$1')
  return (
    <div className="order">
      <div className="top-line">
        <div><b>{o.number}</b><div className="muted" style={{ fontSize: 13 }}>{when(o.createdAt)}</div></div>
        <select className="input" style={{ width: 'auto', minHeight: 40 }} value={o.status} onChange={(e) => onStatus(o, e.target.value)} aria-label="Status">
          {ORDER_STATUSES.map((s) => <option key={s} value={s}>{s[0].toUpperCase() + s.slice(1)}</option>)}
        </select>
      </div>
      <div style={{ fontSize: 14 }}>
        {o.items.map((i, n) => <div key={n}>{i.name}{i.size && ` (${i.size})`} × {i.qty} · {money(i.price * i.qty)}</div>)}
        <b>Total {money(o.subtotal)}</b>
      </div>
      <div className="muted" style={{ fontSize: 14 }}>
        <b style={{ color: 'var(--text)' }}>{o.customer.name}</b> · {o.customer.phone}<br />
        {o.customer.address}, {o.customer.city} - {o.customer.pincode}
        {o.note && <><br />Note: {o.note}</>}
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <a className="btn btn-wa btn-sm" href={waLink(`Hi ${o.customer.name.split(' ')[0]}, this is Ababeel Fashions about your order ${o.number}.`, phone)} target="_blank" rel="noopener"><MessageCircle size={16} />WhatsApp</a>
        <a className="btn btn-ghost btn-sm" href={`tel:${o.customer.phone}`}><Phone size={16} />Call</a>
      </div>
    </div>
  )
}

export default function Admin() {
  const [signedIn, setSignedIn] = useState(() => !!load('ab-admin', ''))
  const [tab, setTab] = useState<'orders' | 'products'>('orders')
  const [products, setProducts] = useState<Product[]>([])
  const [orders, setOrders] = useState<Order[] | null>(null)
  const [editing, setEditing] = useState<Partial<Product> | null>(null)
  const [err, setErr] = useState('')
  const setShopProducts = useStore((s) => s.setProducts)
  const toast = useStore((s) => s.toast)

  const signOut = useCallback(() => { remove('ab-admin'); setSignedIn(false) }, [])
  const fail = useCallback((e: unknown) => {
    if ((e as { status?: number }).status === 401) signOut()
    else setErr((e as Error).message)
  }, [signOut])

  const refresh = useCallback(async () => {
    setErr('')
    try {
      const [p, o] = await Promise.all([api.allProducts(), api.orders()])
      setProducts(p); setOrders(o)
    } catch (e) { fail(e) }
  }, [fail])

  useEffect(() => { if (signedIn) refresh() }, [signedIn, refresh])
  useEffect(() => { document.title = 'Admin · Ababeel'; return () => { document.title = 'Ababeel Fashions · Ethnic wear, Thiruvananthapuram' } }, [])

  if (!signedIn) return <Login onDone={() => setSignedIn(true)} />

  const saved = (all: Product[]) => { setProducts(all); setShopProducts(all) }
  const setStatus = async (o: Order, status: string) => {
    try {
      const next = await api.setOrderStatus(o.key!, status)
      setOrders((cur) => cur!.map((x) => (x.key === o.key ? next : x)))
      toast(`${o.number} → ${status}`)
    } catch (e) { fail(e) }
  }
  const open = orders?.filter((o) => o.status === 'new' || o.status === 'confirmed').length ?? 0

  return (
    <div className="wrap admin">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: 36 }}>Store admin</h1>
        <div>
          <button className="icon-btn" onClick={refresh} aria-label="Refresh"><RefreshCw size={20} /></button>
          <button className="icon-btn" onClick={signOut} aria-label="Sign out"><LogOut size={20} /></button>
        </div>
      </div>
      <div className="stats">
        <div><b>{open}</b><small>Open orders</small></div>
        <div><b>{orders?.length ?? '–'}</b><small>All orders</small></div>
        <div><b>{products.filter((p) => p.active).length}</b><small>In shop</small></div>
      </div>
      <div className="seg">
        <button className={tab === 'orders' ? 'on' : ''} onClick={() => setTab('orders')}>Orders</button>
        <button className={tab === 'products' ? 'on' : ''} onClick={() => setTab('products')}>Products</button>
      </div>
      {err && <p className="err" role="alert">{err}</p>}

      {tab === 'orders' ? (
        orders === null ? <p className="muted">Loading orders…</p> :
        orders.length === 0 ? <div className="empty"><h3>No orders yet</h3><p className="muted">Orders placed on the website show up here.</p></div> :
        <div style={{ display: 'grid', gap: 12 }}>{orders.map((o) => <OrderCard key={o.key} o={o} onStatus={setStatus} />)}</div>
      ) : (
        <div style={{ display: 'grid', gap: 10 }}>
          <button className="btn btn-primary" onClick={() => setEditing({ ...blank })}><Plus size={20} />Add product</button>
          {products.map((p) => (
            <button key={p.id} className="arow" style={{ textAlign: 'left' }} onClick={() => setEditing(p)}>
              <img src={thumb(p.images[0] ?? '/img/hero-sm.webp')} alt="" />
              <div>
                <h3>{p.name}</h3>
                <span className="muted" style={{ fontSize: 13 }}>{money(p.price)} · {CATEGORIES.find((c) => c.id === p.category)?.label}</span>
              </div>
              <span className={`pill ${p.active ? 'ok' : ''}`}>{p.active ? 'Live' : 'Hidden'}</span>
            </button>
          ))}
        </div>
      )}
      {editing && <ProductForm initial={editing} onClose={() => setEditing(null)} onSaved={saved} />}
    </div>
  )
}
