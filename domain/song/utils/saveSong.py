import os
from datetime import datetime

UPLOAD_DIR = "uploads/song"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def song_path() -> str:
    date_str = datetime.now().strftime("%y%m%d")
    count = sum(1 for f in os.listdir(UPLOAD_DIR) if f.startswith(date_str)) + 1
    filename = f"{date_str}_{count}.wav"
    return os.path.join(UPLOAD_DIR, filename)
