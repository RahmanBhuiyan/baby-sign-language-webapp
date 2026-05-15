import os
import threading

import requests
import torch
import torch.nn as nn
from torchvision.models import resnet18

LABELS = [
    "dont_know", "down", "drink", "eat", "frustrated", "i_love_you",
    "mad_grumpy", "milk", "mine", "mom", "potty", "sorry",
]
NUM_CLASSES = len(LABELS)

# Auto-download source: the original research repo (raw blob URL).
_MODEL_URL = (
    "https://github.com/RoxyDiya/BABY-SIGN-LANGUAGE-RECOGNITION/raw/main/"
    "Code/Trained%20Model/signlanguage_model.pth"
)
_MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
_MODEL_PATH = os.path.join(_MODELS_DIR, "signlanguage_model.pth")


class ResNet18CustomClassifier(nn.Module):
    def __init__(self, num_classes: int):
        super().__init__()
        self.resnet18 = resnet18(weights=None)
        in_features = self.resnet18.fc.in_features
        self.resnet18.fc = nn.Identity()
        self.custom_classifier = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        x = self.resnet18(x)
        return self.custom_classifier(x)


def _ensure_weights() -> str:
    if os.path.isfile(_MODEL_PATH):
        return _MODEL_PATH
    os.makedirs(_MODELS_DIR, exist_ok=True)
    print(f"Downloading trained model weights to {_MODEL_PATH} (~44 MB) ...")
    with requests.get(_MODEL_URL, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(_MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
    print("Model weights downloaded.")
    return _MODEL_PATH


_model = None
_lock = threading.Lock()


def get_model() -> ResNet18CustomClassifier:
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        path = _ensure_weights()
        model = ResNet18CustomClassifier(NUM_CLASSES)
        state = torch.load(path, map_location="cpu")
        model.load_state_dict(state)
        model.eval()
        _model = model
        return _model
