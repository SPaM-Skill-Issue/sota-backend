from fastapi import APIRouter
from ..database_connection import medal_collection, sport_detail_collection, sub_sport_collection

router = APIRouter(prefix="/medal", tags=["medal"])


@router.get("/c/{country_code}")
def get_medal_by_country(country_code: str):
    pipeline = [
        {"$match": {"country_code": country_code}},
        {"$unwind": {"path": "$sports"}},
        {
            "$lookup": {
                "from": sport_detail_collection.name,
                "localField": "sports.sport_id",
                "foreignField": "sport_id",
                "as": "sport_info",
            }
        },
        {"$unwind": {"path": "$sport_info"}},
        {
            "$lookup": {
                "from": sub_sport_collection.name,
                "let": {
                    "type_id_local": "$sports.type_id",
                    "sport_id_local": "$sports.sport_id",
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$type_id", "$$type_id_local"]},
                                    {"$eq": ["$sport_id", "$$sport_id_local"]},
                                ]
                            }
                        }
                    }
                ],
                "as": "matched_from_SubSportType",
            }
        },
        {"$unwind": {"path": "$matched_from_SubSportType"}},
        {
            "$group": {
                "_id": {"sport_id": "$sports.sport_id"},
                "sport_name": {"$first": "$sport_info.sport_name"},
                "country_code": {"$first": "$country_code"},
                "country_name": {"$first": "$country_name"},
                "gold": {"$sum": "$sports.gold"},
                "silver": {"$sum": "$sports.silver"},
                "bronze": {"$sum": "$sports.bronze"},
                "sub_sports": {
                    "$push": {
                        "sub_id": "$sports.type_id",
                        "sub_name": "$matched_from_SubSportType.type_name",
                        "gold": "$sports.gold",
                        "silver": "$sports.silver",
                        "bronze": "$sports.bronze",
                    }
                },
            }
        },
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
                        "sub_sports": "$sub_sports",
                    }
                },
            }
        },
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
        {"$match": {"sports.sport_id": sport_id}},
        {
            "$lookup": {
                "from": sport_detail_collection.name,
                "localField": "sports.sport_id",
                "foreignField": "sport_id",
                "as": "sport_info",
            }
        },
        {"$unwind": {"path": "$sport_info"}},
        {
            "$lookup": {
                "from": sub_sport_collection.name,
                "let": {
                    "type_id_local": "$sports.type_id",
                    "sport_id_local": "$sports.sport_id",
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$type_id", "$$type_id_local"]},
                                    {"$eq": ["$sport_id", "$$sport_id_local"]},
                                ]
                            }
                        }
                    }
                ],
                "as": "matched_from_SubSportType",
            }
        },
        {"$unwind": {"path": "$matched_from_SubSportType"}},
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
                        "sub_name": "$matched_from_SubSportType.type_name",
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


@router.get("/s/{sport_id}/t/{subsport_id}")
def get_medal_by_subsport(sport_id: int, subsport_id: int):
    pipeline = [
        {
            '$unwind': {
                'path': '$sports'
            }
        }, {
            '$match': {
                'sports.sport_id': sport_id,
                'sports.type_id': subsport_id
            }
        }, {
            '$lookup': {
                'from': sport_detail_collection.name,
                'localField': 'sports.sport_id',
                'foreignField': 'sport_id',
                'as': 'sportdetail'
            }
        }, {
            '$unwind': {
                'path': '$sportdetail'
            }
        }, {
            '$lookup': {
                'from': sub_sport_collection.name,
                'let': {
                    'type_id_local': '$sports.type_id',
                    'sport_id_local': '$sports.sport_id'
                },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {
                                        '$eq': [
                                            '$type_id', '$$type_id_local'
                                        ]
                                    }, {
                                        '$eq': [
                                            '$sport_id', '$$sport_id_local'
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ],
                'as': 'matched_from_SubSportType'
            }
        }, {
            '$unwind': {
                'path': '$matched_from_SubSportType'
            }
        }, {
            '$group': {
                '_id': {
                    'sportid': '$sports.sport_id',
                    'typeid': '$sports.type_id'
                },
                'gold': {
                    '$sum': '$sports.gold'
                },
                'silver': {
                    '$sum': '$sports.silver'
                },
                'bronze': {
                    '$sum': '$sports.bronze'
                },
                'sport_name': {
                    '$first': '$sportdetail.sport_name'
                },
                'type_name': {
                    '$first': '$matched_from_SubSportType.type_name'
                },
                'individual_countries': {
                    '$push': {
                        'country_code': '$country_code',
                        'country_name': '$country_name',
                        'gold': '$sports.gold',
                        'silver': '$sports.silver',
                        'bronze': '$sports.bronze'
                    }
                }
            }
        }, {
            '$project': {
                'sport_id': '$_id.sportid',
                'sport_name': '$sport_name',
                'sub_sport_id': '$_id.typeid',
                'sub_sport_name': '$type_name',
                'gold': 1,
                'silver': 1,
                'bronze': 1,
                'individual_countries': '$individual_countries',
                '_id': 0
            }
        }
    ]
    sport_medals = list(medal_collection.aggregate(pipeline))
    return sport_medals[0] if sport_medals else {}
