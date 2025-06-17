from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from core.config import settings

router = APIRouter()

class SaveInfoRequest(BaseModel):
    title: str
    user_name: str
    description: str
    image_path: str
    song_path: str

@router.post("/info")
def save_info(req: SaveInfoRequest):
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO Album (song_path, title, user_name, description, image_path)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        cursor.execute(insert_query, (
            req.song_path,
            req.title,
            req.user_name,
            req.description,
            req.image_path
        ))
        album_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "message": "성공적으로 저장되었습니다",
            "album_id": album_id
        }

    except Exception as e:
        print("save_info error:", e)
        raise HTTPException(status_code=500, detail="서버 에러 발생")

    finally:
        cursor.close()
        conn.close()
