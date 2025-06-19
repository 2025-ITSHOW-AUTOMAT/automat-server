import sys
import os
import torch

sys.path.append(os.path.join(os.path.dirname(__file__), 'domain', 'song', 'ACE_Step'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from domain.shoot.photo import router as photo
from domain.song.createSong import router as createSong
from domain.emotion.emotion import router as emotion
from domain.album.album import router as album
from domain.album.saveInfo import router as saveInfo
from domain.prompt.prompt import router as prompt
import os

load_dotenv()

app = FastAPI()
app.include_router(photo, prefix="/photo")
app.include_router(prompt, prefix="/prompt")
app.include_router(createSong, prefix="/song")
app.include_router(emotion, prefix="/emotion")
app.include_router(album, prefix="/album")
app.include_router(saveInfo, prefix="/album/save")

@app.get("/")
def hello():
    return {"message": "Hello Automat!"}

@app.get("/gpu-check")
def gpu_check():
    return {
        "gpu_available": torch.cuda.is_available(),
        "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
sys.path.append(os.path.join(os.path.dirname(__file__), 'domain', 'song', 'ACE_Step'))
