from fastapi import APIRouter
import app.responses
import app.idp.controller
import os
from typing import Annotated
from fastapi import Depends
from app.idp.schemas.Client import Client
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/identity", tags=["idp"])


@router.post("/me")
def read_me_account(registration_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Get access token of a registered client, or register a new account if 
    account does not exist.
    """

    client = Client(
        db_src=os.environ.get("DB_URL"),
        username=registration_form.username,
        password=registration_form.password,
    )

    if client.exists():
        jwt = app.idp.controller.read_account(client)
    else:
        app.idp.controller.create_account(
            os.environ.get("DB_URL"),
            registration_form.username,
            registration_form.password,
        )
        jwt = app.idp.controller.read_account(client)

    return app.responses.AccessToken(jwt)
