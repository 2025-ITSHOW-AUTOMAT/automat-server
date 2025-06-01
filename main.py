from fastapi import FastAPI
from domain.shoot import photo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(photo.router, prefix="/photo")

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