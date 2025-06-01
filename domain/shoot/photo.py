from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import base64
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "./uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ImageUploadRequest(BaseModel):
    images: List[str]

@router.post("/save")
async def save_photos(req: ImageUploadRequest):
    saved_paths = []

    for base64_img in req.images:
        try:
            header, encoded = base64_img.split(",", 1)
            img_data = base64.b64decode(encoded)

            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(UPLOAD_DIR, filename)

            with open(filepath, "wb") as f:
                f.write(img_data)

            saved_paths.append(filepath)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"saved_paths": saved_paths}
