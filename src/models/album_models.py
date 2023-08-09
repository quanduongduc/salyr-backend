from datetime import datetime
from typing import List
from models.models import ORJSONModel


class AlbumResponse(ORJSONModel):
    id: int
    title: str
    artist_id: int
    release_date: datetime
    cover_image_url: str
    artist: str
    songs: List[str]