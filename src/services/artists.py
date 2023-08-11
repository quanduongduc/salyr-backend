from db.schema import Artist
from helpers.http_status import StatusCode
from models.artist_models import ArtistCreate, ArtistResponse, ArtistUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_artist(db: Session, artist: ArtistCreate) -> ArtistResponse:
    db_artist = Artist(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)

    return generate_artist_response(db_artist)


def generate_artist_response(artist: Artist) -> ArtistResponse:
    return ArtistResponse(
        id=artist.id,
        name=artist.name,
        gender=artist.gender,
        genre=artist.genre,
        bio=artist.bio,
        albums=artist.albums,
    )


def read_artist(db: Session, artist_id: int) -> ArtistResponse:
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if artist:
        return generate_artist_response(artist)

    raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                        detail="Artist not found")


def update_artist(db: Session, artist_id: int, artist: ArtistUpdate) -> ArtistResponse:
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if db_artist:
        for key, value in artist.dict().items():
            setattr(db_artist, key, value)
        db.commit()
        db.refresh(db_artist)
        return generate_artist_response(db_artist)
    raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                        detail="Artist not found")


def delete_artist(db: Session, artist_id: int):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if artist:
        db.delete(artist)
        db.commit()
    return {"message" : "delete artist successfully"}
