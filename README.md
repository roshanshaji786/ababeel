# Ababeel v5

A standalone online store for **Ababeel Fashions** (ethnic and modest wear, Ambalathara, Thiruvananthapuram).
Mobile-first React web app, installable on a phone, hosted free on Vercel. No Shopify, no Supabase.

- **Live:** https://ababeel-v5.vercel.app
- **Admin:** https://ababeel-v5.vercel.app/#/admin (PIN login)

## How it works

| Part | What it uses |
|---|---|
| Frontend | React 19 + TypeScript + Vite, PWA (`vite-plugin-pwa`), zustand, lucide-react, self-hosted fonts (Cormorant Garamond + Manrope) |
| API | Vercel Functions in `api/` |
| Database and photos | Vercel Blob (free Hobby plan, store `ababeel-v5-store`, Mumbai). Products live in `db/products.json`; each order is its own JSON file under `orders/`; uploaded photos under `images/` |
| Admin login | One shared PIN. Only its scrypt hash is stored (`ADMIN_PIN_HASH`); sessions are HMAC-signed tokens (`SESSION_SECRET`) that last 30 days |
| Checkout | The order is saved, then opens in WhatsApp (+91 98959 84721) with every detail filled in. Payment is arranged on WhatsApp; a Razorpay link can be added once Razorpay is activated |

On first run the API writes the sample catalogue from `shared/seed.ts` to Blob. The app also ships that catalogue so the first screen shows products before the network answers.

## Folders

```
api/            products, orders, login, upload (+ _lib: Blob store, auth)
shared/         types, store details (phone, address), seed products
src/views/      Home, Shop, Product, Bag (checkout + thank-you), Info pages, Admin (lazy-loaded)
src/lib/        zustand store, API client, WhatsApp message, formatting
public/img/     brand and sample product photos (WebP, with -sm thumbnails)
scripts/        dev-api.ts (local API with a .localdb folder), hash-pin.mjs
```

## Run locally

```
npm install
npm run api      # API on :3001, stores data in .localdb/, admin PIN is 1234
npm run dev      # app on :5173, proxies /api to :3001
```

## Environment variables (Vercel → Settings → Environment Variables)

- `BLOB_READ_WRITE_TOKEN`: added automatically by the connected Blob store
- `ADMIN_PIN_HASH`: `node scripts/hash-pin.mjs <new pin>` prints it. Change it here to change the PIN, then redeploy
- `SESSION_SECRET`: any long random string. Changing it signs everyone out

## Free-plan limits (Vercel Blob, Hobby)

1 GB storage, 10k simple and 2k advanced operations a month. Every order and every product save is one write; the public product list is cached at the edge for 30 seconds, so shoppers barely touch the quota.

## Not built yet

- Razorpay payment link at checkout (waiting on Razorpay activation)
- Cash on delivery (not offered; the site doesn't promise it)
- Order emails or WhatsApp API notifications (orders arrive as the customer's WhatsApp message and in the admin)
- Custom domain (deliberately: ababeeltvm.com stays on Shopify)
