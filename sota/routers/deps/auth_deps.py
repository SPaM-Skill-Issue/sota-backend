from typing import Annotated, List, Dict
from enum import Enum
from fastapi import Request, Header, HTTPException
from ...database_connection import keys_collection

resp401 = HTTPException(status_code=401, detail="Unauthorized access")
authorization_type = "Bearer"


class AuthScope(Enum):
    PUBLISH_MEDAL = "PUBLISH_MEDAL"
    PUBLISH_AUDIENCE = "PUBLISH_AUDIENCE"


def check_auth_key(request: Request):
    try:
        authorization = request.headers["authorization"]
    except KeyError:
        raise resp401
    if not authorization.startswith(authorization_type):
        raise resp401
    key: str = authorization.removeprefix(authorization_type).strip()
    if len(key) != 20:
        raise resp401
    key_doc_queried = keys_collection.find_one({"key": key})
    if not key_doc_queried:
        raise resp401
    request.state.key = key_doc_queried
    return key_doc_queried


class CheckPermissionsOfKey:
    """
    A class dependency to check for permissions of key based on
    scope names given in constructor.
    """

    def __init__(self, scope: List[AuthScope]):
        self.scope = scope

    def __call__(self, request: Request) -> bool:
        try:
            key = request.state.key
            print(key)
            allowed_perms: Dict = key["scope"]
            for perm in self.scope:
                if not perm.value in allowed_perms.keys():
                    raise resp401
                if not allowed_perms[perm.value]:
                    raise resp401
            return True
        except AttributeError:  # no key stored in request
            raise resp401
