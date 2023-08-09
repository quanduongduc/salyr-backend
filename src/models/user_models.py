from datetime import datetime
from typing import List
from models.models import ORJSONModel
from models.playlist_models import PlaylistResponse


class UserResponse(ORJSONModel):
    id: int
    username: str
    email: str
    avatar_url: str
    created_at: datetime
    playlists: List['PlaylistResponse']

class UserRequest(ORJSONModel):
    user_name: str
    email: str
    password: str

class CurrentUser():
    user_id: int
    email: str
    user_name: str