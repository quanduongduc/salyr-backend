from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_albums():
    pass


@router.get("/{album_id}")
def get_album(album_id: int):
    pass


@router.post("/")
def create_album():
    pass


@router.put("/{album_id}")
def update_album(album_id: int):
    pass


@router.delete("/{album_id}")
def delete_album(album_id: int):
    pass
