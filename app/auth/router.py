from fastapi import APIRouter
from fastapi import Form, Depends, Query
from fastapi import HTTPException, status
from typing import Annotated
from .utils import apikey as apikey_utils
from .utils import user as user_utils
from app.db.connectors import connector as db_connector
from app.responses import Message, Text, Response
import app.auth.account
import app.exceptions

auth_router = APIRouter(prefix="", tags=["auth"])


@auth_router.get("/api-key", summary="Request API-KEY")
async def read_post_apikey(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    user = user_utils.verify_user(db_connector, username, password)
    apikey = apikey_utils.generate_apikey(user)

    return Response(status="success", data={"apikey": apikey})


@auth_router.post("/account", summary="Request to register/login/")
def read_post_account(
    action: Annotated[list[str], Query()],
    username: Annotated[str, Form()] | None = None,
    password: Annotated[str, Form()] | None = None,
):
    match action:
        case "register":
            if username is None or password is None:
                raise app.exceptions.MissingBody("username", "password")

            app.auth.account.register_account(
                username,
                password,
            )

            return
        case "login":
            if username is None or password is None:
                raise app.exceptions.MissingBody(username, password)

            app.auth.account.register_account(
                username,
                password,
            )
        case _:
            raise app.exceptions.UnsupportedQueryParam("action")
