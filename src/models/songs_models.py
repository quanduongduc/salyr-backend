from datetime import datetime
from typing import List, Optional

from models.artist_models import ArtistResponse
from models.models import ORJSONModel


class SongResponse(ORJSONModel):
    id: int
    title: str
    release_date: datetime
    duration: int
    genre: str
    url: str
    theme_url: str
    artists: Optional[List[ArtistResponse]]
