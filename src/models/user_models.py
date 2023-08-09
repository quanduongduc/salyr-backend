from datetime import datetime
from typing import List

from pydantic import EmailStr, ValidationError, validator
from models.models import ORJSONModel
from models.playlist_models import PlaylistResponse


class UserResponse(ORJSONModel):
    id: int
    username: str
    email: EmailStr
    avatar_url: str
    created_at: datetime
    playlists: List['PlaylistResponse']


class UserRequest(ORJSONModel):
    username: str
    email: EmailStr
    password: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 6 or len(value) > 20:
            raise ValidationError("Username must be between 6 and 20 characters")

        if not value.isalnum():
            raise ValidationError("Username must contain only alphanumeric characters")

        return value


class CurrentUser():
    user_id: int
    email: EmailStr
    username: str
