from fastapi import APIRouter


router = APIRouter(
    prefix="/sport",
    tags=["sport"]
)


@router.get("/{sport_id}")
def get_sport_by_id(sport_id: str):
    return {"test": sport_id}


@router.get("/all")
def get_all_sport():
    return {"test": "all good"}
