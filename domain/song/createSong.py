from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from domain.prompt.prompt import prompt_openai
from domain.song.interpolate import generate_audio

router = APIRouter()

class SongRequest(BaseModel):
    captions: list[str]
    duration_sec: int = 30

@router.post("/generate/song")
def generate_song(req: SongRequest):
    try:
        prompts = prompt_openai(req.captions)
        steps = max(3, req.duration_sec // 10)  # 10초당 프레임 1개라고 가정
        audio_base64 = generate_audio(prompts, steps=steps)
        return {"audio_base64": audio_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
