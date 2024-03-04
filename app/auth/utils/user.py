"""
User authentication & authorization utility
functions.
"""

from fastapi import HTTPException, status
from sqlite3 import Connection
from app.auth.schemas import VerifiedUser
from app.db.utils import hash_bytes


def check_duplicate(db_connection: Connection, username: str) -> bool:
    """Check duplication of username in the Database"""

    is_duplicate = False

    QUERY_USERNAME = """SELECT * FROM user WHERE username=?"""

    query_retval = db_connection.execute(QUERY_USERNAME, (username,))
    retvals = query_retval.fetchall()

    if len(retvals) > 0:  # duplicate username found
        is_duplicate = True
    else:
        is_duplicate = False

    return is_duplicate


def create(db_connection: Connection, username: str, password: str) -> None:
    """Create a user in the Database"""

    CREATE_USER = """INSERT INTO user (username, hashed_password) VALUES (?, ?)"""

    password_binary = password.encode("ascii")
    hashed_bytes = hash_bytes(password_binary)
    hashed_password = hashed_bytes.decode("ascii")

    db_connection.execute(CREATE_USER, (username, hashed_password))
    db_connection.commit()

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

    password_binary = password.encode("ascii")
    hashed_bytes = hash_bytes(password_binary)
    hashed_password = hashed_bytes.decode("ascii")

    query_retval = db_connection.execute(QUERY_USER, (username, hashed_password))
    retvals = query_retval.fetchall()

    if len(retvals) <= 0:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid username and password"
        )

    raw_user = retvals[0]
    user_dict = {"username": raw_user[0]}
    verified_user = VerifiedUser(**user_dict)

    return verified_user
