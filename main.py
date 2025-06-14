import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'domain', 'song', 'ACE_Step'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from domain.shoot import photo
from domain.song import createSong
from domain.emotion.emotion import router as emotion

import os

load_dotenv()

app = FastAPI()
app.include_router(photo.router, prefix="/photo")
app.include_router(createSong.router, prefix="/song")
app.include_router(emotion, prefix="/emotion")

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
