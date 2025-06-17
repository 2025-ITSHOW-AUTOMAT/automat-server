import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'domain', 'song', 'ACE_Step'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from domain.shoot import photo
from domain.song import createSong
from domain.emotion.emotion import router as emotion
from domain.album import album
from domain.album import saveInfo
import os

load_dotenv()

app = FastAPI()
app.include_router(photo.router, prefix="/photo")
app.include_router(createSong.router, prefix="/song")
app.include_router(emotion, prefix="/emotion")
app.include_router(album.router, prefix="/album")
app.include_router(saveInfo.router, prefix="/album/save-info")

@app.get("/")
def hello():
    return {"message": "Hello Automat!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

sys.path.append(os.path.join(os.path.dirname(__file__), 'domain', 'song', 'ACE_Step'))
