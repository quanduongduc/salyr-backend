from fastapi import APIRouter, HTTPException, Query
from fastapi import APIRouter, Depends
from db.database import get_db
from db.schema.schema import Song
from sqlalchemy.orm import Session
from helpers.http_status import StatusCode

from models.songs_models import SongCreate, SongResponse
from services.songs import create_song, delete_song, read_song, update_song

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.post("/", response_model=SongResponse)
def create_song_endpoint(song: SongCreate, db: Session = Depends(get_db)):
    return create_song(db, song)


@router.get("/{song_id}", response_model=SongResponse)
def read_song_endpoint(song_id: int, db: Session = Depends(get_db)):
    song = read_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.put("/{song_id}", response_model=SongResponse)
def update_song_endpoint(
    song_id: int, updated_song: SongCreate, db: Session = Depends(get_db)
):
    song = update_song(db, song_id, updated_song)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.delete("/{song_id}", response_model=SongResponse)
def delete_song_endpoint(song_id: int, db: Session = Depends(get_db)):
    song = delete_song(db, song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


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
