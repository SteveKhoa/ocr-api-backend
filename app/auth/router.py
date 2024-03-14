from fastapi import APIRouter
from fastapi import Form, Depends, Query
from fastapi import HTTPException, status
from typing import Annotated
from .utils import apikey as apikey_utils
from .utils import userdb as user_utils
from app.db.connectors import connector as db_connector
import app._responses
import app.auth.account
import app.auth.utils.jwt
import app._exceptions
import app.auth.schemas
import fastapi.security.http

auth_router = APIRouter(prefix="", tags=["auth"])

http_bearer_scheme = fastapi.security.http.HTTPBearer()


# @auth_router.get("/api-key", summary="Request API-KEY")
# async def read_post_apikey(
#     username: Annotated[str, Form()],
#     password: Annotated[str, Form()],
# ):
#     user = user_utils.verify_user(db_connector, username, password)
#     apikey = apikey_utils.generate_apikey(user)

#     return app._responses.Response(status="success", data={"apikey": apikey})


@auth_router.post("/account", summary="Register or login if account already exists")
def read_register_request(
    username: Annotated[str, Form()],  # id
    password: Annotated[str, Form()],  # secret
):
    """
    Register or login if account already exists. Requires `username` and `password`
    in request body as `application/x-www-form-urlencoded`.

    ## Returns
    ID Token as `JWT`, expires after 30 seconds.
    """
    user = app.auth.schemas.User(username=username, password=password)

    id_jwt = app.auth.account.register_account(
        user.username,
        user.password,
    )

    return app._responses.AccessToken(id_jwt)


@auth_router.patch("/account", summary="Change password of an existing account")
def read_change_password_request(
    id_jwt_credential: Annotated[
        fastapi.security.http.HTTPAuthorizationCredentials,
        Depends(http_bearer_scheme),
    ],
    new_password: Annotated[str, Form()],
):
    """
    Change the password of an existing account. Requires credential to be JWT in
    HTTP header `Authorization: Bearer <JWT ID Token>` and `new_password` in
    request body.

    ## Returns
    app._responses.Response
    """
    id_jwt = id_jwt_credential.credentials

    decoded_jwt = app.auth.utils.jwt.verify_id_token(id_jwt)
    user = app.auth.schemas.User(**decoded_jwt)

    app.auth.account.change_password(user.username, new_password)

    return app._responses.Message("Password changed.")


@auth_router.delete("/account", summary="Delete an existing account")
def read_delete_account_request(
    id_jwt_credential: Annotated[
        fastapi.security.http.HTTPAuthorizationCredentials,
        Depends(http_bearer_scheme),
    ],
):
    """
    Delete an existing account. Requires `jwt` in request header.

    ## Returns
    app._responses.Response
    """
    id_jwt = id_jwt_credential.credentials

    decoded_jwt = app.auth.utils.jwt.verify_id_token(id_jwt)
    user = app.auth.schemas.User(**decoded_jwt)

    app.auth.account.delete_account(user.username)

    return app._responses.Message("Account deleted.")


@auth_router.get("/account", summary="Get information of an account")
def read_get_info_request(
    id_jwt_credential: Annotated[
        fastapi.security.http.HTTPAuthorizationCredentials,
        Depends(http_bearer_scheme),
    ],
    query: Annotated[str, Query()],
):
    """
    Get information of an existing account. Requires `jwt` in request body.

    ## Examples
    `GET /account?query=username`

    `GET /account?query=password`  (fun example, Unsupported)

    `GET /account?query=email`  (Unsupported)


    ## Returns
    app._responses.Response
    """
    id_jwt = id_jwt_credential.credentials

    decoded_jwt = app.auth.utils.jwt.verify_id_token(id_jwt)
    user = app.auth.schemas.User(**decoded_jwt)
    # ohh this is very fake, since i just decode the
    # jwt and get the username, in the future this requires
    # database queries, not just as simple as this

    response = app._responses.Text(getattr(user, query))

    return response
