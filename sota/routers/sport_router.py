from typing import Optional, Dict
from fastapi import APIRouter
from ..database_connection import sport_detail_collection, sub_sport_collection


router = APIRouter(prefix="/sport", tags=["sport"])


def retrieve_sport_info(sport_id: Optional[int] = None):
    """
    Returns a PyMongo's cursor from aggregation, the pipeline works as follow:

    - Matches the sport_id if given,
    - Project the root data with everything except: _id
    - Lookup from the sub sport type collection and
      join the output as `sport_types`
    """

    match_op: Optional[Dict] = None
    if sport_id:
        match_op = {"$match": {"sport_id": sport_id}}

    projection_op = {"$project": {"_id": 0, "sport_id": 0}}

    lookup_op: Dict = {
        "$lookup": {
            "from": sub_sport_collection.name,
            "localField": "sport_id",
            "foreignField": "sport_id",
            "as": "sport_types",
            "pipeline": [projection_op],
        }
    }

    pipeline = []
    if match_op:
        pipeline.append(match_op)
    pipeline.extend(({"$project": {"_id": 0}}, lookup_op))

    return sport_detail_collection.aggregate(pipeline)


@router.get("/all")
def get_all_sport():
    """
    Gets all sport details from collection as list.
    """
    return list(retrieve_sport_info())


@router.get("/{sport_id}")
def get_sport_by_id(sport_id: int):
    """
    Gets a specific sport details as object or blank object if not found.
    """
    res = list(retrieve_sport_info(sport_id))
    if not res:
        return {}
    return res[0]
