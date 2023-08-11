from fastapi import APIRouter, HTTPException, Query, UploadFile
from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session


from models.songs_models import SongCreate, SongResponse
from services.songs import create_song, read_song, update_song

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.post("/")
def create_song_endpoint(audio_file : UploadFile , theme_file : UploadFile, db: Session = Depends(get_db), song: SongCreate = Depends(SongCreate.as_form)):
    return create_song(db=db, song=song, audio_file=audio_file, theme_file=theme_file)


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


# @router.delete("/{song_id}", response_model=SongResponse)
# def delete_song_endpoint(song_id: int, db: Session = Depends(get_db)):
#     song = delete_song(db, song_id)
#     if song is None:
#         raise HTTPException(status_code=404, detail="Song not found")
#     return song


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
