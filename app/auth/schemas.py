"""
Pydantic schemas for Authentication-Authorization module
"""

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from typing import Annotated
import app._exceptions
import re


MAX_USERNAME_LENGTH = 32


class User(BaseModel):
    username: str
    password: str | None = None

    @field_validator("username")
    def validate_username(cls, username):
        if len(username) <= 0:
            raise app._exceptions.InvalidData("username must not be empty.")

        if len(username) > MAX_USERNAME_LENGTH:
            raise app._exceptions.InvalidData("username too long (> 32 characters).")

        USERNAME_PATTERN = r"^[_0-9a-zA-Z]+$"
        if len(re.findall(pattern=USERNAME_PATTERN, string=username)) <= 0:
            raise app._exceptions.InvalidData(
                f"username must be comply pattern [{USERNAME_PATTERN}]."
            )

        return username  # pass all validations


class VerifiedUser(User):
    access_token: str

    @field_validator("access_token")
    def validate_access_token(cls, access_token):
        JWT_PATTERN = r"(^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$)"
        if len(re.findall(pattern=JWT_PATTERN)) <= 0:
            raise app._exceptions.InvalidData("invalid JWT pattern.")

        return access_token  # pass all validations
