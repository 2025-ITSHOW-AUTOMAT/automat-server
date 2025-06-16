FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/app/.cache/huggingface/transformers \
    HF_HOME=/app/.cache/huggingface

ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt update && apt install -y \
    python3.10 python3.10-venv python3.10-dev python3-pip \
    git ffmpeg libsndfile1 libsm6 libxext6 curl unzip \
    && apt clean

RUN python3.10 -m pip install --upgrade pip setuptools
RUN pip install --no-cache-dir "diffusers@git+https://github.com/huggingface/diffusers.git@8adc6003ba4dbf5b61bb4f1ce571e9e55e145a99"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/yourusername/your-repo.git /app/project

WORKDIR /app/project

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

