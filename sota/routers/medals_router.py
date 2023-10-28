from fastapi import APIRouter
from ..database_connection import medal_collection


router = APIRouter(prefix="/medals", tags=["medals"])


@router.get("/")
def get_medals():
    pipeline = [
        {"$unwind": {"path": "$sports"}},
        {
            "$group": {
                "_id": "$country_code",
                "gold": {"$sum": "$sports.gold"},
                "silver": {"$sum": "$sports.silver"},
                "bronze": {"$sum": "$sports.bronze"},
            }
        },
        {
            "$group": {
                "_id": None,
                "data": {
                    "$push": {
                        "k": "$_id",
                        "v": {
                            "gold": "$gold",
                            "silver": "$silver",
                            "bronze": "$bronze",
                        },
                    }
                },
            }
        },
        {"$replaceRoot": {"newRoot": {"$arrayToObject": "$data"}}},
    ]

    medals = list(medal_collection.aggregate(pipeline))
    return medals[0] if medals else {}
