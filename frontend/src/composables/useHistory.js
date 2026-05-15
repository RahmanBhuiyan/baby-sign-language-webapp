import { ref } from 'vue'

const MAX_ITEMS = 5
const DUP_WINDOW_MS = 3000

export function useHistory() {
  const items = ref([])

  function add(labelKey) {
    const now = Date.now()
    const last = items.value[0]
    if (last && last.label === labelKey && (now - last.at) < DUP_WINDOW_MS) return
    items.value = [{ label: labelKey, at: now }, ...items.value].slice(0, MAX_ITEMS)
  }

  function clear() {
    items.value = []
  }

  return { items, add, clear }
}
