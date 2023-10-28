from fastapi import APIRouter


router = APIRouter(
    prefix="/medals",
    tags=["medals"]
)


@router.get("/")
def get_medals():
    return {"test": "all good"}
