from fastapi import APIRouter
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)


router = APIRouter()


@router.get("/")
def get_songs():
    pass


@router.get("/{song_id}")
def get_song(song_id: int):
    pass


@router.post("/")
def create_song():
    pass


@router.put("/{song_id}")
def update_song(song_id: int):
    pass


@router.delete("/{song_id}")
def delete_song(song_id: int):
    pass


@router.post("/{song_id}/artists/{artist_id}")
def associate_artist_with_song(song_id: int, artist_id: int):
    pass


@router.delete("/{song_id}/artists/{artist_id}")
def disassociate_artist_from_song(song_id: int, artist_id: int):
    pass


@router.post("/{song_id}/albums/{album_id}")
def associate_album_with_song(song_id: int, album_id: int):
    pass


@router.delete("/{song_id}/albums/{album_id}")
def disassociate_album_from_song(song_id: int, album_id: int):
    pass
