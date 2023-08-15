from typing import Annotated, List
from sqlalchemy.orm import Session
from db.database import paginate

from db.schema import (
    Artist,
    PlaylistSongAssociation,
    Song,
    SongAlbumAssociation,
    SongArtistAssociation,
)
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
            status_code=StatusCode.HTTP_StatusCode.HTTP_404_NOT_FOUND_NOT_FOUND,
            detail="Artists not found",
        )

    db_song.artists = db_artists

    db.add(db_song)
    db.commit()
    db.refresh(db_song)

    upload_song_asset_to_s3(
        audio_file=audio_file, theme_file=theme_file, song_id=db_song.id
    )

    return {"message": "create successfully", "id": db_song.id}

def get_songs(db: Session, limit: int, page_number: int):
    songs_query = db.query(Song)
    db_songs = paginate(db=db, query=songs_query, page_number=page_number, page_limit=limit).all()
    songs_response = [generate_song_response(song) for song in db_songs]
    return songs_response

def upload_song_asset_to_s3(
    audio_file: UploadFile, theme_file: UploadFile, song_id: str
):
    audio_key = f"{S3_SONG_PATH}{song_id}"
    theme_key = f"{S3_SONG_THEME_PATH}{song_id}"

    upload_file_to_s3(key=audio_key, file=audio_file)
    upload_file_to_s3(key=theme_key, file=theme_file)


def generate_song_response(song: Song) -> SongResponse:
    if not song:
        return None
    theme_url, audio_url = generate_song_presigned_url(song.id)

    artist_response = [
        ArtistResponse(
            id=artist.id,
            name=artist.name,
            bio=artist.bio,
            gender=artist.gender,
            genre=artist.genre,
            avatar_url=""
        )
        for artist in song.artists
    ]

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
        status_code=StatusCode.HTTP_StatusCode.HTTP_404_NOT_FOUND_NOT_FOUND,
        detail="Song not found",
    )


def search_song_by_title(db: Session, song_title: str) -> List[SongResponse]:
    songs = db.query(Song).filter(Song.title.ilike(f"{song_title}%")).all()
    if not songs:
        return []
    songs_response = [generate_song_response(song) for song in songs]
    return songs_response


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
        status_code=StatusCode.HTTP_StatusCode.HTTP_404_NOT_FOUND_NOT_FOUND,
        detail="Song not found",
    )


def associate_artist_with_song(session: Session, song_id: int, artist_id: int):
    existing_association = (
        session.query(SongArtistAssociation)
        .filter_by(song_id=song_id, artist_id=artist_id)
        .first()
    )
    if existing_association:
        raise HTTPException(status_code=400, detail="Association already exists")
    association = SongArtistAssociation(song_id=song_id, artist_id=artist_id)
    session.add(association)
    session.commit()


def disassociate_artist_from_song(session: Session, song_id: int, artist_id: int):
    association = (
        session.query(SongArtistAssociation)
        .filter_by(song_id=song_id, artist_id=artist_id)
        .first()
    )
    if association:
        session.delete(association)
        session.commit()
    else:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Association not found"
        )


def associate_album_with_song(session: Session, song_id: int, album_id: int):
    existing_association = (
        session.query(SongAlbumAssociation)
        .filter_by(song_id=song_id, album_id=album_id)
        .first()
    )
    if existing_association:
        raise HTTPException(status_code=400, detail="Association already exists")
    association = SongAlbumAssociation(song_id=song_id, album_id=album_id)
    session.add(association)
    session.commit()


def disassociate_album_from_song(session: Session, song_id: int, album_id: int):
    association = (
        session.query(SongAlbumAssociation)
        .filter_by(song_id=song_id, album_id=album_id)
        .first()
    )
    if association:
        session.delete(association)
        session.commit()
    else:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Association not found"
        )


def associate_song_with_playlist(session: Session, song_id: int, playlist_id: int):
    existing_association = (
        session.query(PlaylistSongAssociation)
        .filter_by(song_id=song_id, playlist_id=playlist_id)
        .first()
    )
    if existing_association:
        raise HTTPException(status_code=400, detail="Association already exists")

    association = PlaylistSongAssociation(song_id=song_id, playlist_id=playlist_id)
    session.add(association)
    session.commit()


def disassociate_song_from_playlist(session: Session, song_id: int, playlist_id: int):
    association = (
        session.query(PlaylistSongAssociation)
        .filter_by(song_id=song_id, playlist_id=playlist_id)
        .first()
    )
    if association:
        session.delete(association)
        session.commit()
    else:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Association not found"
        )
