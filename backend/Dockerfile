# Baby Sign Helper backend — production image for Hugging Face Spaces.
# Follows HF's required non-root user pattern (uid 1000).
# Model weights are auto-downloaded on first request (~30 s) — keeping the
# build step pure pip so it can't fail on flaky outbound network.

FROM python:3.11-slim

# --- OS deps (must run as root) ---------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# --- Non-root user (HF Spaces requirement) ----------------------------
RUN useradd -m -u 1000 appuser

USER appuser

ENV HOME=/home/appuser \
    PATH=/home/appuser/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=7860

WORKDIR /home/appuser/app

# --- Python deps (CPU-only torch to keep image lean) ------------------
COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir --user \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r requirements.txt

# --- App source --------------------------------------------------------
COPY --chown=appuser:appuser model_loader.py hand_detector.py inference.py app.py ./

# --- Runtime ----------------------------------------------------------
# Both model files (44 MB ResNet weights + 8 MB MediaPipe task) are
# auto-downloaded on first request via the existing _ensure_weights()
# and _ensure_model_file() helpers. That takes ~30 s once per container
# lifetime.
EXPOSE 7860

CMD ["python", "-m", "gunicorn", \
     "--workers", "1", \
     "--worker-class", "gthread", \
     "--threads", "4", \
     "--bind", "0.0.0.0:7860", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "app:app"]
