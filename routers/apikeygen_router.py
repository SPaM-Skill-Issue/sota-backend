from typing import Dict
from fastapi import APIRouter, HTTPException
from database_connection import keys_collection
from pydantic import BaseModel
from .deps.auth_deps import AuthScope
import random, string

router = APIRouter(prefix="/apikeygen", tags=["keygen"])


class ScopeDict(BaseModel):
    scope: Dict[AuthScope, bool]


@router.post("/")
def gen_new_key(scope: ScopeDict):
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
    if not scope:
        return HTTPException(400, detail="No scope defined")

    # generate a unique key
    key = ""
    while True:
        key = "".join(
            random.choices(string.ascii_letters + string.digits, k=20)
        )  # alpha-numeric
        if not keys_collection.find_one({"key": key}):
            break

    keys_collection.insert_one(
        {
            "key": key,
            "scope": {perm.value: state for perm, state in scope.scope.items()},
        }
    )

    return {"key": key}
