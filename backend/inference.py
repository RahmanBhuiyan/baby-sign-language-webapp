import base64
import io

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from hand_detector import find_hand_bbox
from model_loader import get_model, LABELS

IMG_SIZE = 224
OFFSET = 20

_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


def _decode_image(data_url_or_b64: str) -> np.ndarray:
    if "," in data_url_or_b64:
        data_url_or_b64 = data_url_or_b64.split(",", 1)[1]
    raw = base64.b64decode(data_url_or_b64)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def predict(image_b64: str) -> dict:
    img = _decode_image(image_b64)
    bbox = find_hand_bbox(img)

    if bbox is None:
        return {"has_hand": False, "label": None, "confidence": 0.0}

    x, y, w, h = bbox
    H, W = img.shape[:2]
    x1 = max(0, x - OFFSET)
    y1 = max(0, y - OFFSET)
    x2 = min(W, x + w + OFFSET)
    y2 = min(H, y + h + OFFSET)
    crop = img[y1:y2, x1:x2]
    if crop.size == 0:
        return {"has_hand": False, "label": None, "confidence": 0.0}

    resized = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
    tensor = _transform(resized).unsqueeze(0)

    model = get_model()
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]
        idx = int(torch.argmax(probs).item())
        confidence = float(probs[idx].item())

    return {
        "has_hand": True,
        "label": LABELS[idx],
        "confidence": round(confidence, 4),
    }
