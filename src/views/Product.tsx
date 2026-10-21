import { useEffect, useRef, useState } from 'react'
import { ChevronDown, Minus, Plus, MessageCircle, Ruler, ShieldCheck, Truck, ShoppingBag } from 'lucide-react'
import { CATEGORIES } from '../../shared/types'
import { go, useStore } from '../lib/store'
import { money } from '../lib/format'
import { productQuestion, waLink } from '../lib/whatsapp'
import { Price, ProductCard } from '../components/ui'

export default function ProductView({ slug }: { slug?: string }) {
  const { products, loaded, add, toast } = useStore()
  const p = products.find((x) => x.slug === slug)
  const [size, setSize] = useState('')
  const [qty, setQty] = useState(1)
  const [slide, setSlide] = useState(0)
  const [needSize, setNeedSize] = useState(false)
  const [showBar, setShowBar] = useState(false)
  const buyRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setSize(''); setQty(1); setSlide(0); setNeedSize(false)
    if (p) document.title = `${p.name} · Ababeel Fashions`
    return () => { document.title = 'Ababeel Fashions · Ethnic wear, Thiruvananthapuram' }
  }, [p])

  useEffect(() => {
    const el = buyRef.current
    if (!el) return
    const io = new IntersectionObserver(([e]) => setShowBar(!e.isIntersecting && e.boundingClientRect.top < 0))
    io.observe(el)
    return () => io.disconnect()
  }, [p])

  if (!p) {
    return (
      <div className="wrap empty">
        <h3>{loaded ? 'This piece is no longer available' : 'Loading…'}</h3>
        {loaded && <a className="btn btn-primary" href="#/shop">See what’s in store</a>}
      </div>
    )
  }

  const single = p.sizes.length <= 1
  const chosen = single ? p.sizes[0] ?? '' : size
  const allOut = p.sizes.length > 0 && p.sizes.every((s) => p.soldOutSizes.includes(s))
  const cat = CATEGORIES.find((c) => c.id === p.category)
  const related = products.filter((x) => x.id !== p.id && x.category === p.category).concat(products.filter((x) => x.id !== p.id && x.category !== p.category)).slice(0, 4)

  const addToBag = (then?: 'bag') => {
    if (!chosen && p.sizes.length) {
      setNeedSize(true)
      buyRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
      return
    }
    add(p.id, chosen, qty)
    if (then) go('bag')
    else toast(`Added to bag · ${p.name}${chosen ? ` (${chosen})` : ''}`)
  }

  return (
    <div className="wrap">
      <div className="crumbs"><a href="#/">Home</a>/<a href={`#/shop/${p.category}`}>{cat?.label}</a>/<span>{p.name}</span></div>
      <div className="pdp">
        <div className="gallery">
          <div className="slides" onScroll={(e) => setSlide(Math.round(e.currentTarget.scrollLeft / e.currentTarget.clientWidth))}>
            {p.images.map((src, i) => <img key={src} src={src} alt={`${p.name}, photo ${i + 1}`} width={900} height={1200} loading={i ? 'lazy' : 'eager'} />)}
          </div>
          {p.images.length > 1 && <div className="dots">{p.images.map((_, i) => <i key={i} className={i === slide ? 'on' : ''} />)}</div>}
        </div>

        <div className="pdp-info">
          <div style={{ display: 'grid', gap: 8 }}>
            <span className="eyebrow">{cat?.label}</span>
            <h1 style={{ fontSize: 'clamp(30px, 7.5vw, 44px)' }}>{p.name}</h1>
            <Price price={p.price} mrp={p.mrp} />
            <span className="muted" style={{ fontSize: 13 }}>Price includes tax. Delivery charge confirmed on WhatsApp.</span>
          </div>

          {!single && (
            <div style={{ display: 'grid', gap: 10 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <b>Size{chosen && `: ${chosen}`}</b>
                <a href="#/info/size-guide" className="muted" style={{ fontSize: 13, display: 'inline-flex', gap: 6, alignItems: 'center', minHeight: 44 }}><Ruler size={16} />Size guide</a>
              </div>
              <div className="sizes" role="radiogroup" aria-label="Size">
                {p.sizes.map((s) => {
                  const out = p.soldOutSizes.includes(s)
                  return (
                    <button key={s} role="radio" aria-checked={size === s} disabled={out}
                      className={`size ${size === s ? 'on' : ''} ${out ? 'out' : ''}`}
                      onClick={() => { setSize(s); setNeedSize(false) }}>{s}</button>
                  )
                })}
              </div>
              {needSize && <span className="err">Please choose a size.</span>}
            </div>
          )}

          <div className="buy" ref={buyRef}>
            {allOut ? (
              <a className="btn btn-wa btn-block" href={waLink(`Hi Ababeel! "${p.name}" shows sold out. Can you restock or tailor one for me?`)} target="_blank" rel="noopener">
                <MessageCircle size={20} />Sold out · Ask on WhatsApp
              </a>
            ) : (
              <>
                <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                  <div className="qty" aria-label="Quantity">
                    <button onClick={() => setQty(Math.max(1, qty - 1))} aria-label="Less"><Minus size={18} /></button>
                    <span>{qty}</span>
                    <button onClick={() => setQty(Math.min(10, qty + 1))} aria-label="More"><Plus size={18} /></button>
                  </div>
                  <button className="btn btn-primary" style={{ flex: 1 }} onClick={() => addToBag()}><ShoppingBag size={19} />Add to bag</button>
                </div>
                <button className="btn btn-dark btn-block" onClick={() => addToBag('bag')}>Buy now · {money(p.price * qty)}</button>
                <a className="btn btn-ghost btn-block" href={waLink(productQuestion(p, chosen))} target="_blank" rel="noopener"><MessageCircle size={19} />Ask about this on WhatsApp</a>
              </>
            )}
          </div>

          <div className="points">
            <div><Truck size={18} />Delivery across India. Pick up from our store in Ambalathara.</div>
            <div><Ruler size={18} />Free fitting adjustments at the store.</div>
            <div><ShieldCheck size={18} />We confirm every order on WhatsApp before you pay.</div>
          </div>

          <div>
            <details className="acc" open><summary>Details<ChevronDown size={18} /></summary><div>{p.description}</div></details>
            {(p.fabric || p.care) && (
              <details className="acc"><summary>Fabric and care<ChevronDown size={18} /></summary><div>{[p.fabric && `Fabric: ${p.fabric}`, p.care && `Care: ${p.care}`].filter(Boolean).join('\n')}</div></details>
            )}
            <details className="acc"><summary>Delivery and returns<ChevronDown size={18} /></summary><div>We share the dispatch date when we confirm your order on WhatsApp. If something is wrong when it arrives, message us straight away and we will sort it out. <a href="#/info/returns">Read the returns policy</a>.</div></details>
          </div>
        </div>
      </div>

      {related.length > 0 && (
        <section className="section">
          <div className="section-head"><h2>You may also like</h2></div>
          <div className="grid">{related.map((r) => <ProductCard key={r.id} p={r} />)}</div>
        </section>
      )}

      {!allOut && (
        <div className={`sticky-buy ${showBar ? 'show' : ''}`} aria-hidden={!showBar}>
          <div className="meta"><b>{money(p.price)}</b>{chosen ? `Size ${chosen}` : 'Choose a size'}</div>
          <button className="btn btn-primary" tabIndex={showBar ? 0 : -1} onClick={() => addToBag()}>Add to bag</button>
        </div>
      )}
    </div>
  )
}
