from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.prompt.prompt import generate_prompt, prompt_openai
from domain.prompt.translate import translate_prompt
from domain.utils.s3 import upload_s3
from domain.utils.cleanup import clean_temp_dir
import base64
import os

router = APIRouter()

UPLOAD_DIR = "./uploads/images"
TEMP_DIR = "./uploads/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

class ImageUploadRequest(BaseModel):
    images: List[str]

@router.post("/save")
async def save_photos(req: ImageUploadRequest):
    date = datetime.now().strftime("%Y%m%d")
    experience_id = get_date(date)
    saved_paths = []
    saved_s3_urls = []
    temp_paths = []
    prompts = []
    translate_prompts = []
    
    try:
        for i, base64_img in enumerate(req.images):
            header, encoded = base64_img.split(",", 1)
            img_data = base64.b64decode(encoded)

            filename = f"{date}_{experience_id}_{i+1}.png"
            
            image_path = save_filename(img_data, UPLOAD_DIR, filename)
            temp_path = save_filename(img_data, TEMP_DIR, filename)


            s3_key = f"images/{filename}"
            s3_url = upload_s3(image_path, s3_key)

            saved_paths.append(image_path)
            saved_s3_urls.append(s3_url)
            temp_paths.append(temp_path)

        clean_temp_dir()

        for path in temp_paths:
            prompt = generate_prompt(path)
            prompts.append(prompt)
            
            translated = translate_prompt(prompt)
            translate_prompts.append(translated)

        merged_prompt = " ".join(prompts)
        song_prompt = prompt_openai(merged_prompt)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "saved_paths": saved_paths,
        "s3_urls": saved_s3_urls,
        "prompts": prompts,
        "song_prompt": song_prompt,
        "translate_prompts": translate_prompts
    }

def get_date(date: str) -> int:
    files = os.listdir(UPLOAD_DIR)
    return sum(1 for f in files if f.startswith(date)) // 3 + 1

def save_filename(data: bytes, folder: str, filename: str) -> str:
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(data)
    return path

def clean_temp_dir(temp_dir: str = TEMP_DIR, keep: int = 3):
    files = sorted(
        [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)],
        key=os.path.getctime
    )
    for file_path in files[:-keep]:
        os.remove(file_path)
