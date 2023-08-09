from typing import List
from models.models import ORJSONModel


class ArtistResponse(ORJSONModel):
    id: int
    name: str
    bio: str
    genre: str
    albums: List[str]
    songs: List[str]
