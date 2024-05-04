from fastapi import APIRouter
import app.responses
import app.idp.controller
import os
from typing import Annotated
from fastapi import Depends
from app.idp.schemas.Client import Client
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(prefix="/identity", tags=["idp"])
idtok_bearer = OAuth2PasswordBearer("/me")
acctok_bearer = OAuth2PasswordBearer("/me")


"""
    Endpoints for Resource Owner
"""


@router.post("/me")
def read_me_account(registration_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Get ID Token from a Resource owner. Create a new Resource owner
    account in the database if does not have one. Requested from
    Resource Owner.

    Equivalent to basic login/register to the Resource Server (OCR-API).
    """

    client = Client(
        db_src=os.environ.get("DB_URL"),
        username=registration_form.username,
        password=registration_form.password,
    )

    if client.exists():
        id_token = app.idp.controller.read_account(client)
    else:
        app.idp.controller.create_account(
            os.environ.get("DB_URL"),
            registration_form.username,
            registration_form.password,
        )
        id_token = app.idp.controller.read_account(client)

    return app.responses.IDToken(id_token)


@router.post("/me/authorize")
def read_me_authorize(id_token: Annotated[str, Depends(idtok_bearer)]):
    """Authorize a third-party entity several permissions to the Resource server,
    requested from Resource Owner.

    This API does not return any token back to user since this is a one-way request
    from the Resource Owner to Identity Provider.
    """

    """
    "/me/authorize" should be RESOURCE OWNER (id_token) who authorize several 
    PERMISSIONS on the Resource Server. How I handle the permissions on Database
    is not the scope of OAuth2. Since our use case is too simple (only 2 services 
    at the time of this writing), I decided not to implement this function at this 
    time, and this endpoint always returns a successfuly message.
    """

    return app.responses.Text("Permissions authorized successfully!")


"""
    Endpoints for Third-party
"""


@router.post("/{username}/authorize")
def read_authorize():
    """Request for necessary authorization tokens, requested from a third-party
    entity."""
    # access_token = "abcXyZ123"
    # return app.responses.AuthorizedTokens(access_token)
    pass


"""
    Endpoints for Resource Server
"""


@router.post("/introspect")
def read_token_introspect(access_token: Annotated[str, Depends(idtok_bearer)]):
    """Validate access token for resource server. Requested from Resource Server.

    Return access credentials (a dictionary of resource + its permission pairs).
    The request to this endpoint comes from Resource Sever because it wants to
    validate the access token it receives from a third-party. Therefore,
    the response of this endpoint should be a dictionary of resource+permission
    so that the Resource Sever knows: (1) access_token is valid and (2)
    what resources it can access & what actions it can perform.

    Compliance with OAuth2 Token Introspection standard.
    See: https://www.rfc-editor.org/rfc/rfc7662
    """

    """I don't implement this too since I guess no third-party will use my 
    service now :). Also, the architecture of my app is monolithic therefore
    Resource Server and Authorization Server is one single container, there
    would be no need for multi-stage validation as defined in original OAuth2.
    
    I put this here for educational purpose."""
    pass


"""
Truly implement OAuth2 requires multiple redirection between
routes, which takes time to implement. Therefore at this time
I dont implement this, just sketch the skeleton for future
implementation.
"""
