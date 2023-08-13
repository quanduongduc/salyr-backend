from datetime import datetime
from typing import Optional
from helpers.utils import as_form

from models.artist_models import ArtistResponse
from models.models import ORJSONModel
from models.songs_models import SongResponse


@as_form
class AlbumCreate(ORJSONModel):
    artist_id: int
    title: str
    release_date: datetime


class AlbumUpdate(ORJSONModel):
    title: str
    release_date: datetime
    cover_image_url: Optional[str]


class AlbumResponse(ORJSONModel):
    id: int
    title: str
    release_date: datetime
    cover_image_url: str
    artist: ArtistResponse


class AlbumResponseWithArtist(AlbumResponse):
    artist: ArtistResponse


class AlbumResponseWithArtistAndSongs(AlbumResponseWithArtist):
    songs: list[SongResponse]
