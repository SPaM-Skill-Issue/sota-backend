from fastapi import APIRouter
from ..database_connection import audient_collection


router = APIRouter(
    prefix="/audient",
    tags=["audient"]
)


@router.get("/")
def get_audient():
    return {"test": "all good"}
