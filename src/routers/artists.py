from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from services.artists import (
    create_artist,
    get_artists,
    read_artist,
    search_artist_by_name,
    update_artist,
    delete_artist,
)
from models.artist_models import (
    ArtistCreate,
    ArtistResponseWithSongs,
    ArtistUpdate,
    ArtistResponse,
)
from db.database import get_db

router = APIRouter()


@router.post("/", response_model=ArtistResponse)
def create_artist_endpoint(
    artist_avatar: UploadFile,
    artist: ArtistCreate = Depends(ArtistCreate.as_form),
    db: Session = Depends(get_db),
):
    response = create_artist(db=db, artist=artist, avatar_file=artist_avatar)
    return response


@router.get("/search", response_model=List[ArtistResponse])
def search_artist_endpoint(name: str, db: Session = Depends(get_db)):
    response = search_artist_by_name(db=db, artist_name=name)
    return response


@router.get("/query", response_model=List[ArtistResponse])
def read_artist_endpoint(limit: int = 10, page_number : int = 1, db: Session = Depends(get_db)):
    response = get_artists(db=db, limit=limit, page_number=page_number)
    return response


@router.get("/{artist_id}", response_model=ArtistResponseWithSongs)
def read_artist_endpoint(artist_id: int, db: Session = Depends(get_db)):
    response = read_artist(db=db, artist_id=artist_id)
    return response


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
