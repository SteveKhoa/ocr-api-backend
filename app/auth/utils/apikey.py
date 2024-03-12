"""
API-Key utility functions
"""

import base64
from typing import Annotated
from fastapi import Depends
from fastapi.security import APIKeyHeader
from ..schemas import VerifiedUser
import random
from app.db.utils import connector
from sqlite3 import Connection
from fastapi import HTTPException, status

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
    is_duplicate = check_duplicate(connector, apikey)

    if is_duplicate:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Generated API-Key is a duplicate."
        )

    create(connector, apikey)

    return apikey


def verify_apikey(apikey: Annotated[str, Depends(api_key_header)]) -> str:
    """Check validity of provided API-Key.

    ## Returns
    `apikey` as str
    """
    is_duplicate = check_duplicate(connector, apikey)

    if not is_duplicate:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Provided API-Key is not valid."
        )

    return apikey


def check_duplicate(db_connection: Connection, apikey: str) -> bool:
    """Check duplication of apikey on the database.

    ## Return
    `True` if duplicate entry is found.

    `False` if no duplicate entry.
    """

    is_duplicate = False

    QUERY_APIKEY = """SELECT * FROM apikey WHERE str=?"""

    query_retval = db_connection.execute(QUERY_APIKEY, (apikey,))
    retvals = query_retval.fetchall()

    if len(retvals) > 0:  # duplicate apikey found
        is_duplicate = True
    else:
        is_duplicate = False

    return is_duplicate  # pass the check


def create(db_connection: Connection, apikey: str) -> None:
    """Create a database entry for apikey"""

    CREATE_APIKEY = """INSERT INTO apikey VALUES (?)"""

    # Note: raw apikey is stored to the database, no
    # hash is performed.
    db_connection.execute(CREATE_APIKEY, (apikey,))

    return  # done procedure
