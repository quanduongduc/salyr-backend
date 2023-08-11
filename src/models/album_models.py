from datetime import datetime
from typing import List
from pydantic import BaseModel


class AlbumCreate(BaseModel):
    title: str
    release_date: datetime
    cover_image_url: str


class AlbumUpdate(BaseModel):
    title: str
    release_date: datetime
    cover_image_url: str


class AlbumResponse(BaseModel):
    id: int
    title: str
    release_date: datetime
    cover_image_url: str
    artist: str  # Assuming you have an ArtistResponse schema

    class Config:
        orm_mode = True
