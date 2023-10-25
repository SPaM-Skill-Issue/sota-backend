from fastapi import APIRouter
from ..database_connection import medal_collection, sport_detail_collection

router = APIRouter(prefix="/medal", tags=["medal"])


@router.get("/c/{country_code}")
def get_medal_by_country(country_code: str):
    pipeline = [
        # Filter the documents based on the provided country code.
        {"$match": {"country_code": f"{country_code}"}},
        # Deconstruct the "sports" array field from the input documents to output a document for each element.
        {"$unwind": {"path": "$sports"}},
        # Join the current documents with the sport_detail_collection on the sport_id field.
        {
            "$lookup": {
                "from": sport_detail_collection.name,
                "localField": "sports.sport_id",
                "foreignField": "sport_id",
                "as": "sport_info",
            }
        },
        {"$unwind": {"path": "$sport_info"}},
        # Group by sport_id to aggregate the medal counts.
        {
            "$group": {
                "_id": {"sport_id": "$sports.sport_id"},
                "sport_name": {"$first": "$sport_info.sport_name"},
                "country_code": {"$first": "$country_code"},
                "country_name": {"$first": "$country_name"},
                "gold": {"$sum": "$sports.gold"},
                "silver": {"$sum": "$sports.silver"},
                "bronze": {"$sum": "$sports.bronze"},
            }
        },
        # Further group by country_code to aggregate the total medal counts and form the individual_sports array.
        {
            "$group": {
                "_id": "$country_code",
                "country_name": {"$first": "$country_name"},
                "gold": {"$sum": "$gold"},
                "silver": {"$sum": "$silver"},
                "bronze": {"$sum": "$bronze"},
                "individual_sports": {
                    "$push": {
                        "sport_id": "$_id.sport_id",
                        "sport_name": "$sport_name",
                        "gold": "$gold",
                        "silver": "$silver",
                        "bronze": "$bronze",
                    }
                },
            }
        },
        # Restructure the output fields.
        {
            "$project": {
                "country": "$_id",
                "country_name": 1,
                "gold": 1,
                "silver": 1,
                "bronze": 1,
                "individual_sports": 1,
                "_id": 0,
            }
        },
    ]

    result = list(medal_collection.aggregate(pipeline))
    return list(medal_collection.aggregate(pipeline))[0] if result else {}


@router.get("/s/{sport_id}")
def get_medal_by_sport(sport_id: str):
    return {"test": sport_id}
