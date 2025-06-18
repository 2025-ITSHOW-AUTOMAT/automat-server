from fastapi import APIRouter, HTTPException
from typing import List
from schemas.schemas import Album  # Pydantic 모델
from ..utils.db import get_connection  # psycopg2 연결 함수

router = APIRouter()

@router.get("/", response_model=List[Album])
def read_albums():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, song_path, title, user_name, description, image_path FROM album ORDER BY id DESC")
        rows = cursor.fetchall()
        albums = []
        for row in rows:
            albums.append(Album(
                id=row[0],
                song_path=row[1],
                title=row[2],
                user_name=row[3],
                description=row[4],
                image_path=row[5],
            ))
        return albums
    finally:
        cursor.close()
        conn.close()

@router.get("/{album_id}", response_model=Album)
def read_album(album_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, song_path, title, user_name, description, image_path FROM album WHERE id = %s",
            (album_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Album not found")
        album = Album(
            id=row[0],
            song_path=row[1],
            title=row[2],
            user_name=row[3],
            description=row[4],
            image_path=row[5],
        )
        return album
    finally:
        cursor.close()
        conn.close()