from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from domain.song.ace_step_wrapper import ACEWrapper
from domain.utils.saveSong import song_path, save_song
from domain.utils.s3 import upload_s3

import os
import traceback

router = APIRouter()
wrapper = ACEWrapper()

class SongRequest(BaseModel):
    song_prompt: str
    duration_sec: float = 60.0
    lora_path: str | None = None
    lora_weight: float = 1.0
    infer_steps: int = 60

@router.post("/generate")
def generate_song(req: SongRequest):
    try:
        prompt = req.song_prompt
        save_path = song_path()

        result = wrapper.generate(
            prompt=prompt,
            duration=req.duration_sec,
            save_path=save_path,
        )

        audio_local = result["audio_path"]
        metadata_local = result["metadata_path"]

        s3_audio_key = f"songs/{os.path.basename(audio_local)}"
        s3_metadata_key = f"metadata/{os.path.basename(metadata_local)}"

        s3_audio_url = upload_s3(audio_local, s3_audio_key)
        s3_metadata_url = upload_s3(metadata_local, s3_metadata_key)

        song_id = save_song(s3_audio_url)

        return {
            "message": "성공적으로 생성 완료",
            "song_id": song_id,
            "song_url": s3_audio_url,
            "metadata_url": s3_metadata_url,
            "filename": os.path.basename(audio_local)
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

