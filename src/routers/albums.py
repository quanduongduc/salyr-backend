from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.albums import create_album, read_album, update_album, delete_album
from models.album_models import AlbumCreate, AlbumUpdate, AlbumResponse
from db.database import get_db

router = APIRouter()


@router.post("/", response_model=AlbumResponse)
def create_album_endpoint(
    album: AlbumCreate, artist_id: int, db: Session = Depends(get_db)
):
    db_album = create_album(db, album, artist_id)
    return db_album


@router.get("/{album_id}", response_model=AlbumResponse)
def read_album_endpoint(album_id: int, db: Session = Depends(get_db)):
    db_album = read_album(db, album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album


@router.put("/{album_id}", response_model=AlbumResponse)
def update_album_endpoint(
    album_id: int, album: AlbumUpdate, db: Session = Depends(get_db)
):
    db_album = update_album(db, album_id, album)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album


@router.delete("/{album_id}", response_model=bool)
def delete_album_endpoint(album_id: int, db: Session = Depends(get_db)):
    deleted = delete_album(db, album_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Album not found")
    return True
