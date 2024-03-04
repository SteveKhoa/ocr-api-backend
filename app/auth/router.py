from fastapi import APIRouter
from fastapi import Form, Depends
from typing import Annotated
from .utils import apikey as apikey_utils
from .utils import user as user_utils
from app.db.utils import connector as db_connector

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/", summary="Greeting message of the module")
async def auth_readme(apikey: Annotated[str, Depends(apikey_utils.verify_apikey)]):
    """Default greetings reponse when accessing auth module"""

    return {"text": "Hello world, from /auth module!"}


@auth_router.post("/api-key", summary="Request API-KEY")
async def request_api_key(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """API Endpoint to get API Key.

    New API Key generated on each of this request."""
    user = user_utils.verify_user(db_connector, username, password)
    apikey = user_utils.generate_apikey(user)

    return {"apikey": apikey}


@auth_router.post("/registration", summary="Register a user")
async def register_account(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """Account registration API Endpoint."""

    user_utils.check_duplicate(db_connector, username)
    user_utils.create(db_connector, username, password)

    return {"message": "Registration successfully"}
