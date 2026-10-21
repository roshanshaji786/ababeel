const inr = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 })
export const money = (n: number) => inr.format(n)

const dt = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', timeZone: 'Asia/Kolkata' })
export const when = (iso: string) => dt.format(new Date(iso))

export const offPct = (price: number, mrp?: number) => (mrp && mrp > price ? Math.round((1 - price / mrp) * 100) : 0)

/** Smaller version of a bundled image for grids. Uploaded images are returned as-is. */
export const thumb = (src: string) => (src.startsWith('/img/') ? src.replace(/\.webp$/, '-sm.webp') : src)
