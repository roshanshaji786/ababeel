export type Category = 'women' | 'festive' | 'modest' | 'kids' | 'coord'

export interface Product {
  id: string
  slug: string
  name: string
  category: Category
  price: number
  mrp?: number
  sizes: string[]
  soldOutSizes: string[]
  images: string[]
  description: string
  fabric?: string
  care?: string
  featured: boolean
  active: boolean
  createdAt: string
}

export interface OrderItem {
  productId: string
  name: string
  size: string
  qty: number
  price: number
  image?: string
}

export type OrderStatus = 'new' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'

export interface Customer {
  name: string
  phone: string
  address: string
  city: string
  pincode: string
}

export interface Order {
  id: string
  number: string
  createdAt: string
  items: OrderItem[]
  subtotal: number
  customer: Customer
  note?: string
  status: OrderStatus
  /** Blob pathname, set by the server when listing; used to update the order. */
  key?: string
}

export const CATEGORIES: { id: Category; label: string; blurb: string }[] = [
  { id: 'women', label: 'Women', blurb: 'Kurta sets, churidars and anarkalis' },
  { id: 'festive', label: 'Festive & bridal', blurb: 'Silk sarees and occasion wear' },
  { id: 'modest', label: 'Abayas', blurb: 'Hooded and open abayas' },
  { id: 'coord', label: 'Co-ords', blurb: 'Easy matching sets' },
  { id: 'kids', label: 'Kids', blurb: 'Festive sets for little ones' },
]

export const ORDER_STATUSES: OrderStatus[] = ['new', 'confirmed', 'shipped', 'delivered', 'cancelled']

export const STORE = {
  name: 'Ababeel Fashions',
  whatsapp: '919895984721',
  phoneDisplay: '+91 98959 84721',
  email: 'ababeeltvm@gmail.com',
  instagram: 'ababeelfashions2024',
  address: 'Ambalathara, near Cordova School, Bypass Road, Thiruvananthapuram, Kerala 695026',
  owner: 'Ayoob Khan Ashraf',
  mapsUrl: 'https://www.google.com/maps/search/?api=1&query=Ababeel+Fashions+Ambalathara+Thiruvananthapuram',
}
