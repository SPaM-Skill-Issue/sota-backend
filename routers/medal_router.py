from fastapi import APIRouter


router = APIRouter(
    prefix="/medal",
    tags=["medal"]
)


@router.get("/c/{country_code}")
def get_medal_by_country(country_code: str):
    return {"test": country_code}


@router.get("/s/{sport_id}")
def get_medal_by_sport(sport_id: str):
    return {"test": sport_id}
