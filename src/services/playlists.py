from sqlalchemy.orm import Session
from db.database import paginate

from db.schema import Playlist
from helpers.http_status import StatusCode
from models.playlist_models import PlayListResponseWithSongs, PlaylistRequest, PlaylistResponse
from fastapi import HTTPException

from services.songs import generate_song_response


def get_playlists_by_user(db: Session, user_id: int) -> PlaylistResponse:
    return db.query(Playlist).filter_by(user_id=user_id).all()

def get_playlists(db: Session, limit: int, page_number: int, user_id):
    playlists_query = db.query(Playlist).filter(Playlist.user_id == user_id)
    db_playlists = paginate(db=db, query=playlists_query, page_number=page_number, page_limit=limit).all()
    if not db_playlists :
        return []
    playlists_response = [generate_playlist_response(playlist) for playlist in db_playlists]
    return playlists_response

def get_playlist(db: Session, playlist_id: int) -> PlayListResponseWithSongs:
    db_playlist = db.query(Playlist).filter_by(id=playlist_id).first()
    if not db_playlist:
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Playlist not found")

    songs_response = [generate_song_response(song) for song in db_playlist.songs]
    playlist_response = PlayListResponseWithSongs(
        id=db_playlist.id,
        title=db_playlist.title,
        user_id=db_playlist.user_id,
        creation_date=db_playlist.creation_date,
        songs=songs_response
    )
    return playlist_response


def create_playlist(db: Session, playlist_create: PlaylistRequest, user_id: int) -> PlaylistResponse:
    new_playlist = Playlist(
        title=playlist_create.title, user_id=user_id)
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return generate_playlist_response(new_playlist)


def generate_playlist_response(db_playlist: Playlist) -> PlaylistResponse:
    if not db_playlist:
        return None

    return PlaylistResponse(
        id=db_playlist.id,
        title=db_playlist.title,
        user_id=db_playlist.user_id,
        creation_date=db_playlist.creation_date
    )


def update_playlist(db: Session, playlist_id: int, playlist_update: PlaylistRequest, user_id: int) -> PlaylistResponse:
    playlist = db.query(Playlist).filter_by(id=playlist_id).first()

    if not playlist :
        raise HTTPException(status_code=StatusCode.HTTP_404_NOT_FOUND,
                            detail="Playlist not Found")

    if playlist.user_id != user_id:
        raise HTTPException(status_code=StatusCode.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to update this playlist")
    for key, value in playlist_update.dict().items():
        setattr(playlist, key, value)
    db.commit()
    db.refresh(playlist)

    return generate_playlist_response(playlist)


def delete_playlist(db: Session, playlist_id: int, user_id: int) -> bool:
    playlist = db.query(Playlist).filter_by(id=playlist_id).first()
    if playlist.user_id != user_id:
        raise HTTPException(status_code=StatusCode.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to delete this playlist")
    if not playlist :
        return True
    db.delete(playlist)
    db.commit()
    return True
