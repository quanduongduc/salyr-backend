from helpers.utils import as_form
from typing import List, Optional

from helpers.constants import Gender
from models.models import ORJSONModel


class ArtistResponse(ORJSONModel):
    id: int
    name: str
    bio: str
    genre: str
    avatar_url: str


@as_form
class ArtistCreate(ORJSONModel):
    name: str
    bio: str
    genre: str


class ArtistUpdate(ORJSONModel):
    name: str
    bio: str
    genre: str


class ArtistResponseWithSongs(ArtistResponse):
    songs: "List[SongResponse]"


from models.songs_models import SongResponse
ArtistResponseWithSongs.update_forward_refs()
