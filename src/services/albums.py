from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.schema import Album, Artist
from helpers.http_status import StatusCode
from models.album_models import AlbumCreate, AlbumResponse, AlbumUpdate
from models.artist_models import ArtistResponse


def create_album(db: Session, album: AlbumCreate, artist_id: int) -> AlbumResponse:
    db_album = Album(**album.dict(), artist_id=artist_id)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def read_album(db: Session, album_id: int) -> AlbumResponse:
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Album not found")

    artist = db.query(Artist).filter(Artist.id == db_album.artist_id).first()
    if artist is None:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Artist not found")

    album_response = AlbumResponse(
        id=db_album.id,
        title=db_album.title,
        release_date=db_album.release_date,
        cover_image_url=db_album.cover_image_url,
        artist=ArtistResponse(
            id=artist.id, name=artist.name, bio=artist.bio, genre=artist.genre
        ),
    )

    return album_response


def update_album(db: Session, album_id: int, album: AlbumUpdate) -> AlbumResponse:
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album:
        for key, value in album.dict().items():
            setattr(db_album, key, value)
        db.commit()
        db.refresh(db_album)
    return db_album


def delete_album(db: Session, album_id: int) -> bool:
    album = db.query(Album).filter(Album.id == album_id).first()
    if album:
        db.delete(album)
        db.commit()
        return True
    return False
