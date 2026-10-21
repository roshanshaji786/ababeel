import { MessageCircle, Ruler, Store, Truck } from 'lucide-react'
import { useStore } from '../lib/store'
import { ProductCard } from '../components/ui'
import { waLink } from '../lib/whatsapp'

const CATS = [
  { id: 'women', label: 'Women', img: '/img/plum-churidar-sm.webp' },
  { id: 'festive', label: 'Festive', img: '/img/rose-saree-sm.webp' },
  { id: 'modest', label: 'Abayas', img: '/img/grey-abaya-sm.webp' },
  { id: 'kids', label: 'Kids', img: '/img/kids-festive-sm.webp' },
]

export default function Home() {
  const products = useStore((s) => s.products)
  const featured = products.filter((p) => p.featured).slice(0, 8)
  const fresh = [...products].sort((a, b) => b.createdAt.localeCompare(a.createdAt)).slice(0, 4)
  return (
    <>
      <section className="hero">
        <picture>
          <source media="(max-width: 700px)" srcSet="/img/hero-sm.webp" />
          <img src="/img/hero.webp" alt="Model in a maroon zari anarkali in a garden" width={900} height={1844} fetchPriority="high" />
        </picture>
        <div className="wrap">
          <span className="eyebrow">Ababeel Fashions · Thiruvananthapuram</span>
          <h1>Grace for every celebration</h1>
          <p>Anarkalis, kurta sets, silk sarees, abayas and kids festive wear, picked and tailored in Ambalathara.</p>
          <div className="cta">
            <a className="btn btn-primary" href="#/shop">Shop the collection</a>
            <a className="btn btn-ghost" href="#/info/how-to-order">How ordering works</a>
          </div>
        </div>
      </section>

      <div className="wrap">
        <div className="trust">
          <div><MessageCircle size={20} />Order on WhatsApp</div>
          <div><Truck size={20} />Delivery across India</div>
          <div><Ruler size={20} />Custom tailoring</div>
          <div><Store size={20} />Visit us in Ambalathara</div>
        </div>

        <section className="section">
          <div className="section-head">
            <div><span className="eyebrow">Shop by</span><h2>Categories</h2></div>
            <a href="#/shop">View all</a>
          </div>
          <div className="cats">
            {CATS.map((c) => (
              <a key={c.id} className="cat" href={`#/shop/${c.id}`}>
                <img src={c.img} alt="" width={420} height={560} loading="lazy" />
                <span>{c.label}</span>
              </a>
            ))}
          </div>
        </section>

        <section className="section">
          <div className="section-head">
            <div><span className="eyebrow">Handpicked</span><h2>Loved this season</h2></div>
            <a href="#/shop">Shop all</a>
          </div>
          <div className="grid">{featured.map((p) => <ProductCard key={p.id} p={p} />)}</div>
        </section>

        <section className="section">
          <div className="story">
            <div>
              <span className="eyebrow">Our story</span>
              <h2 style={{ marginTop: 8 }}>The right path in fashion</h2>
            </div>
            <div style={{ display: 'grid', gap: 14 }}>
              <p>Ababeel is a family-run store in Ambalathara, Thiruvananthapuram. We choose every piece for its fabric, finish and fit, and our tailors can adjust or make an outfit just for you.</p>
              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <a className="btn btn-primary" href={waLink('Hi Ababeel! I would like to ask about custom tailoring.')} target="_blank" rel="noopener">Ask about tailoring</a>
                <a className="btn btn-ghost" style={{ color: '#fbf3ea', borderColor: 'rgb(255 255 255 / 40%)' }} href="#/info/about">Read more</a>
              </div>
            </div>
          </div>
        </section>

        {fresh.length > 0 && (
          <section className="section">
            <div className="section-head">
              <div><span className="eyebrow">Just in</span><h2>New arrivals</h2></div>
            </div>
            <div className="grid">{fresh.map((p) => <ProductCard key={p.id} p={p} />)}</div>
          </section>
        )}
      </div>
    </>
  )
}
