"""
Authentication-related operations.

Including OAuth2 and APIKey verification steps.
"""
from typing import Annotated
from fastapi import Depends
from fastapi import HTTPException, status
from .schemas import UserInDB
from fastapi.security import APIKeyHeader
from .schemas import VerifiedUser

api_key_header = APIKeyHeader(name="Username-API-Key")


def generate_oauth2_token(user: UserInDB, expiration=60) -> str:
    return "atoken_{}".format(user.name)  # for now let me just return a very fake token


def generate_apikey(user: VerifiedUser):
    return user.username  # for prototyping, i return the username as api-key


def verify_apikey(apikey: Annotated[str, Depends(api_key_header)]):
    # for now, no verification. just return the apikey as-it-is.
    # however, only allows api-key 'jonhdoe' to pass
    if apikey == "jonhdoe":
        return apikey
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API-Key"
    )
