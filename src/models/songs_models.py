from datetime import datetime
from typing import List, Optional

from helpers.utils import as_form

from models.models import ORJSONModel


@as_form
class SongCreate(ORJSONModel):
    title: str
    duration: float
    genre: str
    artists: list[int]


class SongResponse(ORJSONModel):
    id: int
    title: str
    duration: int
    genre: str
    url: str
    theme_url: str
    artists: "Optional[List[ArtistResponse]]"

from models.artist_models import ArtistResponse
SongResponse.update_forward_refs()
