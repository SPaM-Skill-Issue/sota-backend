from fastapi import APIRouter
from pymongo import DESCENDING
from pydantic import BaseModel, validator
from typing import List
from ..database_connection import audient_collection


router = APIRouter(
    prefix="/audient",
    tags=["audient"]
)

class RequestAudientData(BaseModel):
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

@router.post("/update_audient_info")
async def update_audient_info(data: RequestListOfAudientData):
    audient_id = 0
    newest_document = audient_collection.find_one(sort=[("_id", DESCENDING)])

    if newest_document:
        audient_id = newest_document["_id"]

    audient_data = data.dict()
    for audient_info in audient_data["audience"]:
        audient_id += 1
        audient_info["_id"] = audient_id

    audient_collection.insert_many(audient_data["audience"])
    return {"Success": audient_data}
