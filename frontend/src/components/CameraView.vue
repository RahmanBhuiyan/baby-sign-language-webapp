<script setup>
import { ref, onBeforeUnmount } from 'vue'

const emit = defineEmits(['frame', 'error'])
const props = defineProps({
  intervalMs: { type: Number, default: 200 },
  jpegQuality: { type: Number, default: 0.7 }
})

const videoEl = ref(null)
const started = ref(false)
const cameraError = ref(null)
let stream = null
let timer = null
const canvas = document.createElement('canvas')

async function start() {
  cameraError.value = null
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
      audio: false
    })
    videoEl.value.srcObject = stream
    await videoEl.value.play()
    started.value = true
    timer = setInterval(captureFrame, props.intervalMs)
  } catch (e) {
    cameraError.value = e.message || 'Could not access camera'
    emit('error', cameraError.value)
  }
}

function captureFrame() {
  const v = videoEl.value
  if (!v || v.readyState < 2) return
  canvas.width = v.videoWidth
  canvas.height = v.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(v, 0, 0, canvas.width, canvas.height)
  const data = canvas.toDataURL('image/jpeg', props.jpegQuality)
  emit('frame', data)
}

function stop() {
  if (timer) { clearInterval(timer); timer = null }
  if (stream) {
    stream.getTracks().forEach(t => t.stop())
    stream = null
  }
  started.value = false
}

onBeforeUnmount(stop)
defineExpose({ start, stop })
</script>

<template>
  <div class="camera-view">
    <video ref="videoEl" playsinline muted></video>
    <button v-if="!started" class="start-btn" @click="start">
      <span class="start-emoji">📷</span>
      <span>Start camera</span>
    </button>
    <p v-if="cameraError" class="cam-error">{{ cameraError }}</p>
  </div>
</template>

<style scoped>
.camera-view {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #1a1a2e;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1); /* mirror like a selfie */
}
.start-btn {
  position: absolute;
  inset: 0;
  margin: auto;
  width: 220px;
  height: 80px;
  border: none;
  border-radius: 18px;
  background: #ff7eb6;
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(255,126,182,0.45);
}
.start-btn:hover { background: #ff5fa3; }
.start-emoji { font-size: 1.8rem; }
.cam-error {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  background: rgba(255,0,0,0.85);
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  margin: 0;
}
</style>
