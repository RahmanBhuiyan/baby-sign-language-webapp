<script setup>
const props = defineProps({
  modelValue: { type: Boolean, default: true },
  supported:  { type: Boolean, default: true }
})
defineEmits(['update:modelValue'])
</script>

<template>
  <button
    class="speak-toggle"
    :class="{ on: modelValue, disabled: !supported }"
    :disabled="!supported"
    :title="supported ? 'Toggle spoken word' : 'Speech not supported in this browser'"
    @click="$emit('update:modelValue', !modelValue)"
  >
    <span class="icon">{{ modelValue && supported ? '🔊' : '🔈' }}</span>
    <span class="text">{{ modelValue && supported ? 'Voice on' : 'Voice off' }}</span>
  </button>
</template>

<style scoped>
.speak-toggle {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  border: 2px solid #e6e0f2;
  background: white;
  color: #555;
  padding: 0.55rem 1rem;
  border-radius: 999px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.speak-toggle.on {
  background: #ff7eb6;
  border-color: #ff7eb6;
  color: white;
}
.speak-toggle.disabled { opacity: 0.5; cursor: not-allowed; }
.icon { font-size: 1.1rem; }
</style>
