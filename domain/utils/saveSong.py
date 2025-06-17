import os
from datetime import datetime
from core.config import settings
import psycopg2

UPLOAD_DIR = "uploads/song"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def song_path() -> str:
    date_str = datetime.now().strftime("%y%m%d")
    count = sum(1 for f in os.listdir(UPLOAD_DIR) if f.startswith(date_str)) + 1
    filename = f"{date_str}_{count}.wav"
    return os.path.join(UPLOAD_DIR, filename)

def save_song(song_path: str) -> int:
    conn = psycopg2.connect(settings.DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Songs (song_path) VALUES (%s) RETURNING id;",
            (song_path,)
        )
        song_id = cursor.fetchone()[0]
        conn.commit()
        return song_id
    finally:
        cursor.close()
        conn.close()
