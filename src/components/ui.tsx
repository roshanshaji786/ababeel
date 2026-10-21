import { useEffect, type ReactNode } from 'react'
import { X } from 'lucide-react'
import type { Product } from '../../shared/types'
import { money, offPct, thumb } from '../lib/format'

export function Price({ price, mrp }: { price: number; mrp?: number }) {
  const off = offPct(price, mrp)
  return (
    <div className="price">
      <b>{money(price)}</b>
      {off > 0 && <><s>{money(mrp!)}</s><span className="off">{off}% off</span></>}
    </div>
  )
}

export function ProductCard({ p, eager }: { p: Product; eager?: boolean }) {
  const allOut = p.sizes.length > 0 && p.sizes.every((s) => p.soldOutSizes.includes(s))
  return (
    <a className="card" href={`#/p/${p.slug}`}>
      <div className="ph">
        <img src={thumb(p.images[0] ?? '/img/hero-sm.webp')} alt={p.name} width={420} height={560} loading={eager ? 'eager' : 'lazy'} decoding="async" />
        {allOut ? <span className="tag">Sold out</span> : offPct(p.price, p.mrp) > 0 ? <span className="tag">{offPct(p.price, p.mrp)}% off</span> : null}
      </div>
      <h3>{p.name}</h3>
      <Price price={p.price} mrp={p.mrp} />
    </a>
  )
}

export function GridSkeleton({ n = 4 }: { n?: number }) {
  return (
    <div className="grid" aria-hidden>
      {Array.from({ length: n }, (_, i) => (
        <div key={i} style={{ display: 'grid', gap: 8 }}>
          <div className="skel" style={{ aspectRatio: '3/4' }} />
          <div className="skel" style={{ height: 14, width: '80%' }} />
          <div className="skel" style={{ height: 14, width: '40%' }} />
        </div>
      ))}
    </div>
  )
}

export function Sheet({ title, onClose, children }: { title: string; onClose: () => void; children: ReactNode }) {
  useEffect(() => {
    const k = (e: KeyboardEvent) => e.key === 'Escape' && onClose()
    document.addEventListener('keydown', k)
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => { document.removeEventListener('keydown', k); document.body.style.overflow = prev }
  }, [onClose])
  return (
    <>
      <div className="scrim" onClick={onClose} />
      <div className="sheet" role="dialog" aria-modal="true" aria-label={title}>
        <div className="grab" />
        <div className="sheet-head">
          <h3>{title}</h3>
          <button className="icon-btn" onClick={onClose} aria-label="Close"><X size={22} /></button>
        </div>
        {children}
      </div>
    </>
  )
}
