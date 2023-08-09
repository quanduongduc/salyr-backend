from datetime import datetime
from typing import List, Optional

from models.artist_models import ArtistResponse
from models.models import ORJSONModel



class SongBase(ORJSONModel):
    title: str
    release_date: str
    duration: float
    genre: str

class SongCreate(SongBase):
    pass

class SongResponse(SongBase):
    id: int

    class Config:
        orm_mode = True
class SongResponse(SongBase):
    id: int
    title: str
    release_date: datetime
    duration: int
    genre: str
    url: str
    theme_url: str
    artists: Optional[List[ArtistResponse]]
