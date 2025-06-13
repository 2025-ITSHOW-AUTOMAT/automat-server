import psycopg2
from psycopg2 import sql
import os

def insert_song_path(experience_num: int, song_path: str):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cur = conn.cursor()
    query = sql.SQL("INSERT INTO songs (experience_num, song_path) VALUES (%s, %s)")
    cur.execute(query, (experience_num, song_path))
    conn.commit()
    cur.close()
    conn.close()
