import { lazy, Suspense, useEffect } from 'react'
import { Home as HomeIcon, LayoutGrid, Menu, MessageCircle, Search, ShoppingBag } from 'lucide-react'
import { STORE } from '../shared/types'
import { bagCount, useStore } from './lib/store'
import { waLink } from './lib/whatsapp'
import Home from './views/Home'
import Shop from './views/Shop'
import ProductView from './views/Product'
import Bag from './views/Bag'
import Info, { More } from './views/Info'

const Admin = lazy(() => import('./views/Admin'))

function Header({ route }: { route: string }) {
  const count = useStore(bagCount)
  const on = (r: string) => (route.split('/')[0] === r ? 'on' : '')
  return (
    <header className="top">
      <div className="wrap">
        <a className="brand" href="#/" aria-label="Ababeel Fashions home">
          <img className="logo-deep" src="/img/logo-deep.webp" alt="Ababeel" width={114} height={38} />
          <img className="logo-gold" src="/img/logo-gold.webp" alt="Ababeel" width={114} height={38} />
        </a>
        <nav aria-label="Main">
          <a className={on('shop')} href="#/shop">Shop all</a>
          <a href="#/shop/women">Women</a>
          <a href="#/shop/festive">Festive</a>
          <a href="#/shop/modest">Abayas</a>
          <a href="#/shop/kids">Kids</a>
          <a className={on('info')} href="#/info/contact">Contact</a>
        </nav>
        <div className="spacer" />
        <a className="icon-btn" href="#/shop?search" aria-label="Search"><Search size={22} /></a>
        <a className="icon-btn" href="#/bag" aria-label={`Bag, ${count} items`}>
          <ShoppingBag size={22} />
          {count > 0 && <span className="badge">{count}</span>}
        </a>
      </div>
    </header>
  )
}

function TabBar({ route }: { route: string }) {
  const count = useStore(bagCount)
  const r = route.split('/')[0]
  return (
    <nav className="tabbar" aria-label="Tabs">
      <a className={r === '' ? 'on' : ''} href="#/"><HomeIcon size={22} />Home</a>
      <a className={r === 'shop' || r === 'p' ? 'on' : ''} href="#/shop"><LayoutGrid size={22} />Shop</a>
      <a className={r === 'bag' || r === 'order' ? 'on' : ''} href="#/bag">
        <ShoppingBag size={22} />Bag{count > 0 && <span className="badge">{count}</span>}
      </a>
      <a className="wa" href={waLink('Hi Ababeel! I have a question.')} target="_blank" rel="noopener"><MessageCircle size={22} />WhatsApp</a>
      <a className={r === 'more' || r === 'info' ? 'on' : ''} href="#/more"><Menu size={22} />More</a>
    </nav>
  )
}

function Footer() {
  return (
    <footer>
      <div className="wrap cols">
        <div className="about">
          <h4>Ababeel Fashions</h4>
          <p>Ethnic and modest wear for women and kids, with custom tailoring. {STORE.address}.</p>
        </div>
        <div>
          <h4>Shop</h4>
          <a href="#/shop/women">Women</a><a href="#/shop/festive">Festive</a><a href="#/shop/modest">Abayas</a><a href="#/shop/kids">Kids</a>
        </div>
        <div>
          <h4>Help</h4>
          <a href="#/info/how-to-order">How to order</a><a href="#/info/size-guide">Size guide</a><a href="#/info/shipping">Shipping</a><a href="#/info/returns">Returns</a>
        </div>
        <div>
          <h4>About</h4>
          <a href="#/info/about">Our story</a><a href="#/info/contact">Contact</a><a href="#/info/privacy">Privacy</a><a href="#/info/terms">Terms</a>
        </div>
      </div>
    </footer>
  )
}

function Toasts() {
  const toasts = useStore((s) => s.toasts)
  return <div className="toasts" aria-live="polite">{toasts.map((t) => <div key={t.id} className="toast">{t.text}</div>)}</div>
}

export default function App() {
  const route = useStore((s) => s.route)
  const loadProducts = useStore((s) => s.loadProducts)
  useEffect(() => { loadProducts() }, [loadProducts])

  const [head, ...rest] = route.split('?')[0].split('/')
  let view
  switch (head) {
    case '': view = <Home />; break
    case 'shop': view = <Shop category={rest[0]} focusSearch={route.includes('?search')} />; break
    case 'p': view = <ProductView slug={rest[0]} />; break
    case 'bag': case 'order': view = <Bag step={head === 'order' ? 'done' : rest[0]} />; break
    case 'info': view = <Info page={rest[0]} />; break
    case 'more': view = <More />; break
    case 'admin': view = <Suspense fallback={<div className="wrap" style={{ padding: 40 }}>Loading…</div>}><Admin /></Suspense>; break
    default: view = <Info page="404" />
  }
  return (
    <>
      <Header route={route} />
      <main>{view}</main>
      {head !== 'admin' && <Footer />}
      <TabBar route={route} />
      <Toasts />
    </>
  )
}
