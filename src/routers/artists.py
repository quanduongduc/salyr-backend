from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_artists():
    pass

@router.get("/{artist_id}")
def get_artist(artist_id: int):
    pass

@router.post("/")
def create_artist():
    pass

@router.put("/{artist_id}")
def update_artist(artist_id: int):
    pass

@router.delete("/{artist_id}")
def delete_artist(artist_id: int):
    pass
