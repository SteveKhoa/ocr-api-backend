from .schemas import UserInDB
from typing import Annotated
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="Basic-API-Key")


fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "fakehashed123456",
        "full_name": "Admin of this api",
        "email": "fakeemail@gmail.com",
        "disabled": False,
    },
    "jonhdoe": {
        "username": "jonhdoe",
        "full_name": "Jonh Doe",
        "email": "jonhdoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


fake_apikey_db = {
    "admin-123456-shouldbehashed",
    "client-123456-shouldbehashed",
}


def hash_password(password: str):
    return "fakehashed" + password


def verify_user(username: str, password: str, database: dict) -> UserInDB:
    """
    Verify a user authencity based on `username` & `password` against `database` records.

    ### Return
    This method returns Pydantic model

    ### Exceptions
    This method raises `HTTPException` if username and password does not match records on
    the database.
    """
    # Check username
    user_dict = database.get(username)
    if not user_dict:
        print("Username not found")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Check password
    user = UserInDB(**user_dict)  # validate data & turn it into Python object
    hashed_password = hash_password(password)
    if not (hashed_password == user.hashed_password):
        print("Password not found")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # If all passed, return UserInDB Pydantic model
    return user


def generate_oauth2_token(user: UserInDB, expiration=60) -> str:
    return "atoken_{}".format(user.name)  # for now let me just a very very fake token


def verify_apikey(
    apikey: Annotated[str, Depends(api_key_header)],
) -> str:
    if apikey not in fake_apikey_db:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid or Missing APIKey"
        )

    return apikey
