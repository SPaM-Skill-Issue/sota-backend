from fastapi import APIRouter
from database_connection import keys_collection
from pydantic import BaseModel

router = APIRouter(
    prefix="/apikeygen",
    tags=["keygen"]
)

class ScopeEnum(BaseModel):
    PUBLISH_MEDAL: bool
    PUBLISH_AUDIENCE: bool

@router.post("/")
def gen_new_key(scope: ScopeEnum):

    """
    Generate 20 character long key,
    check permissions via payload (body),
    save to new entry in collection.
    
    Expected body:
    {
        "scope": {
            "PUBLISH_MEDAL": true,
            "PUBLISH_AUDIENCE": false
        }
    }
    """
    pass