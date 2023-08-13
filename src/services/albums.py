from typing import List
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from db.database import paginate
from db.schema import Album, Artist
from helpers.constants import S3_ALBUM_COVER_IMAGE_PATH
from helpers.http_status import StatusCode
from helpers.s3 import generate_presigned_download_url, upload_file_to_s3
from models.album_models import AlbumCreate, AlbumResponse, AlbumResponseWithArtistAndSongs, AlbumUpdate
from services.artists import generate_artist_response
from services.songs import generate_song_response


def create_album(db: Session, album: AlbumCreate, cover_img : UploadFile, artist_id: int) -> AlbumResponse:
    db_album = Album(title=album.title,
                     release_date=album.release_date, artist_id=artist_id)

    db.add(db_album)
    db.commit()
    db.refresh(db_album)

    if cover_img:
        key = f"{S3_ALBUM_COVER_IMAGE_PATH}{db_album.id}"
        upload_file_to_s3(key=key, file=cover_img)

    return generate_album_response(db_album)


def read_album(db: Session, album_id: int) -> AlbumResponseWithArtistAndSongs:
    db_album = db.query(Album).filter(Album.id == album_id).first()
    if db_album is None:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Album not found")

    songs_response = [generate_song_response(song) for song in db_album.songs]
    artist_response = generate_artist_response(db_album.artist)

    key = f"{S3_ALBUM_COVER_IMAGE_PATH}{db_album.id}"
    cover_img_url = generate_presigned_download_url(key)

    album_response = AlbumResponseWithArtistAndSongs(
        id=db_album.id,
        title=db_album.title,
        release_date=db_album.release_date,
        cover_image_url=cover_img_url,
        artist=artist_response,
        songs=songs_response
    )

    return album_response


def generate_album_response(db_album):

    key = f"{S3_ALBUM_COVER_IMAGE_PATH}{db_album.id}"
    cover_img_url = generate_presigned_download_url(key)
    arist_response = generate_artist_response(db_album.artist)
    return AlbumResponse(
        id=db_album.id,
        title=db_album.title,
        release_date=db_album.release_date,
        cover_image_url=cover_img_url,
        artist=arist_response
    )


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

def get_albums(db: Session, limit: int, page_number: int):
    db_albums = paginate(db=db, Base=Album, page_number=page_number, page_limit=limit)
    albums_response = [generate_album_response(album) for album in db_albums]
    return albums_response

def search_album_by_title(db: Session, album_title: str) -> List[AlbumResponse]:
    albums = db.query(Album).filter(Album.title.ilike(f'{album_title}%')).all()  
    if not albums:
        return []  
    albums_response = [generate_album_response(album) for album in albums]
    return albums_response
