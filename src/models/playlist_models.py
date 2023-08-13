from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from models.models import ORJSONModel
from models.songs_models import SongResponse


class PlaylistRequest(ORJSONModel):
    title: str


class PlaylistResponse(ORJSONModel):
    id: str
    title: str
    creation_date: datetime


class PlayListResponseWithSongs(PlaylistResponse):
    songs: list[SongResponse]
