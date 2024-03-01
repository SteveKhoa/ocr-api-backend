"""Users-related objects and operations on Database.

Interacting with `user` database by importing `connector`
from this module and use the functions defined in this module.
"""

import sqlite3
import hashlib
from fastapi import HTTPException, status
from typing import Annotated
from sqlite3 import Connection
from app.auth.schemas import VerifiedUser

USERS_DB_PATH = "/workspaces/ocr-api-backend/app/db/users.db"

connector = sqlite3.connect(USERS_DB_PATH)


def hash(message: str) -> tuple[str, int]:
    """Hash a message into a string digest.

    ## Return
    `(digest, length)` where, `digest` is the hashed message and `length` is the length (in bytes) of the digest.
    """
    encoded_message = message.encode("utf-8")
    hash_obj = hashlib.md5(encoded_message)
    digest = hash_obj.digest()
    length = len(digest)

    return (digest, length)


def check_duplicate(db_connection: Connection, username: str) -> None:
    """Check duplication of username in the Database"""

    QUERY_USERNAME = """SELECT * FROM user WHERE username=?"""

    query_retval = db_connection.execute(QUERY_USERNAME, (username,))
    retvals = query_retval.fetchall()

    if len(retvals) > 0:  # duplicate username found
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Username duplicated.")

    return


def create(db_connection: Connection, username: str, password: str) -> None:
    """Create a user in the Database"""

    CREATE_USER = (
        """INSERT INTO user (userid, username, hashed_password) VALUES (?, ?, ?)"""
    )

    userid, _ = hash(username)
    hashed_password, _ = hash(password)

    db_connection.execute(CREATE_USER, (userid, username, hashed_password))

    return


def verify_user(
    db_connection: Connection, username: str, password: str
) -> VerifiedUser:
    """Check user inputs `username` and `password` against records
    on `users.db`.

    ## Return
    `VerifiedUser` object.

    For more details of `VerifiedUser`, please see `app/auth/schemas.py`
    """

    QUERY_USER = """SELECT * FROM user WHERE username=? AND hashed_password=?"""

    hashed_password, _ = hash(password)

    query_retval = db_connection.execute(QUERY_USER, (username, hashed_password))
    retvals = query_retval.fetchall()

    print(retvals)

    if len(retvals) <= 0:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid username and password"
        )

    raw_user = retvals[0]
    user_dict = {"username": raw_user[1]}
    verified_user = VerifiedUser(**user_dict)

    return verified_user
