from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies import get_current_user
from helpers.http_status import StatusCode
from models.playlist_models import (
    PlayListResponseWithSongs,
    PlaylistResponse,
    PlaylistRequest,
)
from models.user_models import CurrentUser
from services.playlists import (
    create_playlist,
    delete_playlist,
    get_playlist,
    get_playlists,
    get_playlists_by_user,
    update_playlist,
)

router = APIRouter()


@router.get("/users/{user_id}/playlists", response_model=List[PlaylistResponse])
def get_playlists_endpoint(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    playlists = get_playlists_by_user(db=db, user_id=current_user.user_id)
    return playlists


# @router.get("/users/{user_id}/playlists/{playlist_id}", response_model=PlaylistResponse)
# def get_playlist_endpoint(
#     playlist_id: int,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     playlist = get_playlist_by_id_and_user(
#         db=db, playlist_id=playlist_id, user_id=current_user.user_id
#     )
#     if playlist is None:
#         raise HTTPException(
#             status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Playlist not found"
#         )

#     return playlist


@router.get("/query", response_model=List[PlaylistResponse])
def get_playlist_endpoint(
    limit: int = 10,
    page_number: int = 1,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    playlist = get_playlists(
        limit=limit, page_number=page_number, db=db, user_id=current_user.user_id
    )
    return playlist


@router.get("/{playlist_id}", response_model=PlayListResponseWithSongs)
def get_playlist_endpoint(
    playlist_id: int,
    db: Session = Depends(get_db),
):
    playlist = get_playlist(
        db=db,
        playlist_id=playlist_id,
    )
    if playlist is None:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )

    return playlist


@router.post("/", response_model=PlaylistResponse)
def create_playlist_endpoint(
    playlist_create: PlaylistRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_playlist = create_playlist(
        db=db, playlist_create=playlist_create, user_id=current_user.user_id
    )
    return new_playlist


@router.put("/{playlist_id}", response_model=PlaylistResponse)
def update_playlist_endpoint(
    playlist_id: int,
    playlist_update: PlaylistRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    playlist = update_playlist(
        db=db,
        playlist_id=playlist_id,
        playlist_update=playlist_update,
        user_id=current_user.user_id,
    )
    if playlist is None:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    return playlist


@router.delete("/{playlist_id}", response_model=dict)
def delete_playlist_endpoint(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted = delete_playlist(
        db=db, playlist_id=playlist_id, user_id=current_user.user_id
    )
    if not deleted:
        raise HTTPException(
            status_code=StatusCode.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )
    return {"message": "Playlist deleted"}
