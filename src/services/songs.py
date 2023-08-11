from typing import Annotated
from sqlalchemy.orm import Session

from db.schema import Artist, Song
from helpers.constants import S3_SONG_PATH, S3_SONG_THEME_PATH
from helpers.http_status import StatusCode
from helpers.s3 import generate_presigned_download_url, upload_file_to_s3
from models.artist_models import ArtistResponse
from models.songs_models import SongCreate, SongResponse
from fastapi import File, UploadFile
from fastapi import HTTPException


def create_song(
    db: Session, audio_file: UploadFile, theme_file: UploadFile, song: SongCreate
):
    db_song = Song(title=song.title, duration=song.duration, genre=song.genre)
    db_artists = db.query(Artist).filter(Artist.id.in_(song.artists)).all()

    if not db_artists:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Artists not found"
        )

    db_song.artists = db_artists

    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    upload_song_asset_to_s3(
        audio_file=audio_file, theme_file=theme_file, song_id=db_song.id
    )

    return {"message": "Create Song Successfully"}


def upload_song_asset_to_s3(audio_file: UploadFile, theme_file: UploadFile, song_id : str):
    audio_key = f"{S3_SONG_PATH}{song_id}"
    theme_key = f"{S3_SONG_THEME_PATH}{song_id}"

    upload_file_to_s3(key=audio_key, file=audio_file)
    upload_file_to_s3(key=theme_key, file=theme_file)


def generate_song_response(song: Song) -> SongResponse:
    theme_url, audio_url = generate_song_presigned_url(song.id)

    artist_response = [ArtistResponse(
        id=artist.id,
        name=artist.name,
        bio=artist.bio,
        gender=artist.gender,
        genre=artist.genre,
    )for artist in song.artists]

    return SongResponse(
        id=song.id,
        title=song.title,
        duration=song.duration,
        genre=song.genre,
        url=audio_url,
        theme_url=theme_url,
        artists=artist_response,
    )


def read_song(db: Session, song_id: int) -> SongResponse:
    song_db = db.query(Song).filter(Song.id == song_id).first()

    if song_db:
        song = generate_song_response(song_db)

        return song
    raise HTTPException(
        status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Song not found"
    )


def generate_song_presigned_url(song_id: int):
    key = f"{S3_SONG_PATH}{song_id}"
    theme_key = f"{S3_SONG_THEME_PATH}{song_id}"

    theme_url = generate_presigned_download_url(theme_key)
    audio_url = generate_presigned_download_url(key)

    return theme_url, audio_url


def update_song(db: Session, song_id: int, updated_song: SongCreate) -> SongResponse:
    db_song = db.query(Song).filter(Song.id == song_id).first()

    if db_song:
        for key, value in updated_song.dict().items():
            setattr(db_song, key, value)
        db.commit()
        db.refresh(db_song)

        updated_song_response = generate_song_response(db_song)

        return updated_song_response
    raise HTTPException(
        status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Song not found"
    )
