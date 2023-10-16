from fastapi import APIRouter


router = APIRouter(
    prefix="/sports",
    tags=["sports"]
)


@router.get("/sports")
def get_all_sports_id():
    return {"test": "all good"}
