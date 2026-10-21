import type { ReactNode } from 'react'
import { ChevronRight, FileText, Camera, Mail, MapPin, MessageCircle, Moon, Phone, Ruler, Scissors, ShieldCheck, Store, Truck, Undo2, HelpCircle, Lock } from 'lucide-react'
import { STORE } from '../../shared/types'
import { useStore } from '../lib/store'
import { waLink } from '../lib/whatsapp'

const updated = 'Last updated: 21 October 2026'

const PAGES: Record<string, { title: string; body: ReactNode }> = {
  about: {
    title: 'Our story',
    body: (
      <>
        <p>Ababeel Fashions is a family-run store in Ambalathara, Thiruvananthapuram, selling women's and kids' ethnic and modest wear. Our name comes from the Ababeel bird, and our promise is in our tagline: the right path in fashion.</p>
        <p>We pick every anarkali, kurta set, saree and abaya ourselves, checking the fabric, the finish and how it falls. Our in-house tailors can adjust a ready piece or stitch one to your measurements.</p>
        <p>Shop here, message us on WhatsApp, or come and see us at the store. Please WhatsApp before you visit so we can keep your size ready.</p>
      </>
    ),
  },
  'how-to-order': {
    title: 'How ordering works',
    body: (
      <>
        <h2>1. Add to bag</h2><p>Pick your size and add pieces to your bag.</p>
        <h2>2. Place your order</h2><p>Enter your name, WhatsApp number and address. Your order is saved and opens in WhatsApp with all the details filled in. Just press send.</p>
        <h2>3. We confirm</h2><p>We check stock, tell you the delivery charge and the dispatch date, and answer any fitting questions.</p>
        <h2>4. Pay and relax</h2><p>We send you a secure payment link or UPI details. Once paid, we pack and ship your order, or keep it ready for pick-up at the store.</p>
      </>
    ),
  },
  tailoring: {
    title: 'Custom tailoring',
    body: (
      <>
        <p>Want a different length, sleeve or fit? Our tailors can adjust ready pieces or stitch an outfit to your measurements.</p>
        <p>Message us on WhatsApp with the piece you like and your measurements, or visit the store for a fitting. We will tell you the cost and time before we start.</p>
      </>
    ),
  },
  'size-guide': {
    title: 'Size guide',
    body: (
      <>
        <p>Body measurements in inches. If you are between sizes, choose the larger one; we can take it in for you.</p>
        <table className="sz">
          <thead><tr><th>Size</th><th>Bust</th><th>Waist</th><th>Hip</th></tr></thead>
          <tbody>
            <tr><td>S</td><td>34</td><td>28</td><td>37</td></tr>
            <tr><td>M</td><td>36</td><td>30</td><td>39</td></tr>
            <tr><td>L</td><td>38</td><td>32</td><td>41</td></tr>
            <tr><td>XL</td><td>40</td><td>34</td><td>43</td></tr>
            <tr><td>XXL</td><td>42</td><td>36</td><td>45</td></tr>
          </tbody>
        </table>
        <h2>Abayas</h2><p>Abaya sizes (52 to 58) are the length in inches from shoulder to hem. Measure from the top of your shoulder to just above your ankle.</p>
        <h2>Kids</h2><p>Kids sizes go by age. Send us your child's height on WhatsApp if you are not sure.</p>
      </>
    ),
  },
  shipping: {
    title: 'Shipping policy',
    body: (
      <>
        <p>{updated}</p>
        <h2>Where we ship</h2><p>We ship across India. You can also pick up your order from our store in Ambalathara, Thiruvananthapuram.</p>
        <h2>Delivery charge and time</h2><p>We confirm the delivery charge and the dispatch date on WhatsApp before you pay. Delivery times are estimates and can be affected by the courier, weather or holidays.</p>
        <h2>Tracking</h2><p>Once your order ships, we send the tracking number on WhatsApp where the courier provides one.</p>
        <h2>Address</h2><p>Please check your address and pincode. If you need to change it, message us as soon as possible.</p>
      </>
    ),
  },
  returns: {
    title: 'Returns and refunds',
    body: (
      <>
        <p>{updated}</p>
        <h2>Damaged or wrong item</h2><p>Please check your order when it arrives. If an item is damaged, defective or not what you ordered, message us on WhatsApp straight away with a photo and we will make it right.</p>
        <h2>Returns and exchanges</h2><p>Contact us before sending anything back so we can tell you whether the item can be returned or exchanged. Items must be unworn and unwashed, with tags and original packaging. Custom-tailored and altered pieces cannot be returned. Unless the item was damaged or wrong, return shipping is paid by you.</p>
        <h2>Refunds</h2><p>We tell you once we receive and check your return. Approved refunds go back to your original payment method. Your bank may take a few days to show it.</p>
      </>
    ),
  },
  privacy: {
    title: 'Privacy policy',
    body: (
      <>
        <p>{updated}</p>
        <h2>What we collect</h2><p>When you place an order we collect your name, WhatsApp number and delivery address, and the items you order. We do not collect or store card or UPI details.</p>
        <h2>How we use it</h2><p>Only to confirm, deliver and support your order, and to reply when you message us. We share your address and phone number only with the courier delivering your order.</p>
        <h2>Where it is kept</h2><p>Orders are stored securely with our hosting provider (Vercel). Your browser also remembers your bag and delivery details on your own device to save you typing.</p>
        <h2>Your choices</h2><p>Ask us on WhatsApp or by email to see, correct or delete your information.</p>
        <h2>Contact</h2><p>{STORE.owner}, {STORE.name}, {STORE.address}. {STORE.phoneDisplay} · {STORE.email}</p>
      </>
    ),
  },
  terms: {
    title: 'Terms of service',
    body: (
      <>
        <p>{updated}</p>
        <p>This website is run by {STORE.name}, owned by {STORE.owner}, {STORE.address}.</p>
        <h2>Orders</h2><p>Placing an order on this site is a request to buy. An order is confirmed only when we confirm it with you on WhatsApp and payment is received. We may decline an order, for example if an item is out of stock.</p>
        <h2>Prices and products</h2><p>Prices are in Indian rupees and include tax. Delivery is charged separately and confirmed before you pay. Colours can look slightly different on different screens.</p>
        <h2>Content</h2><p>All text, photos and logos on this site belong to {STORE.name} and may not be copied without permission.</p>
        <h2>Law</h2><p>These terms are governed by the laws of India. Courts in Thiruvananthapuram, Kerala have jurisdiction.</p>
        <h2>Questions and complaints</h2><p>Contact {STORE.owner} at {STORE.email} or {STORE.phoneDisplay}. We reply within 48 hours.</p>
      </>
    ),
  },
  contact: {
    title: 'Contact us',
    body: (
      <>
        <p>Questions about a piece, a size or an occasion? We reply fastest on WhatsApp.</p>
        <div className="contact-cards" style={{ marginTop: 16 }}>
          <a href={waLink('Hi Ababeel!')} target="_blank" rel="noopener"><MessageCircle size={22} /><span><b>WhatsApp</b><small>{STORE.phoneDisplay} · fastest reply</small></span></a>
          <a href={`tel:+${STORE.whatsapp}`}><Phone size={22} /><span><b>Call the store</b><small>{STORE.phoneDisplay}</small></span></a>
          <a href={`mailto:${STORE.email}`}><Mail size={22} /><span><b>Email</b><small>{STORE.email}</small></span></a>
          <a href={STORE.mapsUrl} target="_blank" rel="noopener"><MapPin size={22} /><span><b>Visit us</b><small>{STORE.address}. Open daily; please WhatsApp before visiting.</small></span></a>
          <a href={`https://instagram.com/${STORE.instagram}`} target="_blank" rel="noopener"><Camera size={22} /><span><b>Instagram</b><small>@{STORE.instagram}</small></span></a>
        </div>
      </>
    ),
  },
  '404': {
    title: 'Page not found',
    body: <><p>That page doesn't exist. </p><p><a href="#/">Go to the home page</a></p></>,
  },
}

