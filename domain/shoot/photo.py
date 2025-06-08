from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from datetime import datetime
from domain.prompt.prompt import generate_prompt
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
    temp_paths = []
    prompts = []
    
    try:
        for i, base64_img in enumerate(req.images):
            header, encoded = base64_img.split(",", 1)
            img_data = base64.b64decode(encoded)

            filename = f"{date}_{experience_id}_{i+1}.png"
            image_path = save_filename(img_data, UPLOAD_DIR, filename)
            temp_path = save_filename(img_data, TEMP_DIR, filename)

            saved_paths.append(image_path)
            temp_paths.append(temp_path)

        for path in temp_paths:
            prompt = generate_prompt(path)
            prompts.append(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"saved_paths": saved_paths}

def get_date(date: str) -> int:
    files = os.listdir(UPLOAD_DIR)
    return sum(1 for f in files if f.startswith(date)) // 3 + 1

def save_filename(data: bytes, folder: str, filename: str) -> str:
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(data)
    return path