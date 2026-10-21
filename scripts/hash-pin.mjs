// Usage: node scripts/hash-pin.mjs <pin>  → prints the value for ADMIN_PIN_HASH
import { randomBytes, scryptSync } from 'node:crypto'
const pin = process.argv[2]
if (!pin) { console.error('Usage: node scripts/hash-pin.mjs <pin>'); process.exit(1) }
const salt = randomBytes(16).toString('hex')
console.log(`${salt}:${scryptSync(pin, salt, 32).toString('hex')}`)
