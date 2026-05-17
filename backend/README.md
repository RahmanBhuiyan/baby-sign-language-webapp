---
title: Baby Sign Helper API
emoji: 👶
colorFrom: pink
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Baby Sign Helper — Backend API

The Flask + PyTorch backend for the
[Baby Sign Helper](https://github.com/RahmanBhuiyan/baby-sign-language-webapp)
mobile / web app.

Built on top of the [BABY-SIGN-LANGUAGE-RECOGNITION](https://github.com/RoxyDiya/BABY-SIGN-LANGUAGE-RECOGNITION)
research project from Sapienza University of Rome. Reads webcam frames,
finds the hand with MediaPipe, classifies the sign with a fine-tuned
ResNet-18, returns the label and confidence.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET`  | `/api/health`  | Liveness probe — returns `{"status":"ok"}` |
| `POST` | `/api/predict` | Body: `{"image":"data:image/jpeg;base64,..."}` → `{"has_hand":bool,"label":str,"confidence":float}` |

## Recognized signs

`milk 🍼 · eat 🍽️ · drink 🥤 · down ⬇️ · mom 👩 · mine 🙋 · potty 🚽 · sorry 😢 · I love you ❤️ · mad/grumpy 😠 · frustrated 😤 · don't know 🤷`

## Notes for callers

- CORS is wide open — call it from any origin (Capacitor APK, browser, curl…).
- One gunicorn worker, 4 threads. Single-frame inference takes ~150 ms on the
  HF Spaces CPU runtime.
- Both model files (ResNet weights + MediaPipe hand-landmarker) are baked
  into the Docker image, so cold starts don't pay a download tax.
