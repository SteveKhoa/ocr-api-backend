from fastapi import APIRouter
from fastapi import Form
from typing import Annotated
from .utils import generate_apikey
from app.db import users as users_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/", summary="Greeting message of the module")
async def auth_readme():
    """Default greetings reponse when accessing auth module"""

    return {"text": "Hello world, from /auth module!"}


# @auth_router.post("/token", summary="Request OAuth2 token")
# async def request_oauth2_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     """API Endpoint to get OAuth2 Token.

#     Implement for fun, currently there is no api endpoint requiring oauth2"""

#     user = verify_user(form_data.username, form_data.password, fake_users_db)
#     token = generate_oauth2_token(user)

#     # Provide access-token
#     return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/api-key", summary="Request API-KEY")
async def request_api_key(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """API Endpoint to get API Key."""
    user = users_db.verify_user(users_db.connector, username, password)
    apikey = generate_apikey(user)

    return apikey


@auth_router.post("/registration", summary="Register a user")
async def register_account(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):
    """Account registration API Endpoint."""

    users_db.check_duplicate(users_db.connector, username)
    users_db.create(users_db.connector, username, password)

    return {"message": "Registration successfully"}
