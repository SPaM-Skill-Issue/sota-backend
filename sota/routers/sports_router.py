from fastapi import APIRouter
from ..database_connection import sport_detail_collection

router = APIRouter(prefix="/sports", tags=["sports"])


@router.get("/")
def get_all_sports_id():

    sport_pairs = sport_detail_collection.aggregate(
        [
            {
                "$replaceRoot": {
                    "newRoot": {
                        "$arrayToObject": [
                            [{"k": {"$toString": "$sport_id"}, "v": "$sport_name"}]
                        ]
                    }
                }
            }
        ]
    )

    res = dict()
    for entry in sport_pairs:
        item = list(entry.items())[0]
        res[item[0]] = item[1]

    return res
