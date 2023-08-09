from datetime import datetime
from typing import List
from models.models import ORJSONModel

class PlaylistResponse(ORJSONModel):
    id: int
    user_id: int
    title: str
    creation_date: datetime
    songs: List[str]