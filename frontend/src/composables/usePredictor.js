import { ref } from 'vue'

// Build-time configurable. For local dev, leave empty so /api hits the Vite proxy.
// For the Android APK, set VITE_API_BASE to your hosted backend (e.g. https://baby-sign.example.com).
const API_BASE = import.meta.env.VITE_API_BASE || ''

export function usePredictor() {
  const prediction = ref({ has_hand: false, label: null, confidence: 0 })
  const error = ref(null)
  let inFlight = false

  async function predict(base64Jpeg) {
    if (inFlight) return
    inFlight = true
    try {
      const res = await fetch(`${API_BASE}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64Jpeg })
      })
      if (!res.ok) throw new Error('HTTP ' + res.status)
      prediction.value = await res.json()
      error.value = null
    } catch (e) {
      error.value = e.message || String(e)
    } finally {
      inFlight = false
    }
  }

  return { prediction, error, predict }
}
