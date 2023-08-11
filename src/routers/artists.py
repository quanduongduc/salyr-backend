from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from helpers.http_status import StatusCode
from services.artists import create_artist, read_artist, update_artist, delete_artist
from models.artist_models import ArtistCreate, ArtistUpdate, ArtistResponse
from db.database import get_db

router = APIRouter()


@router.post("/", response_model=ArtistResponse)
def create_artist_endpoint(artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = create_artist(db, artist)
    return db_artist


@router.get("/{artist_id}", response_model=ArtistResponse)
def read_artist_endpoint(artist_id: int, db: Session = Depends(get_db)):
    db_artist = read_artist(db, artist_id)
    if db_artist is None:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Artist not found")
    return db_artist


@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist_endpoint(
    artist_id: int, artist: ArtistUpdate, db: Session = Depends(get_db)
):
    response = update_artist(db, artist_id, artist)
    return response


@router.delete("/{artist_id}")
def delete_artist_endpoint(artist_id: int, db: Session = Depends(get_db)):
    response = delete_artist(db, artist_id)
    return response
