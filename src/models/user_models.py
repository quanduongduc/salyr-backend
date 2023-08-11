from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import Form, UploadFile

from pydantic import EmailStr, ValidationError, validator
from helpers.utils import as_form
from models.models import ORJSONModel
from models.playlist_models import PlaylistResponse
from models.songs_models import SongResponse


class UserResponse(ORJSONModel):
    id: int
    username: str
    alias: str
    email: EmailStr
    avatar_url: str
    created_at: datetime
    playlists: List['PlaylistResponse']
    last_play: Optional[SongResponse]


class UserCreate(ORJSONModel):
    username: str
    email: EmailStr
    password: str
    alias: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 6 or len(value) > 20:
            raise ValidationError("Username must be between 6 and 20 characters")

        if not value.isalnum():
            raise ValidationError("Username must contain only alphanumeric characters")

        return value

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase character")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        return value


@as_form
class UserUpdate(ORJSONModel):
    alias: str


class CurrentUser(ORJSONModel):
    user_id: int
    email: EmailStr
    username: str
