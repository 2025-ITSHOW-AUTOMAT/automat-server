from pydantic import BaseModel
from typing import Optional

# class Song(BaseModel):
#     # id: int
#     song_path: str

#     class Config:
#         orm_mode = True

class Album(BaseModel):
    id: int
    song_path: str
    # title: str
    user_name: str
    description: str
    image_path: str

    class Config:
        orm_mode = True
