import { useEffect, useMemo, useRef, useState } from 'react'
import { Search, SearchX } from 'lucide-react'
import { CATEGORIES } from '../../shared/types'
import { useStore } from '../lib/store'
import { GridSkeleton, ProductCard } from '../components/ui'

type Sort = 'featured' | 'new' | 'low' | 'high'

export default function Shop({ category, focusSearch }: { category?: string; focusSearch?: boolean }) {
  const { products, loaded } = useStore()
  const [q, setQ] = useState('')
  const [sort, setSort] = useState<Sort>('featured')
  const input = useRef<HTMLInputElement>(null)
  useEffect(() => { if (focusSearch) input.current?.focus() }, [focusSearch])
  const cat = CATEGORIES.find((c) => c.id === category)

  const list = useMemo(() => {
    const words = q.toLowerCase().split(/\s+/).filter(Boolean)
    const out = products.filter((p) =>
      (!cat || p.category === cat.id) &&
      words.every((w) => `${p.name} ${p.description} ${p.fabric ?? ''} ${p.category}`.toLowerCase().includes(w)))
    if (sort === 'low') out.sort((a, b) => a.price - b.price)
    else if (sort === 'high') out.sort((a, b) => b.price - a.price)
    else if (sort === 'new') out.sort((a, b) => b.createdAt.localeCompare(a.createdAt))
    else out.sort((a, b) => Number(b.featured) - Number(a.featured))
    return out
  }, [products, cat, q, sort])

  return (
    <div className="wrap">
      <div className="shop-head">
        <div>
          <span className="eyebrow">{cat ? cat.blurb : 'Everything in store'}</span>
          <h1 style={{ fontSize: 'clamp(32px, 8vw, 48px)' }}>{cat ? cat.label : 'Shop all'}</h1>
        </div>
        <label className="search">
          <span className="sr">Search</span>
          <Search size={20} />
          <input ref={input} className="input" type="search" placeholder="Search anarkali, saree, abaya…" value={q} onChange={(e) => setQ(e.target.value)} enterKeyHint="search" />
        </label>
        <div className="chips" role="list">
          <a className={`chip ${!cat ? 'on' : ''}`} href="#/shop">All</a>
          {CATEGORIES.map((c) => <a key={c.id} className={`chip ${cat?.id === c.id ? 'on' : ''}`} href={`#/shop/${c.id}`}>{c.label}</a>)}
        </div>
      </div>
      <div className="toolbar">
        <span className="muted">{list.length} {list.length === 1 ? 'piece' : 'pieces'}</span>
        <label>
          <span className="sr">Sort</span>
          <select value={sort} onChange={(e) => setSort(e.target.value as Sort)}>
            <option value="featured">Featured</option>
            <option value="new">Newest</option>
            <option value="low">Price: low to high</option>
            <option value="high">Price: high to low</option>
          </select>
        </label>
      </div>
      {!loaded && products.length === 0 ? <GridSkeleton /> : list.length ? (
        <div className="grid">{list.map((p, i) => <ProductCard key={p.id} p={p} eager={i < 4} />)}</div>
      ) : (
        <div className="empty">
          <SearchX size={40} />
          <h3>Nothing here yet</h3>
          <p className="muted">{q ? `No pieces match "${q}".` : 'New pieces are on the way.'} Ask us on WhatsApp and we will check the store for you.</p>
          {q && <button className="btn btn-ghost" onClick={() => setQ('')}>Clear search</button>}
        </div>
      )}
    </div>
  )
}