export default function Info({ page }: { page?: string }) {
  const p = PAGES[page ?? ''] ?? PAGES['404']
  return (
    <div className="wrap">
      <article className="page">
        <h1 style={{ fontSize: 'clamp(32px, 8vw, 48px)' }}>{p.title}</h1>
        {p.body}
      </article>
    </div>
  )
}

const LINKS: [string, string, typeof Store][] = [
  ['how-to-order', 'How ordering works', HelpCircle],
  ['size-guide', 'Size guide', Ruler],
  ['tailoring', 'Custom tailoring', Scissors],
  ['about', 'Our story', Store],
  ['contact', 'Contact and store address', MapPin],
  ['shipping', 'Shipping policy', Truck],
  ['returns', 'Returns and refunds', Undo2],
  ['privacy', 'Privacy policy', ShieldCheck],
  ['terms', 'Terms of service', FileText],
]

export function More() {
  const { theme, setTheme } = useStore()
  const next = theme === 'system' ? 'dark' : theme === 'dark' ? 'light' : 'system'
  return (
    <div className="wrap" style={{ paddingTop: 20, display: 'grid', gap: 16 }}>
      <h1 style={{ fontSize: 40 }}>More</h1>
      <div className="list">
        {LINKS.map(([id, label, Icon]) => <a key={id} href={`#/info/${id}`}><Icon size={20} />{label}<ChevronRight className="chev" size={18} /></a>)}
      </div>
      <div className="list">
        <button onClick={() => setTheme(next)}><Moon size={20} />Theme: {theme === 'system' ? 'Match phone' : theme === 'dark' ? 'Dark' : 'Light'}<ChevronRight className="chev" size={18} /></button>
        <a href="#/admin"><Lock size={20} />Store admin<ChevronRight className="chev" size={18} /></a>
      </div>
      <p className="muted" style={{ fontSize: 13 }}>{STORE.name} · {STORE.address}</p>
    </div>
  )
}
