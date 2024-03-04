"""
Authentication-related operations.

Including OAuth2 and APIKey verification steps.
"""

import base64
from typing import Annotated
from fastapi import Depends
from fastapi.security import APIKeyHeader
from .schemas import VerifiedUser
import random
from app.db.utils import hash_bytes
from app.db.apikeys import check_duplicate, create, check_exist
from app.db.utils import connector

api_key_header = APIKeyHeader(name="Username-API-Key")


def generate_apikey(user: VerifiedUser) -> bytes:
    """Generate a random apikey, store it in the database,
    and return the apikey.

    ## Returns
    `apikey` as a `str`.

    ## Notes
    Generation procedure:
    1. Generate an API Key
        API-KEY = base64(random_numbers)
        Check duplicate on API-Key (Not implemented)
        Regenerate if api-key already exists (Not implemented)
    2. Write the API Key down to the database
    3. Return API Key to the user
    """

    # Notes: although the interface requires `user` parameter,
    # this method does not use it. I just put it there with
    # the intention of "requiring user to be verified before
    # generating the apikey".
    #
    # Perhaps in the future apikey should associate with a user.
    # (For now it does not)

    # Why using base64?
    # some bytes in other encoding schemes are not safe (\n, \r, etc.).
    # base64 convert other bytes encoding schemes (utf-8, unicode)
    # into safe bytes.
    random_bytes = random.randbytes(16)  # 128 random bits
    apikey_bytes = base64.b64encode(random_bytes)  # bytes to bytes
    apikey = apikey_bytes.decode("ascii")  # returns string
    check_duplicate(connector, apikey)
    create(connector, apikey)

    return apikey


def verify_apikey(apikey: Annotated[str, Depends(api_key_header)]) -> str:
    """Check validity of provided API-Key."""
    check_exist(connector, apikey)

    return apikey  # pass
