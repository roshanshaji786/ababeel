import type { Product } from './types.js'

const WOMEN = ['S', 'M', 'L', 'XL', 'XXL']
const FREE = ['Free size']
const t = '2026-10-21T00:00:00.000Z'

/** Sample catalogue. Shown before the network answers and written to storage on first run. */
export const SEED_PRODUCTS: Product[] = [
  {
    id: 'p-maroon-anarkali', slug: 'maroon-zari-anarkali', name: 'Maroon Zari Anarkali Suit', category: 'festive',
    price: 2450, mrp: 2950, sizes: WOMEN, soldOutSizes: ['XXL'],
    images: ['/img/maroon-anarkali.webp'],
    description: 'A floor-length anarkali in deep maroon with gold zari work on the yoke and hem, paired with a sheer embroidered dupatta. Made for weddings, Eid and evening functions.',
    fabric: 'Georgette with zari embroidery, cotton lining', care: 'Dry clean only',
    featured: true, active: true, createdAt: t,
  },
  {
    id: 'p-rose-saree', slug: 'rose-silk-saree', name: 'Rose Gold Silk Saree', category: 'festive',
    price: 3200, mrp: 3800, sizes: FREE, soldOutSizes: [],
    images: ['/img/rose-saree.webp'],
    description: 'Soft rose silk with a woven gold and magenta border and rich pallu. Comes with an unstitched blouse piece; we can stitch it to your size.',
    fabric: 'Art silk, woven zari border', care: 'Dry clean only',
    featured: true, active: true, createdAt: t,
  },
  {
    id: 'p-mauve-kurta', slug: 'mauve-kurta-set', name: 'Mauve Kurta Set with Dupatta', category: 'women',
    price: 1650, sizes: WOMEN, soldOutSizes: [],
    images: ['/img/mauve-kurta.webp'],
    description: 'A straight mauve kurta with tonal thread work, ivory pants and a light dupatta. Easy enough for the office, pretty enough for a family visit.',
    fabric: 'Cotton silk', care: 'Gentle hand wash, dry in shade',
    featured: true, active: true, createdAt: t,
  },
  {
    id: 'p-plum-churidar', slug: 'plum-silk-churidar-set', name: 'Plum Silk Churidar Set', category: 'women',
    price: 1850, sizes: WOMEN, soldOutSizes: ['S'],
    images: ['/img/plum-churidar.webp'],
    description: 'Plum churidar set with gold buttas and a matching dupatta with a woven border. A rich colour for festive days.',
    fabric: 'Silk blend', care: 'Dry clean recommended',
    featured: false, active: true, createdAt: t,
  },
  {
    id: 'p-grey-abaya', slug: 'grey-hooded-abaya', name: 'Grey Hooded Abaya', category: 'modest',
    price: 1500, sizes: ['52', '54', '56', '58'], soldOutSizes: [],
    images: ['/img/grey-abaya.webp'],
    description: 'A flowing hooded abaya in soft grey with a built-in hood and wide sleeves. Light enough for every day.',
    fabric: 'Nida', care: 'Machine wash cold, gentle cycle',
    featured: true, active: true, createdAt: t,
  },
  {
    id: 'p-maroon-jacket', slug: 'maroon-dress-embroidered-jacket', name: 'Maroon Dress with Embroidered Jacket', category: 'coord',
    price: 890, sizes: ['S', 'M', 'L', 'XL'], soldOutSizes: [],
    images: ['/img/maroon-jacket-dress.webp'],
    description: 'A long maroon dress layered with a short jacket covered in tonal embroidery. Wear them together or apart.',
    fabric: 'Rayon', care: 'Hand wash cold',
    featured: false, active: true, createdAt: t,
  },
  {
    id: 'p-sage-set', slug: 'sage-embroidered-skirt-set', name: 'Sage Embroidered Top and Skirt Set', category: 'coord',
    price: 700, sizes: ['S', 'M', 'L', 'XL'], soldOutSizes: [],
    images: ['/img/sage-skirt-set.webp'],
    description: 'A sage green flared skirt with a printed, embroidered crop top. Fresh, light and easy to style.',
    fabric: 'Cotton blend', care: 'Hand wash cold',
    featured: false, active: true, createdAt: t,
  },
  {
    id: 'p-kids-festive', slug: 'kids-festive-pavada-kurta', name: 'Kids Festive Pavada and Kurta', category: 'kids',
    price: 1150, sizes: ['2-3Y', '4-5Y', '6-7Y', '8-9Y'], soldOutSizes: [],
    images: ['/img/kids-festive.webp'],
    description: 'Matching festive wear for siblings: a cream and maroon pavada set for girls, or a printed kurta with maroon pants for boys. Mention which one in your order note.',
    fabric: 'Cotton silk', care: 'Gentle hand wash',
    featured: true, active: true, createdAt: t,
  },
]
