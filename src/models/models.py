from datetime import datetime
from typing import Any, Callable, List, Optional
from zoneinfo import ZoneInfo

import orjson
from pydantic import BaseModel, root_validator


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}
        allow_population_by_field_name = True

    @root_validator()
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


class UserResponse(ORJSONModel):
    id: int
    username: str
    email: str
    avatar_url: str
    created_at: datetime
    playlists: List['PlaylistResponse']


class SongResponse(ORJSONModel):
    id: int
    title: str
    release_date: datetime
    duration: int
    genre: str
    url: str
    theme_url: str
    artists: Optional[List['ArtistResponse']]
    albums: Optional[List['AlbumResponse']]


class AlbumResponse(ORJSONModel):
    id: int
    title: str
    artist_id: int
    release_date: datetime
    cover_image_url: str
    artist: 'ArtistResponse'
    songs: List[SongResponse]


class ArtistResponse(ORJSONModel):
    id: int
    name: str
    bio: str
    genre: str
    albums: List[AlbumResponse]
    songs: List[SongResponse]


class PlaylistResponse(ORJSONModel):
    id: int
    user_id: int
    title: str
    creation_date: datetime
    user: UserResponse
    songs: List[SongResponse]
