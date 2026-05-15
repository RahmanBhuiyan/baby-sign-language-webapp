"""Thin wrapper around MediaPipe Tasks HandLandmarker.

Replaces cvzone's legacy detector (which relied on the removed
mediapipe.solutions API). Auto-downloads the .task model on first use.
"""
import os
import threading
from typing import Optional

import numpy as np
import requests
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
_MODEL_FILENAME = "hand_landmarker.task"
_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
_MODEL_PATH = os.path.join(_MODEL_DIR, _MODEL_FILENAME)

_detector: Optional[mp_vision.HandLandmarker] = None
_lock = threading.Lock()


def _ensure_model_file() -> str:
    if os.path.isfile(_MODEL_PATH):
        return _MODEL_PATH
    os.makedirs(_MODEL_DIR, exist_ok=True)
    print(f"Downloading hand_landmarker.task to {_MODEL_PATH} ...")
    r = requests.get(_MODEL_URL, timeout=60)
    r.raise_for_status()
    with open(_MODEL_PATH, "wb") as f:
        f.write(r.content)
    print("Hand landmarker model downloaded.")
    return _MODEL_PATH


def get_detector() -> mp_vision.HandLandmarker:
    global _detector
    if _detector is not None:
        return _detector
    with _lock:
        if _detector is not None:
            return _detector
        path = _ensure_model_file()
        options = mp_vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=path),
            running_mode=mp_vision.RunningMode.IMAGE,
            num_hands=1,
            min_hand_detection_confidence=0.5,
        )
        _detector = mp_vision.HandLandmarker.create_from_options(options)
        return _detector


def find_hand_bbox(bgr_image: np.ndarray) -> Optional[tuple[int, int, int, int]]:
    """Return (x, y, w, h) in pixel coords for the first detected hand, or None."""
    detector = get_detector()
    rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_image)
    if not result.hand_landmarks:
        return None
    landmarks = result.hand_landmarks[0]
    H, W = bgr_image.shape[:2]
    xs = [lm.x * W for lm in landmarks]
    ys = [lm.y * H for lm in landmarks]
    x_min, x_max = max(0, int(min(xs))), min(W, int(max(xs)))
    y_min, y_max = max(0, int(min(ys))), min(H, int(max(ys)))
    w = x_max - x_min
    h = y_max - y_min
    if w <= 0 or h <= 0:
        return None
    return x_min, y_min, w, h
