from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

HF_API_TOKEN = os.getenv("hf_api_token")
API_URL = "https://api-inference.huggingface.co/models/riffusion/riffusion-model-v1"

class SongRequest(BaseModel):
    prompts: list[str]
    genre: str
    duration_sec: int = 45

@router.post("/generate")
def generate_song(req: SongRequest):
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }

    joined_prompt = " | ".join(req.prompts) + f" | {req.genre} instrumental music"
    payload = {
        "inputs": joined_prompt,
        "parameters": {
            "duration": req.duration_sec,
            "interpolation": True
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        print("Riffusion API status:", response.status_code)
        print("Riffusion API response text:", response.text)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Riffusion API error: {response.text}")

        data = response.json()
        print("Parsed JSON response:", data)

        audio_base64 = data.get("audio_base64") or data.get("audio")
        if not audio_base64:
            raise HTTPException(status_code=500, detail="No audio data returned from Riffusion")

        print(f"audio_base64 length: {len(audio_base64)}")

        # base64 디코딩 후 실제 mp3 파일로 저장 (임시 확인용)
        audio_data = base64.b64decode(audio_base64)
        test_file_path = "test_output.mp3"
        with open(test_file_path, "wb") as f:
            f.write(audio_data)
        print(f"Audio file saved as {test_file_path}")

        return {"audio_base64": audio_base64}

    except Exception as e:
        print("Exception in Riffusion request:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")