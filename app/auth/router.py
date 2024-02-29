from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import User, UserInDB
from .utils import verify_user, generate_oauth2_token
from .utils import fake_users_db
from .utils import fake_apikey_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/", summary="Greeting message of the module")
async def auth_readme():
    """Default greetings reponse when accessing auth module"""

    return {"text": "Hello world, from /auth module!"}


@auth_router.post("/token", summary="Request OAuth2 token")
async def request_oauth2_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """API Endpoint to get OAuth2 Token.

    Implement for fun, currently there is no api endpoint requiring oauth2"""

    user = verify_user(form_data.username, form_data.password, fake_users_db)
    token = generate_oauth2_token(user)

    # Provide access-token
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/api-key", summary="Request API-KEY")
async def request_api_key():
    """API Endpoint to get API Key."""

    return "admin-123456-shouldbehashed"  # for now i just return an admin api key
