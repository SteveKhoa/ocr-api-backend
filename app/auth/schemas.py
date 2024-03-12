"""
Pydantic schemas for Authentication-Authorization module
"""

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


# Currently duplicate but temporarily ignore it.
# In the future I want to model the schemas based
# on the specific domain, not copying and pasting
# from FastAPI docs
class VerifiedUser(User):
    pass
