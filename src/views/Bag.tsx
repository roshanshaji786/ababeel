import { useState, type FormEvent } from 'react'
import { Check, Info as InfoIcon, MessageCircle, Minus, Plus, ShoppingBag } from 'lucide-react'
import type { Customer } from '../../shared/types'
import { api } from '../lib/api'
import { money, thumb } from '../lib/format'
import { load, save } from '../lib/storage'
import { go, useStore } from '../lib/store'
import { orderMessage, waLink } from '../lib/whatsapp'

function Done() {
  const order = useStore((s) => s.lastOrder)
  if (!order) return <div className="wrap empty"><h3>No recent order</h3><a className="btn btn-primary" href="#/shop">Start shopping</a></div>
  return (
    <div className="wrap done">
      <div className="tick"><Check size={36} /></div>
      <span className="eyebrow">Order {order.number}</span>
      <h1 style={{ fontSize: 36 }}>Thank you, {order.customer.name.split(' ')[0]}!</h1>
      <p className="muted" style={{ maxWidth: 420 }}>
        We have your order. Tap the button below to send it to us on WhatsApp. We will confirm the delivery charge and send a payment link.
      </p>
      <a className="btn btn-wa" href={waLink(orderMessage(order))} target="_blank" rel="noopener"><MessageCircle size={20} />Send order on WhatsApp</a>
      <div className="summary" style={{ width: '100%', maxWidth: 460, textAlign: 'left' }}>
        {order.items.map((i, n) => <div className="r" key={n}><span>{i.name}{i.size && ` (${i.size})`} × {i.qty}</span><b>{money(i.price * i.qty)}</b></div>)}
        <div className="r total"><span>Items total</span><span>{money(order.subtotal)}</span></div>
      </div>
      <a href="#/shop" className="btn btn-ghost">Continue shopping</a>
    </div>
  )
}

