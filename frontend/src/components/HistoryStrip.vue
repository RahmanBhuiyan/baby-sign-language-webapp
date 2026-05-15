<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { LABEL_INFO } from '../constants/labels.js'

defineProps({
  items: { type: Array, default: () => [] }
})

const now = ref(Date.now())
let timer = null
onMounted(() => { timer = setInterval(() => { now.value = Date.now() }, 1000) })
onBeforeUnmount(() => clearInterval(timer))

function ago(t) {
  const s = Math.max(0, Math.floor((now.value - t) / 1000))
  if (s < 60) return s + 's'
  const m = Math.floor(s / 60)
  return m + 'm'
}

function emoji(key) { return LABEL_INFO[key]?.emoji ?? '✨' }
function pretty(key) { return LABEL_INFO[key]?.pretty ?? key }
</script>

<template>
  <div class="history-strip">
    <div class="title">Recent signs</div>
    <div class="chips">
      <div v-if="items.length === 0" class="placeholder">— nothing yet —</div>
      <div v-for="(it, i) in items" :key="it.at" class="chip" :class="{ first: i === 0 }">
        <span class="emoji">{{ emoji(it.label) }}</span>
        <span class="name">{{ pretty(it.label) }}</span>
        <span class="time">{{ ago(it.at) }} ago</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-strip {
  background: white;
  border-radius: 18px;
  padding: 1rem 1.25rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
.title {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #888;
  margin-bottom: 0.6rem;
}
.chips {
  display: flex;
  gap: 0.6rem;
  overflow-x: auto;
  padding-bottom: 0.2rem;
}
.chip {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 84px;
  padding: 0.6rem 0.8rem;
  background: #f7f3ff;
  border-radius: 14px;
}
.chip.first {
  background: #ffe9f3;
  outline: 2px solid #ff7eb6;
}
.chip .emoji { font-size: 1.8rem; line-height: 1; }
.chip .name { font-size: 0.95rem; font-weight: 700; color: #2d2d44; margin-top: 0.15rem; }
.chip .time { font-size: 0.75rem; color: #999; margin-top: 0.1rem; font-variant-numeric: tabular-nums; }
.placeholder { color: #aaa; font-size: 0.95rem; padding: 0.4rem 0; }
</style>
