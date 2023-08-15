from typing import List
from db.database import paginate
from db.schema import Artist
from helpers.constants import S3_Artist_AVATAR_PATH
from helpers.http_status import StatusCode
from helpers.s3 import generate_presigned_download_url, upload_file_to_s3
from models.artist_models import ArtistCreate, ArtistResponse, ArtistResponseWithSongs, ArtistUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile

from services.songs import generate_song_response


def create_artist(db: Session, artist: ArtistCreate, avatar_file : UploadFile) -> ArtistResponse:
    db_artist = Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    key = f"{S3_Artist_AVATAR_PATH}{db_artist.id}"
    upload_file_to_s3(key=key, file=avatar_file)
    return generate_artist_response(db_artist)


def generate_artist_response(artist: Artist) -> ArtistResponse:
    if not artist:
        return None
    key = f"{S3_Artist_AVATAR_PATH}{artist.id}"
    avatar_url = generate_presigned_download_url(key)
    return ArtistResponse(
        id=artist.id,
        name=artist.name,
        genre=artist.genre,
        bio=artist.bio,
        avatar_url=avatar_url,
    )


def read_artist(db: Session, artist_id: int) -> ArtistResponseWithSongs:
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Artist not found"
        )

    songs_response = [generate_song_response(song) for song in artist.songs]

    artist_response = ArtistResponseWithSongs(
        **generate_artist_response(artist),
        songs=songs_response,
    )

    return artist_response


def update_artist(db: Session, artist_id: int, artist: ArtistUpdate) -> ArtistResponse:
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if db_artist:
        for key, value in artist.dict().items():
            setattr(db_artist, key, value)
        db.commit()
        db.refresh(db_artist)
        return generate_artist_response(db_artist)
    raise HTTPException(
        status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Artist not found"
    )


def delete_artist(db: Session, artist_id: int):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if artist:
        db.delete(artist)
        db.commit()
    return {"message": "delete artist successfully"}


def get_artists(db: Session, limit: int, page_number: int):
    db_artists = paginate(db=db, Base=Artist, page_number=page_number, page_limit=limit).all()
    artists_response = [generate_artist_response(artist) for artist in db_artists]
    return artists_response
    

def search_artist_by_name(db: Session, artist_name : str) -> List[ArtistResponse]:
    artists = db.query(Artist).filter(Artist.name.ilike(f'{artist_name}%')).all()
    if not artists:
        return []
    artists_response = [generate_artist_response(artist) for artist in artists]
    return artists_response
