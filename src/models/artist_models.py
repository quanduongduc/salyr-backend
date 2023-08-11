from typing import List, Optional

from pydantic import BaseModel
from helpers.constants import Gender
from models.album_models import AlbumResponse
from models.models import ORJSONModel


class ArtistResponse(ORJSONModel):
    id: int
    name: str
    bio: str
    genre: str
    gender: Gender
    albums: Optional[List[AlbumResponse]]


class ArtistCreate(BaseModel):
    name: str
    bio: str
    genre: str
    gender: Gender


class ArtistUpdate(BaseModel):
    name: str
    bio: str
    genre: str
