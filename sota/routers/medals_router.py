from pydantic import BaseModel, model_validator, Field
import pycountry
from fastapi import APIRouter
from pydantic import BaseModel
from ..database_connection import medal_collection, sub_sport_collection


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


class RequestMedal(BaseModel):
    gold: int = Field(default=0, ge=0)
    silver: int = Field(default=0, ge=0)
    bronze: int = Field(default=0, ge=0)


class RequestParticipant(BaseModel):
    country: str
    medal: RequestMedal


class RequestUpdateMedal(BaseModel):
    sport_id: int = Field(gt=0)
    sport_type_id: int = Field(gt=0)
    participants: list[RequestParticipant]

    # This validator checks if the participating countries are valid for the given sport and sport type.
    @model_validator(mode="after")
    def check_countries_in_participation(self):
        # Retrieve details from the model instance
        sport_id = self.sport_id
        sport_type_id = self.sport_type_id
        participants = self.participants

        # Fetch the participating countries for the given sport and type
        participating_countries = get_participating_countries(sport_id, sport_type_id)

        # Loop through all participants to verify their country's participation
        for participant in participants:
            country = participant.country
            if country not in participating_countries:
                raise ValueError(
                    f"Country {country} is not participating in the given sport_id {sport_id} and type_id {sport_type_id}"
                )
        return self


# Helper function to retrieve participating countries based on sport and type.
def get_participating_countries(sport_id: int, sport_type_id: int) -> list:
    # Query the database to find the details of the sport type.
    detail = sub_sport_collection.find_one(
        {"sport_id": sport_id, "type_id": sport_type_id}
    )
    return detail["participating_countries"] if detail else []


@router.post("/update_medal")
async def update_medal(data: RequestUpdateMedal):
    for request_participant in data.participants:
        country_code = request_participant.country
        sport_data = {
            "sport_id": data.sport_id,
            "type_id": data.sport_type_id,
            "gold": request_participant.medal.gold,
            "silver": request_participant.medal.silver,
            "bronze": request_participant.medal.bronze,
        }

        # Attempt to update existing document or create a new one
        updated = medal_collection.update_one(
            {
                "country_code": country_code,
                "sports.sport_id": data.sport_id,
                "sports.type_id": data.sport_type_id,
            },
            {
                "$set": {
                    "sports.$.gold": request_participant.medal.gold,
                    "sports.$.silver": request_participant.medal.silver,
                    "sports.$.bronze": request_participant.medal.bronze,
                }
            },
        ).matched_count

        if not updated:
            # If not updated, either push to sports or insert a new document
            updated = medal_collection.update_one(
                {"country_code": country_code}, {"$push": {"sports": sport_data}}
            ).matched_count

            if not updated:
                country_name = pycountry.countries.get(alpha_2=country_code).name
                medal_collection.insert_one(
                    {
                        "country_code": country_code,
                        "country_name": country_name,
                        "sports": [sport_data],
                    }
                )

    return {"Success": data}
