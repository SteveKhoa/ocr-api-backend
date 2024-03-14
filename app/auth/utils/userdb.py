"""
User authentication & authorization utility
functions.
"""

from fastapi import HTTPException, status
from sqlite3 import Connection
from app.auth.schemas import VerifiedUser
from app.db.security import hash_bytes


def __hash_password_to_b64_string(password: str) -> str:
    password_binary = password.encode("ascii")
    hashed_bytes = hash_bytes(password_binary)
    hashed_password = hashed_bytes.decode("ascii")

    return hashed_password


def check_duplicate(
    db_connection: Connection,
    username: str,
) -> bool:
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


def create(
    db_connection: Connection,
    username: str,
    password: str,
) -> None:
    """Create a user in the Database"""

    CREATE_USER = """INSERT INTO user (username, hashed_password) VALUES (?, ?)"""

    hashed_password = __hash_password_to_b64_string(password)

    db_connection.execute(CREATE_USER, (username, hashed_password))
    db_connection.commit()

    return


def verify_user(
    db_connection: Connection,
    username: str,
    password: str,
) -> None:
    """Check user inputs `username` and `password` against records
    on `users.db`.
    """

    QUERY_USER = """SELECT * FROM user WHERE username=? AND hashed_password=?"""

    hashed_password = __hash_password_to_b64_string(password)

    query_retval = db_connection.execute(QUERY_USER, (username, hashed_password))
    retvals = query_retval.fetchall()

    if len(retvals) <= 0:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid username and password"
        )

    return


def change_password(
    db_connection: Connection,
    username: str,
    new_password: str,
) -> None:
    CHANGE_PASSWORD = """UPDATE user SET hashed_password=? WHERE username=?"""

    hashed_password = __hash_password_to_b64_string(new_password)

    db_connection.execute(CHANGE_PASSWORD, (hashed_password, username))
    db_connection.commit()

    return


def delete(
    db_connection: Connection,
    username: str,
) -> None:
    DELETE_ACCOUNT = """DELETE FROM user WHERE username=?"""

    db_connection.execute(DELETE_ACCOUNT, (username,))
    db_connection.commit()

    return


def get(
    db_connection: Connection,
    username: str,
    query: str,
) -> str:
    GET_INFO = """SELECT ? FROM user WHERE username=?"""

    query_retval = db_connection.execute(GET_INFO, (query, username))
    retvals = query_retval.fetchall()

    return str(retvals[0])
