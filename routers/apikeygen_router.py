from fastapi import APIRouter, HTTPException
from ..database_connection import keys_collection
from pydantic import BaseModel
import random, string

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
    if scope.PUBLISH_MEDAL or scope.PUBLISH_AUDIENCE is None:
        return HTTPException(400, detail="Permission should not be null")

    key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))  # alpha-numeric
    keys_collection.insert_one(
        {
            "key": key,
            "scope": {
                "PUBLISH_MEDAL": scope.PUBLISH_MEDAL,
                "PUBLISH_AUDIENCE": scope.PUBLISH_AUDIENCE
            }
        }
    )
