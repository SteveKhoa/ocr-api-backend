import jwt
import time
import os
from app.idp.schemas.Client import Client
from app.exceptions import InvalidAccount


def read_account(client: Client) -> str:
    """Create an JWT ID Token based on identity of a registered client.

    Args:
        client (Client):

    Raises:
        InvalidAccount:
            this exception is raised when the registered client does not
            exist in the database or username or password is invalid.

    Returns:
        encoded_jwt(str): JWT ID Token
    """
    if client.exists():
        id_token = jwt.encode(
            payload={
                "name": str(client.username),
                "iat": time.time(),
                "exp": time.time() + 60 * 60,
            },
            key=os.environ.get("SECRET_KEY"),
            algorithm="HS256",
        )

        return id_token
    else:
        raise InvalidAccount(client)


def create_account(db_url: str, username: str, password: str) -> Client:
    """Create a new client in the database.

    Args:
        db_url (str):
        username (str):
        password (str):

    Raises:
        InvalidAccount: when client is already existed

    Returns:
        client(Client):
    """
    client = Client(db_src=db_url, username=username, password=password)

    if not client.exists():
        client.create()
    else:
        raise InvalidAccount(client)

    return client