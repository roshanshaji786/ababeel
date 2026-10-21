// localStorage throws in some private modes; never let that break the app.
export function load<T>(key: string, fallback: T): T {
  try {
    const v = localStorage.getItem(key)
    return v ? (JSON.parse(v) as T) : fallback
  } catch { return fallback }
}
export function save(key: string, value: unknown) {
  try { localStorage.setItem(key, JSON.stringify(value)) } catch { /* ignore */ }
}
export function remove(key: string) {
  try { localStorage.removeItem(key) } catch { /* ignore */ }
}
