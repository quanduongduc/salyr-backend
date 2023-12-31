from typing import Dict, List
from fastapi import APIRouter, Depends, UploadFile
from db.database import get_db
from db.schema import User

from dependencies import get_current_user
from sqlalchemy.orm import Session
from models.songs_models import SongResponse


from models.user_models import CurrentUser, UserResponse, UserUpdate
from services.users import add_to_favorites, get_favorites, get_user_by_id, remove_from_favorites, update_user, update_user_lastplay
router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_user_endpoint(db : Session = Depends(get_db) , current_user: CurrentUser = Depends(get_current_user)) -> UserResponse:
    response = get_user_by_id(db, current_user.user_id)

    return response


@router.put("/lastplay/{song_id}", response_model=Dict)
def update_lastplay_endpoint(song_id: str, db : Session = Depends(get_db) , current_user: CurrentUser = Depends(get_current_user)) -> UserResponse:
    response = update_user_lastplay(
        db=db, user_id=current_user.user_id, song_id=song_id)

    return response


@router.get("/favorites", response_model=List[SongResponse])
def get_favorites_endpoint(db : Session = Depends(get_db) , user: CurrentUser = Depends(get_current_user)):
    response = get_favorites(db, user.user_id)
    return response


# @router.get("/{user_id}")
# def get_user_endpoint(user_id: int, db : Session = Depends(get_db), ):
#     pass


@router.put("/", response_model=UserResponse)
def update_user_endpoint(user_info : UserUpdate = Depends(UserUpdate.as_form), avatar: UploadFile = None, db : Session = Depends(get_db) , user: CurrentUser = Depends(get_current_user)):
    response = update_user(db=db, id=user.user_id,
                           avatar_file=avatar, user_info=user_info)
    return response


@router.post("/favorites/{song_id}", response_model=Dict)
def add_to_favorites_endpoint(song_id: int, user: CurrentUser = Depends(get_current_user), db : Session = Depends(get_db)):
    response = add_to_favorites(db=db, user_id=user.user_id, song_id=song_id)
    if response :
        return {"message": "add favorite successfully"}
    return {"message": "user not found"}


@router.post("/remove-favorites/{song_id}", response_model=Dict)
def add_to_favorites_endpoint(song_id: int, user: CurrentUser = Depends(get_current_user), db : Session = Depends(get_db)):
    response = remove_from_favorites(db=db, user_id=user.user_id, song_id=song_id)
    if response :
        return {"message": "remove favorite successfully"}
    return {"message": "fail to remove favorite"}
