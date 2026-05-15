import { ref } from 'vue'

export function usePredictor() {
  const prediction = ref({ has_hand: false, label: null, confidence: 0 })
  const error = ref(null)
  let inFlight = false

  async function predict(base64Jpeg) {
    if (inFlight) return
    inFlight = true
    try {
      const res = await fetch('/api/predict', {
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
