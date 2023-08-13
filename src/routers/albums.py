from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from helpers.http_status import StatusCode
from services.albums import create_album, get_albums, read_album, search_album_by_title, update_album, delete_album
from models.album_models import AlbumCreate, AlbumResponseWithArtistAndSongs, AlbumUpdate, AlbumResponse
from db.database import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=AlbumResponse)
def create_album_endpoint(
    cover_img: UploadFile, album: AlbumCreate = Depends(AlbumCreate.as_form), db: Session = Depends(get_db)
):
    db_album = create_album(
        db=db, album=album, artist_id=album.artist_id, cover_img=cover_img)
    return db_album


@router.get("/search", response_model=List[AlbumResponse])
def search_albums_by_title(
    title: str,
    db: Session = Depends(get_db)
):
    albums = search_album_by_title(db, title)
    return albums

@router.get("/query", response_model=List[AlbumResponse])
def read_albums_endpoint(limit: int = 10, page_number : int = 1, db: Session = Depends(get_db)):
    response = get_albums(db=db, limit=limit, page_number=page_number)
    return response

@router.get("/{album_id}", response_model=AlbumResponseWithArtistAndSongs)
def read_album_endpoint(album_id: int, db: Session = Depends(get_db)):
    db_album = read_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Album not found")
    return db_album


@router.put("/{album_id}", response_model=AlbumResponse)
def update_album_endpoint(
    album_id: int, album: AlbumUpdate, db: Session = Depends(get_db)
):
    db_album = update_album(db, album_id, album)
    if db_album is None:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Album not found")
    return db_album


@router.delete("/{album_id}", response_model=Dict)
def delete_album_endpoint(album_id: int, db: Session = Depends(get_db)):
    deleted = delete_album(db, album_id)
    if not deleted:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Album not found")
    return {"Message": "deleted album successfully"}