export default function Bag({ step }: { step?: string }) {
  const { bag, products, setQty, removeLine, clearBag, setLastOrder } = useStore()
  const [c, setC] = useState<Customer>(() => load('ab-customer', { name: '', phone: '', address: '', city: 'Thiruvananthapuram', pincode: '' }))
  const [note, setNote] = useState('')
  const [hp, setHp] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')

  if (step === 'done') return <Done />

  const lines = bag.map((l) => ({ ...l, p: products.find((p) => p.id === l.productId) })).filter((l) => l.p)
  const total = lines.reduce((s, l) => s + l.p!.price * l.qty, 0)
  const checkout = step === 'checkout'

  if (!lines.length) {
    return (
      <div className="wrap empty">
        <ShoppingBag size={44} />
        <h2>Your bag is empty</h2>
        <p className="muted">Pieces you add will show up here.</p>
        <a className="btn btn-primary" href="#/shop">Start shopping</a>
      </div>
    )
  }

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setErr('')
    if (c.phone.replace(/\D/g, '').length < 10) return setErr('Please enter a 10-digit phone number.')
    if (!/^\d{6}$/.test(c.pincode)) return setErr('Please enter a 6-digit pincode.')
    setBusy(true)
    save('ab-customer', c)
    // Open the WhatsApp tab now, inside the tap, so phones don't block it as a pop-up.
    const win = window.open('', '_blank')
    try {
      const order = await api.placeOrder({ items: lines.map((l) => ({ productId: l.productId, size: l.size, qty: l.qty })), customer: c, note, website: hp })
      setLastOrder(order)
      clearBag()
      if (win) win.location.href = waLink(orderMessage(order))
      go('order')
    } catch (ex) {
      win?.close()
      setErr((ex as Error).message)
    } finally {
      setBusy(false)
    }
  }

  const set = (k: keyof Customer) => (e: { target: { value: string } }) => setC({ ...c, [k]: e.target.value })

  return (
    <div className="wrap">
      <div style={{ paddingTop: 20 }}>
        <span className="eyebrow">{checkout ? 'Step 2 of 2' : 'Step 1 of 2'}</span>
        <h1 style={{ fontSize: 'clamp(32px, 8vw, 44px)' }}>{checkout ? 'Delivery details' : 'Your bag'}</h1>
      </div>
      <div className="bag-layout">
        {checkout ? (
          <form className="form" onSubmit={submit} id="checkout">
            <div className="field"><label htmlFor="n">Full name</label><input id="n" className="input" required autoComplete="name" value={c.name} onChange={set('name')} /></div>
            <div className="field"><label htmlFor="ph">WhatsApp number</label><input id="ph" className="input" required type="tel" inputMode="tel" autoComplete="tel" placeholder="98xxx xxxxx" value={c.phone} onChange={set('phone')} /></div>
            <div className="field"><label htmlFor="ad">Address</label><textarea id="ad" className="input" required autoComplete="street-address" placeholder="House name, street, landmark" value={c.address} onChange={set('address')} /></div>
            <div className="row2">
              <div className="field"><label htmlFor="ci">City</label><input id="ci" className="input" required autoComplete="address-level2" value={c.city} onChange={set('city')} /></div>
              <div className="field"><label htmlFor="pin">Pincode</label><input id="pin" className="input" required inputMode="numeric" maxLength={6} autoComplete="postal-code" value={c.pincode} onChange={(e) => setC({ ...c, pincode: e.target.value.replace(/\D/g, '') })} /></div>
            </div>
            <div className="field"><label htmlFor="nt">Note (optional)</label><input id="nt" className="input" placeholder="Tailoring, gift wrap, best time to call…" value={note} onChange={(e) => setNote(e.target.value)} /></div>
            <input className="sr" tabIndex={-1} autoComplete="off" aria-hidden value={hp} onChange={(e) => setHp(e.target.value)} name="website" />
          </form>
        ) : (
          <div>
            {lines.map((l, i) => (
              <div className="line" key={`${l.productId}-${l.size}`}>
                <a href={`#/p/${l.p!.slug}`}><img src={thumb(l.p!.images[0] ?? '')} alt="" width={84} height={112} /></a>
                <div>
                  <h3>{l.p!.name}</h3>
                  <span className="muted" style={{ fontSize: 13 }}>{l.size && `Size ${l.size} · `}{money(l.p!.price)}</span>
                  <div className="row">
                    <div className="qty">
                      <button onClick={() => setQty(i, l.qty - 1)} aria-label="Less"><Minus size={16} /></button>
                      <span>{l.qty}</span>
                      <button onClick={() => setQty(i, l.qty + 1)} aria-label="More"><Plus size={16} /></button>
                    </div>
                    <b>{money(l.p!.price * l.qty)}</b>
                  </div>
                  <button className="link-btn" onClick={() => removeLine(i)}>Remove</button>
                </div>
              </div>
            ))}
          </div>
        )}
        <aside className="summary">
          <div className="r"><span>Items ({lines.reduce((n, l) => n + l.qty, 0)})</span><span>{money(total)}</span></div>
          <div className="r"><span>Delivery</span><span className="muted">Confirmed on WhatsApp</span></div>
          <div className="r total"><span>Total</span><span>{money(total)}</span></div>
          {err && <p className="err" role="alert">{err}</p>}
          {checkout ? (
            <button className="btn btn-wa btn-block" type="submit" form="checkout" disabled={busy}><MessageCircle size={20} />{busy ? 'Placing order…' : 'Place order on WhatsApp'}</button>
          ) : (
            <a className="btn btn-primary btn-block" href="#/bag/checkout">Checkout</a>
          )}
          <p className="note"><InfoIcon size={16} />{checkout ? 'Your order is saved and opens in WhatsApp. We confirm stock and delivery, then send a secure payment link.' : 'No payment yet. You pay after we confirm your order on WhatsApp.'}</p>
          {checkout && <a className="btn btn-ghost btn-sm" href="#/bag">Back to bag</a>}
        </aside>
      </div>
    </div>
  )
}
