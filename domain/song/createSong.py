from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from domain.prompt.prompt import prompt_openai
from domain.song.ace_step_wrapper import ACEWrapper
from domain.song.utils.saveSong import song_path

router = APIRouter()
wrapper = ACEWrapper()

class SongRequest(BaseModel):
    song_prompt: list[str]
    duration_sec: float = 60.0
    lora_path: str | None = None
    lora_weight: float = 1.0
    infer_steps: int = 100

@router.post("/generate")
def generate_song(req: SongRequest):
    try:
        prompt = prompt_openai(req.song_prompt)
        save_path = song_path()

        result = wrapper.generate(
            prompt=prompt,
            lyrics="",
            duration=req.duration_sec,
            save_path=save_path,
            lora_path=req.lora_path,
            lora_weight=req.lora_weight,
            infer_steps=req.infer_steps
        )

        return {
            "message": "성공적으로 생성 완료",
            "song_path": result["audio_path"].replace("\\", "/"),
            "metadata_path": result["metadata_path"].replace("\\", "/")
        }

    except Exception as e:
        print("generate_song error:", e)
        raise HTTPException(status_code=500, detail=str(e))
