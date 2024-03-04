from fastapi import APIRouter
from fastapi import Form, Depends
from typing import Annotated
from .utils import generate_apikey, verify_apikey
from app.db.utils import connector as db_connector
from app.db import users as users_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/", summary="Greeting message of the module")
async def auth_readme(apikey: Annotated[str, Depends(verify_apikey)]):
    """Default greetings reponse when accessing auth module"""

    return {"text": "Hello world, from /auth module!"}


@auth_router.post("/api-key", summary="Request API-KEY")
async def request_api_key(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """API Endpoint to get API Key.

    New API Key generated on each of this request."""
    user = users_db.verify_user(db_connector, username, password)
    apikey = generate_apikey(user)

    return {"apikey": apikey}


@auth_router.post("/registration", summary="Register a user")
async def register_account(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """Account registration API Endpoint."""

    users_db.check_duplicate(db_connector, username)
    users_db.create(db_connector, username, password)

    return {"message": "Registration successfully"}
