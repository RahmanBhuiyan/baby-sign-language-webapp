<script setup>
import { watch } from 'vue'
import CameraView    from './components/CameraView.vue'
import LabelCard     from './components/LabelCard.vue'
import HistoryStrip  from './components/HistoryStrip.vue'
import SpeakToggle   from './components/SpeakToggle.vue'
import { usePredictor } from './composables/usePredictor.js'
import { useSpeech }    from './composables/useSpeech.js'
import { useHistory }   from './composables/useHistory.js'
import { HIGH_CONF }    from './constants/labels.js'

const { prediction, error, predict } = usePredictor()
const { enabled: speakOn, supported: speechSupported, speak } = useSpeech()
const { items: history, add: addHistory } = useHistory()

function onFrame(dataUrl) { predict(dataUrl) }

watch(prediction, (p) => {
  if (p.has_hand && p.label && p.confidence >= HIGH_CONF) {
    addHistory(p.label)
    speak(p.label)
  }
})
</script>

<template>
  <div class="page">
    <header class="header">
      <h1>👶 Baby Sign Helper</h1>
      <SpeakToggle v-model="speakOn" :supported="speechSupported" />
    </header>

    <main class="stack">
      <CameraView @frame="onFrame" :interval-ms="200" />
      <LabelCard
        :has-hand="prediction.has_hand"
        :label="prediction.label"
        :confidence="prediction.confidence"
      />
      <HistoryStrip :items="history" />
      <p v-if="error" class="net-error">⚠️ {{ error }}</p>
      <p class="hint">Hold one hand clearly in the camera view. The app reads the sign and shows it here.</p>
    </main>
  </div>
</template>

<style scoped>
.page {
  max-width: 720px;
  margin: 0 auto;
  padding: 1rem 1rem 2rem;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.header h1 {
  font-size: 1.6rem;
  margin: 0;
  color: #2d2d44;
  letter-spacing: -0.01em;
}
.stack { display: flex; flex-direction: column; gap: 1rem; }
.net-error {
  background: #ffefef;
  color: #b00020;
  padding: 0.6rem 0.9rem;
  border-radius: 10px;
  margin: 0;
}
.hint {
  text-align: center;
  color: #888;
  font-size: 0.9rem;
  margin: 0.3rem 0 0;
}
@media (max-width: 480px) {
  .header h1 { font-size: 1.3rem; }
}
</style>
