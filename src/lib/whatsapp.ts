import { STORE, type Order, type Product } from '../../shared/types'
import { money } from './format'

export const waLink = (text: string, phone = STORE.whatsapp) => `https://wa.me/${phone}?text=${encodeURIComponent(text)}`

export function orderMessage(o: Order): string {
  const lines = o.items.map((i, n) => `${n + 1}. ${i.name}${i.size ? ` (${i.size})` : ''} × ${i.qty} = ${money(i.price * i.qty)}`)
  return [
    `Hi Ababeel! I placed order ${o.number} on your website.`,
    '',
    ...lines,
    '',
    `Items total: ${money(o.subtotal)}`,
    '',
    `Name: ${o.customer.name}`,
    `Phone: ${o.customer.phone}`,
    `Address: ${o.customer.address}, ${o.customer.city} - ${o.customer.pincode}`,
    o.note ? `Note: ${o.note}` : '',
    '',
    'Please confirm the delivery charge and send the payment link.',
  ].filter((l, i, a) => !(l === '' && a[i - 1] === '')).join('\n')
}

export const productQuestion = (p: Product, size?: string) =>
  `Hi Ababeel! I'm interested in "${p.name}"${size ? ` in size ${size}` : ''} (${money(p.price)}). ${location.origin}/#/p/${p.slug}`
