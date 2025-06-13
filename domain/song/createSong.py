from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from domain.prompt.prompt import prompt_openai
from domain.song.generateSong import generate_ace_step
from datetime import datetime
import os

router = APIRouter()
UPLOAD_DIR = "uploads/song"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class SongRequest(BaseModel):
    song_prompt: list[str]
    duration_sec: int = 45


@router.post("/generate")
def generate_song(req: SongRequest):
    try:
        song_prompts = prompt_openai(req.song_prompt)
        wav_bytes = generate_ace_step(req.song_prompt, req.duration_sec)

        date_str = datetime.now().strftime("%y%m%d")
        experience_id = get_date(date_str)

        filename = f"{date_str}_{experience_id}.wav"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(wav_bytes)

        song_path = file_path.replace("\\", "/")

        return {"song_path": song_path}
    except Exception as e:
        print("generate_song error:", e)
        raise HTTPException(status_code=500, detail=str(e))


def get_date(date: str) -> int:
    files = os.listdir(UPLOAD_DIR)
    return sum(1 for f in files if f.startswith(date)) + 1
