from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from core.config import settings
from domain.utils.s3 import random_s3
import random
import os

router = APIRouter()

SONG_DIR = "song"

class SaveInfoRequest(BaseModel):
    title: str
    user_name: str
    description: str
    image_path: str

@router.post("/info")
def save_info(req: SaveInfoRequest):
    try:
        song_url, chosen_song = random_s3()

        conn = psycopg2.connect(settings.DATABASE_URL)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO Album (song_path, title, user_name, description, image_path)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        cursor.execute(insert_query, (
            song_url,
            req.title,
            req.user_name,
            req.description,
            req.image_path
        ))
        album_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "message": "성공적으로 저장되었습니다",
            "album_id": album_id,
            "song_file": chosen_song,
            "song_url": song_url
        }

    except Exception as e:
        print("save_info error:", e)
        raise HTTPException(status_code=500, detail="서버 에러 발생")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()