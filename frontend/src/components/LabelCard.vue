<script setup>
import { computed } from 'vue'
import { LABEL_INFO, HIGH_CONF, MIN_CONF } from '../constants/labels.js'

const props = defineProps({
  hasHand:    { type: Boolean, default: false },
  label:      { type: String,  default: null },
  confidence: { type: Number,  default: 0 }
})

const info = computed(() =>
  props.label && LABEL_INFO[props.label]
    ? LABEL_INFO[props.label]
    : null
)

const state = computed(() => {
  if (!props.hasHand) return 'no-hand'
  if (props.confidence >= HIGH_CONF) return 'high'
  if (props.confidence >= MIN_CONF)  return 'medium'
  return 'low'
})

const barColor = computed(() => ({
  high: '#48c774',
  medium: '#ffd166',
  low: '#cccccc',
  'no-hand': '#cccccc'
})[state.value])

const pct = computed(() => Math.round(props.confidence * 100))
</script>

<template>
  <div class="label-card" :class="state">
    <template v-if="state === 'no-hand'">
      <div class="emoji">👀</div>
      <div class="text">Looking for hands…</div>
    </template>
    <template v-else-if="state === 'low'">
      <div class="emoji">👋</div>
      <div class="text">Show me a sign</div>
    </template>
    <template v-else>
      <div class="emoji">{{ info?.emoji ?? '✨' }}</div>
      <div class="text">{{ info?.pretty ?? label }}</div>
      <div class="bar-wrap">
        <div class="bar" :style="{ width: pct + '%', background: barColor }"></div>
      </div>
      <div class="pct">{{ pct }}%</div>
    </template>
  </div>
</template>

<style scoped>
.label-card {
  background: white;
  border-radius: 18px;
  padding: 1.5rem 1.25rem 1.25rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
  text-align: center;
  transition: transform 0.15s ease;
}
.label-card.high { transform: scale(1.02); }
.emoji {
  font-size: 4.5rem;
  line-height: 1;
  margin-bottom: 0.3rem;
}
.text {
  font-size: 2.4rem;
  font-weight: 800;
  color: #2d2d44;
  letter-spacing: -0.01em;
}
.bar-wrap {
  margin-top: 1rem;
  height: 14px;
  background: #f1f1f5;
  border-radius: 999px;
  overflow: hidden;
}
.bar {
  height: 100%;
  transition: width 0.25s ease, background 0.25s ease;
  border-radius: 999px;
}
.pct {
  margin-top: 0.4rem;
  font-size: 0.95rem;
  color: #777;
  font-variant-numeric: tabular-nums;
}
</style>
