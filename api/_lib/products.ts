import type { Product } from '../../shared/types.js'
import { SEED_PRODUCTS } from '../../shared/seed.js'
import { readJSON, writeJSON } from './store.js'

const PATH = 'db/products.json'

export async function loadProducts(): Promise<Product[]> {
  const data = await readJSON<Product[]>(PATH)
  if (data) return data
  await writeJSON(PATH, SEED_PRODUCTS)
  return SEED_PRODUCTS
}

export const saveProducts = (items: Product[]) => writeJSON(PATH, items)
