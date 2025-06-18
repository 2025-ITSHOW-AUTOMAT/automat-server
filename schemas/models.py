from sqlalchemy import Column, Integer, String, Text, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from schemas.session import Base

# class Songs(Base):
#     __tablename__ = "songs"
#     id = Column(Integer, primary_key=True, index=True)
#     song_path = Column(Text, nullable=False)    
#     # 1대1 설정
#     album = relationship("Album", back_populates="songs", uselist=False)

class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True, index=True)
    song_path = Column(Text, nullable=False)
    title = Column(String(50), nullable=False)
    user_name = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(Text, nullable=False)
    
    song = relationship("Songs", back_populates="album", uselist=False)