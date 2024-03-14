from .utils import userdb
from app.db.connectors import connector as db_connector
from app._responses import Message
import app._exceptions
import app.auth.utils.jwt
import app.auth.schemas


def register_account(username: str, password: str) -> str:
    """Create a new entry for `user` on the database.

    If `user` already exists, then database will not
    create new one.

    ### Returns
    `encoded_jwt` as `str`
    """

    is_duplicate = userdb.check_duplicate(db_connector, username)
    if is_duplicate:
        userdb.verify_user(db_connector, username, password)
        pass
    else:
        userdb.create(db_connector, username, password)

    encoded_jwt = app.auth.utils.jwt.create_id_token({"username": username})

    return encoded_jwt


def change_password(username: str, new_password: str) -> None:
    """Change password of an account

    If account is invalid or not existed, returns response message.
    """

    exist = userdb.check_duplicate(db_connector, username)
    if not exist:
        raise app._exceptions.DatabaseEntryNotExisted("username")

    userdb.change_password(db_connector, username, new_password)


def delete_account(username: str) -> None:
    """Delete an account permanently

    If account is invalid or not existed, returns response message."""

    exist = userdb.check_duplicate(db_connector, username)
    if not exist:
        raise app._exceptions.DatabaseEntryNotExisted("username")

    userdb.delete(db_connector, username)


def get_info(username: str, query: str) -> str:
    """Query an account's information

    If account is invalid or not existed, returns response message."""

    exist = userdb.check_duplicate(db_connector, username)
    if not exist:
        raise app._exceptions.DatabaseEntryNotExisted("username")

    data = userdb.get(db_connector, username, query)

    return data
