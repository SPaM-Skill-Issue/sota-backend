from fastapi import APIRouter, Depends
from pymongo import DESCENDING
from pydantic import BaseModel, validator
from typing import List
from ..database_connection import audient_collection
from .deps.auth_deps import check_auth_key, CheckPermissionsOfKey, AuthScope


router = APIRouter(
    prefix="/audient",
    tags=["audient"]
)

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
            raise ValueError("Invalid value for gender. It must be 'M', 'F', or 'N'.")
        return value

class RequestListOfAudientData(BaseModel):
    audience: List[RequestAudientData]

def convert_data(data):
    return{
        "country_code": data["country_code"],
        "sport_id": data["sport_id"],
        "gender": data["gender"],
        "age": data["age"]
    }

@router.get("/")
def get_audient():
    audient_all = [convert_data(audient) for audient in audient_collection.find()]
    return audient_all

@router.post("/update_audient_info", dependencies=[
    Depends(check_auth_key),
    Depends(CheckPermissionsOfKey([
        AuthScope.PUBLISH_AUDIENCE
    ]))
])
async def update_audient_info(data: RequestListOfAudientData):
    audient_data = data.dict()
    for item in audient_data["audience"]:
        audient_collection.update_one(
            {"_id": item["id"]},
            {"$set": item},
            upsert=True
        )
    return {"Success": audient_data}
