# Baby Sign Helper backend — production image for Hugging Face Spaces.
# Pre-downloads both models at build time so cold starts don't pay the
# 50+ MB download cost on the first request.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860 \
    HF_HOME=/tmp/hf

# OS deps needed by opencv-python (libGL, libgthread)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps. Force the CPU-only PyTorch index so we don't pull
# ~1 GB of CUDA wheels we'd never use on HF Spaces' CPU runtime.
COPY requirements.txt ./
RUN pip install --no-cache-dir \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r requirements.txt

# Copy app source.
COPY model_loader.py hand_detector.py inference.py app.py ./

# Pre-bake both models into the image (44 MB ResNet weights + ~8 MB
# MediaPipe hand-landmarker task). First request will be fast.
RUN python -c "from model_loader import get_model; from hand_detector import get_detector; get_model(); get_detector(); print('Models pre-loaded.')"

EXPOSE 7860

# One worker — model is loaded once into memory.
# Threads handle concurrent inference requests cheaply (GIL-released
# inside torch / opencv kernels).
CMD ["gunicorn", \
     "--workers", "1", \
     "--worker-class", "gthread", \
     "--threads", "4", \
     "--bind", "0.0.0.0:7860", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "app:app"]
