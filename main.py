from dotenv import load_dotenv
from fastapi import FastAPI
from domain.shoot import photo
from domain.song import createSong
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.include_router(photo.router, prefix="/photo")
app.include_router(createSong.router, prefix="/song")

@app.get("/")
def hello():
    return { "message" : "Hello Automat!" }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)