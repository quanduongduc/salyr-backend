from fastapi import APIRouter

router = APIRouter()


@router.get("/{user_id}")
def get_user(user_id: int):
    pass


@router.put("/{user_id}")
def update_user(user_id: int):
    pass


@router.get("/{user_id}/favorites")
def get_favorites(user_id: int):
    pass


@router.post("/{user_id}/favorites/{song_id}")
def add_to_favorites(user_id: int, song_id: int):
    pass


@router.delete("/{user_id}/favorites/{song_id}")
def remove_from_favorites(user_id: int, song_id: int):
    pass


@router.get("{user_id}/play-history")
def get_play_history(user_id: int):
    pass


@router.post("{user_id}/play-history/{song_id}")
def add_to_play_history(user_id: int, song_id: int):
    pass
