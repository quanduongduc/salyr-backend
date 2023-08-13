from typing import Dict, List
from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session


from models.songs_models import SongCreate, SongResponse
from services.songs import (
    associate_album_with_song,
    associate_artist_with_song,
    associate_song_with_playlist,
    create_song,
    disassociate_album_from_song,
    disassociate_artist_from_song,
    disassociate_song_from_playlist,
    get_songs,
    read_song,
    search_song_by_title,
    update_song,
)

router = APIRouter()


@router.post("/", response_model=Dict)
def create_song_endpoint(
    audio_file: UploadFile,
    theme_file: UploadFile,
    db: Session = Depends(get_db),
    song: SongCreate = Depends(SongCreate.as_form),
):
    return create_song(db=db, song=song, audio_file=audio_file, theme_file=theme_file)


@router.get("/search", response_model=List[SongResponse])
def search_song_by_title_endpoint(title: str, db: Session = Depends(get_db)):
    song = search_song_by_title(db=db, song_title=title)
    return song

@router.get("/query", response_model=List[SongResponse])
def read_songs_endpoint(limit: int = 10, page_number: int = 1, db: Session = Depends(get_db)):
    response = get_songs(db=db, limit=limit, page_number=page_number)
    return response

@router.get("/search", response_model=List[SongResponse])
def search_song_by_title_endpoint(title: str, db: Session = Depends(get_db)):
    song = search_song_by_title(db=db, song_title=title)
    return song

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


@router.post("/{song_id}/artists/{artist_id}")
def associate_artist_with_song_route(
    song_id: int, artist_id: int, session: Session = Depends(get_db)
):
    associate_artist_with_song(session, song_id, artist_id)
    return {"message": "Artist associated with song"}


@router.delete("/{song_id}/artists/{artist_id}")
def disassociate_artist_from_song_route(
    song_id: int, artist_id: int, session: Session = Depends(get_db)
):
    disassociate_artist_from_song(session, song_id, artist_id)
    return {"message": "Artist disassociated from song"}


@router.post("/{song_id}/albums/{album_id}")
def associate_album_with_song_route(
    song_id: int, album_id: int, session: Session = Depends(get_db)
):
    associate_album_with_song(session, song_id, album_id)
    return {"message": "Album associated with song"}


@router.delete("/{song_id}/albums/{album_id}")
def disassociate_album_from_song_route(
    song_id: int, album_id: int, session: Session = Depends(get_db)
):
    disassociate_album_from_song(session, song_id, album_id)
    return {"message": "Album disassociated from song"}


@router.post("/{song_id}/playlists/{playlist_id}")
def associate_song_with_playlist_route(
    song_id: int, playlist_id: int, session: Session = Depends(get_db)
):
    associate_song_with_playlist(session, song_id, playlist_id)
    return {"message": "Song associated with playlist"}


# Disassociate song from playlist
@router.delete("/{song_id}/playlists/{playlist_id}")
def disassociate_song_from_playlist_route(
    song_id: int, playlist_id: int, session: Session = Depends(get_db)
):
    disassociate_song_from_playlist(session, song_id, playlist_id)
    return {"message": "Song disassociated from playlist"}
