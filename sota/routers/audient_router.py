from fastapi import APIRouter
from ..database_connection import audient_collection


router = APIRouter(
    prefix="/audient",
    tags=["audient"]
)

def convert_data(data):
    return{
        "country": data["country_code"],
        "sport_id": data["sport_id"],
        "gender": data["gender"],
        "age": data["age"]
    }

@router.get("/")
def get_audient():
    audient_all = [convert_data(audient) for audient in audient_collection.find()]
    return audient_all
