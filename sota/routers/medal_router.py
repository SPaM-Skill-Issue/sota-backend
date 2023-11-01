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

    country_medals = list(medal_collection.aggregate(pipeline))
    return country_medals[0] if country_medals else {}


@router.get("/s/{sport_id}")
def get_medal_by_sport(sport_id: int):
    pipeline = [
        {"$unwind": {"path": "$sports"}},
        {"$match": {"sports.sport_id": 1}},
        {
            "$lookup": {
                "from": "SportDetail",
                "localField": "sports.sport_id",
                "foreignField": "sport_id",
                "as": "sport_info",
            }
        },
        {"$unwind": {"path": "$sport_info"}},
        {
            "$group": {
                "_id": "$country_code",
                "gold": {"$sum": "$sports.gold"},
                "silver": {"$sum": "$sports.silver"},
                "bronze": {"$sum": "$sports.bronze"},
                "country_name": {"$first": "$country_name"},
                "sport_id": {"$first": "$sports.sport_id"},
                "sport_name": {"$first": "$sport_info.sport_name"},
                "sub_sports": {
                    "$push": {
                        "sub_id": "$sports.type_id",
                        "gold": "$sports.gold",
                        "silver": "$sports.silver",
                        "bronze": "$sports.bronze",
                    }
                },
            }
        },
        {
            "$group": {
                "_id": "$sport_id",
                "sport_name": {"$first": "$sport_name"},
                "gold": {"$sum": "$gold"},
                "silver": {"$sum": "$silver"},
                "bronze": {"$sum": "$bronze"},
                "individual_countries": {
                    "$push": {
                        "country_code": "$_id",
                        "country_name": "$country_name",
                        "gold": "$gold",
                        "silver": "$silver",
                        "bronze": "$bronze",
                        "sub_sports": "$sub_sports",
                    }
                },
            }
        },
        {
            "$project": {
                "_id": 0,
                "sport": "$_id",
                "sport_name": 1,
                "gold": 1,
                "silver": 1,
                "bronze": 1,
                "individual_countries": 1,
            }
        },
    ]

    sport_medals = list(medal_collection.aggregate(pipeline))
    return sport_medals[0] if sport_medals else {}
