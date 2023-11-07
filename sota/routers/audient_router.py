# Standard library imports
from typing import List

# Third-party imports
from fastapi import APIRouter, Depends
from pydantic import BaseModel, validator
import pycountry

# Local application imports
from ..database_connection import audient_collection, sport_detail_collection
from .deps.auth_deps import check_auth_key, CheckPermissionsOfKey, AuthScope


country_codes = [country.alpha_2 for country in pycountry.countries]
router = APIRouter(prefix="/audient", tags=["audient"])


class RequestAudientData(BaseModel):
    id: str
    country_code: str
    sport_id: List[int]
    gender: str
    age: int

    @validator("gender")
    def validate_gender(cls, value):
        allowed_values = {"M", "F", "N"}
        if value not in allowed_values:
            raise ValueError(
                f"Invalid value for gender {value}. It must be 'M', 'F', or 'N'."
            )
        return value

    @validator("country_code")
    def validate_country_code(cls, value):
        if value not in country_codes:
            raise ValueError(f"Country {value} doesn't exist")
        return value

    @validator("sport_id", each_item=True)
    def validate_sport_id(cls, value):
        if not sport_detail_collection.find_one({"sport_id": value}):
            raise ValueError(f"The sport_id {value} doesn't exist")
        return value


class RequestListOfAudientData(BaseModel):
    audience: List[RequestAudientData]


def convert_data(data):
    return {
        "country_code": data["country_code"],
        "sport_id": data["sport_id"],
        "gender": data["gender"],
        "age": data["age"],
    }


@router.get("/")
def get_audient():
    audient_all = [convert_data(audient) for audient in audient_collection.find()]
    return audient_all


@router.post(
    "/update_audient_info",
    dependencies=[
        Depends(check_auth_key),
        Depends(CheckPermissionsOfKey([AuthScope.PUBLISH_AUDIENCE])),
    ],
)
async def update_audient_info(data: RequestListOfAudientData):
    audient_data = data.model_dump()
    for item in audient_data["audience"]:
        audient_collection.update_one({"_id": item["id"]}, {"$set": item}, upsert=True)
    return {"Success": audient_data}
