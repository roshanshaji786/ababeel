import { create } from 'zustand'
import type { Order, Product } from '../../shared/types'
import { SEED_PRODUCTS } from '../../shared/seed'
import { api } from './api'
import { load, save } from './storage'

export interface BagLine { productId: string; size: string; qty: number }
export interface Toast { id: number; text: string }

interface State {
  route: string
  products: Product[]
  loaded: boolean
  loadError: string
  bag: BagLine[]
  lastOrder: Order | null
  toasts: Toast[]
  theme: 'system' | 'light' | 'dark'
  setRoute: (r: string) => void
  loadProducts: () => Promise<void>
  setProducts: (p: Product[]) => void
  add: (productId: string, size: string, qty?: number) => void
  setQty: (i: number, qty: number) => void
  removeLine: (i: number) => void
  clearBag: () => void
  setLastOrder: (o: Order) => void
  toast: (text: string) => void
  setTheme: (t: State['theme']) => void
}

const readHash = () => decodeURIComponent(location.hash.replace(/^#\/?/, ''))

export const useStore = create<State>((set, get) => ({
  route: readHash(),
  products: load<Product[]>('ab-products', SEED_PRODUCTS),
  loaded: false,
  loadError: '',
  bag: load<BagLine[]>('ab-bag', []),
  lastOrder: load<Order | null>('ab-last-order', null),
  toasts: [],
  theme: load<State['theme']>('ab-theme', 'system'),
  setRoute: (route) => set({ route }),
  loadProducts: async () => {
    try {
      const products = await api.products()
      save('ab-products', products)
      set({ products, loaded: true, loadError: '' })
    } catch (e) {
      set({ loaded: true, loadError: (e as Error).message })
    }
  },
  setProducts: (products) => { save('ab-products', products.filter((p) => p.active)); set({ products: products.filter((p) => p.active) }) },
  add: (productId, size, qty = 1) => {
    const bag = [...get().bag]
    const i = bag.findIndex((l) => l.productId === productId && l.size === size)
    if (i >= 0) bag[i] = { ...bag[i], qty: Math.min(10, bag[i].qty + qty) }
    else bag.push({ productId, size, qty })
    save('ab-bag', bag)
    set({ bag })
  },
  setQty: (i, qty) => {
    const bag = get().bag.map((l, n) => (n === i ? { ...l, qty: Math.max(1, Math.min(10, qty)) } : l))
    save('ab-bag', bag)
    set({ bag })
  },
  removeLine: (i) => {
    const bag = get().bag.filter((_, n) => n !== i)
    save('ab-bag', bag)
    set({ bag })
  },
  clearBag: () => { save('ab-bag', []); set({ bag: [] }) },
  setLastOrder: (o) => { save('ab-last-order', o); set({ lastOrder: o }) },
  toast: (text) => {
    const id = Date.now() + Math.random()
    set({ toasts: [...get().toasts, { id, text }] })
    setTimeout(() => set({ toasts: get().toasts.filter((t) => t.id !== id) }), 2600)
  },
  setTheme: (theme) => {
    save('ab-theme', theme)
    if (theme === 'system') delete document.documentElement.dataset.theme
    else document.documentElement.dataset.theme = theme
    set({ theme })
  },
}))

window.addEventListener('hashchange', () => {
  useStore.getState().setRoute(readHash())
  window.scrollTo({ top: 0, behavior: 'instant' })
})

export const go = (r: string) => { location.hash = `/${r}` }

export const bagCount = (s: State) => s.bag.reduce((n, l) => n + l.qty, 0)
