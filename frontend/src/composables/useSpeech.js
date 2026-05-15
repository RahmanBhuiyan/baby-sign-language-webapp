import { ref } from 'vue'
import { LABEL_INFO } from '../constants/labels.js'

const REPEAT_SUPPRESS_MS = 2000

export function useSpeech() {
  const enabled = ref(true)
  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window
  let lastSpoken = null
  let lastSpokenAt = 0

  function speak(labelKey) {
    if (!enabled.value || !supported || !labelKey) return
    const now = Date.now()
    if (labelKey === lastSpoken && (now - lastSpokenAt) < REPEAT_SUPPRESS_MS) return

    const phrase = LABEL_INFO[labelKey]?.pretty ?? labelKey
    const utter = new SpeechSynthesisUtterance(phrase)
    utter.rate = 0.95
    utter.pitch = 1.1
    window.speechSynthesis.cancel()
    window.speechSynthesis.speak(utter)

    lastSpoken = labelKey
    lastSpokenAt = now
  }

  return { enabled, supported, speak }
}
