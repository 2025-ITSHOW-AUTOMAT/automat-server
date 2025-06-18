FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/app/.cache/huggingface/transformers \
    HF_HOME=/app/.cache/huggingface \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-venv python3.10-dev python3-pip \
    git ffmpeg libsndfile1 libsm6 libxext6 curl unzip \
    && rm -rf /var/lib/apt/lists/*

# python 명령어를 python3.10으로 연결
RUN ln -sf /usr/bin/python3.10 /usr/bin/python && python -m pip install --upgrade pip setuptools

# requirements 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 코드 복사
COPY . /app

# 포트 열기 (FastAPI)
EXPOSE 8080

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
