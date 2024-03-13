from .utils import user as user_utils
from app.db.connectors import connector as db_connector
from app._responses import Message


def register_account(username: str, password: str):
    """Account registration API Endpoint."""

    user_utils.check_duplicate(db_connector, username)
    user_utils.create(db_connector, username, password)

    return Message("Registration successfully")
