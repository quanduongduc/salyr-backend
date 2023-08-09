from typing import Annotated
from sqlalchemy.orm import Session

from db.schema import Song
from models.songs_models import SongCreate
from fastapi import File, UploadFile


def create_song(db: Session,file: Annotated[bytes, File()] , song: SongCreate):
    db_song = Song(**song.dict())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def read_song(db: Session, song_id: int):
    return db.query(Song).filter(Song.id == song_id).first()


def update_song(db: Session, song_id: int, updated_song: SongCreate):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song:
        for key, value in updated_song.dict().items():
            setattr(db_song, key, value)
        db.commit()
        db.refresh(db_song)
    return db_song


def delete_song(db: Session, song_id: int):
    db_song = db.query(Song).filter(Song.id == song_id).first()
    if db_song:
        db.delete(db_song)
        db.commit()
    return db_song
