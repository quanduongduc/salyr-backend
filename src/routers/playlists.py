from fastapi import APIRouter

router = APIRouter()


@router.get("/users/{user_id}/playlists")
def get_playlists(user_id: int):
    pass


@router.get("/users/{user_id}/playlists/{playlist_id}")
def get_playlist(user_id: int, playlist_id: int):
    pass


@router.post("/users/{user_id}/playlists")
def create_playlist(user_id: int):
    pass


@router.put("/users/{user_id}/playlists/{playlist_id}")
def update_playlist(user_id: int, playlist_id: int):
    pass


@router.delete("/users/{user_id}/playlists/{playlist_id}")
def delete_playlist(user_id: int, playlist_id: int):
    pass


@router.post("/users/{user_id}/playlists/{playlist_id}/songs/{song_id}")
def add_song_to_playlist(user_id: int, playlist_id: int, song_id: int):
    pass


@router.delete("/users/{user_id}/playlists/{playlist_id}/songs/{song_id}")
def remove_song_from_playlist(user_id: int, playlist_id: int, song_id: int):
    pass
