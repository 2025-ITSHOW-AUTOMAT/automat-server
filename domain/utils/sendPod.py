import os
import requests
from dotenv import load_dotenv

load_dotenv()

RUNPOD_URL = os.getenv("RUNPOD_URL")
RUNPOD = f"{RUNPOD_URL}/generate/song_prompt"

def send_runpod(image_paths: list[str]) -> dict:
    try:
        response = requests.post(
            RUNPOD,
            json=image_paths,
            timeout=3000000
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[RunPod 요청 실패] {e}")
        return {
            "base_prompts": [],
            "song_prompts": []
        }
